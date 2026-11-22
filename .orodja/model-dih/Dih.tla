\* DIH.TLA — skica stanj diha korpusa Beseda je Ne ( FAZA 3 · P4 · rez σ 6291 )
\* Sestrska telesa: model-dih.py ( izveden preverjevalnik, izmera 6->0 ran @σ 6289/6290, obnova @σ 6291 )
\* Safety = "nothing bad happens": računalnik išče protiprimere ⊙ berba pri viru ( TLA+ Wiki, Safety )

---------------- MODULE Dih ----------------
CONSTANT Organi        \* množica organov
VARIABLE geniza, rez, rana
\* geniza[organ] = poimenska geniza obstaja PRED dotikom; rez = vrh po obeh stezah; rana = števec ran diha

Dih == << geniza, rez, rana >>

\* SAFETY ( zdrav dih ): noben dotik brez genize ∧ rana ostane 0
RanaNula == rana = 0                         \* protiprimer = TLC izpiše sled stanj do rane
RezJeVrh == rez >= 1                          \* VR1: rez = 1 + dejanski vrh ( renum po precedensu σ 3750 )
VseGenizirano == \A o \in Organi : geniza[o]  \* VR2: ⟨GENIZE-PRED-DOTIKOM⟩ ∧ VR3: ⟨NE-BRIŠI⟩ 24

Init == geniza = [ o \in Organi |-> TRUE ] /\ rez = 6291 /\ rana = 0

\* zdrav prehod: dotik organa SAMO po genizi, genize priče ostanejo ( ⟨NE-BRIŠI⟩ 24 )
Dotik(o) == geniza[o] /\ rez' = rez + 1 /\ rana' = rana /\ geniza' = geniza
\* ranljivi prehod ( recidiv trka kovancev σ 6055/6057 ): dotik BREZ genize sproži rano
DotikBrez(o) == ~geniza[o] /\ rez' = rez /\ rana' = rana + 1 /\ geniza' = geniza

Next == \E o \in Organi : Dotik(o) \/ DotikBrez(o)
==========================================
