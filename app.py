from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Render sönməməsi üçün pinger
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
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Plus+Jakarta+Sans:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { background: #000; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
        .video-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.15; filter: blur(5px); pointer-events: none; }
        .video-bg iframe { width: 100vw; height: 100vh; border: none; }
        
        .container { background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(20px); border: 1px solid rgba(255, 215, 0, 0.3); width: 92%; max-width: 380px; padding: 40px 25px; border-radius: 40px; text-align: center; box-shadow: 0 40px 100px #000; position: relative; z-index: 10; }
        h1 { font-family: 'Orbitron', sans-serif; font-size: 32px; background: linear-gradient(90deg, #fff, #ffd700, #fff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: 5px; }
        .sub { font-size: 9px; color: #555; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 35px; }

        .search { display: flex; background: #000; border: 1px solid #222; border-radius: 20px; padding: 5px; margin-bottom: 25px; }
        input { flex: 1; background: transparent; border: none; padding: 15px; color: #fff; outline: none; font-size: 14px; }
        .btn { background: #ffd700; color: #000; border: none; padding: 0 25px; border-radius: 16px; font-weight: 900; cursor: pointer; }

        .dl { margin-bottom: 25px; padding: 15px; background: rgba(255,215,0,0.1); border-radius: 20px; }
        .dl a { color: #ffd700; text-decoration: none; font-weight: 800; font-size: 14px; }

        /* Professional Player UI */
        .player { background: #111; border: 1px solid #222; padding: 15px; border-radius: 25px; display: flex; align-items: center; gap: 15px; }
        .p-btn { width: 45px; height: 45px; background: #ffd700; border: none; border-radius: 50%; font-size: 18px; cursor: pointer; color: #000; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 15px rgba(255,215,0,0.3); }
        .n-btn { background: none; border: 1px solid #333; color: #fff; width: 35px; height: 35px; border-radius: 50%; cursor: pointer; font-size: 12px; }
        .m-info { text-align: left; flex: 1; }
        .m-name { font-size: 12px; font-weight: 700; color: #ffd700; display: block; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max-width: 140px; }
        .m-art { font-size: 9px; color: #666; }

        /* Bot */
        #c-win { display: none; position: fixed; bottom: 100px; right: 25px; width: 300px; height: 400px; background: #0a0a0a; border: 1px solid #ffd700; border-radius: 25px; flex-direction: column; overflow: hidden; z-index: 1000; }
        .c-h { background: #ffd700; color: #000; padding: 15px; font-weight: 800; font-size: 13px; }
        .c-b { flex: 1; padding: 15px; overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 10px; border-radius: 15px; max-width: 85%; }
        .bot { background: #1a1a1a; align-self: flex-start; }
        .user { background: #ffd700; color: #000; align-self: flex-end; font-weight: 700; }
        .c-f { padding: 10px; border-top: 1px solid #222; }
        .c-f input { margin: 0; padding: 10px; background: #000; border-radius: 12px; }

        #c-trig { position: fixed; bottom: 30px; right: 30px; width: 60px; height: 60px; background: #ffd700; border-radius: 20px; border: none; font-size: 26px; cursor: pointer; z-index: 1001; }
    </style>
</head>
<body>
    <div class="video-bg">
        <iframe src="https://www.youtube.com/embed/videoseries?list=PLPazg0nI_S06R0lP5oG15w0607K1h4-0z&autoplay=1&mute=1&loop=1" allow="autoplay"></iframe>
    </div>

    <div class="container">
        <h1>ZODIAC</h1>
        <div class="sub">Premium System v3.0</div>

        <form method="POST" class="search">
            <input type="text" name="u" placeholder="Link bura yapışdır..." required>
            <button type="submit" class="btn">GO</button>
        </form>

        {% if dl %}
        <div class="dl"><a href="{{ dl }}" target="_blank">📥 VİDEONU YÜKLƏ (.MP4)</a></div>
        {% endif %}

        <div class="player">
            <button class="p-btn" onclick="tglM()" id="ctrl">▶</button>
            <div class="m-info">
                <span class="m-name" id="m-name">Yüklənir...</span>
                <span class="m-art">Playlist Mode</span>
            </div>
            <button class="n-btn" onclick="nxt()">⏭</button>
        </div>
    </div>

    <div id="c-win">
        <div class="c-h">ZODIAC DƏSTƏK</div>
        <div class="c-b" id="cb"><div class="msg bot">Salam brat! Mahnıları sənin GitHub-dan bir-bir çəkirəm. Keçid üçün ⏭ düyməsini istifadə elə.</div></div>
        <div class="c-f"><input type="text" id="ci" placeholder="Yaz..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="c-trig" onclick="tglC()">💬</button>

    <audio id="audio" onended="nxt()"></audio>

    <script>
        const a = document.getElementById('audio');
        // Sənin GitHub-dakı fayl adların (Boşluq və simvollar dəqiq!)
        const playlist = [
            "Lotular(MP3_160K).mp3",
            "AIS - Пыяла x Sari.mp3",
            "Ara Usaidari(MP3_320K).mp3",
            "Elsevər Rəhimov - .mp3",
            "Seide Sultan - Nel.mp3"
        ];
        let cur = 0;

        function load(i) {
            // URL kodlaşdırması əlavə edildi ki, xüsusi simvollar (ə, ö, boşluq) işləsin
            a.src = "/music/" + encodeURIComponent(playlist[i]);
            document.getElementById('m-name').innerText = playlist[i].split('(')[0].replace('.mp3', '');
        }

        load(cur);

        function tglM() {
            if(a.paused) { 
                a.play().then(()=>document.getElementById('ctrl').innerText="||")
                .catch(()=>alert("Zəhmət olmasa ekranda bir yerə toxun, sonra PLAY-ə bas. Brauzer icazə vermir.")); 
            }
            else { a.pause(); document.getElementById('ctrl').innerText="▶"; }
        }

        function nxt() { cur = (cur + 1) % playlist.length; load(cur); a.play(); document.getElementById('ctrl').innerText="||"; }

        function tglC() { const w = document.getElementById('c-win'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg user">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Mahnını dəyişmək üçün ⏭ düyməsini istifadə elə.";
                if(v.includes("salam")) r = "Salam brat! Xoş gəldin.";
                b.innerHTML += `<div class="msg bot">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 500);
        }
    </script>
</body>
</html>
"""

@app.route('/music/<path:filename>')
def serve_music(filename):
    # Faylları birbaşa repozitoriyadan çəkir
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
