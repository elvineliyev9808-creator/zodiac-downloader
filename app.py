from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Serverin sönməməsi üçün daxili pinger
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
    <title>ZODIAC PREMIUM</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root { --gold: #ffd700; --dark: #050505; --glass: rgba(255, 255, 255, 0.05); }
        body { background: var(--dark); color: white; font-family: 'Inter', sans-serif; margin: 0; overflow: hidden; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        
        /* Canlı Arxa Fon (Animated Particles) */
        #bg-canvas { position: fixed; top: 0; left: 0; z-index: -1; }

        .card { background: var(--glass); backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.1); width: 90%; max-width: 380px; padding: 30px; border-radius: 30px; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        h1 { font-family: 'Orbitron', sans-serif; font-size: 26px; color: var(--gold); margin-bottom: 25px; text-shadow: 0 0 15px rgba(255, 215, 0, 0.3); }

        /* Downloader Section */
        .search-form { display: flex; gap: 10px; margin-bottom: 20px; }
        input { flex: 1; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); padding: 12px 15px; border-radius: 15px; color: white; outline: none; font-size: 14px; }
        input:focus { border-color: var(--gold); }
        .btn { background: var(--gold); color: black; border: none; padding: 0 20px; border-radius: 15px; font-weight: 700; cursor: pointer; }

        /* Compact Player */
        .player-box { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 20px; display: flex; align-items: center; justify-content: space-between; border: 1px solid rgba(255,215,0,0.2); }
        #t-title { font-size: 11px; font-weight: 600; color: var(--gold); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }
        .ctrls { display: flex; gap: 8px; }
        .p-btn, .n-btn { background: var(--gold); border: none; width: 35px; height: 35px; border-radius: 50%; cursor: pointer; font-size: 14px; font-weight: bold; }
        .n-btn { background: white; color: black; }

        /* AI Support Bot */
        #c-win { display: none; position: fixed; bottom: 90px; right: 20px; width: 300px; height: 420px; background: #111; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.5); flex-direction: column; overflow: hidden; border: 1px solid var(--gold); z-index: 1000; }
        .c-head { background: var(--gold); color: black; padding: 15px; font-weight: 800; font-size: 14px; text-align: left; }
        .c-body { flex: 1; padding: 15px; overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 10px; background: #0a0a0a; }
        .m { padding: 10px; border-radius: 12px; max-width: 85%; line-height: 1.5; }
        .bot { background: #222; color: #ddd; align-self: flex-start; border-left: 3px solid var(--gold); }
        .user { background: var(--gold); color: black; align-self: flex-end; font-weight: 600; }
        .c-foot { padding: 10px; background: #111; border-top: 1px solid #222; display: flex; }
        .c-foot input { flex: 1; background: #000; border: 1px solid #333; padding: 10px; border-radius: 10px; font-size: 12px; color: white; }

        #bot-trigger { position: fixed; bottom: 25px; right: 25px; width: 60px; height: 60px; background: var(--gold); border-radius: 50%; border: none; color: black; font-size: 28px; cursor: pointer; box-shadow: 0 0 20px rgba(255,215,0,0.4); z-index: 1001; }
    </style>
</head>
<body>
    <canvas id="bg-canvas"></canvas>

    <div class="card">
        <h1>ZODIAC ELITE</h1>
        
        <form method="POST" class="search-form">
            <input type="text" name="u" placeholder="Video linkini bura qoy..." required>
            <button type="submit" class="btn">ENDİR</button>
        </form>

        {% if dl %}
        <div style="margin-bottom: 20px;">
            <a href="{{ dl }}" style="display: block; background: white; color: black; text-decoration: none; padding: 12px; border-radius: 15px; font-weight: 800; font-size: 14px;" target="_blank">📥 VİDEONU YÜKLƏ</a>
        </div>
        {% endif %}

        <div class="player-box">
            <div id="t-title">Yüklənir...</div>
            <div class="ctrls">
                <button class="p-btn" onclick="togglePlay()" id="play-icon">▶</button>
                <button class="n-btn" onclick="nextSong()">⏭</button>
            </div>
        </div>
    </div>

    <div id="c-win">
        <div class="c-head">ZODIAC AI DƏSTƏK</div>
        <div class="c-body" id="chat-box">
            <div class="m bot">Salam! Mən Zodiac AI. Azərbaycan dilində bütün suallarınızı cavablandırmağa hazıram. Buyurun!</div>
        </div>
        <div class="c-foot">
            <input type="text" id="chat-in" placeholder="Sualınızı yazın..." onkeypress="if(event.key=='Enter') chat()">
        </div>
    </div>
    <button id="bot-trigger" onclick="toggleChat()">💬</button>

    <audio id="audio" onended="nextSong()"></audio>

    <script>
        // Musiqi Faylları (Tam dəqiq adlarla)
        const playlist = [
            {n: "MAHİR AY - LOTULAR", s: "Lotular(MP3_160K).mp3"},
            {n: "MAHİR AY - ARA USAQLARI", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - ПЫЯЛА", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];

        let curIdx = 0;
        const player = document.getElementById('audio');

        function load(i) {
            player.src = "/music/" + encodeURIComponent(playlist[i].s);
            document.getElementById('t-title').innerText = playlist[i].n;
        }
        load(curIdx);

        function togglePlay() {
            if(player.paused) {
                player.play().then(() => document.getElementById('play-icon').innerText = "||")
                .catch(() => alert("Ekrana bir dəfə toxunun!"));
            } else { player.pause(); document.getElementById('play-icon').innerText = "▶"; }
        }

        function nextSong() {
            curIdx = (curIdx + 1) % playlist.length;
            load(curIdx); player.play();
            document.getElementById('play-icon').innerText = "||";
        }

        function toggleChat() {
            const win = document.getElementById('c-win');
            win.style.display = (win.style.display === 'flex') ? 'none' : 'flex';
        }

        function chat() {
            const inp = document.getElementById('chat-in');
            const box = document.getElementById('chat-box');
            if(!inp.value) return;

            box.innerHTML += `<div class="m user">${inp.value}</div>`;
            const q = inp.value.toLowerCase();
            inp.value = "";
            box.scrollTop = box.scrollHeight;

            setTimeout(() => {
                let r = "Bunu hələ öyrənməmişəm, amma linki yuxarı qoyub video yükləyə bilərsiniz!";
                
                // Azərbaycan dilində geniş cavab bazası
                if(q.includes("salam")) r = "Salam! Xoş gəldiniz. Sizə necə kömək edə bilərəm?";
                else if(q.includes("necesen") || q.includes("necəsən")) r = "Mən Zodiac AI sistemiyəm, hər zaman oyağam! Siz necəsiniz?";
                else if(q.includes("sag ol") || q.includes("sağ ol") || q.includes("tesekkur")) r = "Buyurun, hər zaman xidmətinizdəyik!";
                else if(q.includes("islemir") || q.includes("problem") || q.includes("xeta")) r = "Linkin tam kopyalandığından və videonun silinmədiyindən əmin olun.";
                else if(q.includes("kimsen") || q.includes("adın nə")) r = "Mən Zodiac-ın rəsmi dəstək botuyam.";
                else if(q.includes("mahnı") || q.includes("musiqi")) r = "Aşağıdakı pleyerdə ən son hitlər var, dinləyə bilərsiniz.";
                else if(q.includes("ais") || q.includes("səslənmir")) r = "Ais mahnısının linki artıq düzəldildi, '⏭' düyməsi ilə keçib yoxlayın.";
                else if(q.includes("haralısan")) r = "Mən rəqəmsal dünyadayam, amma ürəyim Azərbaycanladır!";
                else if(q.includes("kim yaratdı")) r = "Bu sistemi sizin üçün Zodiac Developer qrupu hazırlayıb.";

                box.innerHTML += `<div class="m bot">${r}</div>`;
                box.scrollTop = box.scrollHeight;
            }, 600);
        }

        // Animated Background
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        let particles = [];
        for(let i=0; i<40; i++) particles.push({x: Math.random()*canvas.width, y: Math.random()*canvas.height, r: Math.random()*2, d: Math.random()*0.5});
        function draw() {
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "rgba(255, 215, 0, 0.2)";
            particles.forEach(p => {
                ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
                p.y -= p.d; if(p.y < 0) p.y = canvas.height;
            });
            requestAnimationFrame(draw);
        }
        draw();
    </script>
</body>
</html>
"""

@app.route('/music/<path:f>')
def g_m(f): return send_from_directory(os.getcwd(), f)

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
