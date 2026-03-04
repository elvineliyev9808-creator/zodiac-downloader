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
    <title>Zodiac Premium 🇦🇿</title>
    <style>
        :root { --primary: #00f2fe; --secondary: #4facfe; --bg: #05070a; --card: rgba(21, 25, 33, 0.8); }
        
        /* Hərəkətli Ulduzlu Fon */
        body { 
            background: var(--bg); color: white; font-family: 'Poppins', sans-serif; 
            margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh;
            background-image: radial-gradient(circle at center, #111 0%, #05070a 100%);
            overflow-x: hidden;
        }

        .container { 
            background: var(--card); backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 242, 254, 0.2); padding: 40px 25px; 
            border-radius: 30px; max-width: 450px; width: 90%;
            box-shadow: 0 0 50px rgba(0, 242, 254, 0.1); text-align: center;
        }

        /* HD Bayraq və Neon Başlıq */
        .az-flag { 
            width: 90px; height: 50px; margin: 0 auto 15px;
            background: url('https://flagcdn.com/w320/az.png') no-repeat center; 
            background-size: cover; border-radius: 8px; 
            filter: drop-shadow(0 0 15px rgba(0,242,254,0.6));
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

        h1 { 
            font-size: 42px; margin: 0; font-weight: 900; letter-spacing: 5px;
            background: linear-gradient(to right, #00f2fe, #4facfe);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.5));
        }

        .box { 
            background: rgba(13, 17, 23, 0.6); padding: 25px; border-radius: 20px; 
            border: 1px solid rgba(255, 255, 255, 0.05); margin-top: 25px;
            transition: 0.4s;
        }
        .box:hover { border-color: var(--primary); transform: translateY(-5px); }

        .label { font-size: 12px; text-transform: uppercase; letter-spacing: 2px; color: var(--primary); margin-bottom: 15px; display: block; font-weight: bold; }

        input { 
            width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #30363d; 
            background: #0d1117; color: white; box-sizing: border-box; 
            margin-bottom: 15px; transition: 0.3s;
        }
        input:focus { border-color: var(--primary); box-shadow: 0 0 15px rgba(0, 242, 254, 0.3); outline: none; }

        button { 
            width: 100%; padding: 16px; border: none; color: white; font-weight: bold; 
            border-radius: 12px; cursor: pointer; font-size: 16px; text-transform: uppercase;
            transition: 0.3s;
        }
        .btn-tt { background: linear-gradient(45deg, #ff0050, #00f2fe); box-shadow: 0 4px 15px rgba(255, 0, 80, 0.3); }
        .btn-ig { background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045); box-shadow: 0 4px 15px rgba(253, 29, 29, 0.3); }
        button:hover { transform: scale(1.03); filter: brightness(1.2); }

        .dl-link { 
            display: block; margin-top: 20px; background: #238636; color: white; 
            text-decoration: none; padding: 18px; border-radius: 12px; font-weight: bold;
            box-shadow: 0 5px 20px rgba(35, 134, 54, 0.4); animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }

        .footer { margin-top: 30px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; }
        .tg-btn { 
            display: inline-block; width: 45%; margin: 5px; padding: 10px; 
            border: 1px solid #30363d; border-radius: 10px; color: var(--primary);
            text-decoration: none; font-size: 12px; font-weight: bold; transition: 0.3s;
        }
        .tg-btn:hover { background: rgba(0, 242, 254, 0.1); border-color: var(--primary); }

        .counter { font-size: 10px; color: #8b949e; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="az-flag"></div>
        <h1>ZODIAC</h1>
        <p style="font-size: 12px; color: #8b949e;">Premium Video Downloader</p>

        <div class="box">
            <span class="label">🎵 TikTok Video</span>
            <form method="POST">
                <input type="hidden" name="t" value="tt">
                <input type="text" name="u" placeholder="Linki bura yapışdır..." required>
                <button type="submit" class="btn-tt">Analiz Et</button>
            </form>
            {% if tt %}<a href="{{ tt }}" class="dl-link" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        </div>

        <div class="box">
            <span class="label">📸 Instagram Reels</span>
            <form method="POST">
                <input type="hidden" name="t" value="ig">
                <input type="text" name="u" placeholder="Linki bura yapışdır..." required>
                <button type="submit" class="btn-ig">Analiz Et</button>
            </form>
            {% if ig %}<a href="{{ ig }}" class="dl-link" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        </div>

        {% if e %}<p style="color:#ff4b4b; font-size: 14px; margin-top: 15px;">{{ e }}</p>{% endif %}

        <div class="footer">
            <a href="https://t.me/zodiac06" class="tg-btn">✈️ ADMİN</a>
            <a href="https://t.me/BakuUnderground" class="tg-btn">📢 KANAL</a>
            <div class="counter">
                Ziyarətçi: <br>
                <img src="https://hitwebcounter.com/counter/counter.php?page=zodiac_v8&style=0006&nbdigits=5">
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tt, ig, e = None, None, None
    if request.method == 'POST':
        t, u = request.form.get('t'), request.form.get('u')
        try:
            if t == "tt":
                res = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
                tt = res['data']['play']
            elif t == "ig":
                # Instagram üçün ən güclü API
                res = requests.get(f"https://api.vppandora.com/get_video?url={u}").json()
                ig = res['video_url']
        except:
            e = "Video tapılmadı! Linkin doğruluğunu yoxlayın."
    return render_template_string(HTML, tt=tt, ig=ig, e=e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
