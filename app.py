from flask import Flask, render_template_string, request
import requests, os, threading, time

app = Flask(__name__)

# Render-in yuxuya getməməsi üçün pinger
def keep_alive():
    while True:
        try: requests.get("http://127.0.0.1:10000")
        except: pass
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

# HTML və Dizayn bir yerdə
HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        body { background: #000; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .card { background: rgba(255,255,255,0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); width: 90%; max-width: 400px; padding: 50px 30px; border-radius: 40px; text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,0.5); }
        h1 { font-family: 'Orbitron', sans-serif; font-size: 30px; letter-spacing: 8px; margin: 0; color: #fff; }
        .tag { display: inline-block; margin-top: 10px; padding: 5px 15px; background: rgba(0,242,255,0.1); color: #00f2ff; font-size: 10px; font-weight: 800; border-radius: 50px; text-transform: uppercase; }
        input { width: 100%; background: #111; border: 1px solid #222; padding: 18px; border-radius: 15px; color: #fff; margin-top: 30px; text-align: center; }
        .btn { width: 100%; background: #fff; color: #000; border: none; padding: 18px; border-radius: 15px; font-weight: 800; margin-top: 15px; cursor: pointer; transition: 0.2s; }
        .btn:active { transform: scale(0.96); background: #00f2ff; }
        .res { margin-top: 25px; padding: 15px; border: 1px dashed #00f2ff; border-radius: 15px; }
        .res a { color: #00f2ff; text-decoration: none; font-weight: 800; }
        #bot { position: fixed; bottom: 20px; right: 20px; background: #fff; color: #000; width: 50px; height: 50px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <h1>ZODIAC</h1>
        <div class="tag">7/24 Xidmətinizdəyik</div>
        <form method="POST">
            <input type="text" name="u" placeholder="TikTok Linki" required>
            <button type="submit" class="btn">VİDEONU TAP</button>
        </form>
        {% if dl %}
        <div class="res"><a href="{{ dl }}" target="_blank">📥 YÜKLƏMƏYƏ HAZIRDIR</a></div>
        {% endif %}
    </div>
    <div id="bot" onclick="alert('Zodiac AI: 7/24 xidmətinizdəyik! Linki yapışdırın və endirin.')">💬</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    dl = None
    if request.method == 'POST':
        u = request.form.get('u')
        try:
            # TikTok API sorğusu
            r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
            dl = r['data']['play']
        except: pass
    return render_template_string(HTML, dl=dl)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
