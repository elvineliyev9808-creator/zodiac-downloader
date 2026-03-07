from flask import Flask, render_template_string, request
import requests, os, threading, time

app = Flask(__name__)

# Serverin oyaq qalması üçün pinger
def keep_alive():
    while True:
        try: requests.get("http://127.0.0.1:10000")
        except: pass
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { --accent: #00f2ff; --bg: #000; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        body { background: var(--bg); color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        .bg-gradient { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #111 0%, #000 100%); z-index: -2; }
        .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(50px); border: 1px solid rgba(255, 255, 255, 0.08); width: 90%; max-width: 400px; padding: 50px 30px; border-radius: 45px; text-align: center; box-shadow: 0 40px 100px rgba(0,0,0,0.7); position: relative; z-index: 10; transition: transform 0.2s; }
        .main-card:active { transform: scale(0.99); }
        h1 { font-family: 'Orbitron', sans-serif; font-size: 32px; letter-spacing: 12px; margin: 0; background: linear-gradient(180deg, #fff 0%, #444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .service-tag { display: inline-block; margin-top: 15px; padding: 5px 15px; background: rgba(0, 242, 255, 0.08); color: var(--accent); font-size: 9px; font-weight: 800; letter-spacing: 2px; border-radius: 50px; text-transform: uppercase; border: 1px solid rgba(0, 242, 255, 0.1); }
        .input-group { margin-top: 40px; }
        input { width: 100%; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; color: #fff; font-size: 15px; text-align: center; transition: 0.3s; }
        input:focus { border-color: var(--accent); background: rgba(255, 255, 255, 0.08); box-shadow: 0 0 30px rgba(0, 242, 255, 0.1); }
        .btn { width: 100%; margin-top: 15px; padding: 18px; background: #fff; color: #000; border: none; border-radius: 18px; font-weight: 800; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; cursor: pointer; transition: 0.2s; }
        .btn:active { transform: scale(0.95); background: var(--accent); }
        .result { margin-top: 25px; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 20px; border: 1px dashed rgba(0, 242, 255, 0.3); }
        .result a { color: var(--accent); text-decoration: none; font-weight: 800; font-size: 12px; }
        #bot-ui { display: none; position: fixed; bottom: 100px; right: 25px; width: 310px; height: 420px; background: rgba(10, 10, 10, 0.95); backdrop-filter: blur(30px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; flex-direction: column; overflow: hidden; z-index: 1000; }
        .b-h { background: rgba(255,255,255,0.03); padding: 20px; font-size: 12px; font-weight: 800; color: var(--accent); border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; }
        .b-b { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; }
        .msg { padding: 12px 16px; border-radius: 18px; font-size: 13px; max-width: 85%; }
        .bot { background: rgba(255,255,255,0.05); color: #ccc; align-self: flex-start; }
        .user { background: var(--accent); color: #000; align-self: flex-end; font-weight: 600; }
        .b-f { padding: 15px; display: flex; gap: 10px; }
        #bot-trigger { position: fixed; bottom: 30px; right: 30px; width: 65px; height: 65px; background: #fff; border-radius: 22px; border: none; cursor: pointer; z-index: 1001; font-size: 24px; }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="main-card">
        <h1>ZODIAC</h1>
        <div class="service-tag">7/24 Xidmətinizdəyik</div>
        <form method="POST" class="input-group">
            <input type="text" name="u" placeholder="TikTok linkini yapışdırın" required autocomplete="off">
            <button type="submit" class="btn">İndi Yüklə</button>
        </form>
        {% if dl %}
        <div class="result"><a href="{{ dl }}" target="_blank">📥 VİDEONU QALEREYAYA YAZ</a></div>
        {% endif %}
    </div>
    <div id="bot-ui">
        <div class="b-h"><span>ZODIAC DƏSTƏK AI</span> <span onclick="tglC()" style="cursor:pointer;">✕</span></div>
        <div class="b-b" id="cb"><div class="msg bot">Salam! 7/24 xidmətinizdəyik. Buyurun, sualınızı verin!</div></div>
        <div class="b-f"><input type="text" id="ci" placeholder="Yaz..." onkeypress="if(event.key=='Enter') snd()" style="text-align:left; padding:12px;"></div>
    </div>
    <button id="bot-trigger" onclick="tglC()">💬</button>
    <script>
        function tglC() { const w = document.getElementById('bot-ui'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "7/24 aktivik! Linki yapışdırıb videonu dərhal endirə bilərsiniz.";
                if(v.includes("salam")) r = "Salam! Sizə necə kömək edə bilərəm?";
                b.innerHTML += `<div class="msg bot">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 500);
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    dl = None
    if request.method == 'POST':
        u = request.form.get('u')
        try:
            r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
            dl = r['data']['play']
        except: pass
    return render_template_string(HTML_TEMPLATE, dl=dl)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
