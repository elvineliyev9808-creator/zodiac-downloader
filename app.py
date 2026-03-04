from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Zodiac 🇦🇿</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0b0e11; color: white; text-align: center; font-family: sans-serif; padding: 20px; }
        .box { background: #151921; padding: 20px; border-radius: 15px; max-width: 400px; margin: auto; }
        input { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; }
        button { background: #2ea043; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .flag { font-size: 40px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="flag">🇦🇿</div>
        <h1>ZODIAC DOWNLOADER</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="TikTok linkini bura qoy..." required>
            <button type="submit">ENDİR</button>
        </form>
        {% if video_url %}
            <br><a href="{{ video_url }}" style="color: #4facfe; font-weight: bold;">📥 VİDEONU YÜKLƏ</a>
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
