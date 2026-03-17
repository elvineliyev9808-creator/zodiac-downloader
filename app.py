from flask import Flask, render_template_string, request
import requests, os, threading, time

app = Flask(__name__)

# 1. ANTI-SLEEP MEXANİZMİ: Saytın sönməməsi üçün daxili pinger
def keep_alive():
    while True:
        try:
            # Buradakı URL-i öz Render sayt ünvanınla dəyişdir
            requests.get("https://zodiac-downloader.onrender.com", timeout=10)
        except:
            pass
        time.sleep(120) # Hər 2 dəqiqədən bir özünə sorğu göndərir

threading.Thread(target=keep_alive, daemon=True).start()

# 2. MOBİL VƏ TOXUNUŞ OPTİMİZASİYALI DİZAYN
HTML_CODE = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ZODIAC | 24/7</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { background: #000; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
        .main-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); width: 100%; max-width: 380px; padding: 45px 25px; border-radius: 35px; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.6); }
        h1 { font-family: 'Orbitron', sans-serif; font-size: 26px; letter-spacing: 6px; margin: 0; background: linear-gradient(to bottom, #fff, #444); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .tag { display: inline-block; margin-top: 10px; padding: 5px 15px; background: rgba(0,242,255,0.1); color: #00f2ff; font-size: 10px; font-weight: 800; border-radius: 50px; text-transform: uppercase; border: 1px solid rgba(0,242,255,0.1); }
        input { width: 100%; background: #080808; border: 1px solid #222; padding: 18px; border-radius: 16px; color: #fff; margin-top: 40px; text-align: center; font-size: 14px; outline: none; transition: 0.3s; }
        input:focus { border-color: #00f2ff; box-shadow: 0 0 20px rgba(0,242,255,0.1); }
        .btn { width: 100%; background: #fff; color: #000; border: none; padding: 18px; border-radius: 16px; font-weight: 800; margin-top: 15px; cursor: pointer; transition: 0.2s; font-size: 13px; letter-spacing: 1px; }
        .btn:active { transform: scale(0.96); background: #00f2ff; }
        .res-box { margin-top: 25px; padding: 15px; background: rgba(0,242,255,0.05); border: 1px dashed #00f2ff; border-radius: 18px; animation: slideUp 0.5s ease; }
        .res-box a { color: #00f2ff; text-decoration: none; font-weight: 800; font-size: 12px; }
        
        /* DƏSTƏK BOTU */
        #bot-ui { display: none; position: fixed; bottom: 90px; right: 20px; width: 300px; height: 380px; background: #0a0a0a; border: 1px solid #222; border-radius: 25px; flex-direction: column; z-index: 1000; box-shadow: 0 20px 40px #000; overflow: hidden; }
        .b-h { background: #111; padding: 15px; font-size: 11px; font-weight: 800; color: #00f2ff; border-bottom: 1px solid #222; }
        .b-b { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 10px 14px; border-radius: 15px; font-size: 12px; line-height: 1.4; max-width: 85%; }
        .bot { background: #1a1a1a; align-self: flex-start; }
        .user { background: #00f2ff; color: #000; align-self: flex-end; font-weight: 600; }
        .b-f { padding: 10px; border-top: 1px solid #222; }
        .b-f input { margin: 0; padding: 10px; font-size: 11px; text-align: left; }
        
        #bot-btn { position: fixed; bottom: 25px; right: 25px; width: 55px; height: 55px; background: #fff; color: #000; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer; z-index: 1001; box-shadow: 0 10px 20px rgba(0,0,0,0.4); }
        @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="main-card">
        <h1>ZODIAC</h1>
        <div class="tag">7/24 Xidmətinizdəyik</div>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini bura qoyun" required autocomplete="off">
            <button type="submit" class="btn">İNDİ YÜKLƏ</button>
        </form>
        {% if dl %}
        <div class="res-box"><a href="{{ dl }}" target="_blank">📥 VİDEONU QALEREYAYA YAZ</a></div>
        {% endif %}
    </div>

    <div id="bot-ui">
        <div class="b-h">ZODIAC SUPPORT AI</div>
        <div class="b-b" id="chat"><div class="msg bot">Salam! 7/24 xidmətinizdəyik. Necə kömək edə bilərəm?</div></div>
        <div class="b-f"><input type="text" id="msg-in" placeholder="Yaz..." onkeypress="if(event.key=='Enter') sendMsg()"></div>
    </div>
    <div id="bot-btn" onclick="toggleBot()">💬</div>

    <script>
        function toggleBot() { const u = document.getElementById('bot-ui'); u.style.display = (u.style.display==='flex')?'none':'flex'; }
        function sendMsg() {
            const i = document.getElementById('msg-in'); const b = document.getElementById('chat');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Sistem 7/24 aktivdir. Linki yapışdırıb düyməyə basmağınız kifayətdir.";
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
        u = request.form.get('url')
        try:
            r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
            dl = r['data']['play']
        except: pass
    return render_template_string(HTML_CODE, dl=dl)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
