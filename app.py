from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# Azərbaycan üçün professional Dark Mode dizayn
HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zodiac Downloader 🇦🇿</title>
    <style>
        body { background: #0d1117; color: white; font-family: sans-serif; text-align: center; padding: 50px 15px; }
        .box { background: #161b22; border: 1px solid #30363d; padding: 30px; border-radius: 12px; max-width: 400px; margin: auto; }
        h1 { color: #58a6ff; text-shadow: 0 0 10px #58a6ff; }
        input { width: 100%; padding: 12px; margin: 20px 0; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #238636; border: none; color: white; font-weight: bold; border-radius: 6px; cursor: pointer; }
        .dl-link { display: block; margin-top: 25px; background: #1f6feb; color: white; text-decoration: none; padding: 12px; border-radius: 6px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h1>ZODIAC 🇦🇿</h1>
        <p>TikTok Videolarını Logosuz Endir</p>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini yapışdırın..." required>
            <button type="submit">VİDEONU HAZIRLA</button>
        </form>
        {% if video_url %}
            <a href="{{ video_url }}" class="dl-link" target="_blank">📥 VİDEONU YÜKLƏ</a>
        {% endif %}
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
            res = requests.get(f"https://www.tikwm.com/api/?url={link}").json()
            video_url = res['data']['play']
        except: pass
    return render_template_string(HTML, video_url=video_url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
