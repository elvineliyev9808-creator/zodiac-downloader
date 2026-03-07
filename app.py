from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Render-də saytı oyaq saxlayan sistem
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
    <title>ZODIAC | ULTIMATE V30</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --accent: #6366f1; --bg: #020617; --card: rgba(30, 41, 59, 0.75); }
        * { box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: white; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        
        /* Canlı Neon Fon */
        .mesh { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #020617 100%); }
        .glow { position: absolute; width: 400px; height: 400px; background: var(--accent); filter: blur(130px); border-radius: 50%; opacity: 0.15; animation: move 15s infinite alternate; }

        .container { background: var(--card); backdrop-filter: blur(25px); border: 1px solid rgba(255,255,255,0.1); width: 92%; max-width: 390px; padding: 35px; border-radius: 35px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.6); position: relative; z-index: 10; }
        h1 { font-size: 30px; font-weight: 800; margin: 0; background: linear-gradient(to right, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .tag { font-size: 10px; color: #6366f1; font-weight: 800; letter-spacing: 3px; margin-bottom: 30px; display: block; }

        /* Yığcam Axtarış */
        .input-box { background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 22px; padding: 5px; display: flex; margin-bottom: 25px; }
        input { flex: 1; background: transparent; border: none; padding: 12px 18px; color: white; outline: none; font-size: 14px; }
        .btn-go { background: var(--accent); color: white; border: none; padding: 12px 22px; border-radius: 18px; font-weight: 700; cursor: pointer; transition: 0.3s; }

        /* Player Kartı */
        .p-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 15px; display: flex; align-items: center; gap: 15px; }
        .p-btn { width: 45px; height: 45px; border-radius: 15px; background: var(--accent); border: none; color: white; cursor: pointer; font-size: 18px; }
        .p-info { text-align: left; }
        .p-title { font-size: 12px; font-weight: 700; color: #f8fafc; display: block; }
        .p-sub { font-size: 9px; color: #94a3b8; }

        /* AI Çat Pəncərəsi */
        #c-win { display: none; position: fixed; bottom: 100px; right: 25px; width: 310px; height: 430px; background: #0f172a; border-radius: 25px; flex-direction: column; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); z-index: 1000; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        .c-h { background: var(--accent); padding: 18px; font-weight: 800; font-size: 13px; display: flex; justify-content: space-between; }
        .c-b { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; font-size: 12px; }
        .msg { padding: 10px 14px; border-radius: 15px; max-width: 85%; line-height: 1.5; }
        .bot { background: #1e293b; color: #cbd5e1; align-self: flex-start; }
        .user { background: var(--accent); color: white; align-self: flex-end; }
        .c-i { padding: 12px; background: #1e293b; display: flex; }
        .c-i input { background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 8px; flex: 1; color: white; font-size: 12px; }

        #c-trigger { position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: var(--accent); border-radius: 20px; color: white; border: none; font-size: 26px; cursor: pointer; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4); z-index: 1001; }

        @keyframes move { from { transform: translate(0,0); } to { transform: translate(40px, 40px); } }
    </style>
</head>
<body>
    <div class="mesh"></div>
    <div class="glow" style="top:20%; left:10%;"></div>
    <div class="glow" style="bottom:10%; right:15%; background:#c084fc;"></div>

    <div class="container">
        <h1>ZODIAC</h1>
        <span class="tag">ULTIMATE EDITION</span>

        <form method="POST" class="input-box">
            <input type="text" name="u" placeholder="Video linkini bura qoy..." required>
            <button type="submit" class="btn-go">ENDİR</button>
        </form>

        {% if dl %}
        <div style="margin-bottom: 25px;">
            <a href="{{ dl }}" style="display:block; background:#fff; color:#000; text-decoration:none; padding:15px; border-radius:20px; font-weight:800; font-size:13px;" target="_blank">📥 VİDEONU YÜKLƏ</a>
        </div>
        {% endif %}

        <div class="p-card">
            <button class="p-btn" onclick="tglM()" id="ctrl">▶</button>
            <div class="p-info">
                <span class="p-title">Trend Background Mix</span>
                <span class="p-sub" id="sts">Audio System Active</span>
            </div>
        </div>
    </div>

    <div id="c-win">
        <div class="c-h"><span>ZODIAC AI DƏSTƏK</span> <span onclick="tglC()" style="cursor:pointer">✕</span></div>
        <div class="c-b" id="cb"><div class="msg bot">Salam! Mən Zodiac AI. Azərbaycan dilində bütün suallarınızı cavablandırıram. Necə kömək edim?</div></div>
        <div class="c-i"><input type="text" id="ci" placeholder="Yazın..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="c-trigger" onclick="tglC()">💬</button>

    <audio id="audio" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"></audio>

    <script>
        const a = document.getElementById('audio');
        function tglM() {
            if(a.paused) { a.play().then(()=> {document.getElementById('ctrl').innerText="||"; document.getElementById('sts').innerText="İndi Oxuyur...";}); }
            else { a.pause(); document.getElementById('ctrl').innerText="▶"; document.getElementById('sts').innerText="Pauza Edildi"; }
        }
        function tglC() { const w = document.getElementById('c-win'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Bunu hələ öyrənməmişəm. Amma video yükləmək üçün linki yuxarı qoya bilərsiniz.";
                if(v.includes("salam")) r = "Salam! Xoş gördük. Sizə necə kömək edə bilərəm?";
                else if(v.includes("necesen")) r = "Çox sağ olun! Mən botam, amma özümü əla hiss edirəm. Siz necəsiniz?";
                else if(v.includes("islemir")) r = "Linki düzgün kopyaladığınızdan və videonun hər kəsə açıq olduğundan əmin olun.";
                else if(v.includes("sagol") || v.includes("təşəkkür")) r = "Xoşdur! Hər zaman xidmətinizdəyik.";
                else if(v.includes("haralisan")) r = "Mən buludlarda yaşayıram, amma doğma dilim Azərbaycandır!";
                b.innerHTML += `<div class="msg bot">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 600);
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
