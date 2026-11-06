import os
import socket
import pathlib
import segno
from flask import Flask, request, render_template_string, Response, stream_with_context

# Configuration du stockage
DOSSIER = "partage"
os.makedirs(DOSSIER, exist_ok=True)

app = Flask(__name__)

# Désactive la limite de taille par défaut de Flask pour autoriser les fichiers volumineux
app.config['MAX_CONTENT_LENGTH'] = None 

# Interface HTML/CSS Modernisée et Responsivisée
HTML = """
<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ibzo - Speed Drop</title>
    <style>
        :root {
            --bg-color: #0b0d11;
            --card-bg: #15181f;
            --accent: #4a90e2;
            --accent-glow: rgba(74, 144, 226, 0.15);
            --success: #00ffcc;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --border: #262b36;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            width: 100%;
            max-width: 550px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        header { text-align: center; margin-bottom: 8px; }
        h1 { font-size: 1.8rem; font-weight: 700; letter-spacing: -0.025em; display: flex; align-items: center; justify-content: center; gap: 8px; }
        h1 span { color: var(--accent); }
        .subtitle { font-size: 0.95rem; color: var(--text-muted); margin-top: 6px; font-mono; }
        
        /* Zone de Drop */
        .drop {
            border: 2px dashed var(--border);
            background: var(--card-bg);
            border-radius: 16px;
            padding: 48px 24px;
            text-align: center;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        .drop:hover {
            border-color: var(--accent);
            box-shadow: 0 0 25px var(--accent-glow);
            transform: translateY(-2px);
        }
        .drop-icon { font-size: 2.5rem; margin-bottom: 12px; display: block; }
        .drop-title { font-size: 1.05rem; font-weight: 500; margin-bottom: 6px; }
        .drop-desc { font-size: 0.85rem; color: var(--text-muted); }
        
        /* Barre de Progression */
        .progress-container {
            width: 100%;
            background: var(--card-bg);
            border-radius: 9999px;
            display: none;
            overflow: hidden;
            border: 1px solid var(--border);
            padding: 3px;
        }
        .progress-bar {
            width: 0%;
            height: 16px;
            background: linear-gradient(90deg, var(--accent), var(--success));
            border-radius: 9999px;
            transition: width 0.1s ease;
            text-align: center;
            font-size: 10px;
            line-height: 16px;
            font-weight: 700;
            color: #000;
        }
        
        /* Liste des Fichiers */
        .file-list { display: flex; flex-direction: column; gap: 10px; }
        .file-item {
            background: var(--card-bg);
            border: 1px solid var(--border);
            padding: 14px 18px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            animation: fadeIn 0.3s ease;
        }
        .file-name {
            font-size: 0.95rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #e5e7eb;
        }
        .btn-dl {
            background: var(--accent);
            color: white;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: 8px;
            transition: background 0.2s;
            flex-shrink: 0;
        }
        .btn-dl:hover { background: #357abd; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1>⚡ ibzo <span>.</span></h1>
        <div class="subtitle">Serveur local actif : http://{{ip}}:8000</div>
    </header>

    <div class="drop" id="drop" onclick="document.getElementById('f').click()">
        <span class="drop-icon">🚀</span>
        <div class="drop-title">Glissez vos fichiers ici</div>
        <div class="drop-desc">Ou cliquez pour parcourir votre appareil<br><b>Zéro compression • Qualité 100% originale</b></div>
        <input type="file" id="f" multiple style="display:none">
    </div>

    <div class="progress-container" id="p_cont">
        <div class="progress-bar" id="p_bar">0%</div>
    </div>

    <div class="file-list" id="list">
        {% for f in files %}
        <div class="file-item">
            <span class="file-name" title="{{f}}">{{f}}</span>
            <a href="/dl/{{f}}" class="btn-dl">Télécharger</a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
const drop = document.getElementById('drop'), inp = document.getElementById('f'), pCont = document.getElementById('p_cont'), pBar = document.getElementById('p_bar');

function upload(files){
    if(files.length === 0) return;
    pCont.style.display = 'block';
    
    let file = files[0];
    let fd = new FormData();
    fd.append('file', file);
    
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload', true);
    
    xhr.upload.onprogress = e => {
        if (e.lengthComputable) {
            let percent = Math.round((e.loaded / e.total) * 100);
            pBar.style.width = percent + '%';
            pBar.innerText = percent + '%';
        }
    };
    
    xhr.onload = () => { location.reload(); };
    xhr.send(fd);
}

drop.ondragover = e => { e.preventDefault(); drop.style.borderColor = 'var(--accent)' };
drop.ondragleave = () => { drop.style.borderColor = 'var(--border)' };
drop.ondrop = e => { e.preventDefault(); drop.style.borderColor = 'var(--border)'; upload(e.dataTransfer.files) };
inp.onchange = () => upload(inp.files);
window.onpaste = e => { if(e.clipboardData.files.length) upload(e.clipboardData.files) }
</script>
</body>
</html>
"""

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

@app.route("/")
def index():
    files = os.listdir(DOSSIER)
    return render_template_string(HTML, files=files, ip=get_ip())

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files: return "no file"
    file = request.files['file']
    if file.filename == '': return "no filename"
    
    chemin_fichier = os.path.join(DOSSIER, file.filename)
    
    with open(chemin_fichier, 'wb') as f:
        while chunk := file.stream.read(1024 * 1024): 
            f.write(chunk)
    return "ok"

@app.route("/dl/<name>")
def dl(name):
    chemin_complet = pathlib.Path(DOSSIER).absolute() / name
    def generer_flux():
        with open(chemin_complet, 'rb') as f:
            while chunk := f.read(1024 * 1024):
                yield chunk
                
    return Response(stream_with_context(generer_flux()), 
                    headers={"Content-Disposition": f"attachment; filename={name}"},
                    content_type="application/octet-stream")

if __name__ == "__main__":
    ip = get_ip()
    url_partage = f"http://{ip}:8000"
    
    print("\n" + "="*50)
    print(f"🚀 SYSTÈME BOOSTÉ ACTIF : {url_partage}")
    print("="*50 + "\n")
    
    qr = segno.make_qr(url_partage)
    qr.terminal(compact=True)
    print("\n")
    
    app.run(host="0.0.0.0", port=8000, threaded=True)
