from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Serveri oyaq saxlamaq üçün pinger
def keep_alive():
    while True:
        try: requests.get("http://127.0.0.1:10000")
        except: pass
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC SSSTIK | TikTok Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { background: #f0f2f5; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        header { background: white; padding: 15px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .logo { font-weight: 900; font-size: 22px; color: #1e293b; }
        .logo span { color: #009efd; }
        .hero { background: linear-gradient(135deg, #009efd 0%, #2af598 100%); padding: 50px 20px; text-align: center; color: white; }
        .search-area { max-width: 600px; margin: -30px auto 30px; padding: 0 15px; }
        .s-form { background: white; padding: 8px; border-radius: 50px; display: flex; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        input { flex: 1; border: none; padding: 12px 20px; outline: none; font-size: 15px; border-radius: 50px; }
        .btn { background: #1e293b; color: white; border: none; padding: 0 25px; border-radius: 50px; font-weight: 700; cursor: pointer; }
        .res { max-width: 400px; margin: 20px auto; background: white; padding: 20px; border-radius: 20px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .dl-b { display: block; background: #22c55e; color: white; text-decoration: none; padding: 12px; border-radius: 10px; font-weight: 700; margin-top: 10px; }
        
        /* Mini Player */
        .player { position: fixed; bottom: 20px; left: 20px; background: white; padding: 10px 15px; border-radius: 40px; display: flex; align-items: center; gap: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); z-index: 100; border: 1px solid #eee; }
        .p-btn { width: 35px; height: 35px; border-radius: 50%; border: none; background: #009efd; color: white; cursor: pointer; }
        
        /* Chat */
        #c-win { display: none; position: fixed; bottom: 90px; right: 20px; width: 300px; height: 380px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); flex-direction: column; overflow: hidden; z-index: 1000; border: 1px solid #eee; }
        .c-h { background: #1e293b; color: white; padding: 15px; font-weight: 700; font-size: 13px; }
        .c-b { flex: 1; padding: 15px; overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 8px; }
        .msg { padding: 8px 12px; border-radius: 12px; max-width: 85%; }
        .bot { background: #f1f5f9; align-self: flex-start; }
        .user { background: #009efd; color: white; align-self: flex-end; }
        .c-f { padding: 10px; border-top: 1px solid #eee; display: flex; }
        .c-f input { flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 8px; }
        #c-trig { position: fixed; bottom: 20px; right: 20px; width: 55px; height: 55px; background: #1e293b; border-radius: 50%; color: white; border: none; font-size: 22px; cursor: pointer; z-index: 1001; }
    </style>
</head>
<body>
    <header><div class="logo">ZODIAC<span>SSSTIK</span></div></header>
    <div class="hero"><h1>TikTok Downloader</h1><p>Videoları loqosuz və sürətli endirin</p></div>
    <div class="search-area">
        <form method="POST" class="s-form">
            <input type="text" name="u" placeholder="Video linkini yapışdırın..." required>
            <button type="submit" class="btn">ENDİR</button>
        </form>
        {% if dl %}
        <div class="res">
            <div style="font-weight:700; color:#22c55e;">Hazırdır! ✅</div>
            <a href="{{ dl }}" class="dl-b" target="_blank">📥 VİDEONU YÜKLƏ</a>
        </div>
        {% endif %}
    </div>
    <div class="player"><button class="p-btn" onclick="tglM()" id="p-ctrl">▶</button><div style="font-size:11px; font-weight:700;">Trend Mix</div></div>
    <div id="c-win">
        <div class="c-h">ZODIAC DƏSTƏK</div>
        <div class="c-b" id="cb"><div class="msg bot">Salam! Sizə necə kömək edə bilərəm?</div></div>
        <div class="c-f"><input type="text" id="ci" placeholder="Yazın..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="c-trig" onclick="tglC()">💬</button>
    <audio id="audio" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"></audio>
    <script>
        const a = document.getElementById('audio');
        function tglM() { if(a.paused) { a.play(); document.getElementById('p-ctrl').innerText="||"; } else { a.pause(); document.getElementById('p-ctrl').innerText="▶"; } }
        function tglC() { const w = document.getElementById('c-win'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Anlamadım, linki yuxarı qoyub endirin.";
                if(v.includes("salam")) r = "Salam! Necə kömək edim?";
                else if(v.includes("islemir")) r = "Linkin düzgünlüyünü yoxlayın.";
                else if(v.includes("sagol")) r = "Buyurun!";
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
    return render_template_string(HTML, dl=dl)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
