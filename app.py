from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# Dalğalanan bayraq və dinamik effektlərlə yenilənmiş kod
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
        
        /* Dalğalanan Bayraq Effekti */
        .flag-wrapper { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 5px; }
        .flag-wrapper h1 { background: linear-gradient(45deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; margin: 0; }
        .waving-flag { width: 50px; height: 30px; background-image: url('https://flagcdn.com/w160/az.png'); background-size: cover; background-position: center; border-radius: 4px; animation: wave 1.5s ease-in-out infinite; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
        @keyframes wave { 0%, 100% { transform: translateY(0) rotate(0); } 50% { transform: translateY(-5px) rotate(3deg); } }

        .tagline { color: #8b949e; font-size: 14px; margin-bottom: 30px; }
        input { width: 100%; padding: 16px; margin-bottom: 20px; border-radius: 12px; border: 1px solid #30363d; background: #1c2128; color: white; box-sizing: border-box; font-size: 16px; transition: 0.3s; }
        input:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 10px rgba(0, 242, 254, 0.2); }
        
        button { width: 100%; padding: 16px; background: linear-gradient(45deg, #238636, #2ea043); border: none; color: white; font-weight: bold; border-radius: 12px; cursor: pointer; font-size: 16px; transition: 0.3s; box-shadow: 0 4px 15px rgba(35, 134, 54, 0.3); position: relative; overflow: hidden; }
        button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(35, 134, 54, 0.4); }
        button::after { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: rgba(255, 255, 255, 0.1); transform: rotate(45deg); transition: 0.5s; }
        button:hover::after { left: 100%; top: 100%; }

        .dl-link { display: block; margin-top: 25px; background: linear-gradient(45deg, var(--secondary), var(--primary)); color: white; text-decoration: none; padding: 16px; border-radius: 12px; font-weight: bold; animation: pulse 2s infinite; }
        .contact-box { margin-top: 30px; padding-top: 20px; border-top: 1px solid #2d333b; text-align: center; }
        .tg-link { display: block; color: var(--primary); text-decoration: none; font-weight: bold; font-size: 15px; margin: 10px 0; padding: 8px; border: 1px dashed #30363d; border-radius: 8px; transition: 0.3s; position: relative; }
        .tg-link:hover { background: rgba(0, 242, 254, 0.1); border-color: var(--primary); }
        .tg-link::before { content: '✈️'; position: absolute; left: 15px; top: 50%; transform: translateY(-50%); }

        .counter { margin-top: 20px; font-size: 12px; color: #8b949e; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; display: inline-block; }
        
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.9; transform: scale(1.03); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="flag-wrapper">
            <h1>ZODIAC</h1>
            <div class="waving-flag"></div>
        </div>
        <p class="tagline">TikTok Videolarını Logosuz Endir</p>
        
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok video linkini bura qoyun..." required>
            <button type="submit">VİDEONU ANALİZ ET & YÜKLƏ</button>
        </form>

        {% if video_url %}
            <a href="{{ video_url }}" class="dl-link" target="_blank" download>📥 LOGOSUZ VİDEONU YÜKLƏ</a>
        {% endif %}

        <div class="contact-box">
            <p style="color: #8b949e; font-size: 13px; margin-bottom: 10px;">Reklam və Əməkdaşlıq üçün:</p>
            <a href="https://t.me/zodiac06" class="tg-link">@zodiac06</a>
            <a href="https://t.me/BakuUnderground" class="tg-link">@BakuUnderground</a>
            
            <div class="counter">
                Ziyarətçi sayı:<br>
                <img src="https://hitwebcounter.com/counter/counter.php?page=zodiac_downloader_v2&style=0006&nbdigits=5&type=page&initCount=0" title="Free Counter" Alt="web counter" border="0" style="margin-top: 5px;">
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
            # TikWM API vasitəsilə videonu çəkirik
            res = requests.get(f"https://www.tikwm.com/api/?url={link}").json()
            video_url = res['data']['play']
        except:
            pass
    return render_template_string(HTML, video_url=video_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
