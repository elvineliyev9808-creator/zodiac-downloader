from flask import Flask, render_template_string, request, send_from_directory
import requests
import os
import threading
import time

app = Flask(__name__)

# --- SERVERİN SÖNMƏMƏSİ ÜÇÜN (KEEP-ALIVE) ---
def keep_alive():
    while True:
        try: requests.get("http://127.0.0.1:10000")
        except: pass
        time.sleep(300)

threading.Thread(target=keep_alive, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | Professional Video Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --blue: #0062ff; --bg: #f8fafc; --text: #1e293b; --white: #ffffff; }
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: var(--bg); color: var(--text); margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        
        /* Nav */
        nav { background: var(--white); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-weight: 700; font-size: 22px; color: var(--blue); letter-spacing: -1px; }

        /* Main Section */
        .hero { padding: 60px 20px; text-align: center; background: linear-gradient(135deg, #0062ff 0%, #00d4ff 100%); color: white; }
        h1 { margin: 0 0 10px; font-size: 32px; font-weight: 700; }
        p { opacity: 0.9; font-size: 15px; }

        .search-area { max-width: 600px; margin: -40px auto 0; padding: 20px; }
        .input-group { background: var(--white); padding: 10px; border-radius: 15px; display: flex; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        input { flex: 1; border: none; padding: 15px; outline: none; font-size: 16px; border-radius: 10px; }
        .btn-dl { background: var(--blue); color: white; border: none; padding: 0 30px; border-radius: 10px; font-weight: 600; cursor: pointer; transition: 0.3s; }
        .btn-dl:hover { background: #004ecc; }

        /* Player Box */
        .m-player { max-width: 400px; margin: 40px auto; background: white; padding: 15px; border-radius: 20px; display: flex; align-items: center; gap: 15px; border: 1px solid #e2e8f0; }
        .p-btn { width: 45px; height: 45px; border-radius: 50%; border: none; background: #f1f5f9; cursor: pointer; color: var(--blue); font-size: 18px; }

        /* AI CHAT BOT SYSTEM */
        #chat-widget { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
        #chat-btn { width: 60px; height: 60px; background: var(--blue); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; cursor: pointer; box-shadow: 0 5px 20px rgba(0,98,255,0.4); border: none; }
        #chat-window { display: none; width: 300px; height: 400px; background: white; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); position: absolute; bottom: 80px; right: 0; flex-direction: column; overflow: hidden; border: 1px solid #eee; }
        .chat-header { background: var(--blue); color: white; padding: 15px; font-weight: 600; font-size: 14px; }
        .chat-body { flex: 1; padding: 15px; overflow-y: auto; font-size: 13px; background: #f9f9f9; }
        .msg { margin-bottom: 10px; padding: 8px 12px; border-radius: 10px; max-width: 80%; }
        .bot { background: #e2e8f0; align-self: flex-start; }
        .user { background: var(--blue); color: white; align-self: flex-end; margin-left: auto; }
        .chat-footer { padding: 10px; display: flex; border-top: 1px solid #eee; }
        .chat-footer input { padding: 8px; border: 1px solid #ddd; border-radius: 5px; flex: 1; font-size: 12px; }

        @media (max-width: 600px) { h1 { font-size: 24px; } .btn-dl { padding: 0 15px; } }
    </style>
</head>
<body>

    <nav><div class="logo">ZODIAC.</div></nav>

    <div class="hero">
        <h1>Video Downloader</h1>
        <p>TikTok və Instagram videolarını bir kliklə endirin</p>
    </div>

    <div class="search-area">
        <form method="POST" class="input-group">
            <input type="text" name="u" placeholder="Video linkini bura yapışdırın..." required>
            <button type="submit" class="btn-dl">ENDİR</button>
        </form>

        {% if dl %}
        <div style="margin-top: 20px; text-align: center; background: white; padding: 20px; border-radius: 15px; border: 1px solid #22c55e;">
            <p style="font-weight: 600; color: #166534; margin: 0 0 10px;">Hazırdır! ✅</p>
            <a href="{{ dl }}" style="background: #22c55e; color: white; text-decoration: none; padding: 12px 25px; border-radius: 8px; font-weight: 600; display: inline-block;" target="_blank">📥 VİDEONU YÜKLƏ</a>
        </div>
        {% endif %}
    </div>

    <div class="m-player">
        <button class="p-btn" onclick="toggleM()" id="mBtn">▶</button>
        <div>
            <div id="t-title" style="font-size: 12px; font-weight: 600;">Lotular - Mahir Ay</div>
            <div style="font-size: 10px; color: #64748b;">Playlist Mode</div>
        </div>
    </div>

    <div id="chat-widget">
        <div id="chat-window">
            <div class="chat-header">Zodiac Dəstək Botu</div>
            <div class="chat-body" id="chatBody">
                <div class="msg bot">Salam! Mən Zodiac. Sizə necə kömək edə bilərəm?</div>
            </div>
            <div class="chat-footer">
                <input type="text" id="chatInp" placeholder="Mesaj yaz..." onkeypress="if(event.key=='Enter') sendMsg()">
            </div>
        </div>
        <button id="chat-btn" onclick="toggleChat()">💬</button>
    </div>

    <audio id="audio" onended="nextS()"></audio>

    <script>
        // Musiqi Sistemi
        const songs = [
            {n: "Lotular - Mahir Ay", s: "Lotular(MP3_160K).mp3"},
            {n: "Ara Usaqlari - Mahir Ay", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - Пыяла", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];
        let cur = 0;
        const aud = document.getElementById('audio');
        const tit = document.getElementById('t-title');
        function load(i) { aud.src = "/music/" + encodeURIComponent(songs[i].s); tit.innerText = songs[i].n; }
        load(cur);
        function toggleM() { aud.paused ? aud.play().then(()=>document.getElementById('mBtn').innerText="||") : aud.pause(); }
        function nextS() { cur = (cur+1)%songs.length; load(cur); aud.play(); }

        // AI Chat Sistemi
        function toggleChat() { 
            const win = document.getElementById('chat-window');
            win.style.display = (win.style.display === 'flex') ? 'none' : 'flex';
        }
        function sendMsg() {
            const inp = document.getElementById('chatInp');
            const body = document.getElementById('chatBody');
            if(!inp.value) return;
            
            body.innerHTML += `<div class="msg user">${inp.value}</div>`;
            let val = inp.value.toLowerCase();
            inp.value = "";
            
            setTimeout(() => {
                let reply = "Başa düşmədim, lütfən linki bura yapışdırın.";
                if(val.includes("salam")) reply = "Salam! Xoş gəldiniz. Sizə necə kömək edim?";
                else if(val.includes("sağ ol") || val.includes("sagol")) reply = "Buyurun! Həmişə xidmətinizdəyik.";
                else if(val.includes("işləmir")) reply = "Linki tam kopyalayıb yapışdırdığınızdan əmin olun.";
                
                body.innerHTML += `<div class="msg bot">${reply}</div>`;
                body.scrollTop = body.scrollHeight;
            }, 600);
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
