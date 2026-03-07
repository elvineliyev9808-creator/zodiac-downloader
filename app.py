from flask import Flask, render_template_string, request, send_from_directory
import requests, os, threading, time

app = Flask(__name__)

# Serverin sönməməsi üçün
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
    <title>ZODIAC</title>
    <style>
        * { box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background: #fdfdfd; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        
        .card { background: #fff; width: 90%; max-width: 350px; padding: 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: center; border: 1px solid #eee; }
        h1 { font-size: 24px; color: #007aff; margin: 0 0 5px; font-weight: 900; }
        p { font-size: 11px; color: #888; margin-bottom: 20px; }

        input { width: 100%; padding: 12px; border: 1px solid #eee; border-radius: 12px; outline: none; background: #f9f9f9; font-size: 14px; margin-bottom: 10px; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 12px; background: #000; color: #fff; font-weight: 700; cursor: pointer; }
        
        .dl-res { margin-top: 15px; padding: 15px; background: #e8f5e9; border-radius: 12px; }
        .dl-link { color: #2e7d32; text-decoration: none; font-weight: 800; font-size: 13px; }

        /* Yığcam Azeri Player */
        .player { margin-top: 20px; display: flex; align-items: center; justify-content: center; gap: 10px; background: #f0f0f0; padding: 8px; border-radius: 50px; }
        .p-btn { border: none; background: #007aff; color: #fff; width: 30px; height: 30px; border-radius: 50%; font-size: 10px; cursor: pointer; }
        .p-txt { font-size: 10px; font-weight: 600; color: #555; }

        /* Bot */
        #chat { display: none; position: fixed; bottom: 80px; right: 20px; width: 280px; height: 350px; background: #fff; border-radius: 15px; box-shadow: 0 5px 25px rgba(0,0,0,0.1); flex-direction: column; overflow: hidden; border: 1px solid #eee; }
        .c-h { background: #000; color: #fff; padding: 10px; font-size: 12px; font-weight: 700; }
        .c-b { flex: 1; padding: 10px; overflow-y: auto; font-size: 12px; display: flex; flex-direction: column; gap: 5px; }
        .m { padding: 8px; border-radius: 10px; max-width: 80%; }
        .b { background: #f0f0f0; align-self: flex-start; }
        .u { background: #007aff; color: #fff; align-self: flex-end; }
        .c-f { padding: 5px; border-top: 1px solid #eee; }
        .c-f input { margin: 0; padding: 8px; font-size: 11px; }

        #btn-c { position: fixed; bottom: 20px; right: 20px; width: 50px; height: 50px; background: #000; color: #fff; border-radius: 50%; border: none; cursor: pointer; font-size: 20px; }
    </style>
</head>
<body>

    <div class="card">
        <h1>ZODIAC</h1>
        <p>TikTok Video Downloader</p>
        
        <form method="POST">
            <input type="text" name="u" placeholder="Linki yapıştır..." required>
            <button type="submit" class="btn">ENDİR</button>
        </form>

        {% if dl %}
        <div class="dl-res">
            <a href="{{ dl }}" class="dl-link" target="_blank">📥 VİDEONU SAXLA</a>
        </div>
        {% endif %}

        <div class="player">
            <button class="p-btn" onclick="tglM()" id="ctrl">▶</button>
            <span class="p-txt">Azeri Trend Mix 🇦🇿</span>
        </div>
    </div>

    <div id="chat">
        <div class="c-h">DƏSTƏK</div>
        <div class="c-b" id="cb"><div class="m b">Salam, mən Zodiac! Sualın var?</div></div>
        <div class="c-f"><input type="text" id="ci" placeholder="Mesaj..." onkeypress="if(event.key=='Enter') snd()"></div>
    </div>
    <button id="btn-c" onclick="tglC()">💬</button>

    <audio id="audio" loop src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"></audio>

    <script>
        const a = document.getElementById('audio');
        function tglM() { if(a.paused) { a.play(); document.getElementById('ctrl').innerText="||"; } else { a.pause(); document.getElementById('ctrl').innerText="▶"; } }
        function tglC() { const w = document.getElementById('chat'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function snd() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="m u">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = ""; b.scrollTop = b.scrollHeight;
            setTimeout(() => {
                let r = "Linki yuxarı qoyub endirə bilərsən.";
                if(v.includes("salam")) r = "Salam! Necə kömək edim?";
                else if(v.includes("necesen")) r = "Şükür, yaxşıyam! Sən necəsən?";
                else if(v.includes("islemir")) r = "Linkin düzgünlüyünü yoxla.";
                b.innerHTML += `<div class="m b">${r}</div>`; b.scrollTop = b.scrollHeight;
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
