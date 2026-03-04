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
    <title>ZODIAC ELITE 🇦🇿</title>
    <style>
        :root { --tt: #00f2fe; --ig: #ff0050; --bg: #000; }
        body { background: var(--bg); color: white; font-family: 'Courier New', monospace; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow-x: hidden; }
        #matrix { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.2; }
        .container { width: 95%; max-width: 450px; text-align: center; z-index: 1; padding: 20px; }
        h1 { font-size: 45px; text-shadow: 0 0 15px var(--tt); letter-spacing: 8px; margin-bottom: 20px; }
        .music-card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 20px; }
        .p-btn { background: var(--tt); border: none; color: black; padding: 15px; border-radius: 10px; font-weight: 900; cursor: pointer; width: 100%; box-shadow: 0 0 20px var(--tt); font-size: 16px; }
        .box { background: rgba(0,0,0,0.85); padding: 20px; border-radius: 15px; margin-top: 15px; border: 1px solid #222; }
        .tt-box { border-top: 4px solid var(--tt); }
        .ig-box { border-top: 4px solid var(--ig); }
        input { width: 100%; padding: 12px; background: #080808; border: 1px solid #333; color: white; border-radius: 8px; margin-bottom: 10px; box-sizing: border-box; outline: none; }
        button.exec { width: 100%; padding: 12px; border: none; color: black; font-weight: bold; border-radius: 8px; cursor: pointer; text-transform: uppercase; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <div class="container">
        <h1>ZODIAC</h1>
        <div class="music-card">
            <p style="font-size: 12px; color: #888; margin-top:0;">🔊 DAXİLİ SİSTEM: MAHİR AY BRAT</p>
            <button class="p-btn" onclick="playMusic()" id="btnM">▶ MUSİQİNİ BAŞLAT</button>
        </div>
        <div class="box tt-box">
            <form method="POST"><input type="hidden" name="t" value="tt"><input type="text" name="u" placeholder="TikTok Linki..." required><button type="submit" class="exec" style="background:var(--tt)">ANALİZ ET</button></form>
            {% if tt %}<p style="margin-top:10px;"><a href="{{ tt }}" style="color:white; font-weight:bold;" target="_blank">📥 VİDEONU YÜKLƏ</a></p>{% endif %}
        </div>
        <div class="box ig-box">
            <form method="POST"><input type="hidden" name="t" value="ig"><input type="text" name="u" placeholder="Instagram Linki..." required><button type="submit" class="exec" style="background:var(--ig)">ANALİZ ET</button></form>
            {% if ig %}<p style="margin-top:10px;"><a href="{{ ig }}" style="color:white; font-weight:bold;" target="_blank">📥 VİDEONU YÜKLƏ</a></p>{% endif %}
        </div>
    </div>

    <audio id="player" loop src="/music/Lotular(MP3_160K).mp3"></audio>

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

        const a = document.getElementById('player');
        const b = document.getElementById('btnM');
        function playMusic() {
            if(a.paused) { 
                a.play().catch(e => alert("Səhifəyə toxun, sonra bas!")); 
                b.innerText = "⏸ DAYANDIR"; b.style.background = "#ff0050"; b.style.boxShadow = "0 0 20px #ff0050";
            } else { 
                a.pause(); b.innerText = "▶ BAŞLAT"; b.style.background = "#00f2fe"; b.style.boxShadow = "0 0 20px #00f2fe";
            }
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
