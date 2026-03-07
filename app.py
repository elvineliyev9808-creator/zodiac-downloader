from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Render-də 24/7 aktiv qalmaq üçün
def stay_online():
    while True:
        try: requests.get("http://127.0.0.1:10000")
        except: pass
        time.sleep(300)

threading.Thread(target=stay_online, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { background: #f4f7f6; font-family: 'Inter', sans-serif; margin: 0; padding: 0; color: #1a1a1a; }
        header { background: white; padding: 20px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
        .logo { font-weight: 900; font-size: 26px; color: #000; letter-spacing: -1px; }
        .logo span { color: #0062ff; }
        
        .main-hero { background: linear-gradient(135deg, #0062ff 0%, #00d4ff 100%); padding: 60px 20px; text-align: center; color: white; }
        .main-hero h1 { margin: 0; font-size: 32px; font-weight: 900; }
        .main-hero p { opacity: 0.9; font-size: 14px; margin-top: 10px; }

        .search-container { max-width: 650px; margin: -35px auto 40px; padding: 0 15px; }
        .input-group { background: white; padding: 10px; border-radius: 50px; display: flex; box-shadow: 0 15px 35px rgba(0,0,0,0.1); border: 1px solid #eee; }
        input { flex: 1; border: none; padding: 15px 25px; outline: none; font-size: 16px; border-radius: 50px; }
        .btn-download { background: #000; color: white; border: none; padding: 0 30px; border-radius: 50px; font-weight: 700; cursor: pointer; transition: 0.3s; }
        .btn-download:hover { transform: scale(1.03); background: #222; }

        .result-box { max-width: 450px; margin: 30px auto; background: white; padding: 30px; border-radius: 25px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
        .dl-btn { display: block; background: #00c853; color: white; text-decoration: none; padding: 15px; border-radius: 15px; font-weight: 800; font-size: 15px; }

        /* Azerbaijan Trend Player */
        .player-bar { position: fixed; bottom: 25px; left: 25px; background: white; padding: 12px 20px; border-radius: 50px; display: flex; align-items: center; gap: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); z-index: 100; border: 1px solid #f0f0f0; }
        .play-btn { width: 40px; height: 40px; border-radius: 50%; border: none; background: #0062ff; color: white; cursor: pointer; font-size: 14px; }
        .track-name { font-size: 12px; font-weight: 700; color: #444; }

        /* Smart AI Support */
        #chat-window { display: none; position: fixed; bottom: 100px; right: 25px; width: 320px; height: 450px; background: white; border-radius: 25px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); flex-direction: column; overflow: hidden; border: 1px solid #eee; z-index: 1000; }
        .chat-header { background: #000; color: white; padding: 20px; font-weight: 800; font-size: 14px; }
        .chat-body { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; font-size: 13px; background: #fdfdfd; }
        .msg { padding: 12px 16px; border-radius: 18px; max-width: 85%; line-height: 1.5; }
        .bot-msg { background: #f0f2f5; color: #333; align-self: flex-start; }
        .user-msg { background: #0062ff; color: white; align-self: flex-end; }
        .chat-footer { padding: 15px; border-top: 1px solid #eee; display: flex; gap: 8px; }
        .chat-footer input { flex: 1; padding: 10px 15px; border: 1px solid #ddd; border-radius: 12px; font-size: 13px; outline: none; }

        #chat-btn { position: fixed; bottom: 25px; right: 25px; width: 65px; height: 65px; background: #000; border-radius: 50%; color: white; border: none; font-size: 26px; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.2); z-index: 1001; }
    </style>
</head>
<body>

    <header><div class="logo">ZODIAC</div></header>

    <div class="main-hero">
        <h1>TikTok Video Downloader</h1>
        <p>Filtrsiz və loqosuz saniyələr içində yüklə</p>
    </div>

    <div class="search-container">
        <form method="POST" class="input-group">
            <input type="text" name="u" placeholder="TikTok linkini bura yapışdır..." required>
            <button type="submit" class="btn-download">ENDİR</button>
        </form>

        {% if dl %}
        <div class="result-box">
            <div style="font-weight: 800; color: #00c853; margin-bottom: 15px;">Video Tapıldı! ✅</div>
            <a href="{{ dl }}" class="dl-btn" target="_blank">📥 VİDEONU YÜKLƏ (.MP4)</a>
        </div>
        {% endif %}
    </div>

    <div class="player-bar">
        <button class="play-btn" onclick="toggleM()" id="m-ctrl">▶</button>
        <div class="track-name">Trend Azerbaijan Mood</div>
    </div>

    <div id="chat-window">
        <div class="chat-header">ZODIAC DƏSTƏK AI</div>
        <div class="chat-body" id="chat-b"><div class="msg bot-msg">Salam! Mən Zodiac AI. Azərbaycan dilində bütün suallarınızı cavablandırmağa hazıram.</div></div>
        <div class="chat-footer"><input type="text" id="chat-i" placeholder="Sualınızı yazın..." onkeypress="if(event.key=='Enter') sendM()"></div>
    </div>
    <button id="chat-btn" onclick="toggleC()">💬</button>

    <audio id="audio" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"></audio>

    <script>
        const audio = document.getElementById('audio');
        function toggleM() {
            if(audio.paused) { audio.play(); document.getElementById('m-ctrl').innerText = "||"; }
            else { audio.pause(); document.getElementById('m-ctrl').innerText = "▶"; }
        }
        function toggleC() {
            const win = document.getElementById('chat-window');
            win.style.display = (win.style.display === 'flex') ? 'none' : 'flex';
        }
        function sendM() {
            const inp = document.getElementById('chat-i');
            const box = document.getElementById('chat-b');
            if(!inp.value) return;
            box.innerHTML += `<div class="msg user-msg">${inp.value}</div>`;
            const v = inp.value.toLowerCase(); inp.value = ""; box.scrollTop = box.scrollHeight;
            setTimeout(() => {
                let r = "Bunu hələ ki anlamıram, amma TikTok linkini endirmək üçün kömək edə bilərəm.";
                if(v.includes("salam")) r = "Salam! Necə kömək edə bilərəm?";
                else if(v.includes("necesen")) r = "Mən Zodiac AI-am, hər şey qaydasındadır! Siz necəsiniz?";
                else if(v.includes("islemir")) r = "Linkin tam kopyalandığından və videonun silinmədiyindən əmin olun.";
                else if(v.includes("sagol") || v.includes("təşəkkür")) r = "Xoşdur! Hər zaman buradayam.";
                box.innerHTML += `<div class="msg bot-msg">${r}</div>`; box.scrollTop = box.scrollHeight;
            }, 600);
        }
    </script>
</body>
</html>
"""

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
