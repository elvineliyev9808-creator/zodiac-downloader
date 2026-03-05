from flask import Flask, render_template_string, request, send_from_directory
import requests
import os

app = Flask(__name__)

# Premium Dark Glassmorphism Design
HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC PREMIUM</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #00f2fe; --secondary: #4facfe; --accent: #ff0050; --bg: #050505; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { background: var(--bg); color: white; font-family: 'Inter', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow-x: hidden; }
        
        /* Premium Background */
        #canvas-bg { position: fixed; top: 0; left: 0; z-index: -1; filter: blur(1px); }
        .glow { position: fixed; width: 300px; height: 300px; background: var(--primary); filter: blur(150px); border-radius: 50%; opacity: 0.1; z-index: -1; animation: move 20s infinite alternate; }
        @keyframes move { from { top: 0; left: 0; } to { bottom: 0; right: 0; } }

        .main-card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; width: 90%; max-width: 400px; padding: 40px 30px; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        
        h1 { font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 32px; margin: 0 0 10px; background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 4px; }
        .subtitle { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }

        /* Premium Player */
        .player-zone { background: rgba(0,0,0,0.4); border-radius: 20px; padding: 20px; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.05); }
        .track-title { font-size: 12px; color: var(--primary); font-weight: 600; margin-bottom: 15px; height: 15px; overflow: hidden; }
        .play-btn { background: white; color: black; border: none; width: 60px; height: 60px; border-radius: 50%; font-size: 20px; cursor: pointer; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 10px 20px rgba(255,255,255,0.1); }
        .play-btn:active { transform: scale(0.9); }
        .playing { background: var(--accent); color: white; box-shadow: 0 10px 20px rgba(255, 0, 80, 0.3); }

        /* Input Premium */
        .input-group { margin-top: 20px; text-align: left; }
        label { font-size: 11px; color: #888; margin-left: 15px; margin-bottom: 8px; display: block; }
        input { width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 15px 20px; border-radius: 15px; color: white; outline: none; transition: 0.3s; font-size: 14px; }
        input:focus { border-color: var(--primary); background: rgba(255,255,255,0.08); }
        .submit-btn { width: 100%; margin-top: 15px; background: linear-gradient(45deg, var(--primary), var(--secondary)); border: none; padding: 15px; border-radius: 15px; color: black; font-weight: 700; cursor: pointer; font-size: 14px; transition: 0.3s; }
        
        .dl-card { margin-top: 20px; padding: 15px; background: rgba(0,242,254,0.1); border-radius: 15px; border: 1px dashed var(--primary); }
        .dl-link { color: var(--primary); text-decoration: none; font-size: 13px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="glow"></div>
    <canvas id="canvas-bg"></canvas>

    <div class="main-card">
        <h1>ZODIAC</h1>
        <div class="subtitle">Elite Downloader System</div>

        <div class="player-zone">
            <div class="track-title" id="t-name">Sistem Hazır</div>
            <button class="play-btn" onclick="ctrl()" id="p-ctrl">▶</button>
        </div>

        <form class="input-group" method="POST">
            <label>VİDEO LİNKİNİ DAXİL EDİN</label>
            <input type="text" name="u" placeholder="https://..." required>
            <button type="submit" class="submit-btn">ANALİZİ BAŞLAT</button>
        </form>

        {% if dl %}
        <div class="dl-card">
            <a href="{{ dl }}" class="dl-link" target="_blank">📥 VİDEONU YÜKLƏMƏK ÜÇÜN KLİKLƏ</a>
        </div>
        {% endif %}
    </div>

    <audio id="player" onended="next()"></audio>

    <script>
        // Sənin yüklədiyin faylları tapmaq üçün adları tam dəqiq yazırıq
        const list = [
            {n: "Lotular - Mahir Ay Brat", s: "Lotular(MP3_160K).mp3"},
            {n: "Ara Usaqlari - Mahir Ay Brat", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - Пыяла", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];

        let cur = 0;
        const a = document.getElementById('player');
        const b = document.getElementById('p-ctrl');
        const t = document.getElementById('t-name');

        function load(i) {
            // URL-dəki boşluqları və xüsusi simvolların xəta verməməsi üçün encode edirik
            a.src = "/music/" + encodeURIComponent(list[i].s);
            t.innerText = list[i].n;
        }

        load(cur);

        function ctrl() {
            if(a.paused) {
                a.play().then(() => {
                    b.innerHTML = "||"; b.classList.add('playing');
                }).catch(() => alert("Lütfən ekranın istənilən yerinə toxunun, sonra düyməyə basın."));
            } else {
                a.pause(); b.innerHTML = "▶"; b.classList.remove('playing');
            }
        }

        function next() {
            cur = (cur + 1) % list.length;
            load(cur); a.play();
        }

        // Premium Background (Particles)
        const canvas = document.getElementById('canvas-bg');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let p = [];
        for(let i=0; i<50; i++) p.push({x:Math.random()*canvas.width, y:Math.random()*canvas.height, r:Math.random()*2, d:Math.random()*1});
        function draw() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "rgba(0, 242, 254, 0.3)";
            p.forEach(i => {
                ctx.beginPath(); ctx.arc(i.x, i.y, i.r, 0, Math.PI*2); ctx.fill();
                i.y -= i.d; if(i.y < 0) i.y = canvas.height;
            });
            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

@app.route('/music/<path:filename>')
def get_music(filename):
    # Fayl adındakı boşluqları və mötərizələri avtomatik tanıyır
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
