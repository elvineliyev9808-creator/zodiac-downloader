from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# Sənin bütün istəklərin daxil olan tam dizayn
HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zodiac Downloader 🇦🇿</title>
    <style>
        :root { --primary: #00f2fe; --secondary: #4facfe; --bg: #0b0e11; --card: #151921; }
        body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 40px 15px; margin: 0; }
        .container { background: var(--card); border: 1px solid #2d333b; padding: 35px; border-radius: 20px; max-width: 450px; margin: auto; box-shadow: 0 15px 35px rgba(0,0,0,0.7); }
        
        /* Dalğalanan Bayraq */
        .flag-wrapper { display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 5px; }
        h1 { background: linear-gradient(45deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 35px; margin: 0; font-weight: 900; }
        .waving-flag { width: 45px; height: 28px; background: url('https://flagcdn.com/w160/az.png') no-repeat center; background-size: cover; border-radius: 4px; animation: wave 2s ease-in-out infinite; }
        @keyframes wave { 0%, 100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-6px) rotate(4deg); } }

        .tagline { color: #8b949e; font-size: 14px; margin-bottom: 30px; }
        input { width: 100%; padding: 18px; margin-bottom: 20px; border-radius: 15px; border: 1px solid #30363d; background: #0d1117; color: white; box-sizing: border-box; font-size: 16px; transition: 0.4s; }
        input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 15px rgba(0, 242, 254, 0.2); }
        
        button { width: 100%; padding: 18px; background: linear-gradient(45deg, #238636, #2ea043); border: none; color: white; font-weight: bold; border-radius: 15px; cursor: pointer; font-size: 17px; transition: 0.3s; }
        button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(35, 134, 54, 0.5); }

        .dl-link { display: block; margin-top: 25px; background: linear-gradient(45deg, var(--secondary), var(--primary)); color: white; text-decoration: none; padding: 18px; border-radius: 15px; font-weight: bold; animation: pulse 2s infinite; font-size: 18px; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.03); } }

        .contact-box { margin-top: 35px; padding-top: 25px; border-top: 1px solid #2d333b; }
        .tg-link { display: block; color: var(--primary); text-decoration: none; font-weight: bold; font-size: 15px; margin: 12px 0; padding: 12px; border: 1px solid #30363d; border-radius: 12px; transition: 0.3s; }
        .tg-link:hover { background: rgba(0, 242, 254, 0.1); border-color: var(--primary); }

        .counter { margin-top: 20px; font-size: 12px; color: #8b949e; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="flag-wrapper">
            <h1>ZODIAC</h1>
            <div class="waving-flag"></div>
        </div>
        <p class="tagline">TikTok və Instagram Videolarını Logosuz Endir 🇦🇿</p>
        
        <form method="POST">
            <input type="text" name="url" placeholder="Video linkini bura qoyun..." required>
            <button type="submit">VİDEONU ANALİZ ET</button>
        </form>

        {% if video_url %}
            <a href="{{ video_url }}" class="dl-link" target="_blank" download>📥 VİDEONU YÜKLƏ</a>
        {% endif %}

        <div class="contact-box">
            <p style="color: #8b949e; font-size: 13px; margin-bottom: 12px;">Reklam və Əməkdaşlıq üçün:</p>
            <a href="https://t.me/zodiac06" class="tg-link">✈️ @zodiac06</a>
            <a href="https://t.me/BakuUnderground" class="tg-link">📢 @BakuUnderground</a>
            
            <div class="counter">
                Ziyarətçi sayı:<br>
                <img src="https://hitwebcounter.com/counter/counter.php?page=zodiac_final_v2&style=0006&nbdigits=5&type=page&initCount=0" border="0" style="margin-top: 8px;">
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    if request.method == 'POST':
        link = request.form.get('url')
        try:
            if "tiktok.com" in link:
                res = requests.get(f"https://www.tikwm.com/api/?url={link}").json()
                video_url = res['data']['play']
            elif "instagram.com" in link:
                # Instagram üçün sürətli API
                res = requests.get(f"https://api.snapany.com/api/v1/download?url={link}").json()
                video_url = res['data']['media'][0]['url']
        except:
            pass
    return render_template_string(HTML, video_url=video_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
