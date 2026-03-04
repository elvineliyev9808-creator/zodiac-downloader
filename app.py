from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# Bu hissə saytın dizaynı və musiqi sistemidir
HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC ELITE</title>
    <style>
        body { background: #050505; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .card { background: #111; padding: 30px; border-radius: 20px; border: 1px solid #333; width: 90%; max-width: 400px; text-align: center; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #444; background: #000; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; border-radius: 8px; border: none; background: white; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #00f2fe; }
        .m-btn { background: none; border: 1px solid #444; color: #888; padding: 5px 10px; margin: 5px; cursor: pointer; border-radius: 5px; font-size: 10px; }
        .dl-link { display: block; margin-top: 15px; background: #00f2fe; color: black; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: bold; }
        .footer { margin-top: 20px; font-size: 11px; color: #555; }
        a { color: #888; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1 style="letter-spacing: 3px; color: #00f2fe;">ZODIAC</h1>
        <div class="music-box">
            <button class="m-btn" onclick="play('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3')">LOFI</button>
            <button class="m-btn" onclick="play('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3')">PHONK</button>
            <button class="m-btn" onclick="document.getElementById('bg').pause()">🔇</button>
        </div>
        <form method="POST">
            <input type="text" name="u" placeholder="TikTok və ya Instagram linki..." required>
            <button type="submit">VİDEONU TAP</button>
        </form>
        {% if d %}<a href="{{ d }}" class="dl-link" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        {% if e %}<p style="color:red; font-size: 12px;">{{ e }}</p>{% endif %}
        <audio id="bg" loop></audio>
        <div class="footer">
            <a href="https://t.me/zodiac06">ADMIN</a> | <a href="https://t.me/BakuUnderground">CHANNEL</a>
        </div>
    </div>
    <script>function play(s){var a=document.getElementById('bg');a.src=s;a.play();}</script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    d, e = None, None
    if request.method == 'POST':
        u = request.form.get('u', '')
        try:
            if "tiktok.com" in u:
                r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
                d = r['data'].get('play')
            elif "instagram.com" in u:
                r = requests.get(f"https://api.vppandora.com/get_video?url={u}").json()
                d = r.get('video_url')
            if not d: e = "Video tapılmadı və ya profil gizlidir."
        except Exception:
            e = "Xəta baş verdi. Linki yoxlayın."
    return render_template_string(HTML, d=d, e=e)

if __name__ == "__main__":
    # Render üçün port tənzimləməsi
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
