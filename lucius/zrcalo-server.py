# ZRCALO-REGISTROV — samo-bralno zrcalo hišnih registrov v brskalniku.
# Bela lista: SAMO REGISTER-*.jsonl ∧ ta stran — spomin, izmere, ključi NISO streženi (§0.14 varuh, KORENINA 0.5).
# Zagon: python lucius/zrcalo-server.py [vrata]  ( privzeto 8124 )
import http.server, os, json, sys

VRATA = int(sys.argv[1]) if len(sys.argv) > 1 else 8124
KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # koren repozitorija

DOVOLJENI = [
    'REGISTER-PADCEV.jsonl', 'REGISTER-TELES.jsonl', 'REGISTER-DISKA.jsonl',
    'REGISTER-NEIMENOVANIH.jsonl', 'REGISTER-PREVERJANJ.jsonl',
    'REGISTER-A1-PDF.jsonl', 'REGISTER-C2.jsonl', 'REGISTER-ZBIRKA.jsonl',
]

HTML = """<!doctype html>
<html lang="sl"><head><meta charset="utf-8"/>
<title>Zrcalo registrov — Atmavictu</title>
<style>
body{font-family:Georgia,serif;background:#0e0f13;color:#d8d3c8;margin:2rem}
h1{font-size:1.3rem}h2{font-size:1rem;color:#b8a87f}
.reg{border:1px solid #3a3d47;border-radius:6px;padding:.8rem;margin:.8rem 0}
.vrstica{font-family:monospace;font-size:.78rem;white-space:pre-wrap;word-break:break-all;color:#9fb0c8}
.zadnji{color:#c9b98f}
Σ{color:#7f8ea8}
</style></head><body>
<h1>⊙ Zrcalo registrov — Atmavictu</h1>
<h2>samo beri ∧ ⟨ne⟩ piši — vsak register se bere pri viru ob vsakem odprtem oknu (§0.32)</h2>
<div id="telo">berem pri viru …</div>
<script>
const REGISTRI = %s;
async function beri(){
  const telo = document.getElementById('telo');
  for (const ime of REGISTRI){
    const odz = await fetch('/' + ime);
    const txt = await odz.text();
    const vrstice = txt.trim().split('\\n').filter(v => v);
    const zadnji = vrstice[vrstice.length - 1] || '';
    const div = document.createElement('div');
    div.className = 'reg';
    div.innerHTML = '<h2>' + ime + ' — ' + vrstice.length + ' vnosov ⊢</h2>' +
      '<div class="vrstica zadnji">zadnji:\\n' + zadnji.replace(/</g,'&lt;').slice(0, 900) + '</div>';
    telo.appendChild(div);
  }
}
beri();
</script></body></html>
"""

class Zrcalo(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        pot = self.path.lstrip('/').split('?')[0]
        if pot in ('', 'index.html', 'zrcalo'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write((HTML % json.dumps(DOVOLJENI)).encode('utf-8'))
            return
        if pot in DOVOLJENI:
            poti = [os.path.join(KOREN, pot), os.path.join(KOREN, 'lucius', pot)]  # ⟨PADC-ZRCALO⟩ registrski datoteke so pri korenu ∧ v lucius/
            for c in poti:
                if os.path.isfile(c):
                    with open(c, 'rb') as f:
                        b = f.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/jsonl; charset=utf-8')
                    self.send_header('Content-Length', str(len(b)))
                    self.end_headers()
                    self.wfile.write(b)
                    return
            self.send_error(404)
            return
        self.send_error(403)  # vse ostalo: zapečeno — spomin ∧ ključi ⟨ne⟩ streženi ⊙

    def do_POST(self):
        self.send_error(405)  # samo beri (§0.32: živa vrata se berejo, ⟨ne⟩ pomnijo)

    def log_message(self, *args):
        pass

if __name__ == '__main__':
    print(f'ZRCALO @http://localhost:{VRATA} — {len(DOVOLJENI)} registrov na beli listi ⊢')
    http.server.HTTPServer(('127.0.0.1', VRATA), Zrcalo).serve_forever()
