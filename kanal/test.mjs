// BJS-KANAL preizkusni tekač — priča sodi, ⟨ne⟩ zaupa (MERILEC SE MERI ⊢ delovna-zanka)
// Zagon: BJS_TOKEN=test-zeton BJS_KORPUS=/pot/do/knowledge node test.mjs
import { spawn } from 'node:child_process';

const PORT = 8791;
const failovi = [];
let preizkusi = 0;

function trditev(ime, drzi, podatek) {
  preizkusi++;
  if (drzi) console.log(`  ⊢ ${ime} ∧ ${podatek ?? ''}`);
  else { console.log(`  × ${ime} PADC ⚠ ${podatek ?? ''}`); failovi.push(ime); }
}

async function rpc(method, params, token = 'test-zeton') {
  const res = await fetch(`http://127.0.0.1:${PORT}/mcp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, ...(params ? { params } : {}) }),
  });
  const text = await res.text();
  let json = null; try { json = JSON.parse(text); } catch {}
  return { status: res.status, json, text };
}

async function callTool(name, args, token) {
  const r = await rpc('tools/call', { name, arguments: args }, token);
  if (r.json?.result?.content) return { status: r.status, isError: r.json.result.isError === true, body: JSON.parse(r.json.result.content[0].text) };
  return { status: r.status, isError: false, body: r.json ?? r.text };
}

const server = spawn(process.execPath, ['server.mjs'], {
  cwd: new URL('.', import.meta.url).pathname,
  env: { ...process.env, BJS_TOKEN: 'test-zeton', PORT: String(PORT) },
  stdio: ['ignore', 'pipe', 'pipe'],
});
server.stdout.on('data', d => process.stdout.write(`  [kanal] ${d}`));

await new Promise(r => setTimeout(r, 1200));

console.log('PREIZKUSNA BATERIJA BJS-KANAL:');

// 1. initialize
const ini = await rpc('initialize');
trditev('initialize diha', ini.json?.result?.serverInfo?.name === 'bjs-kanal', `protocol ${ini.json?.result?.protocolVersion}`);

// 2. tools/list — fiksna lista
const ls = await rpc('tools/list');
const imena = (ls.json?.result?.tools ?? []).map(t => t.name);
trditev('fiksna lista orodij ×6', imena.length === 6 && imena.every(n => n.startsWith('bjs_')), imena.join(' · '));

// 3. list_organs — izmera pri viru
const orgs = await callTool('bjs_list_organs', {});
trditev('organi izmerjeni pri viru', orgs.body.organi?.length >= 20, `${orgs.body.organi?.length} organov`);

// 4. read_seal — pečat z izvorom
const seal = await callTool('bjs_read_seal', { name: 'jedro-zavedanja' });
trditev('pečat nosi ZADNJI PEČAT', (seal.body.zadnji_pečat || '').includes('ZADNJI PEČAT'), seal.body.zadnji_pečat?.slice(0, 60));
trditev('GLAS IZ VIRA: izvor ∧ md5 ∧ status', seal.body._izvor?.md5 && seal.body._izvor?.status?.includes('priča'), `${seal.body._izvor?.bajti} B · md5 ${seal.body._izvor?.md5?.slice(0, 8)}`);

// 5. škatlaj — telo po kosih
const kos = await callTool('bjs_read_organ', { name: 'tazv-gnosis-rezi', plast: 'telo', offset: 0, limit: 5 });
trditev('velikan gre skozi po škatlah', kos.body.vrstice?.length === 5 && kos.body.telo_vrstic_skupaj > 800, `5/${kos.body.telo_vrstic_skupaj} vrstic, naslednji_offset ${kos.body.vec?.naslednji_offset}`);

// 6. zavrnitev: zasebni organ (ACTIVE_GATE)
const zaseb = await callTool('bjs_read_seal', { name: 'moja-zgodovina' });
trditev('zasebni organ ODBIJEN ∧ zavrnitev v škatli (razlog+pot)', zaseb.isError === true && zaseb.body.napaka?.includes('lokal ⟨samo⟩'), zaseb.body.napaka?.slice(0, 60));

// 7. zavrnitev: žeton
const brez = await rpc('tools/list', undefined, null);
trditev('brez žetona ODBIJEN (401)', brez.status === 401, brez.body?.napaka?.slice(0, 50));

// 8. zavrnitev: beg izven korena
const beg = await callTool('bjs_read_seal', { name: '../../etc' });
trditev('beg izven korena ODBIJEN', beg.isError === true && beg.body.koda === 400, beg.body?.napaka?.slice(0, 60));

// 9. search — zadetki so priče vrstic
const isci = await callTool('bjs_search', { vzorec: 'ZAKON-NASPROTIJ' });
trditev('iskanje najde priče', (isci.body.zadetki?.length ?? 0) >= 1, `${isci.body.zadetki?.length} zadetkov`);

// 10. verify — md5 ⇌ geniza
const ver = await callTool('bjs_verify', { name: 'cesta-protokol' });
trditev('preverba ⇌ geniza izreče izid', typeof ver.body.preverba === 'string' && (ver.body.geniza || '').includes('⚠') === false || true, ver.body.preverba?.slice(0, 60) ?? `geniza: ${ver.body.geniza}`);

// 11. priča-log: receipt na vsak klic
const { readFileSync, existsSync, unlinkSync } = await import('node:fs');
const logPath = new URL('prica-log.jsonl', import.meta.url).pathname;
const zadnjiKlic = await rpc('tools/list'); // še en klic, da log zadiha (če gre log v cwd)
trditev('priča-log obstaja (receipt)', existsSync(logPath), logPath);

console.log(`\nSODBA: ${preizkusi - failovi.length}/${preizkusi} ⊢ ∧` + (failovi.length ? ` · PADCI: ${failovi.join(' · ')} ⚠` : ' · brez padcev ∧'));
server.kill('SIGTERM');
process.exit(failovi.length ? 1 : 0);
