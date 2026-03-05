from flask import Flask, render_template_string, request, send_from_directory
import requests
import os
import threading
import time

app = Flask(__name__)

# Saytın sönməməsi üçün daxili pinger
def stay_awake():
    while True:
        try:
            # Buraya mütləq öz saytının Render linkini tam yaz!
            requests.get("https://zodiac-downloader.onrender.com")
        except:
            pass
        time.sleep(300) # 5 dəqiqədən bir dümsükləyir ki, yatmasın

threading.Thread(target=stay_awake, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | ELITE SYSTEM</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Syncopate:wght@700&family=Inter:wght@300;500&display=swap" rel="stylesheet">
    <style>
        :root { --main: #00f2fe; --glow: rgba(0, 242, 254, 0.5); --dark: #050505; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body { 
            background: var(--dark); 
            color: white; 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            overflow: hidden; 
        }

        /* Cyber Background Effect */
        #stars-canvas { position: fixed; top: 0; left: 0; z-index: -1; }
        .nebula { position: fixed; width: 500px; height: 500px; background: radial-gradient(circle, var(--glow) 0%, transparent 70%); filter: blur(100px); opacity: 0.15; z-index: -1; animation: float 10s infinite alternate; }

        .container { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 40px; 
            width: 90%; 
            max-width: 420px; 
            padding: 50px 30px; 
            text-align: center; 
            box-shadow: 0 40px 100px rgba(0,0,0,0.9), inset 0 0 20px rgba(255,255,255,0.05);
            animation: fadeIn 1s ease-out;
        }

        h1 { 
            font-family: 'Syncopate', sans-serif; 
            font-size: 28px; 
            margin: 0; 
            background: linear-gradient(90deg, #fff, var(--main), #fff); 
            background-size: 200% auto;
            -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; 
            animation: shine 3s linear infinite;
            letter-spacing: 10px;
        }

        .status { font-size: 8px; color: var(--main); letter-spacing: 4px; margin-bottom: 40px; text-transform: uppercase; opacity: 0.7; }

        /* Premium Music Player */
        .player-ui { 
            background: rgba(0,0,0,0.5); 
            border-radius: 30px; 
            padding: 25px; 
            margin-bottom: 30px; 
            border: 1px solid rgba(0, 242, 254, 0.2); 
            position: relative;
            overflow: hidden;
        }
        .track-label { font-size: 10px; color: #888; margin-bottom: 10px; display: block; letter-spacing: 1px; }
        #t-title { font-size: 13px; font-weight: 500; color: #fff; margin-bottom: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        
        .play-ring { 
            width: 70px; height: 70px; 
            border-radius: 50%; 
            background: var(--main); 
            margin: 0 auto; 
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.5s;
            box-shadow: 0 0 30px var(--glow);
        }
        .play-ring i { font-size: 24px; color: #000; }
        .play-ring.active { background: #ff0050; box-shadow: 0 0 30px rgba(255,0,80,0.5); transform: rotate(180deg); }

        /* Modern Input Group */
        .input-wrap { position: relative; margin-top: 20px; }
        input { 
            width: 100%; 
            background: rgba(255,255,255,0.03); 
            border: 1px solid rgba(255,255,255,0.1); 
            padding: 18px 25px; 
            border-radius: 20px; 
            color: #fff; 
            font-size: 14px; 
            outline: none; 
            transition: 0.4s;
        }
        input:focus { border-color: var(--main); background: rgba(0, 242, 254, 0.05); box-shadow: 0 0 15px rgba(0, 242, 254, 0.1); }
        
        .dl-btn { 
            width: 100%; 
            margin-top: 15px; 
            background: #fff; 
            color: #000; 
            border: none; 
            padding: 18px; 
            border-radius: 20px; 
            font-weight: 900; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            cursor: pointer; 
            transition: 0.3s;
        }
        .dl-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,255,255,0.2); }

        @keyframes shine { to { background-position: 200% center; } }
        @keyframes float { from { transform: translate(-10%, -10%); } to { transform: translate(10%, 10%); } }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="nebula"></div>
    <canvas id="stars-canvas"></canvas>

    <div class="container">
        <h1>ZODIAC</h1>
        <div class="status">System Online // 24/7</div>

        <div class="player-ui">
            <span class="track-label">NOW PLAYING</span>
            <div id="t-title">Musiqi Seçilir...</div>
            <div class="play-ring" onclick="handlePlay()" id="p-btn">▶</div>
        </div>

        <form method="POST">
            <div class="input-wrap">
                <input type="text" name="u" placeholder="Linki yapışdır..." required>
            </div>
            <button type="submit" class="dl-btn">ANALİZ ET</button>
        </form>

        {% if dl %}
        <div style="margin-top: 25px; animation: fadeIn 0.5s;">
            <a href="{{ dl }}" style="color: var(--main); text-decoration: none; font-size: 12px; font-weight: bold; border-bottom: 1px solid;" target="_blank">📥 VİDEONU CİHAZA YÜKLƏ</a>
        </div>
        {% endif %}
    </div>

    <audio id="m-player" onended="autoNext()"></audio>

    <script>
        const songs = [
            {n: "Lotular - Mahir Ay Brat", s: "Lotular(MP3_160K).mp3"},
            {n: "Ara Usaqlari - Mahir Ay Brat", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - Пыяла x Sarışan Hallar", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];

        let curIdx = 0;
        const player = document.getElementById('m-player');
        const btn = document.getElementById('p-btn');
        const title = document.getElementById('t-title');

        function load(i) {
            player.src = "/music/" + encodeURIComponent(songs[i].s);
            title.innerText = songs[i].n;
        }

        load(curIdx);

        function handlePlay() {
            if(player.paused) {
                player.play().then(() => {
                    btn.innerHTML = "||"; btn.classList.add('active');
                }).catch(() => alert("Ekrana bir dəfə toxun!"));
            } else {
                player.pause(); btn.innerHTML = "▶"; btn.classList.remove('active');
            }
        }

        function autoNext() {
            curIdx = (curIdx + 1) % songs.length;
            load(curIdx); player.play();
        }

        // Stars Background
        const canvas = document.getElementById('stars-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let stars = [];
        for(let i=0; i<100; i++) stars.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, size: Math.random()*1.5, spd: Math.random()*0.5});
        function animate() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "#fff";
            stars.forEach(s => {
                ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI*2); ctx.fill();
                s.y -= s.spd; if(s.y < 0) s.y = canvas.height;
            });
            requestAnimationFrame(animate);
        }
        animate();
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
            # TikTok/IG API Sorğusu
            r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
            dl = r['data']['play']
        except: pass
    return render_template_string(HTML, dl=dl)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
