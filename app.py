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
    <title>Zodiac Downloader 🇦🇿</title>
    <style>
        :root { --primary: #00f2fe; --secondary: #4facfe; --bg: #0b0e11; --card: #151921; }
        body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px 15px; margin: 0; }
        .container { background: var(--card); border: 1px solid #2d333b; padding: 25px; border-radius: 20px; max-width: 450px; margin: auto; box-shadow: 0 15px 35px rgba(0,0,0,0.7); }
        
        h1 { background: linear-gradient(45deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 30px; margin: 10px 0; font-weight: 900; }
        .section-title { color: var(--primary); font-size: 16px; margin-bottom: 12px; font-weight: bold; text-transform: uppercase; }
        
        .box { background: #0d1117; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 25px; }
        input { width: 100%; padding: 15px; margin-bottom: 15px; border-radius: 10px; border: 1px solid #30363d; background: #151921; color: white; box-sizing: border-box; }
        
        .btn-tt { background: linear-gradient(45deg, #ff0050, #00f2fe); }
        .btn-ig { background: linear-gradient(45deg, #833ab4, #fd1d1d, #fcb045); }
        button { width: 100%; padding: 15px; border: none; color: white; font-weight: bold; border-radius: 10px; cursor: pointer; transition: 0.3s; }
        button:hover { transform: scale(1.02); opacity: 0.9; }

        .dl-link { display: block; margin-top: 15px; background: #238636; color: white; text-decoration: none; padding: 15px; border-radius: 10px; font-weight: bold; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }

        .contact-box { margin-top: 20px; border-top: 1px solid #2d333b; padding-top: 20px; }
        .tg-link { display: block; color: var(--primary); text-decoration: none; font-weight: bold; font-size: 14px; margin: 8px 0; padding: 12px; border: 1px solid #30363d; border-radius: 12px; transition: 0.3s; }
        .tg-link:hover { background: rgba(0, 242, 254, 0.1); border-color: var(--primary); }
    </style>
</head>
<body>
    <div class="container">
        <h1>ZODIAC 🇦🇿</h1>

        <div class="box">
            <div class="section-title">🎵 TikTok Video</div>
            <form method="POST">
                <input type="hidden" name="type" value="tiktok">
                <input type="text" name="url" placeholder="TikTok linkini bura qoyun..." required>
                <button type="submit" class="btn-tt">TIKTOK ANALİZ ET</button>
            </form>
            {% if tt_url %}
                <a href="{{ tt_url }}" class="dl-link" target="_blank">📥 TIKTOK VİDEONU YÜKLƏ</a>
            {% endif %}
        </div>

        <div class="box">
            <div class="section-title">📸 Instagram Video</div>
            <form method="POST">
                <input type="hidden" name="type" value="insta">
                <input type="text" name="url" placeholder="Instagram linkini bura qoyun..." required>
                <button type="submit" class="btn-ig">INSTAGRAM ANALİZ ET</button>
            </form>
            {% if ig_url %}
                <a href="{{ ig_url }}" class="dl-link" target="_blank">📥 INSTA VİDEONU YÜKLƏ</a>
            {% endif %}
        </div>

        {% if error %} <p style="color:#ff4b4b">{{ error }}</p> {% endif %}

        <div class="contact-box">
            <p style="color: #8b949e; font-size: 13px; margin-bottom: 10px;">Reklam və Əməkdaşlıq üçün:</p>
            <a href="https://t.me/zodiac06" class="tg-link">✈️ @zodiac06</a>
            <a href="https://t.me/BakuUnderground" class="tg-link">📢 @BakuUnderground</a>
            
            <p style="font-size: 11px; color: #8b949e; margin-top: 15px;">
                Ziyarətçi sayı:<br>
                <img src="https://hitwebcounter.com/counter/counter.php?page=zodiac_v4&style=0006&nbdigits=5&type=page&initCount=0" border="0">
            </p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    tt_url = None
    ig_url = None
    error = None
    if request.method == 'POST':
        mode = request.form.get('type')
        link = request.form.get('url')
        try:
            if mode == "tiktok":
                res = requests.get(f"https://www.tikwm.com/api/?url={link}").json()
                tt_url = res['data']['play']
            elif mode == "insta":
                # Instagram üçün sürətli API sorğusu
                res = requests.get(f"https://api.snapany.com/api/v1/download?url={link}").json()
                ig_url = res['data']['media'][0]['url']
        except:
            error = "Video tapılmadı. Zəhmət olmasa linki yoxlayın."
            
    return render_template_string(HTML, tt_url=tt_url, ig_url=ig_url, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
