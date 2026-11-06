import os, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HTML = """<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Personal AI | 웹 데모</title><style>body{font-family:system-ui;background:#101827;color:#f4f6fc;max-width:680px;margin:35px auto;padding:20px}h1{font-size:2rem}section{background:#202c40;border-radius:16px;padding:22px;margin:18px 0}label{display:block;margin:16px 0}input{width:100%}button{background:#7dd3fc;color:#07111e;border:0;border-radius:12px;padding:12px 20px;font-weight:bold}small{color:#a9b8cc}.value{font-size:1.3rem;font-weight:bold}</style><h1>🚗 Personal AI</h1><p>차량의 데이터를 성격과 기분으로 표현하는 웹 시뮬레이터</p><section><h2>차량 상태</h2><label>에너지 <b id="energyText">70%</b><input id="energy" type="range" min="0" max="100" value="70"></label><label><input type="checkbox" id="newPlace"> 처음 가는 목적지</label><label><input type="checkbox" id="driving"> 2시간 이상 운전 중</label><label><input type="checkbox" id="tire"> 타이어 공기압 경고</label><button onclick="update()">상태 적용</button></section><section><h2>지금의 기분</h2><div class="value" id="mood">😄 활기차요</div><p id="reason">에너지 넉넉 (70%)</p></section><section><h2>장기적 성격</h2><p>모험성 · 규칙성 · 노련함 · 활력</p><small>장기 성격은 실제 주행 이력에 따라 서서히 변화합니다. 원본 Kotlin 엔진은 Android 프로젝트에 보존되어 있으며, 이 화면은 기분 판단 로직을 옮긴 초기 웹 데모입니다.</small></section><small>실제 차량 데이터가 아닌 시뮬레이션입니다. Claude 대화 및 Pleos 연동은 아직 웹 데모에 연결되지 않았습니다.</small><script>function update(){let e=+document.querySelector('#energy').value,t=document.querySelector('#tire').checked,n=document.querySelector('#newPlace').checked,d=document.querySelector('#driving').checked;document.querySelector('#energyText').textContent=e+'%';let m,r;if(t){m='😣 불편해요';r='타이어 공기압 낮음 — 안전한 곳에 정차해 점검하세요.'}else if(e<=25){m='🥱 기운이 없어요';r='에너지 '+e+'%'}else if(n){m='🤩 설레요';r='처음 가 보는 목적지'}else if(d){m='😮‍💨 조금 지쳤어요';r='2시간 넘게 달리는 중'}else if(e>=60){m='😄 활기차요';r='에너지 넉넉 ('+e+'%)'}else{m='😌 편안해요';r='특별한 일 없음'}document.querySelector('#mood').textContent=m;document.querySelector('#reason').textContent=r}document.querySelector('#energy').addEventListener('input',update);update()</script></html>"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            body=b'ok'; kind='text/plain'
        elif self.path == '/':
            body=HTML.encode('utf-8');kind='text/html; charset=utf-8'
        else:
            self.send_error(404);return
        self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','10000'))),Handler).serve_forever()
