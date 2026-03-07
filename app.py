from flask import Flask, render_template_string, request, send_from_directory
import requests
import os
import threading
import time

app = Flask(__name__)

# --- SÖNMƏMƏ SİSTEMİ (KEEP-ALIVE) ---
def pinger():
    while True:
        try:
            # Saytın sönməməsi üçün öz-özünə sorğu göndərir
            requests.get("http://127.0.0.1:10000") 
        except:
            pass
        time.sleep(300) # 5 dəqiqə

threading.Thread(target=pinger, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --main: #00f2fe; --dark: #0f172a; --accent: #4facfe; }
        body { background-color: var(--dark); color: white; font-family: 'Poppins', sans-serif; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        
        /* Header */
        header { width: 100%; padding: 20px; text-align: center; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.1); }
        h1 { margin: 0; font-size: 28px; background: linear-gradient(to right, var(--main), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }

        /* Downloader Section */
        .container { width: 90%; max-width: 500px; margin-top: 40px; text-align: center; }
        .hero-text { font-size: 14px; color: #94a3b8; margin-bottom: 30px; }
        
        .input-box { background: #1e293b; padding: 8px; border-radius: 15px; display: flex; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid #334155; }
        input { flex: 1; background: transparent; border: none; padding: 15px; color: white; outline: none; font-size: 15px; }
        .dl-btn { background: linear-gradient(to right, var(--main), var(--accent)); border: none; padding: 12px 25px; border-radius: 12px; color: #000; font-weight: 700; cursor: pointer; transition: 0.3s; }
        .dl-btn:hover { opacity: 0.9; transform: scale(1.02); }

        /* Result Area */
        .result-card { margin-top: 25px; background: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid var(--main); animation: fadeIn 0.5s; }
        .save-btn { display: inline-block; text-decoration: none; background: white; color: black; padding: 12px 30px; border-radius: 10px; font-weight: bold; margin-top: 10px; }

        /* Mini Player Card */
        .player-card { margin-top: 40px; background: rgba(0, 242, 254, 0.05); border-radius: 20px; padding: 15px; border: 1px solid rgba(0, 242, 254, 0.2); width: 100%; }
        #track-name { font-size: 12px; color: var(--main); margin-bottom: 10px; font-weight: 600; }
        .play-btn { background: var(--main); border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; font-size: 18px; }

        /* Dəstək Botu Düyməsi */
        .support-bot { position: fixed; bottom: 25px; right: 25px; background: #24A1DE; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 14px; box-shadow: 0 5px 20px rgba(36, 161, 222, 0.4); display: flex; align-items: center; gap: 8px; transition: 0.3s; z-index: 100; }
        .support-bot:hover { transform: translateY(-5px); }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <header><h1>ZODIAC</h1></header>

    <div class="container">
        <div class="hero-text">TikTok & Instagram Video Downloader</div>

        <form method="POST" class="input-box">
            <input type="text" name="u" placeholder="Video linkini bura yapışdır..." required>
            <button type="submit" class="dl-btn">ENDİR</button>
        </form>

        {% if dl %}
        <div class="result-card">
            <p style="margin:0 0 15px 0; font-size: 13px;">Video Analiz Olundu ✅</p>
            <a href="{{ dl }}" class="save-btn" target="_blank">📥 VİDEONU YÜKLƏ</a>
        </div>
        {% endif %}

        <div class="player-card">
            <div id="track-name">Musiqi: Lotular</div>
            <button class="play-btn" onclick="togglePlay()" id="p-ctrl">▶</button>
        </div>
    </div>

    <a href="https://t.me/Senin_Telegram_Adin" class="support-bot" target="_blank">
        <span>✈</span> Dəstək Botu
    </a>

    <audio id="audio" onended="autoNext()"></audio>

    <script>
        const playlist = [
            {n: "MAHİR AY - LOTULAR", s: "Lotular(MP3_160K).mp3"},
            {n: "MAHİR AY - ARA USAQLARI", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - ПЫЯЛА REMIX", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];

        let cur = 0;
        const a = document.getElementById('audio');
        const b = document.getElementById('p-ctrl');
        const t = document.getElementById('track-name');

        function load(i) {
            a.src = "/music/" + encodeURIComponent(playlist[i].s);
            t.innerText = "Musiqi: " + playlist[i].n;
        }

        load(cur);

        function togglePlay() {
            if(a.paused) {
                a.play().then(() => b.innerText = "||").catch(() => alert("Ekrana bir dəfə toxun!"));
            } else {
                a.pause(); b.innerText = "▶";
            }
        }

        function autoNext() {
            cur = (cur + 1) % playlist.length;
            load(cur); a.play();
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
    dl = None
    if request.method == 'POST':
        u = request.form.get('u')
        try:
            r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
            dl = r['data']['play']
        except: pass
    return render_template_string(HTML, dl=dl)

if __name__ == "__main__":
    # Render port ayarı
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
