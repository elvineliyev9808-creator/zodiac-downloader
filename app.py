from flask import Flask, render_template_string, request
import requests, os, threading, time

app = Flask(__name__)

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
    <title>ZODIAC | Official</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --gold: #ffd700; 
            --accent: #00f2ff;
            --bg: #000;
            --glass: rgba(255, 255, 255, 0.03);
        }
        
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        
        body { 
            background: var(--bg); color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; 
            margin: 0; display: flex; align-items: center; justify-content: center; 
            min-height: 100vh; overflow: hidden;
        }

        .bg-gradient { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #111 0%, #000 100%); z-index: -2; }
        .aura { position: fixed; width: 500px; height: 500px; background: var(--accent); filter: blur(150px); opacity: 0.04; border-radius: 50%; animation: float 15s infinite alternate; z-index: -1; }

        .main-card {
            background: var(--glass); backdrop-filter: blur(50px); border: 1px solid rgba(255, 255, 255, 0.08);
            width: 90%; max-width: 400px; padding: 50px 30px; border-radius: 45px; text-align: center;
            box-shadow: 0 40px 100px rgba(0,0,0,0.7); position: relative; z-index: 10;
        }

        h1 { font-family: 'Orbitron', sans-serif; font-size: 32px; letter-spacing: 12px; margin: 0; background: linear-gradient(180deg, #fff 0%, #444 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .service-tag { display: inline-block; margin-top: 15px; padding: 5px 15px; background: rgba(0, 242, 255, 0.08); color: var(--accent); font-size: 9px; font-weight: 800; letter-spacing: 2px; border-radius: 50px; text-transform: uppercase; border: 1px solid rgba(0, 242, 255, 0.1); }

        .input-group { margin-top: 40px; position: relative; }
        input { width: 100%; background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; color: #fff; font-size: 15px; text-align: center; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        input:focus { border-color: var(--accent); background: rgba(255, 255, 255, 0.08); box-shadow: 0 0 30px rgba(0, 242, 255, 0.1); transform: translateY(-2px); }

        .btn { width: 100%; margin-top: 15px; padding: 18px; background: #fff; color: #000; border: none; border-radius: 18px; font-weight: 800; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; cursor: pointer; transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .btn:active { transform: scale(0.96); background: var(--accent); }

        {% if dl %}
        .result { margin-top: 25px; padding: 20px; background: rgba(255, 255, 255, 0.02); border-radius: 20px; border: 1px dashed rgba(0, 242, 255, 0.3); animation: slide 0.5s ease; }
        .result a { color: var(--accent); text-decoration: none; font-weight: 800; font-size: 12px; letter-spacing: 1px; }
        {% endif %}

        /* REBORN BOT DESIGN */
        #bot-ui { 
            display: none; position: fixed; bottom: 100px; right: 25px; width: 310px; height: 420px; 
            background: rgba(10, 10, 10, 0.95); backdrop-filter: blur(30px); border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 30px; flex-direction: column; overflow: hidden; z-index: 1000; box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        }
        .b-h { background: rgba(255,255,255,0.03); padding: 20px; font-size: 12px; font-weight: 800; color: var(--accent); border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; }
        .b-b { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; scroll-behavior: smooth; }
        .msg { padding: 12px 16px; border-radius: 18px; font-size: 13px; line-height: 1.5; max-width: 85%; }
        .bot { background: rgba(255,255,255,0.05); color: #ccc; align-self: flex-start; border-bottom-left-radius: 5px; }
        .user { background: var(--accent); color: #000; align-self: flex-end; font-weight: 600; border-bottom-right-radius: 5px; }
        .b-f { padding: 15px; background: rgba(0,0,0,0.2); display: flex; gap: 10px; }
        .b-f input { padding: 12px; font-size: 12px; border-radius: 12px; text-align: left; background: #111; border: 1px solid #222; }

        #bot-trigger { 
            position: fixed; bottom: 30px; right: 30px; width: 65px; height: 65px; 
            background: #fff; color: #000; border-radius: 22px; border: none; cursor: pointer; 
            z-index: 1001; box-shadow: 0 15px 30px rgba(0,0,0,0.4); font-size: 24px;
            transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        #bot-trigger:active { transform: scale(0.9) rotate(-10deg); }

        @keyframes float { 0% { transform: translate(0,0); } 100% { transform: translate(40px, 40px); } }
        @keyframes slide { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="aura"></div>

    <div class="main-card">
        <h1>ZODIAC</h1>
        <div class="service-tag">7/24 Xidmətinizdəyik</div>

        <form method="POST" class="input-group">
            <input type="text" name="u" placeholder="TikTok linkini yapışdırın" required autocomplete="off">
            <button type="submit" class="btn">İndi Yüklə</button>
        </form>

        {% if dl %}
        <div class="result">
            <a href="{{ dl }}" target="_blank">📥 VİDEONU QALEREYAYA YAZ</a>
        </div>
        {% endif %}
    </div>

    <div id="bot-ui">
        <div class="b-h"><span>ZODIAC DƏSTƏK AI</span> <span onclick="tglC()" style="cursor:pointer; opacity: 0.5;">✕</span></div>
        <div class="b-b" id="cb"><div class="msg bot">Salam! Zodiac AI hər zaman yanınızdadır. 7/24 xidmətinizdəyik, buyurun sualınızı verin!</div></div>
        <div class="b-f"><input type="text" id="ci" placeholder="Mesajınızı yazın..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="bot-trigger" onclick="tglC()">💬</button>

    <script>
        function tglC() { const w = document.getElementById('bot-ui'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Mən Zodiac sisteminin rəsmi botuyam. Hazırda sistem aktivdir və 7/24 video yükləmək üçün hazırdır.";
                if(v.includes("salam")) r = "Salam! Necə kömək edə bilərəm?";
                else if(v.includes("necesen")) r = "Təşəkkür edirəm! Sizin üçün 7/24 buradayam, əla işləyirəm.";
                else if(v.includes("kim")) r = "Mən Zodiac AI dəstək sistemiyəm. Sizin suallarınızı cavablandırmaq üçün buradayam.";
                b.innerHTML += `<div class="msg bot">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 600);
        }

        // Haptic feedback simulation
        document.querySelectorAll('button, input').forEach(el => {
            el.addEventListener('touchstart', () => { if (window.navigator.vibrate) window.navigator.vibrate(12); });
        });
    </script>
</body>
</html>
