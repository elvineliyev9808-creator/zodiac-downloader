from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC V15 🇦🇿</title>
    <style>
        :root { --tt: #00f2fe; --ig: #ff0050; --bg: #000; }
        body { background: var(--bg); color: white; font-family: 'Courier New', monospace; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow-x: hidden; }
        #matrix { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.2; }
        .container { width: 90%; max-width: 450px; text-align: center; z-index: 1; }
        h1 { font-size: 40px; text-shadow: 0 0 15px var(--tt); letter-spacing: 5px; margin-bottom: 20px; }
        .music-box { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 20px; }
        .play-btn { background: var(--tt); border: none; color: black; padding: 15px 30px; border-radius: 10px; font-weight: 900; cursor: pointer; box-shadow: 0 0 20px var(--tt); font-size: 16px; width: 100%; }
        .play-btn:active { transform: scale(0.95); }
        .box { background: rgba(0,0,0,0.8); padding: 20px; border-radius: 15px; margin-top: 15px; border: 1px solid #222; }
        .tt-box { border-top: 4px solid var(--tt); }
        .ig-box { border-top: 4px solid var(--ig); }
        input { width: 100%; padding: 12px; background: #080808; border: 1px solid #333; color: white; border-radius: 8px; margin-bottom: 10px; box-sizing: border-box; }
        button.exec { width: 100%; padding: 12px; border: none; color: black; font-weight: bold; border-radius: 8px; cursor: pointer; }
        .dl-btn { display: block; margin-top: 10px; background: white; color: black; padding: 10px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="container">
        <h1>ZODIAC</h1>
        
        <div class="music-box">
            <p style="font-size: 12px; color: #888; margin-top:0;">🎵 MAHİR AY BRAT - SƏSİ AÇ:</p>
            <button class="play-btn" onclick="toggleM()" id="mBtn">▶ MUSIQINI BAŞLAT</button>
        </div>

        <div class="box tt-box">
            <form method="POST"><input type="hidden" name="t" value="tt"><input type="text" name="u" placeholder="TikTok Linki..." required><button type="submit" class="exec" style="background:var(--tt)">ANALIZ ET</button></form>
            {% if tt %}<a href="{{ tt }}" class="dl-btn" target="_blank">📥 YÜKLƏ</a>{% endif %}
        </div>

        <div class="box ig-box">
            <form method="POST"><input type="hidden" name="t" value="ig"><input type="text" name="u" placeholder="Instagram Linki..." required><button type="submit" class="exec" style="background:var(--ig)">ANALIZ ET</button></form>
            {% if ig %}<a href="{{ ig }}" class="dl-btn" target="_blank">📥 YÜKLƏ</a>{% endif %}
        </div>
    </div>

    <audio id="bgA" loop>
        <source src="https://www.mboxdrive.com/Mahir%20Ay%20Brat%20-%20Brat.mp3" type="audio/mpeg">
    </audio>

    <script>
        // Matrix fonu
        const canvas = document.getElementById('matrix'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const letters = "ZODIAC01"; const fontSize = 16;
        const columns = canvas.width / fontSize; const drops = Array(Math.floor(columns)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.1)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#00f2fe"; ctx.font = fontSize + "px monospace";
            for (let i = 0; i < drops.length; i++) {
                const text = letters.charAt(Math.floor(Math.random() * letters.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(draw, 35);

        // Musiqi idarəsi
        const a = document.getElementById('bgA');
        const btn = document.getElementById('mBtn');
        function toggleM() {
            if (a.paused) {
                a.play().then(() => { btn.innerText = "⏸ MUSIQINI DAYANDIR"; btn.style.background = "#ff0050"; btn.style.boxShadow = "0 0 20px #ff0050"; })
                .catch(() => alert("Xəta! Səhifəni yenilə və yenidən bas."));
            } else {
                a.pause(); btn.innerText = "▶ MUSIQINI BAŞLAT"; btn.style.background = "#00f2fe"; btn.style.boxShadow = "0 0 20px #00f2fe";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tt, ig = None, None
    if request.method == 'POST':
        t, u = request.form.get('t'), request.form.get('u')
        try:
            if t == "tt":
                r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
                tt = r['data']['play']
            elif t == "ig":
                r = requests.get(f"https://api.vppandora.com/get_video?url={u}").json()
                ig = r['video_url']
        except: pass
    return render_template_string(HTML, tt=tt, ig=ig)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
