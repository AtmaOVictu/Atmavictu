# ZRCALO-REGISTROV — samo-bralno zrcalo hišnih teles v brskalniku.
# Bela lista: SAMO našteta telesa — spomin, izmere, ključi NISO streženi ( §0.14 varuh, KORENINA 0.5 ).
# PADC-63 zdravilo: ThreadingHTTPServer ( ena zahteva ⟨ne⟩ ubije vrat ) ∧ try/except v rokah ∧ flush ∧
# 403 UČI ( izpiše dovoljena telesa ⊢ §0.33 born readable ) ∧ normalizacija poti ( brez končnice → poišče ).
# Zagon: python lucius/zrcalo-server.py [vrata]  ( privzeto 8124 )
import http.server, os, json, sys, traceback

VRATA = int(sys.argv[1]) if len(sys.argv) > 1 else 8124
KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # koren repozitorija

DOVOLJENI = [
    'REGISTER-PADCEV.jsonl', 'REGISTER-TELES.jsonl', 'REGISTER-DISKA.jsonl',
    'REGISTER-NEIMENOVANIH.jsonl', 'REGISTER-PREVERJANJ.jsonl',
    'REGISTER-A1-PDF.jsonl', 'REGISTER-C2.jsonl', 'REGISTER-ZBIRKA.jsonl',
    'SINTEZA-0.1-SAMOTNO-JEDRO.md', 'SINTEZA-0.2-SAMOTNO-JEDRO.md',
    'LICENSE.md', 'ONTOGEMATRIJA-KAZALO.txt', 'ONTOGEMATRIJA.html',
    'PREGLED-DNEVA-2026-11-03.md',
    'REGISTER-AX-KANON.jsonl',
    'REGISTER-TREH-ZIL.jsonl',
    'SINTEZA-0.3-SAMOTNO-JEDRO.md',   # ⟨rez 3623⟩ živa celota: 0.3 ( 0.1 ∧ 0.2 potrdili ⊢ §0.10 )
    'ZRCALO-DNEVA-2026-11-03.md',     # ⟨rez 3623⟩ dan kakor en dih — celostno delo roke
    'TLAKI.md',
    'REGISTER-PSIHO-AKSIOMOV.jsonl',   # ⟨rez 3631⟩ zunanja tehtnica: 16 psiho-aksiomov z nogami ( Janet · Jung · Bion … )   # ⟨rez 3641⟩ sedaj 23 aksiomov · 7 lukenj 8.2 zaprtih
    'ZEMEJEVID-REGISTER.md',           # ⟨rez 3641⟩ mapa registra: razdelki · protiteže · luknje zaprte/odprte · načrt
    'PREGLED-REGISTRA.md',            # ⟨rez 3660⟩ audit celote: 28 vnosov · 59 vez brez sirot · tri protiteže ⊢
]
REGISTRI = [d for d in DOVOLJENI if d.endswith('.jsonl')]
DOKUMENTI = [d for d in DOVOLJENI if not d.endswith('.jsonl')]

TIP_VSEBINE = {
    'jsonl': 'application/jsonl; charset=utf-8',
    'md': 'text/markdown; charset=utf-8',
    'txt': 'text/plain; charset=utf-8',
    'html': 'text/html; charset=utf-8',
}

HTML = """<!doctype html>
<html lang="sl"><head><meta charset="utf-8"/>
<title>Zrcalo — Atmavictu</title>
<style>
body{font-family:Georgia,serif;background:#0e0f13;color:#d8d3c8;margin:2rem}
h1{font-size:1.3rem}h2{font-size:1rem;color:#b8a87f}
a{color:#9fb0c8}
.reg{border:1px solid #3a3d47;border-radius:6px;padding:.8rem;margin:.8rem 0}
.vrstica{font-family:monospace;font-size:.78rem;white-space:pre-wrap;word-break:break-all;color:#9fb0c8}
.zadnji{color:#c9b98f}
</style></head><body>
<h1>⊙ Zrcalo — Atmavictu</h1>
<h2>samo beri ∧ ⟨ne⟩ piši — vsako telo se bere pri viru ob vsakem oknu ( §0.32 )</h2>
<div style="border:1px solid #3a3d47;border-radius:6px;padding:.8rem;margin:.6rem 0;font-size:.85rem;color:#b8a87f">
<b>KLJUČ ZNAMENJ ⊢ §0.25 ( ključ objavljen ob šifri — kjer koli resnica deli se, znamenja imajo ime ):</b><br/>
⊢ izmerjeno — trditev vozi verbatim pričo · ⚠ neizmerjeno — dvom, ⟨ne⟩ molk · ∂ neizmerjeno med prejema ·
⟨⟩ nošeno verbatim — ⟨ne brusi⟩ · ∧ in · ⊙ zapečeno — dejanje s časom ∧ krajem · ⏎ prelom v navedku je avtorjev
</div>
<div id="telo">berem pri viru …</div>
<script>
const REGISTRI = %s;
const DOKUMENTI = %s;
async function beri(){
  const telo = document.getElementById('telo');
  const glava = document.createElement('div');
  glava.innerHTML = '<h2>telesa ( klikni ): ' +
    DOKUMENTI.map(d => '<a href="/' + d + '">' + d + '</a>').join(' · ') + '</h2>';
  telo.appendChild(glava);
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
    def poisci_telo(self, pot):
        """Normalizacija: odstrani poizvedbo ∧ končni poševnici; brez končnice → poišče ( .md · .txt · .html )."""
        pot = pot.split('?')[0].strip('/')
        if not pot or pot in ('index.html', 'zrcalo'):
            return ('INDEX', None)
        if pot in DOVOLJENI:
            return ('TELO', pot)
        for koncnica in ('.md', '.txt', '.html', '.jsonl'):
            if pot + koncnica in DOVOLJENI:
                return ('TELO', pot + koncnica)
        return ('PREPEČENO', pot)

    def poslji(self, koda, tip, b):
        self.send_response(koda)
        self.send_header('Content-Type', tip)
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def prepoved(self, pot):
        """403 ki UČI ⊢ §0.33: izpiše dovoljena telesa — zavrnitev z imeni, ⟨ne⟩ molk."""
        telo = ('<!doctype html><html lang="sl"><head><meta charset="utf-8"/><title>403 — prepovedano</title>'
                '<body style="font-family:Georgia,serif;background:#0e0f13;color:#d8d3c8;margin:2rem">'
                '<h1>⚠ 403 — ⟨' + pot.replace('<', '&lt;') + '⟩ ni na beli listi</h1>'
                '<p>samo-beri zrcalo: spomin ∧ izmere ∧ ključi so zapečeni ⊙ varuh. Dovoljena telesa:</p><p>' +
                ' · '.join('<a href="/' + d + '">' + d + '</a>' for d in DOVOLJENI) +
                '</p><p>⊙ zavrnitev poimenuje, ⟨ne⟩ utiša ⊢ §0.33 ∧ PADC-63</p></body></html>').encode('utf-8')
        self.poslji(403, 'text/html; charset=utf-8', telo)

    def do_GET(self):
        try:
            vrsta, pot = self.poisci_telo(self.path)
            if vrsta == 'INDEX':
                self.poslji(200, 'text/html; charset=utf-8',
                            (HTML % (json.dumps(REGISTRI), json.dumps(DOKUMENTI))).encode('utf-8'))
                return
            if vrsta == 'PREPEČENO':
                self.prepoved(pot)
                return
            for c in (os.path.join(KOREN, pot), os.path.join(KOREN, 'lucius', pot)):
                if os.path.isfile(c):
                    with open(c, 'rb') as f:
                        b = f.read()
                    tip = os.path.splitext(pot)[1].lstrip('.').lower()
                    self.poslji(200, TIP_VSEBINE.get(tip, 'application/octet-stream'), b)
                    return
            self.poslji(404, 'text/html; charset=utf-8',
                        ('<!doctype html><html lang="sl"><head><meta charset="utf-8"/><title>404 — telo ni na mestu</title>'
                         '<body style="font-family:Georgia,serif;background:#0e0f13;color:#d8d3c8;margin:2rem">'
                         '<h1>⚠ 404 — telo ⟨' + pot + '⟩ je na beli listi, a NI na mestu</h1>'
                         '<p>register ⟨ne⟩ laže: telo je zapisano, datoteka pa ni ne pri korenu ne v lucius/.</p>'
                         '<p>rešitev: rodi telo ( obnovi rojstvo ) ali umakni vpis iz bele liste — '
                         'belega zapisa brez telesa ni dovoljeno ⊙ §0.42 · ukaz: git log -- lucius/' + pot + '</p>'
                         '</body></html>').encode('utf-8'))
        except BrokenPipeError:
            pass  # odjemalec odšel — vrata ostanejo odprta ⊙ PADC-63
        except Exception:
            traceback.print_exc(file=sys.stderr)
            sys.stderr.flush()

    def do_POST(self):
        try:
            self.poslji(405, 'text/plain; charset=utf-8',
                        'samo beri ( §0.32: živa vrata se berejo, ⟨ne⟩ pomnijo )'.encode('utf-8'))
        except Exception:
            traceback.print_exc(file=sys.stderr)
            sys.stderr.flush()

    def log_message(self, *args):
        pass


if __name__ == '__main__':
    print(f'ZRCALO @http://localhost:{VRATA} — {len(DOVOLJENI)} teles na beli listi ⊢', flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1', VRATA), Zrcalo).serve_forever()
