/**
 * 語言學概論練習頁的成績後端。貼進 Google Sheet 的 Apps Script，部署成網頁應用程式。
 * 部署步驟見 ../DEPLOY.md。
 *
 * answers 分頁：每次作答一列，只新增不覆蓋。網路重送可能讓同一個 event_id 出現兩次，重算總表時只算一次。
 * summary 分頁：從 answers 算出來的成績總表，按選單「成績 → 重算總表」更新。
 *   首次分數 = 每題「最早那次作答」（依伺服器收到的時間）答對的題數；最佳分數 = 每題「任何一次答對過」的題數。
 *   學生可以重做，但重做不會蓋掉首次作答。
 *
 * 前端用 JSONP GET 呼叫，避開 CORS，也能確認寫入成功。
 */
var ANSWERS = 'answers';
var SUMMARY = 'summary';
var HEADER = ['event_id', 'server_time', 'client_time', 'quiz', 'student_id', 'name',
              'part', 'level', 'qid', 'prompt', 'response', 'correct', 'attempt'];
var QUIZZES = {'ch01_morphology': true};   // 新增章節時把 quiz id 加進來

function doGet(e) {
  var cb = (e && e.parameter && e.parameter.callback) || 'callback';
  if (!/^[A-Za-z0-9_]+$/.test(cb)) cb = 'callback';
  if (!e || !e.parameter || !e.parameter.data) return jsonp_(cb, {ok: true, ping: true});
  var d;
  try { d = JSON.parse(e.parameter.data); } catch (err) { return jsonp_(cb, {ok: false, error: 'bad json'}); }
  if (!QUIZZES[d.quiz]) return jsonp_(cb, {ok: false, error: 'unknown quiz'});
  if (!/^[A-Z][0-9]{8}$/.test(String(d.student_id))) return jsonp_(cb, {ok: false, error: 'bad student_id'});
  if (!d.event_id) return jsonp_(cb, {ok: false, error: 'missing event_id'});
  try {
    // appendRow 本身是原子操作，不加鎖、不查重，整班同時作答也不會排隊。
    // 網路重送造成的重複 event_id 留在 answers 裡無妨，rebuildSummary 會去重。
    d.server_time = new Date();
    sheet_(ANSWERS, HEADER).appendRow(HEADER.map(function (k) {
      var v = d[k];
      if (v === undefined || v === null) return '';
      if (typeof v === 'string' && /^[=+\-@]/.test(v)) return "'" + v;  // 防止被當成公式
      return v;
    }));
    return jsonp_(cb, {ok: true, id: d.event_id});
  } catch (err) {
    return jsonp_(cb, {ok: false, retry: true, error: String(err)});  // 暫時性錯誤：前端留著重送
  }
}

function onOpen() {
  SpreadsheetApp.getUi().createMenu('成績').addItem('重算總表', 'rebuildSummary').addToUi();
}

function rebuildSummary() {
  var sh = sheet_(ANSWERS, HEADER);
  var last = sh.getLastRow();
  var rows = last < 2 ? [] : sh.getRange(2, 1, last - 1, HEADER.length).getValues();
  var col = {}; HEADER.forEach(function (k, i) { col[k] = i; });

  // 每個 (學生, 測驗, 題目) 留最早一筆與「有沒有答對過」
  var per = {};      // key: sid|quiz -> {name, lastTime, q: {qid: {t, first, ever, sec}}}
  var seen = {};
  rows.forEach(function (r) {
    var eid = String(r[col.event_id]);
    if (seen[eid]) return;   // 重送造成的重複列
    seen[eid] = true;
    var sid = r[col.student_id], quiz = r[col.quiz], qid = String(r[col.qid]);
    var t = new Date(r[col.server_time] || r[col.client_time]).getTime();  // 用伺服器時間，學生電腦時鐘不準也不影響
    var ok = Number(r[col.correct]) === 1;
    var k = sid + '|' + quiz;
    var s = per[k] || (per[k] = {sid: sid, quiz: quiz, name: r[col.name], lastTime: 0, q: {}});
    if (t > s.lastTime) { s.lastTime = t; s.name = r[col.name]; }
    var sec = r[col.part] === 'A' ? 'A' : 'B' + r[col.level];
    var q = s.q[qid];
    if (!q) s.q[qid] = {t: t, first: ok, ever: ok, sec: sec};
    else { if (t < q.t) { q.t = t; q.first = ok; } q.ever = q.ever || ok; }
  });

  var SECS = ['A', 'B1', 'B2', 'B3', 'B4'];
  var head = ['student_id', 'name', 'quiz', '已作答題數', '首次答對', '最佳答對']
    .concat(SECS.map(function (x) { return x + ' 首次答對'; }))
    .concat(['最後作答時間']);
  var out = Object.keys(per).sort().map(function (k) {
    var s = per[k], n = 0, first = 0, best = 0, bySec = {};
    Object.keys(s.q).forEach(function (qid) {
      var q = s.q[qid]; n++;
      if (q.first) { first++; bySec[q.sec] = (bySec[q.sec] || 0) + 1; }
      if (q.ever) best++;
    });
    return [s.sid, s.name, s.quiz, n, first, best]
      .concat(SECS.map(function (x) { return bySec[x] || 0; }))
      .concat([s.lastTime ? new Date(s.lastTime) : '']);
  });

  var sm = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SUMMARY) ||
           SpreadsheetApp.getActiveSpreadsheet().insertSheet(SUMMARY);
  sm.clearContents();
  sm.getRange(1, 1, 1, head.length).setValues([head]);
  if (out.length) sm.getRange(2, 1, out.length, head.length).setValues(out);
  sm.setFrozenRows(1);
}

function sheet_(name, header) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  if (sh.getLastRow() === 0) { sh.appendRow(header); sh.setFrozenRows(1); }
  return sh;
}

function jsonp_(cb, obj) {
  return ContentService.createTextOutput(cb + '(' + JSON.stringify(obj) + ')')
    .setMimeType(ContentService.MimeType.JAVASCRIPT);
}
