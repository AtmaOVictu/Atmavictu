# -*- coding: utf-8 -*-
# MITHOS-DINAMIKA — SIMULACIJA II ( rez σ 6003 ) — parametrijska spirala + dolga proga
# Formule ⟡ VERBATIM @mithos-dinamika ⟨NE-RETIPKAJ⟩ 24 ; zasute forme ∧ katarza VERBATIM po simulacija.py @σ 5992 ( md5 246542cb ⊢ pri viru )
# KONSTANTE ⚠ HIPOTEZE ⊙ ⟨PROSTOR-KONTROLIRANE-HALUCINACIJE⟩ 3454 : spirala JE kontrolirana, vsaka varianta izmerjena
import json, math
from pathlib import Path
work = Path('/home/user/tool-results/data-analysis/mithos-6003')

BAZA = dict(alpha_c=0.9, beta_c=0.6, gamma_e=0.8, r0=0.5, T_R=40.0,
            gamma_phi=0.2, T=12.0, delta_phi=0.1, o_rate=0.05,
            kappa=0.25, lam=0.35, Theta=0.35)

def simul(K=None, n_steps=600, dt=1.0, zapisuj=False):
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
            Ep = histE[n - 1 - Ti]; Ep2 = histE[n - 1 - 2 * Ti] if n - 1 - 2 * Ti >= 0 else 0.0
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
            katarze.append((n, round(q, 4)))
        histE.append(E)
        if zapisuj and (n % 20 == 0 or n == 1):
            series.append({'dih': n, 'Z': round(Z,4), 'J': round(J,4), 'E': round(E,4), 'N': round(N,4), 'M': round(Z*N,4)})
    per = [b[0]-a[0] for a, b in zip(katarze, katarze[1:])]
    ravn_Z = k['alpha_c'] * ((k['kappa']/k['lam']) / (k['kappa']/k['lam'] + 1)) / k['beta_c']
    return dict(korakov=n_steps, katarze_st=len(katarze),
                prva_katarza=katarze[0][0] if katarze else None,
                perioda=round(sum(per)/len(per), 2) if per else None,
                izpust=round(sum(q for _, q in katarze), 4),
                obrat_ven=round(out_sum, 4),
                koncno={'Z': round(Z,4), 'J': round(J,4), 'E': round(E,4), 'N': round(N,4)},
                Z_analit=round(ravn_Z, 4), N_analit=round(k['kappa']/k['lam'], 4),
                davek_katarze=round((ravn_Z - Z) / ravn_Z * 100, 1) if ravn_Z > 0 else None,
                series=series if zapisuj else None)

# 1. REPLIKA @600 ( priča enakosti z @5993 )
replika = simul(n_steps=600)
# 2. DOLGA PROGA 6000
dolga = simul(n_steps=6000, zapisuj=True)
# 3. PARAMETRIJSKA SPIRALA ( 600 dihov vsaka )
mreza = {}
for ime, Kmreze in {
    'alpha_c': [0.6, 0.9, 1.2],
    'Theta':   [0.2, 0.35, 0.5],
    'kappa':   [0.15, 0.25, 0.35],
    'gamma_phi': [0.1, 0.2, 0.3],
}.items():
    mreza[ime] = {f'{ime}={v}': simul(K={ime: v}) for v in Kmreze}

res = {'rez': 'σ 6003', 'baza': BAZA, 'replika_600': replika, 'dolga_6000': dolga, 'spirala': mreza}
(work / 'rezultati-6003.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
print('REPLIKA 600 ⊢ :', replika['katarze_st'], 'katarz · prva @', replika['prva_katarza'], '· perioda', replika['perioda'], '· koncno', replika['koncno'], '· N*', replika['N_analit'])
print('DOLGA 6000 :', dolga['katarze_st'], 'katarz · perioda', dolga['perioda'], '· koncno', dolga['koncno'], '· davek katarze', dolga['davek_katarze'], '%')
for ime, mm in mreza.items():
    for kk, r in mm.items():
        print(f"SPIRALA {kk}: katarz {r['katarze_st']} · perioda {r['perioda']} · Z {r['koncno']['Z']} · E {r['koncno']['E']} · davek {r['davek_katarze']}%")
import hashlib
print('rezultati-6003.md5', hashlib.md5((work/'rezultati-6003.json').read_bytes()).hexdigest())
