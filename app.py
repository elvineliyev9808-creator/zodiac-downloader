from flask import Flask, render_template_string, request
import requests, os, threading, time

app = Flask(__name__)

# Render-in "yuxuya" getməməsi üçün daxili pinger
def keep_alive():
    while True:
        try:
            requests.get("http://127.0.0.1:10000", timeout=5)
        except:
            pass
        time.sleep(300) # Hər 5 dəqiqədən bir özünü yoxlayır

threading.Thread(target=keep_alive, daemon=True).start()

# Mobil telefonlar üçün xüsusi optimizasiya edilmiş dizayn
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ZODIAC | Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { background: #000; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; padding: 20px; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow-x: hidden; }
        .bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #111 0%, #000 100%); z-index: -1; }
        
        /* Mobil ölçülərə uyğun panel */
        .container { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.1); width: 100%; max-width: 380px; padding: 40px 20px; border-radius: 35px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        
        h1 { font-family: 'Orbitron', sans-serif; font-size: 28px; letter-spacing: 5px; margin: 0; color: #fff; text-transform: uppercase; }
        .badge { display: inline-block; margin-top: 10px; padding: 5px 12px; background: rgba(0, 242, 255, 0.1); color: #00f2ff; font-size: 10px; font-weight: 800; border-radius: 50px; text-transform: uppercase; letter-spacing: 1px; }
        
        .form-group { margin-top: 40px; }
        input { width: 100%; background: #0a0a0a; border: 1px solid #222; padding: 18px; border-radius: 15px; color: #fff; font-size: 14px; text-align: center; outline: none; transition: 0.3s; }
        input:focus { border-color: #00f2ff; box-shadow: 0 0 20px rgba(0, 242, 255, 0.1); }
        
        .btn { width: 100%; background: #fff; color: #000; border: none; padding: 18px; border-radius: 15px; font-weight: 800; margin-top: 15px; cursor: pointer; transition: 0.2s; font-size: 13px; letter-spacing: 1px; }
        .btn:active { transform: scale(0.96); background: #00f2ff; }
        
        .result { margin-top: 25px; padding: 15px; background: rgba(0, 242, 255, 0.05); border-radius: 15px; border: 1px dashed #00f2ff; }
        .result a { color: #00f2ff; text-decoration: none; font-weight: 800; font-size: 12px; }

        /* Təkmilləşdirilmiş Dəstək Botu */
        #bot-box { display: none; position: fixed; bottom: 90px; right: 20px; width: 300px; height: 380px; background: #0a0a0a; border: 1px solid #222; border-radius: 20px; flex-direction: column; z-index: 100; box-shadow: 0 20px 40px #000; overflow: hidden; }
        .bot-h { background: #111; padding: 15px; font-size: 11px; font-weight: 800; color: #00f2ff; border-bottom: 1px solid #222; }
        .bot-m { flex: 1; padding: 15px; overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 10px; }
        .m { padding: 10px 14px; border-radius: 15px; max-width: 85%; line-height: 1.4; }
        .b { background: #1a1a1a; align-self: flex-start; border-bottom-left-radius: 2px; }
        .u { background: #00f2ff; color: #000; align-self: flex-end; border-bottom-right-radius: 2px; font-weight: 600; }
        .bot-i { padding: 10px; border-top: 1px solid #222; }
        .bot-i input { padding: 12px; margin: 0; font-size: 12px; text-align: left; }

        #bot-toggle { position: fixed; bottom: 25px; right: 25px; width: 55px; height: 55px; background: #fff; color: #000; border-radius: 18px; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer; z-index: 101; box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: 0.3s; }
        #bot-toggle:active { transform: scale(0.9); }
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="container">
        <h1>ZODIAC</h1>
        <div class="badge">7/24 Xidmətinizdəyik</div>
        
        <form method="POST" class="form-group">
            <input type="text" name="u" placeholder="TikTok video linki..." required autocomplete="off">
            <button type="submit" class="btn">VİDEONU ENDİR</button>
        </form>

        {% if dl %}
        <div class="result">
            <a href="{{ dl }}" target="_blank">📥 VİDEO HAZIRDIR (MP4)</a>
        </div>
        {% endif %}
    </div>

    <div id="bot-box">
        <div class="bot-h">ZODIAC DƏSTƏK AI</div>
        <div class="bot-m" id="chat">
            <div class="m b">Salam! Zodiac AI 7/24 aktivdir. Necə kömək edə bilərəm?</div>
        </div>
        <div class="bot-i"><input type="text" id="msg" placeholder="Mesajınızı yazın..." onkeypress="if(event.key=='Enter') send()"></div>
    </div>
    <div id="bot-toggle" onclick="toggleBot()">💬</div>

    <script>
        function toggleBot() { 
            const b = document.getElementById('bot-box');
            b.style.display = (b.style.display === 'flex') ? 'none' : 'flex';
        }
        function send() {
            const i = document.getElementById('msg');
            const c = document.getElementById('chat');
            if(!i.value) return;
            c.innerHTML += `<div class="m u">${i.value}</div>`;
            const val = i.value.toLowerCase();
            i.value = "";
            c.scrollTop = c.scrollHeight;
            setTimeout(() => {
                let r = "Linki yuxarıdakı sahəyə yapışdırıb 'Endir' düyməsinə basın. Sistem 7/24 aktivdir.";
                if(val.includes("salam")) r = "Salam! Sizə necə kömək edə bilərəm?";
                c.innerHTML += `<div class="msg b">${r}</div>`;
                c.scrollTop = c.scrollHeight;
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
            # TikWM API vasitəsilə endirmə linki
            r = requests.get(f"https://www.tikwm.com/api/?url={u}").json()
            dl = r['data']['play']
        except:
            pass
    return render_template_string(HTML_CONTENT, dl=dl)

if __name__ == "__main__":
    # Render üçün lazımi port təyini
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
