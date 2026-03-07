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
    <title>ZODIAC | Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;800&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --gold: #ffd700; 
            --accent: #00f2ff;
            --bg: #000000;
            --glass: rgba(255, 255, 255, 0.03);
        }
        
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body { 
            background: var(--bg); 
            color: #fff; 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            margin: 0; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            overflow: hidden;
        }

        /* Canlı Fon */
        .bg-gradient {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 50% 50%, #111 0%, #000 100%);
            z-index: -2;
        }
        
        .aura {
            position: fixed;
            width: 500px; height: 500px;
            background: var(--accent);
            filter: blur(150px);
            opacity: 0.05;
            border-radius: 50%;
            animation: float 20s infinite alternate;
            z-index: -1;
        }

        /* Haptic Container */
        .main-card {
            background: var(--glass);
            backdrop-filter: blur(40px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            width: 90%;
            max-width: 420px;
            padding: 60px 30px;
            border-radius: 50px;
            text-align: center;
            box-shadow: 0 50px 100px rgba(0,0,0,0.5);
            transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .main-card:active { transform: scale(0.98); }

        h1 { 
            font-family: 'Orbitron', sans-serif; 
            font-size: 36px; 
            background: linear-gradient(180deg, #fff 0%, #666 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            letter-spacing: 10px;
        }

        .service-tag {
            display: inline-block;
            margin-top: 15px;
            padding: 6px 15px;
            background: rgba(0, 242, 255, 0.1);
            color: var(--accent);
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 2px;
            border-radius: 50px;
            text-transform: uppercase;
        }

        .input-wrapper {
            margin-top: 50px;
            position: relative;
        }

        input {
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 22px;
            border-radius: 20px;
            color: #fff;
            font-size: 15px;
            outline: none;
            transition: 0.3s;
            text-align: center;
        }

        input:focus {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--accent);
            box-shadow: 0 0 30px rgba(0, 242, 255, 0.1);
        }

        .btn-premium {
            width: 100%;
            margin-top: 15px;
            padding: 20px;
            background: #fff;
            color: #000;
            border: none;
            border-radius: 20px;
            font-weight: 800;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            cursor: pointer;
            transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .btn-premium:active {
            transform: scale(0.95);
            background: var(--accent);
        }

        .result-box {
            margin-top: 30px;
            padding: 25px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 25px;
            border: 1px solid rgba(0, 242, 255, 0.2);
            animation: slideUp 0.5s ease;
        }

        .result-box a {
            color: var(--accent);
            text-decoration: none;
            font-weight: 800;
            font-size: 13px;
            display: block;
        }

        .footer-text {
            position: fixed;
            bottom: 30px;
            font-size: 11px;
            color: #444;
            font-weight: 500;
            letter-spacing: 1px;
        }

        @keyframes float { 0% { transform: translate(0,0); } 100% { transform: translate(50px, 50px); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="aura"></div>

    <div class="main-card">
        <h1>ZODIAC</h1>
        <div class="service-tag">7/24 Xidmətinizdəyik</div>

        <form method="POST" class="input-wrapper">
            <input type="text" name="u" placeholder="Linki bura yapışdırın" required autocomplete="off">
            <button type="submit" class="btn-premium">Endirməni Başlat</button>
        </form>

        {% if dl %}
            <div class="result-box">
                <a href="{{ dl }}" target="_blank">📥 VİDEONU QALEREYAYA YÜKLƏ</a>
            </div>
        {% endif %}
    </div>

    <div class="footer-text">ZODIAC AI PLATFORM // 2026</div>

    <script>
        // Haptic touch effect simulation
        document.querySelectorAll('button, input, .main-card').forEach(el => {
            el.addEventListener('touchstart', () => {
                if (window.navigator.vibrate) window.navigator.vibrate(10);
            });
        });
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
