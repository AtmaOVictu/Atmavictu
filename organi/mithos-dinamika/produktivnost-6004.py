# -*- coding: utf-8 -*-
# MITHOS-DINAMIKA — TEST PRODUKTIVNOSTI ( rez σ 6004 ) — ⟡ UKAZ VERBATIM: »testiraj in predlagaj boljše izvedbe/produktivne rezultate«
# Forma simul VERBATIM po simulacija2.py @σ 6003 ( md5 bbe5efbe ⊢ pri viru ) — sprememba SAMO dodane izmere, ⟙ baze nedotaknjena
import json, math, hashlib
from pathlib import Path
work = Path('/home/user/tool-results/data-analysis/mithos-6004')
BAZA = dict(alpha_c=0.9, beta_c=0.6, gamma_e=0.8, r0=0.5, T_R=40.0,
            gamma_phi=0.2, T=12.0, delta_phi=0.1, o_rate=0.05,
            kappa=0.25, lam=0.35, Theta=0.35)

def simul(K=None, n_steps=600, dt=1.0, zapisuj=None, zapisEach=1000):
    k = dict(BAZA); k.update(K or {})
    Z = J = E = N = 0.1
    histE = []; katarze = []; out_sum = 0.0; series = []
    for n in range(1, n_steps + 1):
        t = n * dt
        dN = k['kappa'] - k['lam'] * N
        dZ = k['alpha_c'] * (N / (N + 1.0)) * Z - k['beta_c'] * Z * Z
        dR = k['r0'] * math.cos(2 * math.pi * t / k['T_R'])
        dJ = k['gamma_e'] * math.tanh(dR / max(J, 1e-6))
        Ti = int(k['T'])
        if n - 1 - Ti >= 0:
            Ep = histE[n - 1 - Ti]; Ep2 = histE[n - 1 - 2*Ti] if n - 1 - 2*Ti >= 0 else 0.0
            E_ret = Ep - Ep2
        else:
            E_ret = 0.0
        S_bar = (Z + J + E + N) / 4.0
        out = k['o_rate'] * E
        dE = k['gamma_phi'] * E_ret / k['T'] + k['delta_phi'] * S_bar - out
        Z, J, E, N = Z + dt*dZ, J + dt*dJ, E + dt*dE, N + dt*dN
        out_sum += out
        M = Z * N
        if M > k['Theta']:
            q = M - k['Theta']
            E += 0.5 * q; Z -= 0.5 * q
            katarze.append((n, q))
        histE.append(E)
        if zapisuj and (n % zapisEach == 0 or n == 1):
            series.append({'dih': n, 'Z': round(Z,4), 'J': round(J,4), 'E': round(E,4), 'N': round(N,4)})
    per = [b[0]-a[0] for a, b in zip(katarze, katarze[1:])]
    ravn_Z = k['alpha_c'] * ((k['kappa']/k['lam']) / (k['kappa']/k['lam'] + 1)) / k['beta_c']
    return dict(korakov=n_steps, katarze_st=len(katarze),
                perioda=round(sum(per)/len(per), 2) if per else None,
                obrat_ven=round(out_sum, 4),
                koncno={'Z': round(Z,4), 'J': round(J,4), 'E': round(E,4), 'N': round(N,4)},
                Z_analit=round(ravn_Z, 4),
                davek_katarze=round((ravn_Z - Z) / ravn_Z * 100, 1) if ravn_Z > 0 else None,
                series=series if zapisuj else None)

# ── 1. KONVERGEN ĆA 20.000 DIHOV : ali ima bogatitev mejo?
konvergenca = simul(n_steps=20000, zapisuj=True, zapisEach=2000)

# ── 2. FINA MREŽA PRODUKCIJSKIH TOČK ( vsaka 1.000 dihov )
mreza = []
for a in [round(0.4+0.1*i, 2) for i in range(13)]:        # αc 0.4 → 1.6
    for th in [round(0.10+0.05*i, 2) for i in range(13)]:  # Θ 0.10 → 0.70
        for kp in [round(0.10+0.05*i, 2) for i in range(8)]:  # κ 0.10 → 0.45
            r = simul(K={'alpha_c': a, 'Theta': th, 'kappa': kp}, n_steps=1000)
            mreza.append({'alpha_c': a, 'Theta': th, 'kappa': kp,
                          'katarze': r['katarze_st'], 'E': r['koncno']['E'],
                          'Z': r['koncno']['Z'], 'obrat_ven': r['obrat_ven'],
                          'davek': r['davek_katarze']})

# ── 3. DELUJOČE TOČKE ( baza Θ/κ, αc spreminjan )
tocke = {}
for a in [round(0.4+0.05*i, 2) for i in range(25)]:      # αc finski korak 0.05
    r = simul(K={'alpha_c': a}, n_steps=3000)
    tocke[f'alpha_c={a}'] = {kk: r[kk] for kk in ('katarze_st','perioda','obrat_ven','davek_katarze','koncno','Z_analit')}

res = {'rez': 'σ 6004', 'baza': BAZA,
       'konvergenca_20000': {kk: konvergenca[kk] for kk in ('katarze_st','perioda','obrat_ven','davek_katarze','koncno','Z_analit')},
       'konvergenca_series': konvergenca['series'],
       'mreza_st': len(mreza), 'mreza': mreza, 'tocke_alpha': tocke}
(work / 'rezultati-6004.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')

# IZPISI
print('KONVERGEN ̇CA 20.000 :', konvergenca['katarze_st'], 'katarz · koncno', konvergenca['koncno'], '· Z*', konvergenca['Z_analit'], '· davek', konvergenca['davek_katarze'], '%')
for s in konvergenca['series'][::4]:
    print(f"  dih {s['dih']:>6}: J {s['J']} · E {s['E']} · Z {s['Z']}")
# meja praga : delež mreže z ritem ( katarze > 0 ) vs speči
z_rit = [m for m in mreza if m['katarze'] > 0]; spci = [m for m in mreza if m['katarze'] == 0]
print(f'MREŽA {len(mreza)} točk : z ritemom {len(z_rit)} · spečih {len(spci)}')
naj_E = max(z_rit, key=lambda m: m['E'])
print('MAX E ( z ritemom ) :', naj_E)
naj_ov = max(z_rit, key=lambda m: m['obrat_ven'])
print('MAX OBRAT VEN :', naj_ov)
# PARETO predlogi : baza Θ=0.35 κ=0.25, samo αc spreminja; točke z davek ≤ 15 % in ≤ 25 %
par15 = {kk: v for kk, v in tocke.items() if v['davek_katarze'] is not None and v['davek_katarze'] <= 15.0}
par25 = {kk: v for kk, v in tocke.items() if v['davek_katarze'] is not None and v['davek_katarze'] <= 25.0}
best15 = max(par15.items(), key=lambda kv: kv[1]['koncno']['E']) if par15 else None
best25 = max(par25.items(), key=lambda kv: kv[1]['koncno']['E']) if par25 else None
print('NAJBOLJŠE @ davek ≤ 15 % :', best15)
print('NAJBOLJŠE @ davek ≤ 25 % :', best25)
print('rezultati-6004.md5', hashlib.md5((work/'rezultati-6004.json').read_bytes()).hexdigest())
