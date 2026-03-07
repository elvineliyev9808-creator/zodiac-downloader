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
    <title>ZODIAC | ULTIMATE</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --accent: #6366f1; --bg: #020617; --card: rgba(30, 41, 59, 0.7); }
        * { box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: white; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        
        /* Dynamic Mesh Background */
        .mesh { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #020617 100%); opacity: 0.8; }
        .glow { position: absolute; width: 300px; height: 300px; background: var(--accent); filter: blur(120px); border-radius: 50%; opacity: 0.2; animation: float 10s infinite alternate; }

        .container { background: var(--card); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); width: 92%; max-width: 400px; padding: 32px; border-radius: 32px; text-align: center; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); z-index: 10; }
        h1 { font-size: 28px; font-weight: 800; margin: 0 0 8px; letter-spacing: -1px; background: linear-gradient(to right, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .tagline { font-size: 12px; color: #94a3b8; margin-bottom: 32px; text-transform: uppercase; letter-spacing: 2px; }

        /* Input Styling */
        .input-wrap { background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 6px; display: flex; margin-bottom: 24px; }
        input { flex: 1; background: transparent; border: none; padding: 12px 16px; color: white; outline: none; font-size: 14px; }
        .go-btn { background: var(--accent); color: white; border: none; padding: 12px 24px; border-radius: 16px; font-weight: 700; cursor: pointer; transition: 0.3s; }
        .go-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3); }

        /* Result Button */
        .dl-link { display: block; background: #fff; color: #000; text-decoration: none; padding: 14px; border-radius: 18px; font-weight: 800; font-size: 14px; margin-bottom: 24px; animation: slideUp 0.4s ease; }

        /* Modern Player */
        .player-v3 { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 24px; padding: 16px; display: flex; align-items: center; gap: 16px; }
        .p-btn { width: 48px; height: 48px; border-radius: 16px; background: rgba(255,255,255,0.1); border: none; color: white; cursor: pointer; font-size: 20px; display: flex; align-items: center; justify-content: center; }
        .track-meta { text-align: left; }
        .t-title { font-size: 13px; font-weight: 700; color: #f8fafc; }
        .t-status { font-size: 10px; color: #6366f1; font-weight: 600; margin-top: 2px; }

        /* Smart AI Chat */
        #c-win { display: none; position: fixed; bottom: 100px; right: 20px; width: 320px; height: 450px; background: #0f172a; border-radius: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.6); flex-direction: column; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); z-index: 1000; }
        .c-header { background: var(--accent); padding: 16px; font-weight: 700; font-size: 14px; display: flex; justify-content: space-between; }
        .c-body { flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; font-size: 13px; scroll-behavior: smooth; }
        .m { padding: 12px 16px; border-radius: 16px; max-width: 85%; line-height: 1.5; }
        .bot { background: rgba(255,255,255,0.05); color: #cbd5e1; align-self: flex-start; border-bottom-left-radius: 4px; }
        .user { background: var(--accent); color: white; align-self: flex-end; border-bottom-right-radius: 4px; }
        .c-input { padding: 12px; background: #1e293b; border-top: 1px solid rgba(255,255,255,0.05); display: flex; }
        .c-input input { background: #0f172a; border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 10px; flex: 1; color: white; font-size: 12px; }

        #c-toggle { position: fixed; bottom: 30px; right: 30px; width: 64px; height: 64px; background: var(--accent); border-radius: 20px; color: white; border: none; font-size: 28px; cursor: pointer; box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4); z-index: 1001; transition: 0.3s; }
        #c-toggle:hover { transform: scale(1.1) rotate(10deg); }

        @keyframes float { from { transform: translate(0, 0); } to { transform: translate(50px, 50px); } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="mesh"></div>
    <div class="glow" style="top: 10%; left: 10%;"></div>
    <div class="glow" style="bottom: 10%; right: 10%; background: #c084fc;"></div>

    <div class="container">
        <h1>ZODIAC.</h1>
        <div class="tagline">Global Video Downloader</div>

        <form method="POST" class="input-wrap">
            <input type="text" name="u" placeholder="Video linkini bura daxil edin..." required>
            <button type="submit" class="go-btn">GO</button>
        </form>

        {% if dl %}
        <a href="{{ dl }}" class="dl-link" target="_blank">📥 VİDEONU ENDİR</a>
        {% endif %}

        <div class="player-v3">
            <button class="p-btn" onclick="toggleM()" id="ctrl">▶</button>
            <div class="track-meta">
                <div class="t-title">Trend Melodic Rap</div>
                <div class="t-status" id="sts">System Audio Online</div>
            </div>
        </div>
    </div>

    <div id="c-win">
        <div class="c-header"><span>Zodiac AI Support</span> <span onclick="toggleC()" style="cursor:pointer">✕</span></div>
        <div class="c-body" id="cb">
            <div class="m bot">Salam! Mən Zodiac süni intellektiyəm. Azərbaycanca bütün suallarınızı cavablandıra bilərəm. Necə kömək edim?</div>
        </div>
        <div class="c-input">
            <input type="text" id="ci" placeholder="Mesajınızı bura yazın..." onkeypress="if(event.key=='Enter') send()">
        </div>
    </div>
    <button id="c-toggle" onclick="toggleC()">💬</button>

    <audio id="audio" loop></audio>

    <script>
        const a = document.getElementById('audio');
        // AI tərəfindən yaradılan yeni trend musiqi linki buraya gələcək
        a.src = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"; 

        function toggleM() {
            if(a.paused) {
                a.play().then(() => {
                    document.getElementById('ctrl').innerText = "||";
                    document.getElementById('sts').innerText = "İndi Oxuyur...";
                }).catch(() => alert("Lütfən ekrana bir dəfə toxunun!"));
            } else {
                a.pause();
                document.getElementById('ctrl').innerText = "▶";
                document.getElementById('sts').innerText = "Pauza Edildi";
            }
        }

        function toggleC() {
            const w = document.getElementById('c-win');
            w.style.display = (w.style.display === 'flex') ? 'none' : 'flex';
        }

        function send() {
            const i = document.getElementById('ci');
            const b = document.getElementById('cb');
            if(!i.value) return;

            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase();
            i.value = "";
            b.scrollTop = b.scrollHeight;

            setTimeout(() => {
                let r = "Üzr istəyirəm, hələ ki, yalnız video yükləmə və əsas suallara cavab verə bilirəm.";
                
                // Geniş Azərbaycan söz bazası
                if(v.includes("salam")) r = "Salam! Xoş gördük. Sizə video yükləməkdə necə kömək edə bilərəm?";
                else if(v.includes("necesen") || v.includes("necəsən")) r = "Təşəkkür edirəm! Mən sistem botuyam, hər şey qaydasındadır. Siz necəsiniz?";
                else if(v.includes("islemir") || v.includes("problem")) r = "Linki tam kopyaladığınızdan və profilin gizli olmadığından əmin olun.";
                else if(v.includes("yukle") || v.includes("yüklə")) r = "Linki yuxarıdakı xanaya yapışdırıb 'GO' düyməsinə basın.";
                else if(v.includes("sagol") || v.includes("təşəkkür")) r = "Buyurun! Hər zaman xidmətinizdəyik.";
                else if(v.includes("kim") && v.includes("yaratdı")) r = "Zodiac Downloader sizin üçün ən müasir texnologiyalarla hazırlanıb.";
                else if(v.includes("haralısan")) r = "Mən bulud texnologiyalarındayam, amma ana dilim Azərbaycancadır!";

                b.innerHTML += `<div class="msg bot">${r}</div>`;
                b.scrollTop = b.scrollHeight;
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
