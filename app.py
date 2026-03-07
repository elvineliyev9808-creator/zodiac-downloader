from flask import Flask, render_template_string, request, send_from_directory
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
    <title>ZODIAC | Compact</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --main: #0062ff; --bg: #f3f4f6; }
        body { background: var(--bg); font-family: 'Inter', sans-serif; margin: 0; display: flex; justify-content: center; padding: 20px; }
        .card { background: white; width: 100%; max-width: 360px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); overflow: hidden; }
        .header { background: var(--main); color: white; padding: 20px; text-align: center; }
        .header h1 { margin: 0; font-size: 20px; letter-spacing: -0.5px; }
        .content { padding: 20px; }
        
        /* Compact Input */
        .search-form { display: flex; gap: 8px; margin-bottom: 15px; }
        input { flex: 1; padding: 12px; border: 1px solid #e5e7eb; border-radius: 10px; outline: none; font-size: 14px; }
        .btn { background: var(--main); color: white; border: none; padding: 10px 15px; border-radius: 10px; font-weight: 600; cursor: pointer; }

        /* Tiny Player */
        .player { background: #f9fafb; border: 1px solid #eee; border-radius: 12px; padding: 10px; display: flex; align-items: center; gap: 10px; }
        .p-btn { width: 32px; height: 32px; border-radius: 50%; border: none; background: var(--main); color: white; cursor: pointer; font-size: 12px; }
        #t-title { font-size: 11px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* Support Bot Window */
        #c-win { display: none; position: fixed; bottom: 85px; right: 20px; width: 280px; height: 350px; background: white; border-radius: 15px; box-shadow: 0 5px 30px rgba(0,0,0,0.15); flex-direction: column; overflow: hidden; border: 1px solid #eee; z-index: 999; }
        .c-head { background: #1f2937; color: white; padding: 12px; font-size: 13px; font-weight: 600; }
        .c-body { flex: 1; padding: 10px; overflow-y: auto; font-size: 12px; background: #fff; display: flex; flex-direction: column; gap: 8px; }
        .msg { padding: 8px 12px; border-radius: 10px; max-width: 85%; }
        .b { background: #f3f4f6; align-self: flex-start; }
        .u { background: var(--main); color: white; align-self: flex-end; }
        .c-foot { padding: 8px; border-top: 1px solid #eee; display: flex; }
        .c-foot input { padding: 6px; border-radius: 5px; font-size: 11px; }
        #c-btn { position: fixed; bottom: 20px; right: 20px; width: 55px; height: 55px; background: var(--main); border-radius: 50%; border: none; color: white; font-size: 22px; cursor: pointer; box-shadow: 0 4px 15px rgba(0,98,255,0.3); }
    </style>
</head>
<body>

    <div class="card">
        <div class="header"><h1>ZODIAC.</h1></div>
        <div class="content">
            <form method="POST" class="search-form">
                <input type="text" name="u" placeholder="Linki yapışdır..." required>
                <button type="submit" class="btn">GO</button>
            </form>

            {% if dl %}
            <div style="text-align: center; margin-bottom: 15px;">
                <a href="{{ dl }}" style="display: block; background: #10b981; color: white; text-decoration: none; padding: 10px; border-radius: 10px; font-weight: 600; font-size: 13px;" target="_blank">📥 VİDEONU YÜKLƏ</a>
            </div>
            {% endif %}

            <div class="player">
                <button class="p-btn" onclick="tgl()" id="pb">▶</button>
                <div id="t-title">Musiqi: Lotular</div>
            </div>
        </div>
    </div>

    <div id="c-win">
        <div class="c-head">Zodiac Assistant</div>
        <div class="c-body" id="cb"><div class="msg b">Salam! Mənə sual verə bilərsiniz.</div></div>
        <div class="c-foot"><input type="text" id="ci" placeholder="Yazın..." onkeypress="if(event.key=='Enter') send()"></div>
    </div>
    <button id="c-btn" onclick="tglC()">💬</button>

    <audio id="aud" onended="nxt()"></audio>

    <script>
        const s = [{n:"Lotular - Mahir Ay", s:"Lotular(MP3_160K).mp3"}, {n:"Ara Usaqlari", s:"Ara Usaqlari(MP3_160K).mp3"}, {n:"AIS - Пыяла", s:"AIS - Пыяла x Sarışan hallar(M.mp3"}];
        let c = 0; const a = document.getElementById('aud');
        function ld(i) { a.src = "/music/" + encodeURIComponent(s[i].s); document.getElementById('t-title').innerText = s[i].n; }
        ld(c);
        function tgl() { a.paused ? a.play().then(()=>document.getElementById('pb').innerText="||") : a.pause(); }
        function nxt() { c = (c+1)%s.length; ld(c); a.play(); }

        function tglC() { const w = document.getElementById('c-win'); w.style.display = (w.style.display==='flex')?'none':'flex'; }
        function send() {
            const i = document.getElementById('ci'); const b = document.getElementById('cb');
            if(!i.value) return;
            b.innerHTML += `<div class="msg u">${i.value}</div>`;
            const v = i.value.toLowerCase(); i.value = "";
            setTimeout(() => {
                let r = "Başa düşmədim. TikTok və ya IG linkini yuxarıya yapışdırın.";
                if(v.includes("salam")) r = "Salam! Necə kömək edə bilərəm?";
                else if(v.includes("necəsən") || v.includes("necesen")) r = "Mən botam, amma əlayam! Siz necəsiniz?";
                else if(v.includes("işləmir") || v.includes("problem")) r = "Linkin düzgün olduğuna və videonun gizli olmadığına əmin olun.";
                else if(v.includes("musiqi")) r = "Pleyer aşağıdadır, 'Play' düyməsinə basaraq dinləyə bilərsiniz.";
                else if(v.includes("kim") && v.includes("yaratdı")) r = "Bu sistem Zodiac tərəfindən sizin üçün hazırlanıb.";
                b.innerHTML += `<div class="msg b">${r}</div>`; b.scrollTop = b.scrollHeight;
            }, 500);
        }
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
