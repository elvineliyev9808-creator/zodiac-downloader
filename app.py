from flask import Flask, render_template_string, request, send_from_directory, jsonify
import requests
import os
import threading
import time

app = Flask(__name__)

# --- ANTI-SLEEP SİSTEMİ ---
def stay_awake():
    while True:
        try:
            # ÖZ SAYT LİNKİNİ BURA YAZ (Məsələn: https://zodiac-downloader.onrender.com)
            requests.get("SƏNİN_RENDER_LİNKİN")
        except: pass
        time.sleep(300)

threading.Thread(target=stay_awake, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC | AI ELITE</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --main: #00f2fe; --glow: rgba(0, 242, 254, 0.4); --dark: #080808; }
        body { background: var(--dark); color: white; font-family: 'Inter', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow-x: hidden; }
        
        #stars { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.5; }

        .container { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 40px; 
            width: 95%; max-width: 420px; 
            padding: 40px 25px; 
            text-align: center; 
            box-shadow: 0 50px 100px rgba(0,0,0,0.9);
        }

        h1 { font-family: 'Orbitron', sans-serif; letter-spacing: 8px; font-size: 28px; margin-bottom: 5px; color: #fff; text-shadow: 0 0 15px var(--main); }
        .tag { font-size: 10px; color: var(--main); letter-spacing: 3px; margin-bottom: 30px; opacity: 0.8; }

        /* Bot Chat Style */
        .chat-box { 
            background: rgba(0,0,0,0.6); 
            border-radius: 20px; 
            height: 150px; 
            overflow-y: auto; 
            margin-bottom: 15px; 
            padding: 15px; 
            text-align: left;
            border: 1px solid rgba(255,255,255,0.05);
            font-size: 13px;
        }
        .bot-msg { color: var(--main); margin-bottom: 8px; border-left: 2px solid var(--main); padding-left: 8px; }
        .user-msg { color: #fff; margin-bottom: 8px; opacity: 0.8; text-align: right; }

        .input-group { display: flex; gap: 10px; margin-top: 10px; }
        .chat-input { flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 12px; border-radius: 12px; color: #fff; outline: none; font-size: 13px; }
        .send-btn { background: var(--main); border: none; padding: 10px 15px; border-radius: 12px; cursor: pointer; font-weight: bold; }

        /* Main Downloader */
        .dl-section { margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); }
        input[type="text"] { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 15px; border-radius: 15px; color: #fff; margin-bottom: 10px; }
        .main-btn { width: 100%; background: #fff; color: #000; border: none; padding: 15px; border-radius: 15px; font-weight: 900; cursor: pointer; }
    </style>
</head>
<body>
    <canvas id="stars"></canvas>
    <div class="container">
        <h1>ZODIAC</h1>
        <div class="tag">AI SUPPORT ACTIVE</div>

        <div class="chat-box" id="chat">
            <div class="bot-msg">ZODIAC AI: Salam brat, necəsən? Sənə necə kömək edə bilərəm?</div>
        </div>
        <div class="input-group">
            <input type="text" id="msg" class="chat-input" placeholder="Bota yaz...">
            <button class="send-btn" onclick="askBot()">💬</button>
        </div>

        <div class="dl-section">
            <form method="POST">
                <input type="text" name="u" placeholder="TikTok / IG linkini yapışdır..." required>
                <button type="submit" class="main-btn">ANALİZ ET</button>
            </form>
            {% if dl %}<a href="{{ dl }}" style="color:var(--main); display:block; margin-top:15px; font-weight:bold; text-decoration:none;" target="_blank">📥 VİDEONU YÜKLƏ</a>{% endif %}
        </div>
    </div>

    <script>
        // AI Bot Məntiqi
        function askBot() {
            let msgInput = document.getElementById('msg');
            let chat = document.getElementById('chat');
            let userText = msgInput.value.toLowerCase();
            
            if(!userText) return;

            // User mesajını göstər
            chat.innerHTML += `<div class="user-msg">${msgInput.value}</div>`;
            
            let response = "Başa düşmədim brat, bir də de.";
            
            if(userText.includes("salam")) response = "Salam! Necəsən? Video yükləmək istəyirsənsə linki aşağı yapışdır.";
            else if(userText.includes("necəsən")) response = "Mən botam, həmişə superəm! Sən necəsən?";
            else if(userText.includes("kim") || userText.includes("yaratdı")) response = "Məni ZODIAC ELITE sistemi üçün xüsusi olaraq hazırlayıblar. Mən sənin rəqəmsal köməkçinim.";
            else if(userText.includes("video") || userText.includes("yüklə")) response = "Aşağıdakı xanaya TikTok və ya Instagram linkini qoy, mən sənə birbaşa link verəcəm.";
            else if(userText.includes("sağ ol") || userText.includes("təşəkkür")) response = "Xoşdur brat, həmişə xidmətindəyik! 😎";

            // Bot cavabını göstər
            setTimeout(() => {
                chat.innerHTML += `<div class="bot-msg">ZODIAC AI: ${response}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }, 500);

            msgInput.value = "";
        }

        // Star Background
        const canvas = document.getElementById('stars');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let p = [];
        for(let i=0; i<80; i++) p.push({x:Math.random()*canvas.width, y:Math.random()*canvas.height, s:Math.random()*1});
        function anim() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle="#fff";
            p.forEach(s => { ctx.beginPath(); ctx.arc(s.x, s.y, s.s, 0, Math.PI*2); ctx.fill(); s.y-=0.2; if(s.y<0) s.y=canvas.height; });
            requestAnimationFrame(anim);
        }
        anim();
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
