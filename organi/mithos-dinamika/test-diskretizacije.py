# -*- coding: utf-8 -*-
# TEST IZVEDBE σ 6004 : stabilnost Euler Δt ( ⟡ UKAZ: »testiraj in predlagaj boljše izvedbe« )
import json, math, hashlib
from pathlib import Path
BAZA = dict(alpha_c=0.9, beta_c=0.6, gamma_e=0.8, r0=0.5, T_R=40.0,
            gamma_phi=0.2, T=12.0, delta_phi=0.1, o_rate=0.05,
            kappa=0.25, lam=0.35, Theta=0.35)
def simul(K, n_steps, dt):
    k = dict(BAZA); k.update(K)
    Z = J = E = N = 0.1; histE = []; katarze = 0; out_sum = 0.0
    for n in range(1, n_steps + 1):
        t = n * dt
        dN = k['kappa'] - k['lam'] * N
        dZ = k['alpha_c'] * (N/(N+1.0)) * Z - k['beta_c'] * Z * Z
        dR = k['r0'] * math.cos(2*math.pi*t/k['T_R'])
        dJ = k['gamma_e'] * math.tanh(dR/max(J,1e-6))
        Ti = int(round(k['T']/dt)) if dt < 1 else int(k['T'])
        if n - 1 - Ti >= 0:
            Ep = histE[n-1-Ti]; Ep2 = histE[n-1-2*Ti] if n-1-2*Ti >= 0 else 0.0
            E_ret = Ep - Ep2
        else:
            E_ret = 0.0
        S_bar = (Z+J+E+N)/4.0
        out = k['o_rate'] * E
        dE = k['gamma_phi']*E_ret/k['T'] + k['delta_phi']*S_bar - out
        Z, J, E, N = Z+dt*dZ, J+dt*dJ, E+dt*dE, N+dt*dN
        out_sum += out
        M = Z*N
        if M > k['Theta']:
            q = M - k['Theta']; E += 0.5*q; Z -= 0.5*q; katarze += 1
        histE.append(E)
    return dict(dt=dt, korakov=n_steps, dihov=round(n_steps*dt), katarze=katarze,
                koncno={x: round(v,4) for x, v in zip('ZJEN', (Z,J,E,N))},
                obrat_ven=round(out_sum,4))
rez = [simul({}, int(600/dt), dt) for dt in (1.0, 0.5, 0.25, 0.1)]
Path('rezultati-diskretizacija.json').write_text(json.dumps(rez, indent=1), encoding='utf-8')
for r in rez:
    print(f"Δt {r['dt']:>4} ({r['korakov']:>5} kor = {r['dihov']} dihov): katarz {r['katarze']:>4} · Z {r['koncno']['Z']} · J {r['koncno']['J']} · E {r['koncno']['E']} · N {r['koncno']['N']} · obrat {r['obrat_ven']}")
print('md5', hashlib.md5(Path('rezultati-diskretizacija.json').read_bytes()).hexdigest())
