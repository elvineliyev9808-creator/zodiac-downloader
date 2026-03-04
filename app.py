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
    <title>Zodiac Elite 🇦🇿</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #ffffff; --accent: #00f2fe; --bg: #0a0a0c; }
        body { 
            background: var(--bg); color: white; font-family: 'Inter', sans-serif; 
            margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh;
            background: radial-gradient(circle at top right, #1a1a2e, #0a0a0c);
        }

        .container { 
            background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1); padding: 40px 30px; 
            border-radius: 32px; max-width: 400px; width: 90%; text-align: center;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }

        .flag { width: 60px; margin-bottom: 20px; border-radius: 4px; filter: grayscale(20%); }
        h1 { font-size: 28px; font-weight: 700; letter-spacing: -1px; margin: 0 0 10px; }
        .subtitle { font-size: 13px; color: #888; margin-bottom: 30px; }

        .music-bar { margin-bottom: 30px; display: flex; justify-content: center; gap: 8px; }
        .m-btn { 
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            color: #ccc; padding: 6px 12px; border-radius: 20px; font-size: 11px; cursor: pointer; transition: 0.3s;
        }
        .m-btn:hover { background: white; color: black; }

        .input-group { margin-bottom: 20px; text-align: left; }
        .input-group label { font-size: 11px; color: #555; text-transform: uppercase; margin-left: 10px; font-weight: 700; }
        input { 
            width: 100%; padding: 16px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
            color: white; border-radius: 16px; margin-top: 8px; box-sizing: border-box; outline: none; transition: 0.3s;
        }
        input:focus { border-color: var(--accent); background: rgba(255,255,255,0.08); }

        button { 
            width: 100%; padding: 16px; border: none; color: black; font-weight: 700;
            border-radius: 16px; cursor: pointer; background: white; transition: 0.3s;
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(255,255,255,0.1); }

        .dl-btn { 
            display: block; margin-top: 15px; background: #00f2fe; color: black; 
            padding: 16px; border-radius: 16px; text-decoration: none; font-weight: 700; font-size: 14px;
        }

        .footer { margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px; }
        .footer a { color: #555; text-decoration: none; font-size: 12px; margin: 0 15px; transition: 0.3s; }
        .footer a:hover { color: white; }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://flagcdn.com/w160/az.png" class="flag">
        <h1>ZODIAC</h1>
        <p class="subtitle">Minimalist Video Downloader</p>

        <div class="music-bar">
            <button class="m-btn" onclick="playM('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3')">LOFI</button>
            <button class="m-btn" onclick="playM('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3')">PHONK</button>
            <button class="m-btn" onclick="stopM()">🔇</button>
        </div>

        <form method="POST" class="input-group">
            <label>TikTok / Instagram Link</label>
            <input type="text" name="u" placeholder="Linki bura yerləşdirin..." required>
            <button type="submit" style="margin-top: 15px;">ANALİZ ET</button>
        </form>

        {% if tt or ig %}
            <a href="{{ tt if tt else ig }}" class="dl-btn">VİDEONU YÜKLƏ</a>
        {% endif %}

        {% if e %}<p style="color: #ff4b4b; font-size: 12px;">{{ e }}</p>{% endif %}

        <div class="footer">
            <a href="https://t.me/zodiac06">ADMIN</a>
            <a href="https://t.me/BakuUnderground">CHANNEL</a>
        </div>
    </div>

    <audio id="bgA" loop></audio>

    <script>
        const a = document.getElementById('bgA');
        function playM(s) { a.src = s; a.play(); }
        function stopM() { a.pause(); }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tt, ig, e = None, None, None
    if request.method == 'POST':
        u = request.form.get('u')
        try:
            if "tiktok.com" in u:
                res = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
                tt = res['data']['play']
            elif "instagram.com" in u:
                res = requests.get(f"https://api.vppandora.com/get_video?url={u}").json()
                ig = res['video_url']
            else: e = "Düzgün link daxil edin."
        except: e = "Video tapılmadı."
    return render_template_string(HTML, tt=tt, ig=ig, e=e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
