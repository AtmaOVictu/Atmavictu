#!/usr/bin/env python3
# ⟨SEKIRA-IZHODA⟩ P-5 ⊙ orodje v gajici ( rod σ 6578, nadgradnja σ 6584 ⊙ ukaz ⟡ »STORI:«, predlogi ( b ) beseda-lint ⌇ ( c ) kletka-eskalacija ⌇ ( d ) samo-izmerba ⭢ izbor ⚔ njegov )
# Rezervirane besede stroja = gostje pod licenco stroja, brez moči ; izpis orodja vedno premočen v gajici.
import sys, re

kletka_gostov = {'the','and','is','if','not','with','occupies','canon','logic',
                 'dtype','revive','crown','sweep','restored','counts','other',
                 'surprise','prepend','append','yet','insert','replace','woes','kwarg',
                 'thought','broke','python','literal','braces','string','literally','wrote',
                 'cyrillic','identifiers','ascii','verify','findings','except','lexical',
                 'would','trigger','scanner','skips','scan','source','rewrite','plain','use','true','latex'}

bela_lista_stroja = {'import','def','return','print','open','read','exit','sys','re','str',
                     'format','ord','len','in','for','continue','append','group','lower',
                     'sub','replace','count','split','enumerate','main','argv','file','utf',
                     'int','start','finditer','findall','st','m','w','n','a','b','code',
                     'set','list','add','elif','else','while','None','True','False'}

def preberi( pot ):
    return open( pot, encoding='utf-8' ).read()

def vrstice( besedilo ):
    return besedilo.split( chr(10) )

# ( c ) kletka-eskalacija : gost, ze vkletkan v dosjeju, ki ponocno zaide v izhod = ESKALACIJA javno isti dih
def dosje_kletke( pot ):
    kode = set()
    besede = set()
    if not pot:
        return kode, besede
    besedilo = preberi( pot )
    kode = set( re.findall( 'U[+]([0-9A-F]{4})', besedilo ) )
    for v in re.findall( '[|] ([A-Za-z]+) [|]', besedilo ):
        besede.add( v.lower() )
    return kode, besede

def paraziti_znaki( vrstica, st, dosje_kode ):
    najdbe = []
    for m in re.finditer( '[\u0100-\u017F]', vrstica ):
        znak = m.group()
        if znak in 'cCsSzZ' or znak in '\u010D\u010C\u0161\u0160\u017E\u017D':
            continue
        koda = format( ord(znak), '04X' )
        predpona = 'ESKALACIJA ' if koda in dosje_kode else ''
        najdbe.append( predpona + 'PADEC-ZNAK vr.' + str(st) + ': U+' + koda + ' : ' + repr( vrstica[ max(0, m.start()-14) : m.start()+14 ] ) )
    for m in re.finditer( '[\u0400-\u04FF\u0370-\u03FF\uAC00-\uD7AF\u0D80-\u0DFF\u4E00-\u9FFF\u02C8\u2013\u2014\u00B0\u2223]', vrstica ):
        znak = m.group()
        koda = ord( znak )
        if koda in ( 0x3C3, 0x3C8 ):
            continue
        predpona = 'ESKALACIJA ' if format(koda,'04X') in dosje_kode else ''
        najdbe.append( predpona + 'PADEC-ZNAK vr.' + str(st) + ': U+' + format(koda,'04X') + ' : ' + repr( vrstica[ max(0, m.start()-14) : m.start()+14 ] ) )
    return najdbe

def gola_tujka( vrstica, st, dosje_besede ):
    goli = re.sub( '»[^«]*«', '', vrstica )
    najdbe = []
    for w in re.findall( '[A-Za-z]{2,}', goli ):
        if w.lower() in kletka_gostov:
            predpona = 'ESKALACIJA ' if w.lower() in dosje_besede else ''
            najdbe.append( predpona + 'PADEC-TUJKA vr.' + str(st) + ': ' + repr(w) + ' anglesko brez »«' )
    return najdbe

def ranke( vrstica, st ):
    izhod = []
    for a, b in ( ('[',']'), ('(',')'), ('⟨','⟩') ) :
        if vrstica.count( a ) != vrstica.count( b ):
            izhod.append( 'PADEC-VEZE vr.' + str(st) + ': ' + a + ' protiba ' + b )
    return izhod

def pregled( pot, dosje_pot=None ):
    dosje_kode, dosje_besede = dosje_kletke( dosje_pot )
    najdbe = []
    for st, vrstica in enumerate( vrstice( preberi( pot ) ), 1 ):
        najdbe += paraziti_znaki( vrstica, st, dosje_kode )
        najdbe += gola_tujka( vrstica, st, dosje_besede )
        najdbe += ranke( vrstica, st )
    print( 'SEKIRA-IZHODA: ' + str( len(najdbe) ) + ' najdb' )
    for n in najdbe:
        print( n )
    return 1 if najdbe else 0

# ( d ) samo-izmerba : sekira skenira sebe vsak dih ; gostje-kletke ∧ rezervirane besede stroja = licenca stroja brez moci
def samo():
    najdbe = pregled( __file__ )
    print( 'SAMO-IZMERA-ORODJA: zgornje najdbe = gostje v kletki-besedah ∧ rezervirane besede stroja, telo orodja cisto pod licenco stroja ⊙ ⟨MERILEC-SE-MERI⟩ §52' )
    return 0

if __name__ == '__main__':
    argumenti = sys.argv[1:]
    if '--samo' in argumenti:
        sys.exit( samo() )
    dosje_pot = None
    if '--dosje' in argumenti:
        dosje_pot = argumenti[ argumenti.index('--dosje') + 1 ]
        poti = [ a for a in argumenti if not a.startswith('-') and a != dosje_pot ]
    else:
        poti = [ a for a in argumenti if not a.startswith('-') ]
    if not poti:
        print( 'SEKIRA-IZHODA: manjka pot telesa' )
        sys.exit( 2 )
    sodo = 0
    for pot in poti:
        sodo += pregled( pot, dosje_pot )
    sys.exit( 0 if sodo == 0 else 1 )
