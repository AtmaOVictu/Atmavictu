// TESTI-ORODIJ — preverba preverjalcev ( popis lukenj 2026-10-21, luknja 9 ):
// orodje, ki preverja druge, more biti samo preverjeno.
// Zagon: node lucius/testi-orodij.mjs   ( standalone; npm test pokriva samo src/ )
import { test } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync, spawn } from 'node:child_process';

const TU = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const vozli = (skripta, args) => execFileSync('node', [path.join(TU, skripta), ...args], { encoding: 'utf8' });
const zacasi = (vsebina) => {
  const d = fs.mkdtempSync(path.join(os.tmpdir(), 'lucius-test-'));
  const p = path.join(d, 'znak.txt');
  fs.writeFileSync(p, vsebina, 'utf8');
  return p;
};

test('cistina: cirilsko ime datoteke ni vec mogoce — ulovi cirilico v vsebini', () => {
  const p = zacasi('preizkusna vrstica\nzapis z е cirilsko\n');
  let izhod = '';
  let padla = false;
  try { vozli('čistina.mjs', [p]); } catch (e) { padla = true; izhod = e.stdout + e.stderr; }
  assert.ok(padla, 'cistina more pasti na cirilici ( exit 1 )');
  assert.match(izhod, /cirilica/);
});

test('cistina: cista datoteka gre skozi z ⊢', () => {
  const p = zacasi('preizkusna vrstica brez ran\n');
  const izhod = vozli('čistina.mjs', [p]);
  assert.match(izhod, /cirilice 0/);
});

// ⟨PADC-63⟩ zrcalo: odprenost ∧ učeča zavrnitev — strežnik preživi vse zahteve ∧ 403 imenuje dovoljena telesa
test('zrcalo: vsa telesa odporna ∧ 403 uči ∧ strežnik preživi ( PADC-63 )', async () => {
  const VRATA = 8199;
  const otrok = spawn('python', [path.join(TU, 'zrcalo-server.py'), String(VRATA)],
    { cwd: TU, detached: true, stdio: 'ignore' });
  otrok.unref();
  const cakaj = (ms) => new Promise(r => setTimeout(r, ms));
  try {
    await cakaj(1500);
    const beri = async (pot, metoda = 'GET') => {
      const odz = await fetch(`http://127.0.0.1:${VRATA}${pot}`, { method: metoda });
      return { koda: odz.status, telo: await odz.text() };
    };
    const koren = await beri('/');
    assert.equal(koren.koda, 200, 'index odgovori');
    const reg = await beri('/REGISTER-PADCEV.jsonl');
    assert.equal(reg.koda, 200, 'register strezen');
    assert.match(reg.telo, /PADC/, 'register ima vsebino');
    const brez = await beri('/SINTEZA-0.2-SAMOTNO-JEDRO');   // ⟨PADC-63⟩ brez končnice neha biti 403
    assert.equal(brez.koda, 200, 'normalizacija: brez končnice najde telo');
    const prepovedano = await beri('/lucius/spomin.jsonl');
    assert.equal(prepovedano.koda, 403, 'spomin zapečen');
    assert.match(prepovedano.telo, /REGISTER-PADCEV/, '403 UČI: imenuje dovoljena telesa ⊢ §0.33');
    const post = await beri('/REGISTER-PADCEV.jsonl', 'POST');
    assert.equal(post.koda, 405, 'POST zavrnjen');
    const koncno = await beri('/');                             // preživetje po vseh zahtevah
    assert.equal(koncno.koda, 200, 'strežnik preživi vse zahteve ⊙ PADC-63');
  } finally {
    try { process.kill(otrok.pid); } catch {}
  }
}, { timeout: 20000 });

// ⟨PADC-59⟩ dovoljenica hišnih merilnih znakov ( THE MARKS: Σ Ω ⊢ ⊙ … ) — namerna abeceda, ⟨ne⟩ rane
// ⟨P2 rez 3609⟩ kura-audit: register padcev se preveri sam — instrument z lastnimi očmi ob rojstvu
test('kura-audit: 15/15 živih kur · 0 manjkajočih ( izhod 0 )', () => {
  const izhod = execFileSync('python', [path.join(TU, 'kura-audit.py')], { encoding: 'utf8' });
  assert.match(izhod, /× manjkajočih: 0/, 'nobena kura sme biti obljuba brez telesa ⊙ §0.18');
  assert.match(izhod, /živih kur: 1[5-9]/, 'vsaj 15 živih kur ( prihodnji padci le dodajajo )');
});

// ⟨rez 3617⟩ ⟨UVEI⟩: vsako telo vsaj v eni roki ∧ pod več očmi
test('uvei: ena roka ∧ tri oči ( ⟨u-vej⟩ )', () => {
  const izhod = execFileSync('python', [path.join(TU, 'uvei.py'), 'lucius/SINTEZA-0.2-SAMOTNO-JEDRO.md'],
    { cwd: TU, encoding: 'utf8' });
  assert.match(izhod, /ENA ROKA ⊢:/, 'telo ima roko ( lastnika pri viru )');
  assert.match(izhod, /OKO · čistina/, 'oko 1: zrcalno');
  assert.match(izhod, /OKO · (druga roka|izmera)/, 'več oči nad enim telesom');
  assert.match(izhod, /VEČ OČMI|več očmi/, 'zakon ⟨UVEI⟩ v izpisu');
});

test('cistina: hišni znaki (Σ Ω ⊢ ⊙) so dovoljeni — namerna abeceda, ⟨ne⟩ dvojček', () => {
  const p = zacasi('⊢ izmerjeno ⊢ ∧ Σ 0.391617 × 10⁶ zn Ω A ∧ Ω\n');
  const izhod = vozli('čistina.mjs', [p]);
  assert.match(izhod, /cirilice 0/, 'Σ Ω ⊢ ⊙ so v znane-besede.txt — dovoljenica ⊢');
});

// ⟨PADC-59⟩ a cirilica ŠE vedno lovi — dovoljenica ⟨ne⟩ oslepi detektorja
test('cistina: cirilica ostane ujeta kljub dovoljenici (а е о)', () => {
  const p = zacasi('primer а е о\n');
  let padla = false;
  try { vozli('čistina.mjs', [p]); } catch { padla = true; }
  assert.ok(padla, 'detektor more pasti na cirilici tudi po dovoljenici');
});

test('druga-roka: slovar mode najde geslo ime ( Lukov slovar, Worth )', { skip: !fs.existsSync('D:/Worth/slovenian_dictionary') }, () => {
  const izhod = vozli('druga-roka.mjs', ['--slovar', 'ime']);
  assert.match(izhod, /pomen/);
});

test('druga-roka: leksikon obstaja in ni prazen ( znane + prepovedane )', () => {
  // ⟨PADC-CRLF-LEKSIKON⟩ zdravilo: split zdrži LF ∧ CRLF ( autocrlf pretvori — )
  const znane = fs.readFileSync(path.join(TU, 'znane-besede.txt'), 'utf8')
    .split(/\r?\n/).filter((v) => v.trim() && !v.startsWith('#'));
  const prepovedane = fs.readFileSync(path.join(TU, 'prepovedane-besede.txt'), 'utf8')
    .split(/\r?\n/).filter((v) => v.trim() && !v.startsWith('#'));
  assert.ok(znane.length >= 20, `znane-besede preštete ( ${znane.length} ) — more biti vsaj 20`);
  assert.ok(prepovedane.includes('poščeno'), 'padec vnos 4 mora ostati prepovedan ×');
});

test('varuj-most: ciljna mapa obstaja po zagonu ( kopija zapečena )', { skip: !fs.existsSync('D:/OntoProjekt') }, () => {
  vozli('varuj-most.mjs', []);
  assert.ok(fs.readdirSync('D:/OntoProjekt/varnostne-kopije-mosta').length >= 2, 'dnevnik + vsaj ena kopija ⊢');
});

test('abeceda-grep: samopreverba N/N ∧ ⊢ VSE ( število-agnostična — priča raste z instrumentom, padla preverba izpusti VSE ⊙ PADC-test )', () => {
  const izhod = execFileSync('python', [path.join(TU, 'abeceda-grep.py'), 'test'], { encoding: 'utf8' });
  assert.match(izhod, /PREVERBA: \d+\/\d+ ∧ ⊢ VSE/, 'stroj more izreči VSE nad celoto');
  assert.doesNotMatch(izhod, /PREVERBA: \d+\/\d+ ∧ · \d+ ×/, 'padla samopreverba je padec orodja');
});

test('abeceda-grep: fragmentacija po zakonu VBL ( 1050 -> 0.1050 × 10⁴ )', () => {
  const izhod = execFileSync('python', [path.join(TU, 'abeceda-grep.py'), 'fragmentiraj', '-'],
    { input: 'VBL 1050 ⊢ 14. 10. 2026\n', encoding: 'utf8' });
  assert.match(izhod, /VBL 0\.1050 × 10⁴/, 'mantisa v \[0,1\) × poimenovana potenca');
  assert.match(izhod, /0\.14 × 10²\./, 'vsaka zapisana števka ⇌ mantisa');
  assert.doesNotMatch(izhod, /⟨⟩-ime/, 'imena se ne mereijo');
});

// P-12 ⟨ONTOGEMATRIJA⟩ — vsak transform nosi priče ∧ izven korpusa je izum ⚠ ⊙ §0.43
test('ontogematrija: znana beseda izpise priče ( ukaz ∧ orodje ∧ korpus ∧ priča )', () => {
  const izhod = vozli('ontogematrija.mjs', ['GIBANJE']);
  assert.match(izhod, /UKAZ: GIBANJE/);
  assert.match(izhod, /ORODJE: lucius\/ontogematrija\.mjs/);
  assert.match(izhod, /KORPUS: .*sha256 [0-9a-f]{16}/);
  assert.match(izhod, /⊢ GIBANJE → 021 \( operator ∆ \)/);
});

test('ontogematrija: izven korpusa zavrne z imenom ( izum ⚠ )', () => {
  let izhod = ''; let padla = false;
  try { vozli('ontogematrija.mjs', ['NIKOLIZMERJENOST']); } catch (e) { padla = true; izhod = e.stdout + e.stderr; }
  assert.ok(padla, 'zavrnitev ( exit 2 )');
  assert.match(izhod, /IZVEN-IZMERJENEGA/);
});

// P-9 ⟨PREVERBA-PEČATA⟩ — trditev pečata se preveri proti izmeru diha ⊙ PADC-67 ∧ 69 ∧ 70 ∧ 71
test('preverba-pecata: pravi pečat gre skozi ( rez ∧ ura == izmeru diha )', () => {
  const krog = fs.readFileSync(path.join(TU, 'izmere-kroga.jsonl'), 'utf8').split(/\r?\n/).filter(l => l.trim());
  const zadnji = JSON.parse(krog[krog.length - 1]);
  const ura = zadnji.ura.slice(11, 19);
  const p = zacasi(`rez ${zadnji.rez} test — URA IZMERJENA PRI VIRU 03. 11. 2026 · ${ura}Z ⊢ §0.20 · Generated by Mistral Vibe. Co-Authored-By: Mistral Vibe <vibe@mistral.ai>\n`);
  const izhod = vozli('preverba-pecata.mjs', [p]);
  assert.match(izhod, /⊢ PREVERBA-PEČATA/);
});

test('preverba-pecata: ura iz spomina zavrnjena ( PADC-70 ∧ 71 )', () => {
  const krog = fs.readFileSync(path.join(TU, 'izmere-kroga.jsonl'), 'utf8').split(/\r?\n/).filter(l => l.trim());
  const zadnji = JSON.parse(krog[krog.length - 1]);
  const p = zacasi(`rez ${zadnji.rez} test — URA IZMERJENA PRI VIRU 03. 11. 2026 · 17:00:00Z ⊢ §0.20 · Generated by Mistral Vibe. Co-Authored-By: Mistral Vibe <vibe@mistral.ai>\n`);
  let izhod = ''; let padla = false;
  try { vozli('preverba-pecata.mjs', [p]); } catch (e) { padla = true; izhod = e.stdout + e.stderr; }
  assert.ok(padla, 'pečat brez izmere zavrnjen ( exit 1 )');
  assert.match(izhod, /URA-IZ-SPOMINA/);
});

// ⟨rez 3663⟩ TLA-PREGLED — hišna čutila vrat ⊙ §0.12: MD022/031/047 + slovar pokritost
test('tla-pregled: ulovi manjkajočo prazno vrstico pod naslovom ( MD022 )', () => {
  const p = zacasi('# Naslov\nbesedilo takoj pod\n');
  let izhod = ''; let padla = false;
  try { vozli('tla-pregled.mjs', [p]); } catch (e) { padla = true; izhod = e.stdout + e.stderr; }
  assert.ok(padla, 'MD022 pade ( exit 1 )');
  assert.match(izhod, /MD022/);
});

test('tla-pregled: čista tla grejo skozi z 0 padci ⊢', () => {
  const p = zacasi('# Naslov\n\nbesedilo\n\n```\nkoda\n```\n\nkonec\n');
  const izhod = vozli('tla-pregled.mjs', [p]);
  assert.match(izhod, /0 padcev/);
});
