from flask import Flask, render_template_string, request, send_from_directory
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC ELITE V16 🇦🇿</title>
    <style>
        :root { --tt: #00f2fe; --ig: #ff0050; --bg: #000; }
        body { background: var(--bg); color: white; font-family: 'Courier New', monospace; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow-x: hidden; }
        #matrix { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.15; }
        .container { width: 90%; max-width: 420px; text-align: center; z-index: 1; padding: 20px; }
        h1 { font-size: 45px; text-shadow: 0 0 15px var(--tt); letter-spacing: 8px; margin-bottom: 20px; }
        .player-card { background: rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; border: 1px solid #333; margin-bottom: 20px; box-shadow: 0 0 20px rgba(0,242,254,0.1); }
        .track-name { font-size: 13px; color: var(--tt); margin-bottom: 15px; font-weight: bold; min-height: 1.5em; }
        .p-btn { background: var(--tt); border: none; color: black; padding: 15px; border-radius: 12px; font-weight: 900; cursor: pointer; width: 100%; font-size: 16px; box-shadow: 0 0 15px var(--tt); }
        .box { background: rgba(0,0,0,0.85); padding: 20px; border-radius: 15px; margin-top: 15px; border: 1px solid #222; border-top: 3px solid var(--tt); }
        input { width: 100%; padding: 12px; background: #080808; border: 1px solid #333; color: white; border-radius: 8px; margin-bottom: 10px; box-sizing: border-box; outline: none; }
        button.exec { width: 100%; padding: 12px; border: none; background: var(--tt); color: black; font-weight: bold; border-radius: 8px; cursor: pointer; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="container">
        <h1>ZODIAC</h1>
        <div class="player-card">
            <div class="track-name" id="trackDisplay">Sistem Hazırlanır...</div>
            <button class="p-btn" onclick="toggleM()" id="mBtn">▶ MUSİQİNİ BAŞLAT</button>
        </div>
        <div class="box">
            <form method="POST"><input type="text" name="u" placeholder="TikTok/IG Linki..." required><button type="submit" class="exec">ANALİZ ET</button></form>
            {% if dl %}<a href="{{ dl }}" style="display:block; margin-top:15px; color:white; font-weight:bold; text-decoration:none;" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        </div>
    </div>

    <audio id="aud"></audio>

    <script>
        // Sənin yüklədiyin fayl adlarına tam uyğun siyahı
        const playlist = [
            {n: "LOTULAR - MAHİR AY BRAT", s: "/music/Lotular(MP3_160K).mp3"},
            {n: "ARA USAQLARI - MAHİR AY BRAT", s: "/music/Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - Пыяла x Sarışan Hallar", s: "/music/AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];

        let current = 0;
        const a = document.getElementById('aud');
        const b = document.getElementById('mBtn');
        const t = document.getElementById('trackDisplay');

        function load(idx) {
            a.src = playlist[idx].s;
            t.innerText = "OXUYUR: " + playlist[idx].n;
            a.load();
        }

        load(current);

        function toggleM() {
            if(a.paused) {
                a.play().then(() => { b.innerText = "⏸ DAYANDIR"; b.style.background = "#ff0050"; b.style.boxShadow = "0 0 15px #ff0050"; })
                .catch(() => alert("Ekrana bir dəfə toxun!"));
            } else {
                a.pause(); b.innerText = "▶ BAŞLAT"; b.style.background = "#00f2fe"; b.style.boxShadow = "0 0 15px #00f2fe";
            }
        }

        // MAHNİ BİTDİKDƏ AVTOMATİK NÖVBƏTİ
        a.onended = function() {
            current = (current + 1) % playlist.length;
            load(current);
            a.play();
        };

        // Matrix fonu
        const canvas = document.getElementById('matrix'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const drops = Array(Math.floor(canvas.width/16)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0,0,0,0.1)"; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "#00f2fe"; ctx.font = "16px monospace";
            drops.forEach((y, i) => {
                ctx.fillText("01"[Math.floor(Math.random()*2)], i*16, y*16);
                if(y*16 > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 35);
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
