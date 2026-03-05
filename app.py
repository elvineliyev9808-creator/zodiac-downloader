from flask import Flask, render_template_string, request, send_from_directory
import requests
import os
import threading
import time

app = Flask(__name__)

# --- ANTI-SLEEP SİSTEMİ (Saytın sönməməsi üçün) ---
def keep_alive():
    while True:
        try:
            # Buraya öz saytının linkini yazacaqsan
            requests.get("https://zodiac-downloader.onrender.com")
        except:
            pass
        time.sleep(600) # 10 dəqiqədən bir "oyan" mesajı göndərir

# Arxa fonda işə salırıq
threading.Thread(target=keep_alive, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC PREMIUM V18</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@300;600&display=swap" rel="stylesheet">
    <style>
        :root { --p: #00f2fe; --s: #4facfe; --bg: #0a0a0a; }
        body { background: var(--bg); color: white; font-family: 'Poppins', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        
        /* Premium Background */
        .gradient-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background: radial-gradient(circle at center, #111 0%, #000 100%); }
        .circle { position: absolute; background: var(--p); filter: blur(100px); border-radius: 50%; opacity: 0.15; animation: move 15s infinite alternate; }

        .card { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 35px; width: 90%; max-width: 420px; padding: 45px 35px; text-align: center; box-shadow: 0 40px 100px rgba(0,0,0,0.8); transition: 0.5s; }
        
        h1 { font-family: 'Orbitron', sans-serif; font-size: 35px; margin: 0; background: linear-gradient(45deg, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 5px; }
        .tag { font-size: 9px; letter-spacing: 3px; color: #555; margin-bottom: 30px; text-transform: uppercase; }

        /* Modern Player */
        .player { background: rgba(0,0,0,0.3); border-radius: 25px; padding: 20px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 30px; }
        #track-name { font-size: 11px; color: var(--p); font-weight: 600; margin-bottom: 15px; text-transform: uppercase; }
        .play-btn { background: white; border: none; width: 65px; height: 65px; border-radius: 50%; font-size: 22px; cursor: pointer; transition: 0.4s ease; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,242,254,0.2); }
        .play-btn:active { transform: scale(0.9); }
        .is-playing { background: #ff0050; color: white; box-shadow: 0 10px 25px rgba(255, 0, 80, 0.3); }

        /* Input Styles */
        input { width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 16px 22px; border-radius: 18px; color: white; outline: none; transition: 0.3s; margin-bottom: 15px; }
        input:focus { border-color: var(--p); background: rgba(255,255,255,0.08); }
        .btn { width: 100%; background: linear-gradient(45deg, var(--p), var(--s)); border: none; padding: 16px; border-radius: 18px; color: black; font-weight: 800; cursor: pointer; transition: 0.3s; }

        @keyframes move { from { transform: translate(-20%, -20%); } to { transform: translate(20%, 20%); } }
    </style>
</head>
<body>
    <div class="gradient-bg"><div class="circle" style="width:300px; height:300px; top:10%; left:10%;"></div></div>
    
    <div class="card">
        <h1>ZODIAC</h1>
        <div class="tag">Always Active System</div>

        <div class="player">
            <div id="track-name">Musiqi Hazırlanır...</div>
            <button class="play-btn" onclick="toggle()" id="ctrl-btn">▶</button>
        </div>

        <form method="POST">
            <input type="text" name="u" placeholder="TikTok və ya IG Linki..." required>
            <button type="submit" class="btn">ANALİZ ET</button>
        </form>

        {% if dl %}
        <div style="margin-top:20px; border: 1px dashed var(--p); padding: 15px; border-radius: 15px;">
            <a href="{{ dl }}" style="color:var(--p); text-decoration:none; font-weight:bold; font-size:13px;" target="_blank">📥 VİDEONU YÜKLƏ</a>
        </div>
        {% endif %}
    </div>

    <audio id="audio" onended="nextTrack()"></audio>

    <script>
        const playlist = [
            {n: "Lotular - Mahir Ay Brat", s: "Lotular(MP3_160K).mp3"},
            {n: "Ara Usaqlari - Mahir Ay Brat", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - Пыяла", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];

        let index = 0;
        const player = document.getElementById('audio');
        const btn = document.getElementById('ctrl-btn');
        const info = document.getElementById('track-name');

        function loadTrack(i) {
            // EncodeURIComponent boşluq və mötərizə xətasını həll edir
            player.src = "/music/" + encodeURIComponent(playlist[i].s);
            info.innerText = playlist[i].n;
        }

        loadTrack(index);

        function toggle() {
            if(player.paused) {
                player.play().then(() => {
                    btn.innerHTML = "||"; btn.classList.add('is-playing');
                }).catch(() => alert("Ekrana toxun, sonra Play bas!"));
            } else {
                player.pause(); btn.innerHTML = "▶"; btn.classList.remove('is-playing');
            }
        }

        function nextTrack() {
            index = (index + 1) % playlist.length;
            loadTrack(index);
            player.play();
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
