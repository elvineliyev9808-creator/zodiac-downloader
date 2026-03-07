from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Serverin sönməməsi üçün Keep-Alive
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
    <title>TikTok Video Downloader | ZODIAC SSSTIK</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --main: #2af598; --blue: #009efd; --dark: #1e293b; }
        body { background-color: #f3f7fa; font-family: 'Roboto', sans-serif; margin: 0; padding: 0; color: #333; }
        
        /* Header */
        header { background: white; padding: 15px 5%; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .logo { font-weight: 900; font-size: 24px; color: var(--dark); }
        .logo span { color: var(--blue); }

        /* Hero Section */
        .hero { background: linear-gradient(135deg, var(--blue) 0%, var(--main) 100%); padding: 60px 20px; text-align: center; color: white; }
        .hero h1 { margin: 0 0 10px; font-size: 28px; font-weight: 900; }
        .hero p { opacity: 0.9; font-size: 15px; margin-bottom: 30px; }

        /* Search Box */
        .search-container { max-width: 700px; margin: -40px auto 0; padding: 0 15px; }
        .search-form { background: white; padding: 10px; border-radius: 50px; display: flex; box-shadow: 0 15px 40px rgba(0,0,0,0.1); border: 1px solid #eee; }
        input { flex: 1; border: none; padding: 15px 25px; outline: none; font-size: 16px; border-radius: 50px; color: #444; }
        .btn-dl { background: var(--dark); color: white; border: none; padding: 0 35px; border-radius: 50px; font-weight: 700; cursor: pointer; transition: 0.3s; text-transform: uppercase; font-size: 14px; }
        .btn-dl:hover { background: #000; transform: scale(1.02); }

        /* Result Area */
        .res-card { max-width: 500px; margin: 40px auto; background: white; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05); animation: fadeInUp 0.5s ease; }
        .save-btn { display: block; background: #22c55e; color: white; text-decoration: none; padding: 15px; border-radius: 12px; font-weight: 700; margin-top: 15px; font-size: 15px; }

        /* Trend Player */
        .mini-player { position: fixed; bottom: 30px; left: 30px; background: white; padding: 10px 20px; border-radius: 50px; display: flex; align-items: center; gap: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: 1px solid #eee; z-index: 100; }
        .p-btn { width: 40px; height: 40px; border-radius: 50%; border: none; background: var(--blue); color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 14px; }
        .t-info { font-size: 12px; font-weight: 700; color: #555; }

        /* AI Support Bot */
        #chat-win { display: none; position: fixed; bottom: 100px; right: 30px; width: 320px; height: 400px; background: white; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); flex-direction: column; overflow: hidden; border: 1px solid #eee; z-index: 1000; }
        .ch-h { background: var(--dark); color: white; padding: 15px; font-weight: 700; font-size: 14px; }
        .ch-b { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; font-size: 13px; background: #f9f9f9; }
        .msg { padding: 10px 15px; border-radius: 15px; max-width: 85%; line-height: 1.4; }
        .bot { background: #e2e8f0; align-self: flex-start; color: #333; }
        .user { background: var(--blue); color: white; align-self: flex-end; }
        .ch-f { padding: 10px; border-top: 1px solid #eee; display: flex; background: white; }
        .ch-f input { padding: 10px; border: 1px solid #ddd; border-radius: 10px; font-size: 13px; }

        #chat-trigger { position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: var(--dark); border-radius: 50%; color: white; border: none; font-size: 24px; cursor: pointer; box-shadow: 0 10px 30px rgba(0,0,0,0.2); z-index: 1001; }

        @keyframes fadeInUp { from { opacity:0; transform: translateY(20px); } to { opacity:1; transform: translateY(0); } }
    </style>
</head>
<body>

    <header><div class="logo">ZODIAC<span>SSSTIK</span></div></header>

    <div class="hero">
        <h1>TikTok Video Yükləyici</h1>
        <p>TikTok videolarını loqosuz, sürətli və pulsuz endirin</p>
    </div>

    <div class="search-container">
        <form method="POST" class="search-form">
            <input type="text" name="u" placeholder="TikTok video linkini bura yapışdırın..." required>
            <button type="submit" class="btn-dl">ENDİR</button>
        </form>

        {% if dl %}
        <div class="res-card">
            <div style="color: #22c55e; font-weight: 700; margin-bottom: 10px;">Video Hazırdır! ✅</div>
            <a href="{{ dl }}" class="save-btn" target="_blank">📥 VİDEONU YÜKLƏ (.MP4)</a>
            <p style="font-size: 12px; color: #888; margin-top: 15px;">Əgər yükləmə başlamasa, düyməyə basıb saxlayın və "Saxla" seçin.</p>
        </div>
        {% endif %}
    </div>

    <div class="mini-player">
        <button class="p-btn" onclick="tglM()" id="ctrl">▶</button>
        <div class="t-info">Trend Background Mix</div>
    </div>

    <div id="chat-win">
        <div class="ch-h">ZODIAC DƏSTƏK BOTU</div>
        <div class="ch-b" id="cb"><div class="msg bot">Salam! Mən Zodiac. Sizə necə kömək edə bilərəm?</div></div>
        <div class="ch-f"><input type="text" id="ci" placeholder="Mesajınızı yazın..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="chat-trigger" onclick="tglC()">💬</button>

    <audio id="audio" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"></audio>

    <script>
        const a = document.getElementById('audio');
        function tglM() {
            if(a.paused) { a.play(); document.getElementById('ctrl').innerText = "||"; }
            else { a.pause(); document.getElementById('ctrl').innerText = "▶"; }
        }
        function tglC() { const w = document.getElementById('chat-win'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Üzr istəyirəm, başa düşmədim. TikTok linkini yuxarıya qoyub 'ENDİR' düyməsinə basın.";
                if(v.includes("salam")) r = "Salam! Xoş gördük. Sizə video yükləməkdə necə kömək edim?";
                else if(v.includes("necesen")) r = "Çox sağ olun, yaxşıyam! Siz necəsiniz?";
                else if(v.includes("islemir")) r = "Lütfən linkin düzgün olduğundan və videonun silinmədiyindən əmin olun.";
                else if(v.includes("sagol") || v.includes("təşəkkür")) r = "Buyurun, hər zaman xidmətinizdəyik!";
                b.innerHTML += `<div class="msg bot">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 600);
        }
    </script>
</body>
</html>
