from flask import Flask, render_template_string, request, send_from_directory
import requests
import os
import threading
import time

app = Flask(__name__)

# Serverin sönməməsi üçün daxili pinger sistemi
def keep_alive():
    while True:
        try:
            # Saytın sönməməsi üçün öz-özünə sorğu göndərir
            requests.get("http://127.0.0.1:10000") 
        except:
            pass
        time.sleep(300) # 5 dəqiqə

threading.Thread(target=keep_alive, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC PREMIUM | Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Orbitron:wght@900&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #ffd700; --bg: #000000; --card: rgba(20, 20, 20, 0.7); --white: #ffffff; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body { background-color: var(--bg); color: var(--white); font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; position: relative; }
        
        /* Həcmli Video Arxa Fon Effekti */
        .video-bg-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2; opacity: 0.08; filter: blur(2px); }
        .video-bg-layer iframe { width: 100vw; height: 100vh; border: none; }
        
        /* Parıldayan Canlı Fon (Glow) */
        .neon-glow { position: fixed; width: 400px; height: 400px; background: rgba(255, 215, 0, 0.1); filter: blur(150px); border-radius: 50%; z-index: -1; animation: floatGlow 15s infinite alternate; }

        .container { background: var(--card); backdrop-filter: blur(20px); border: 1px solid rgba(255, 215, 0, 0.15); width: 92%; max-width: 400px; padding: 40px 30px; border-radius: 35px; text-align: center; box-shadow: 0 40px 100px rgba(0,0,0,0.8), inset 0 0 30px rgba(255,215,0,0.05); transition: 0.5s; position: relative; z-index: 10; animation: slideUp 1s ease-out; }
        
        h1 { font-family: 'Orbitron', sans-serif; font-size: 32px; font-weight: 900; margin: 0; background: linear-gradient(90deg, #fff, var(--gold), #fff); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shineText 4s linear infinite; letter-spacing: 5px; }
        .status-text { font-size: 10px; color: #555; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 3px; }

        /* Professional Downloader */
        .search-form { display: flex; background: rgba(0,0,0,0.4); border: 1px solid #222; border-radius: 20px; padding: 5px; gap: 5px; margin-bottom: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
        input { flex: 1; background: transparent; border: none; padding: 15px; color: var(--white); outline: none; font-size: 15px; font-weight: 500; }
        .go-btn { background: var(--white); color: #000; border: none; padding: 0 25px; border-radius: 16px; font-weight: 700; cursor: pointer; transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); text-transform: uppercase; font-size: 13px; letter-spacing: 1px; }
        .go-btn:active { transform: scale(0.9); }

        /* Result Area */
        .res-area { margin-bottom: 25px; animation: fadeIn 0.5s forwards; }
        .dl-link { display: inline-block; background: var(--gold); color: black; text-decoration: none; padding: 15px 35px; border-radius: 16px; font-weight: 800; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3); transition: 0.3s; }

        /* Compact Azerbaijan Player */
        .player-bar { background: rgba(255, 215, 0, 0.05); border-radius: 25px; padding: 15px 20px; border: 1px solid rgba(255, 215, 0, 0.2); display: flex; align-items: center; justify-content: space-between; gap: 15px; margin-top: 20px; }
        .m-ctrl { background: var(--gold); border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; color: black; font-size: 18px; display: flex; align-items: center; justify-content: center; box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3); }
        .n-ctrl { background: rgba(255,255,255,0.05); color: white; width: 35px; height: 35px; font-size: 12px; }
        .m-meta { text-align: left; }
        .m-title { font-size: 12px; font-weight: 700; color: var(--gold); display: block; margin-bottom: 2px; }
        .m-sub { font-size: 9px; color: #777; font-weight: 500; }

        /* Smart Azerbaijan Bot */
        #bot-ui { display: none; position: fixed; bottom: 100px; right: 25px; width: 320px; height: 450px; background: rgba(10, 10, 10, 0.9); backdrop-filter: blur(25px); border-radius: 25px; flex-direction: column; overflow: hidden; border: 1px solid var(--gold); z-index: 1000; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        .ch-h { background: var(--gold); color: #000; padding: 18px; font-weight: 800; font-size: 14px; display: flex; justify-content: space-between; }
        .ch-b { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; font-size: 13px; background: rgba(0,0,0,0.2); scroll-behavior: smooth; }
        .msg { padding: 12px 16px; border-radius: 18px; max-width: 85%; line-height: 1.5; }
        .b { background: rgba(255,255,255,0.05); color: #eee; align-self: flex-start; }
        .u { background: var(--gold); color: #000; align-self: flex-end; font-weight: 600; }
        .ch-i { padding: 15px; background: rgba(0,0,0,0.3); display: flex; }
        .ch-i input { background: #000; border: 1px solid #333; border-radius: 14px; padding: 10px 15px; flex: 1; color: white; font-size: 13px; outline: none; }

        #bot-trigger { position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: var(--gold); border-radius: 20px; color: #000; border: none; font-size: 26px; cursor: pointer; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.4); z-index: 1001; transition: 0.3s; }
        #bot-trigger:hover { transform: translateY(-5px) rotate(5deg); }

        @keyframes floatGlow { from { transform: translate(0,0); } to { transform: translate(40px, 40px); } }
        @keyframes shineText { to { background-position: 200% center; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body>
    <div class="video-bg-layer">
        <iframe src="https://www.youtube.com/embed/videoseries?list=PLPazg0nI_S06R0lP5oG15w0607K1h4-0z&autoplay=1&mute=1&loop=1" frameborder="0" allow="autoplay; encrypted-media"></iframe>
    </div>
    <div class="neon-glow" style="top:20%; left:15%;"></div>
    <div class="neon-glow" style="bottom:10%; right:10%; background:rgba(255,255,255,0.05)"></div>

    <div class="container">
        <h1>ZODIAC</h1>
        <div class="status-text">Premium System v25 // Stay Online</div>

        <form method="POST" class="search-form">
            <input type="text" name="u" placeholder="Video linkini bura daxil edin..." required>
            <button type="submit" class="go-btn">GO</button>
        </form>

        {% if dl %}
        <div class="res-area">
            <a href="{{ dl }}" class="dl-link" target="_blank">📥 VİDEONU YÜKLƏ (.MP4)</a>
        </div>
        {% endif %}

        <div class="player-bar">
            <button class="m-ctrl" onclick="tglP()" id="p-icon">▶</button>
            <div class="m-meta">
                <span class="m-title" id="t-title">Musiqi Yüklənir...</span>
                <span class="m-sub">Azerbaijan Trend Mood</span>
            </div>
            <button class="m-ctrl n-ctrl" onclick="nxt()">⏭</button>
        </div>
    </div>

    <div id="bot-ui">
        <div class="ch-h"><span>ZODIAC DƏSTƏK AI</span> <span onclick="tglC()" style="cursor:pointer">✕</span></div>
        <div class="ch-b" id="cb"><div class="msg b">Salam! Mən Zodiac AI. Azərbaycan dilində hər sualınızı səmimi cavablandırmağa hazıram.</div></div>
        <div class="ch-i"><input type="text" id="ci" placeholder="Sualınızı bura yazın..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="bot-trigger" onclick="tglC()">💬</button>

    <audio id="audio" onended="nxt()"></audio>

    <script>
        const a = document.getElementById('audio');
        // Trend Azerbaijan Musiqiləri
        const songs = [
            {n: "Lotular - Mahir Ay", s: "https://dl.mahnilar.az/download.php?id=30283"}, // Tam lokal trend
            {n: "Meyxana Mix - Azerbaijan Mood", s: "https://dl.mahnilar.az/download.php?id=12345"}, // Simvolik link
            {n: "AIS - Пыяла x Sarışan Hallar", s: "https://dl.mahnilar.az/download.php?id=25234"} // Trend remix
        ];
        let idx = 0;
        function loadS(i) {
            a.src = songs[i].s;
            document.getElementById('t-title').innerText = songs[i].n;
        }
        loadS(idx);
        function tglP() { if(a.paused) { a.play().then(()=> {document.getElementById('p-icon').innerText="||";}).catch(()=> {alert("Ekrana bir dəfə toxunun!")}); } else { a.pause(); document.getElementById('p-icon').innerText="▶"; } }
        function nxt() { idx = (idx+1)%songs.length; loadS(idx); a.play(); document.getElementById('p-icon').innerText="||"; }

        // Bot Sistemi
        function tglC() { const u = document.getElementById('bot-ui'); u.style.display = (u.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg u">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Bunu hələ ki anlamıram, amma TikTok linkini yükləmək üçün kömək edə bilərəm.";
                // Geniş Azerbaijan söz bazası
                if(v.includes("salam")) r = "Salam, xoş gəldiniz! Necə kömək edim?";
                else if(v.includes("necesen")) r = "Mən Zodiac AI sisteminin botuyam, hər şey qaydasındadır! Siz necəsiniz?";
                else if(v.includes("sagol") || v.includes("təşəkkür")) r = "Buyurun, xoşdur! Başqa sualınız var?";
                else if(v.includes("mahnı") || v.includes("musiqi")) r = "Aşağıdakı pleyerdə Azərbaycanın trend hitləri var, '⏭' düyməsi ilə dəyişə bilərsiniz.";
                else if(v.includes("islemir") || v.includes("problem")) r = "Lütfən linkin düzgün olduğundan və profilin açıq olduğundan əmin olun.";
                else if(v.includes("kim yaratdı")) r = "Bu sistemi Zodiac Developer qrupu sizin üçün hazırlayıb.";
                else if(v.includes("haralısan")) r = "Mən rəqəmsal dünyadayam, amma ürəyim Azərbaycanladır!";
                b.innerHTML += `<div class="msg b">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 600);
        }
    </script>
</body>
</html>
"""

@app.route('/music/<path:filename>')
def get_music(filename):
    return send_from_directory(os.getcwd(), filename)

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
