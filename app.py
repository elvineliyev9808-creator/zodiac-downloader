from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Sönməmə sistemi
def stay_awake():
    while True:
        try: requests.get("http://127.0.0.1:10000")
        except: pass
        time.sleep(300)

threading.Thread(target=stay_awake, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC PRO</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --blue: #2563eb; --bg: #f8fafc; --card: #ffffff; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { background: var(--bg); font-family: 'Outfit', sans-serif; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        
        .main-card { background: var(--card); width: 92%; max-width: 380px; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.08); padding: 24px; text-align: center; border: 1px solid #f1f5f9; }
        h1 { font-size: 22px; font-weight: 800; color: var(--blue); margin: 0 0 20px; letter-spacing: -0.5px; }

        /* Yığcam Input Group */
        .input-group { position: relative; display: flex; gap: 8px; background: #f1f5f9; padding: 6px; border-radius: 16px; margin-bottom: 20px; }
        input { flex: 1; background: transparent; border: none; padding: 10px 15px; outline: none; font-size: 14px; font-weight: 500; }
        .dl-btn { background: var(--blue); color: white; border: none; padding: 10px 18px; border-radius: 12px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .dl-btn:active { transform: scale(0.95); }

        /* Yeni Nəsil Musiqi Player */
        .player-mini { background: #1e293b; border-radius: 18px; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; color: white; }
        .track-info { text-align: left; overflow: hidden; }
        #t-name { font-size: 11px; font-weight: 600; white-space: nowrap; text-overflow: ellipsis; display: block; margin-bottom: 2px; }
        .controls { display: flex; gap: 10px; align-items: center; }
        .p-btn, .n-btn { background: rgba(255,255,255,0.1); border: none; color: white; cursor: pointer; border-radius: 50%; width: 32px; height: 32px; font-size: 12px; display: flex; align-items: center; justify-content: center; }
        .p-btn { background: var(--blue); }

        /* Smart AI Chat */
        #chat-ui { display: none; position: fixed; bottom: 90px; right: 20px; width: 300px; height: 400px; background: white; border-radius: 20px; box-shadow: 0 15px 50px rgba(0,0,0,0.15); flex-direction: column; overflow: hidden; border: 1px solid #e2e8f0; z-index: 1000; }
        .c-head { background: var(--blue); color: white; padding: 15px; font-weight: 600; font-size: 14px; display: flex; justify-content: space-between; }
        .c-body { flex: 1; padding: 15px; overflow-y: auto; font-size: 13px; display: flex; flex-direction: column; gap: 10px; background: #f8fafc; }
        .m { padding: 8px 14px; border-radius: 14px; max-width: 85%; line-height: 1.4; }
        .bot { background: white; color: #334155; align-self: flex-start; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
        .user { background: var(--blue); color: white; align-self: flex-end; }
        .c-foot { padding: 10px; border-top: 1px solid #e2e8f0; display: flex; gap: 5px; }
        .c-foot input { flex: 1; padding: 8px 12px; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 13px; }

        #bot-trigger { position: fixed; bottom: 25px; right: 25px; width: 55px; height: 55px; background: var(--blue); border-radius: 50%; color: white; border: none; font-size: 24px; cursor: pointer; box-shadow: 0 8px 25px rgba(37,99,235,0.3); }
    </style>
</head>
<body>

    <div class="main-card">
        <h1>ZODIAC.</h1>
        
        <form method="POST" class="input-group">
            <input type="text" name="u" placeholder="Linki bura qoy..." required>
            <button type="submit" class="dl-btn">ENDİR</button>
        </form>

        {% if dl %}
        <div style="animation: slideUp 0.3s forwards; margin-bottom: 20px;">
            <a href="{{ dl }}" style="background: #10b981; color: white; text-decoration: none; padding: 12px; border-radius: 14px; display: block; font-weight: 600; font-size: 14px;" target="_blank">📥 VİDEONU SAXLA</a>
        </div>
        {% endif %}

        <div class="player-mini">
            <div class="track-info">
                <span id="t-name">Yüklənir...</span>
                <div style="font-size: 9px; opacity: 0.6;">Zodiac Playlist</div>
            </div>
            <div class="controls">
                <button class="p-btn" onclick="toggleP()" id="p-ctrl">▶</button>
                <button class="n-btn" onclick="nextS()">⏭</button>
            </div>
        </div>
    </div>

    <div id="chat-ui">
        <div class="c-head"><span>Zodiac Dəstək</span> <span onclick="toggleC()" style="cursor:pointer">✕</span></div>
        <div class="c-body" id="chat-box">
            <div class="m bot">Salam! Mən Zodiac süni intellekt botuyam. Sizə necə kömək edə bilərəm?</div>
        </div>
        <div class="c-foot">
            <input type="text" id="chat-in" placeholder="Mesajınızı yazın..." onkeypress="if(event.key=='Enter') sendM()">
        </div>
    </div>
    <button id="bot-trigger" onclick="toggleC()">💬</button>

    <audio id="audio" onended="nextS()"></audio>

    <script>
        const songs = [
            {n: "Lotular - Mahir Ay", s: "Lotular(MP3_160K).mp3"},
            {n: "Ara Usaqlari - Mahir Ay", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS - Пыяла", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];
        let idx = 0;
        const player = document.getElementById('audio');

        function load(i) {
            player.src = "/music/" + encodeURIComponent(songs[i].s);
            document.getElementById('t-name').innerText = songs[i].n;
        }
        load(idx);

        function toggleP() {
            if(player.paused) {
                player.play().then(() => document.getElementById('p-ctrl').innerText = "||")
                .catch(() => alert("Ekrana bir dəfə toxunun!"));
            } else {
                player.pause();
                document.getElementById('p-ctrl').innerText = "▶";
            }
        }

        function nextS() {
            idx = (idx + 1) % songs.length;
            load(idx);
            player.play();
            document.getElementById('p-ctrl').innerText = "||";
        }

        function toggleC() {
            const ui = document.getElementById('chat-ui');
            ui.style.display = (ui.style.display === 'flex') ? 'none' : 'flex';
        }

        function sendM() {
            const inp = document.getElementById('chat-in');
            const box = document.getElementById('chat-box');
            if(!inp.value) return;

            box.innerHTML += `<div class="m user">${inp.value}</div>`;
            const val = inp.value.toLowerCase();
            inp.value = "";
            box.scrollTop = box.scrollHeight;

            setTimeout(() => {
                let r = "Üzr istəyirəm, bunu tam başa düşmədim. TikTok və ya IG linkini yuxarıdakı xanaya qoyaraq video endirə bilərsiniz.";
                
                if(val.includes("salam")) r = "Salam, xoş gəldiniz! Sizə necə kömək edim?";
                else if(val.includes("necesen") || val.includes("necəsən")) r = "Çox sağ olun, mən Zodiac sisteminin botuyam, hər şey əladır! Siz necəsiniz?";
                else if(val.includes("sağ ol") || val.includes("sagol")) r = "Buyurun, xoşdur! Başqa sualınız var?";
                else if(val.includes("video") || val.includes("yukle") || val.includes("yüklə")) r = "Videonu yükləmək üçün linki yuxarıdakı xanaya yapışdırıb 'ENDİR' düyməsinə basın.";
                else if(val.includes("musiqi") || val.includes("mahnı")) r = "Musiqi pleyeri aşağıdadır. 'İrəli' düyməsi ilə mahnını dəyişə bilərsiniz.";
                else if(val.includes("kim") && val.includes("yaratdı")) r = "Bu sistem Zodiac tərəfindən Azərbaycan istifadəçiləri üçün yaradılıb.";
                else if(val.includes("islemir") || val.includes("işləmir")) r = "Lütfən linkin düzgün və profilin açıq olduğundan əmin olun.";

                box.innerHTML += `<div class="m bot">${r}</div>`;
                box.scrollTop = box.scrollHeight;
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
