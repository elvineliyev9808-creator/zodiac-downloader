from flask import Flask, render_template_string, request
import requests, os, threading, time

app = Flask(__name__)

# Render-in sönməməsi üçün
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
    <title>ZODIAC | Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Space+Grotesk:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00f2ff; --bg: #050505; }
        * { box-sizing: border-box; transition: 0.3s; }
        
        body { background: var(--bg); color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }

        /* Arxa fon video effekti (Musiqisiz, səssiz) */
        .bg-video { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.1; filter: grayscale(1) blur(5px); pointer-events: none; object-fit: cover; }
        
        .glass-panel { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(25px); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            width: 90%; 
            max-width: 400px; 
            padding: 50px 30px; 
            border-radius: 40px; 
            text-align: center; 
            box-shadow: 0 30px 60px rgba(0,0,0,0.8);
            border-top: 2px solid var(--neon);
        }

        h1 { font-family: 'Syncopate', sans-serif; font-size: 26px; letter-spacing: 6px; margin: 0; color: #fff; text-shadow: 0 0 10px var(--neon); }
        .status { font-size: 9px; color: var(--neon); letter-spacing: 3px; text-transform: uppercase; margin: 15px 0 45px; opacity: 0.6; }

        .input-group { position: relative; margin-bottom: 25px; }
        input { 
            width: 100%; 
            background: rgba(0,0,0,0.5); 
            border: 1px solid #222; 
            padding: 18px; 
            border-radius: 12px; 
            color: #fff; 
            font-size: 14px; 
            outline: none; 
            text-align: center;
        }
        input:focus { border-color: var(--neon); box-shadow: 0 0 15px rgba(0, 242, 255, 0.1); }

        .dl-btn { 
            width: 100%; 
            background: #fff; 
            color: #000; 
            border: none; 
            padding: 16px; 
            border-radius: 12px; 
            font-weight: 800; 
            cursor: pointer; 
            font-size: 13px; 
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .dl-btn:hover { background: var(--neon); transform: scale(1.02); }

        .result { margin-top: 30px; padding: 20px; background: rgba(0, 242, 255, 0.05); border-radius: 15px; border: 1px dashed var(--neon); animation: fadeIn 0.5s; }
        .result a { color: var(--neon); text-decoration: none; font-weight: 700; font-size: 14px; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Bot Trigger */
        #bot-ui { display: none; position: fixed; bottom: 90px; right: 20px; width: 280px; height: 350px; background: #000; border: 1px solid #222; border-radius: 20px; flex-direction: column; overflow: hidden; z-index: 100; }
        .b-h { background: #111; padding: 15px; font-size: 11px; font-weight: 700; border-bottom: 1px solid #222; }
        .b-b { flex: 1; padding: 15px; overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 8px; }
        .m { padding: 10px; border-radius: 10px; max-width: 80%; }
        .bot { background: #111; align-self: flex-start; }
        .user { background: var(--neon); color: #000; align-self: flex-end; }
        .b-f { padding: 10px; border-top: 1px solid #222; }
        .b-f input { padding: 10px; font-size: 11px; }

        #bot-btn { position: fixed; bottom: 25px; right: 25px; width: 55px; height: 55px; background: #111; border: 1px solid #222; border-radius: 50%; color: var(--neon); cursor: pointer; font-size: 20px; }
    </style>
</head>
<body>
    <iframe class="bg-video" src="https://www.youtube.com/embed/videoseries?list=PLPazg0nI_S06R0lP5oG15w0607K1h4-0z&autoplay=1&mute=1&loop=1" allow="autoplay"></iframe>

    <div class="glass-panel">
        <h1>ZODIAC</h1>
        <div class="status">System Online // No Audio</div>

        <form method="POST">
            <div class="input-group">
                <input type="text" name="u" placeholder="TikTok linkini daxil edin" required>
            </div>
            <button type="submit" class="dl-btn">Yüklə</button>
        </form>

        {% if dl %}
            <div class="result">
                <a href="{{ dl }}" target="_blank">>> VİDEONU SAXLA (MP4)</a>
            </div>
        {% endif %}
    </div>

    <div id="bot-ui">
        <div class="b-h">ZODIAC AI DƏSTƏK</div>
        <div class="b-b" id="cb"><div class="m bot">Salam! Musiqi bölməsi ləğv edildi. Necə kömək edə bilərəm?</div></div>
        <div class="b-f"><input type="text" id="ci" placeholder="Yaz..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="bot-btn" onclick="tglC()">💬</button>

    <script>
        function tglC() { const w = document.getElementById('bot-ui'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="m user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Linki yuxarı yapışdırıb 'Yüklə' düyməsinə basaraq videonu götürə bilərsən.";
                if(v.includes("salam")) r = "Salam! Sistem tam hazırdır.";
                b.innerHTML += `<div class="m bot">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 500);
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
