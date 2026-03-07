from flask import Flask, render_template_string, request, send_from_directory
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZODIAC ELITE</title>
    <style>
        body { background: #050505; color: white; font-family: sans-serif; text-align: center; margin: 0; padding-top: 50px; }
        .card { background: rgba(255,255,255,0.05); border: 1px solid #333; border-radius: 20px; width: 90%; max-width: 400px; margin: auto; padding: 30px; }
        h1 { color: #00f2fe; letter-spacing: 5px; }
        .play-btn { background: #00f2fe; border: none; padding: 15px; border-radius: 50%; width: 60px; height: 60px; font-size: 20px; cursor: pointer; margin: 20px 0; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: 1px solid #444; background: #111; color: white; box-sizing: border-box; }
        .btn { width: 100%; padding: 12px; border-radius: 10px; border: none; background: #00f2fe; font-weight: bold; cursor: pointer; }
        #t-name { font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="card">
        <h1>ZODIAC</h1>
        <div id="t-name">Musiqi Hazır</div>
        <button class="play-btn" onclick="t()">▶</button>
        
        <form method="POST">
            <input type="text" name="u" placeholder="Link bura..." required>
            <button type="submit" class="btn">ANALİZ ET</button>
        </form>

        {% if dl %}
        <br><a href="{{ dl }}" style="color:#00f2fe; font-size:13px;" target="_blank">📥 VİDEONU YÜKLƏ</a>
        {% endif %}
    </div>

    <audio id="m" onended="n()"></audio>

    <script>
        const s = [
            {n: "Lotular", s: "Lotular(MP3_160K).mp3"},
            {n: "Ara Usaqlari", s: "Ara Usaqlari(MP3_160K).mp3"},
            {n: "AIS", s: "AIS - Пыяла x Sarışan hallar(M.mp3"}
        ];
        let i = 0;
        const a = document.getElementById('m');
        const d = document.getElementById('t-name');

        function l(idx) {
            a.src = "/music/" + encodeURIComponent(s[idx].s);
            d.innerText = "Oxuyur: " + s[idx].n;
        }
        l(i);

        function t() {
            if(a.paused) { a.play().catch(e => alert("Ekrana bas!")); }
            else { a.pause(); }
        }

        function n() { i = (i + 1) % s.length; l(i); a.play(); }
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
