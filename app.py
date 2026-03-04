from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# Dizayn və Musiqi Sistemi (Matrix + Avara Vibe)
HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC ELITE 🇦🇿</title>
    <style>
        :root { --tt: #00f2fe; --ig: #ff0050; --bg: #000; }
        body { background: var(--bg); color: white; font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        #matrix { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.2; }
        .container { width: 90%; max-width: 450px; text-align: center; z-index: 1; padding: 20px; }
        h1 { font-size: 45px; margin-bottom: 5px; text-shadow: 0 0 15px var(--tt); letter-spacing: 8px; }
        .music-bar { margin-bottom: 20px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; border: 1px solid #333; }
        .m-btn { background: none; border: 1px solid #555; color: #ccc; padding: 8px 12px; cursor: pointer; border-radius: 5px; font-size: 11px; margin: 3px; font-weight: bold; }
        .m-btn:hover { background: white; color: black; }
        .box { background: rgba(0,0,0,0.8); padding: 25px; border-radius: 15px; margin-top: 20px; border: 1px solid #222; }
        .tt-box { border-top: 4px solid var(--tt); box-shadow: 0 5px 15px rgba(0, 242, 254, 0.1); }
        .ig-box { border-top: 4px solid var(--ig); box-shadow: 0 5px 15px rgba(255, 0, 80, 0.1); }
        input { width: 100%; padding: 12px; background: #080808; border: 1px solid #333; color: white; border-radius: 8px; margin-bottom: 10px; box-sizing: border-box; outline: none; }
        button { width: 100%; padding: 12px; border: none; color: black; font-weight: 900; border-radius: 8px; cursor: pointer; text-transform: uppercase; }
        .tt-btn { background: var(--tt); }
        .ig-btn { background: var(--ig); }
        .dl-btn { display: block; margin-top: 15px; background: #fff; color: #000; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; }
        .footer { margin-top: 30px; font-size: 11px; }
        .footer a { color: #555; text-decoration: none; margin: 0 10px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="container">
        <h1>ZODIAC</h1>
        <div class="music-bar">
            <p style="font-size: 10px; color: #888; margin-bottom: 8px;">🎵 VİBE-I SEÇ, BRAT:</p>
            <button class="m-btn" onclick="playM('https://dl.musicaz.net/files/music/2021/08/mahir-ay-brat-320.mp3')">MAHİR AY BRAT</button>
            <button class="m-btn" onclick="stopM()">🔇 STOP</button>
        </div>
        <div class="box tt-box">
            <h2 style="color: var(--tt); font-size: 14px;">TIKTOK MODULE</h2>
            <form method="POST"><input type="hidden" name="t" value="tt"><input type="text" name="u" placeholder="TikTok Linki..." required><button type="submit" class="tt-btn">ANALİZ ET</button></form>
            {% if tt %}<a href="{{ tt }}" class="dl-btn" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        </div>
        <div class="box ig-box">
            <h2 style="color: var(--ig); font-size: 14px;">INSTAGRAM MODULE</h2>
            <form method="POST"><input type="hidden" name="t" value="ig"><input type="text" name="u" placeholder="Instagram Linki..." required><button type="submit" class="ig-btn">ANALİZ ET</button></form>
            {% if ig %}<a href="{{ ig }}" class="dl-btn" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        </div>
        <div class="footer"><a href="https://t.me/zodiac06">@ADMIN</a> | <a href="https://t.me/BakuUnderground">@KANAL</a></div>
    </div>
    <audio id="bgA" loop></audio>
    <script>
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
        const a = document.getElementById('bgA');
        function playM(s) { a.src = s; a.play(); }
        function stopM() { a.pause(); }
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
    # Render-in məcburi tələbi olan port tənzimləməsi
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
