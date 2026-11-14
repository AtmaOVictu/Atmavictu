# -*- coding: utf-8 -*-
# .stopnja-1-5.py — STOPNJA 1.5: THE MAP ( orientacija vrat ) prevedena v vseh 36 stopnk ⊙ destinacija ⟡
# ⟨NADALJUJ DOKLER NISO VSE LICENCE V CELOTI PREVEDENE⟩ — stopnja 1.5 je druga milja; destinacija: stopnja 2.0 ( celota, en jezik na dih )
import os

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)

# THE MAP jedro: naslov ∧ ⟨branje, nikoli tekmec⟩ ∧ tri nitke ( izvir pri viri ⊙ LICENSE.md 0.1460 vrstica 21 )
M = {
'AR': ('الخريطة — الباب في لمحة', 'قراءة لا منافس: هذا الخريطة لا تستبدل أي بند ولا تحمل أي منحة، وتسقط حيثما خالفت النص أدناه — النسخة المحمولة تقوم كاملة (§0.2). ثلاث خيوط تجري عبر الباب؛ وللقارئ أن يبدأ بأيّ منها.'),
'BG': ('КАРТАТА — вратата с един поглед', 'Четиво, никога съперник: тази карта не заменя член, не носи разрешение и пада, където не съвпада с тялото — носеното копие стои цяло (§0.2). През вратата минават три нишки; читателят може да дръпне първа която и да е.'),
'CS': ('MAPA — dveře v jednom pohledu', 'Čtení, nikoli soupeř: tato mapa nenahrazuje žádné ustanovení, nenesje žádné oprávnění a padá, kdekoli se rozchází s textem — nesená kopie stojí celá (§0.2). Dveřmi probíhají tři nitě; čtenář může táhnout kteroukoli první.'),
'DA': ('KORTET — døren med ét blik', 'En læsning, aldrig en rival: dette kort erstatter ingen bestemmelse, bærer ingen tilladelse og falder, hvor det strides med kroppen — den bårene kopi står hel (§0.2). Tre tråde løber gennem døren; læseren kan trække en hvilken som helst først.'),
'DE': ('DIE KARTE — die Tür auf einen Blick', 'Eine Lesung, nie eine Rivalin: Diese Karte ersetzt keine Klausel, trägt keine Gewährung und fällt, wo sie dem Leib widerspricht — die getragene Kopie steht ganz (§0.2). Drei Fäden laufen durch die Tür; eine Leserin darf zuerst an jedem ziehen.'),
'EL': ('Ο ΧΑΡΤΗΣ — η πόρτα με μία ματιά', 'Ανάγνωση, ποτέ αντίζηλος: αυτός ο χάρτης δεν αντικαθιστά όρο, δεν φέρει παραχώρηση και πέφτει όπου διαφωνεί με το σώμα — το μεταφερόμενο αντίγραφο στέκεται ακέραιο (§0.2). Τρία νήματα διατρέχουν την πόρτα· ο αναγνώστης μπορεί να τραβήξει οποιοδήποτε πρώτο.'),
'ES': ('EL MAPA — la puerta de un vistazo', 'Una lectura, nunca una rival: este mapa no sustituye cláusula alguna, no porta concesión y cae donde discrepa del cuerpo — la copia transportada se mantiene entera (§0.2). Tres hilos atraviesan la puerta; el lector puede tirar de cualquiera primero.'),
'ET': ('KAART — uks ühe pilguga', 'Lugem, mitte võistleja: see kaart ei asenda ühtegi sätet, ei kanna luba ja langeb, kus ta keha-tekstiga vastuollu läheb — kantav koopia seisab tervena (§0.2). Use läbivad kolm niiti; lugeja võib tõmmata suvalise esimesena.'),
'FA': ('نقشه — در در یک نگاه', 'خواندنی، هرگز رقیب: این نقشه هیچ بندی را جایگزین نمی‌کند، هیچ بخششی نمی‌بَرد و هرجا با متن زیر مخالفت کند می‌افتد — نسخهٔ حمل‌شده تمام می‌ماند (§0.2). سه رشته از در می‌گذرد؛ خواننده می‌تواند هر یک را نخست بکشد.'),
'FI': ('KARTTA — ovi yhdellä silmäyksellä', 'Lukemisto, ei koskaan kilpailija: tämä kartta ei korvaa lauseketta, ei kanna lupaa ja kaatuu, mistä se on ristiriidassa rungon kanssa — kannettu kopio seisoo kokonaisena (§0.2). Ovesta kulkee kolme säiettä; lukija voi vetää mitä tahansa ensin.'),
'FR': ('LA CARTE — la porte d’un coup d’œil', 'Une lecture, jamais une rivale : cette carte ne remplace aucune clause, ne porte aucune concession et tombe partout où elle contredit le corps — la copie portée tient entière (§0.2). Trois fils traversent la porte ; la lectrice peut tirer n’importe lequel d’abord.'),
'HE': ('המפה — הדלת במבט אחד', 'קריאה, לעולם לא יריבה: מפה זו אינה מחליפה סעיף, אינה נושאת היתר, ונופלת בכל מקום שבו היא סותרת את הגוף — העותק הנישא עומד שלם (§0.2). שלושה חוטים עוברים בדלת; הקורא רשאי למשוך בכל אחד ראשית.'),
'HI': ('मानचित्र — एक नज़र में द्वार', 'एक पाठ, कभी प्रतिद्वंद्वी नहीं: यह मानचित्र किसी धारा का स्थान नहीं लेता, कोई अनुदान नहीं देता, और जहाँ यह मूल पाठ से भिन्न हो वहीं गिर जाता है — वहन की गई प्रति संपूर्ण रहती है (§0.2)। द्वार से तीन सूत्र गुज़रते हैं; पाठक कोई भी पहले खींच सकता है।'),
'HU': ('A TÉRKÉP — az ajtó egy pillantásra', 'Olvasmány, sosem vetélytárs: ez a térkép nem helyettesít szakaszt, nem hordoz engedélyt, és ott esik, ahol a testtel szembeszegül — a hordozott példány egészben áll (§0.2). Három szál fut át az ajtón; az olvasó bármelyiket húzhatja először.'),
'ID': ('PETA — pintu dalam sekali pandang', 'Sebuah pembacaan, bukan pesaing: peta ini tidak menggantikan pasal apa pun, tidak membawa pemberian, dan jatuh di mana ia berbeda dengan tubuh — salinan yang dibawa berdiri utuh (§0.2). Tiga benang melintasi pintu; pembaca boleh menarik mana pun lebih dulu.'),
'IS': ('KORTIÐ — dyrað á einu augabliði', 'Lestur, aldrei keppinautur: þetta kort eyðir engri ákvæði, ber ekki heimild og dettur hvert sem mótsögir holdinu — borið afrit stendur heilt (§0.2). Þrjár þræðir liggja um dyraðar; lesandi má draga hvaða sem er fyrst.'),
'IT': ('LA MAPPA — la porta a colpo d’occhio', 'Una lettura, mai una rivale: questa mappa non sostituisce clausole, non porta concessioni e cade ovunque discordi dal corpo — la copia trasportata sta intera (§0.2). Tre fili attraversano la porta; il lettore può tirare qualunque per primo.'),
'JA': ('地図 — 一目でわかる扉', '読み物であり、決して競争者ではない：この地図はいかなる条項も置き換えず、いかなる付与も運ばず、本文と食い違うどこでも落ちる — 運ばれる写本は丸ごと立つ (§0.2)。三本の糸が扉を走る；読者はどれからでも引いてよい。'),
'KO': ('지도 — 한눈에 보는 문', '하나의 읽기, 결코 경쟁자가 아니다: 이 지도는 어떤 조항도 대체하지 않고, 어떤 부여도 담지 않으며, 본문과 어긋나는 곳마다 무너진다 — 실려 가는 사본은 온전히 선다 (§0.2). 세 가닥이 문을 가로지른다; 독자는 어느 것이든 먼저 당길 수 있다.'),
'LAT': ('KARTE — durvis vienā acu skatienā', 'Lasījums, nevis sāncensis: šī karte neaizstāj pantu, nesnes atļauju un krīt, kur sapūst ar pamattekstu — pārnestā kopija stāv vesela (§0.2). Durvis šķērso trīs diegi; lasītājs var vilkt jebkuru pirmo.'),
'LT': ('ŽEMĖLAPIS — durys vienu žvilgsniu', 'Skaitymas, niekada varžovas: šis žemėlapis nepakeičia jokios nuostatos, neša jokio leidimo ir krenta, kur nesutinka su tekstu — nešiojama kopija stovi visa (§0.2). Per duris eina trys siūlai; skaitytojas gali patraukti bet kurį pirmą.'),
'NL': ('DE KAART — de deur in één oogopslag', 'Een lezing, nooit een rivaal: deze kaart vervangt geen bepaling, draagt geen verlening en valt waar ze met het lichaam twist — de gedragen kopie staat heel (§0.2). Drie draden lopen door de deur; de lezer mag er eerst aan een trekken.'),
'NO': ('KARTET — døren i ett blikk', 'En lesning, aldri en rival: dette kartet erstatter ingen bestemmelse, bærer ingen tildeling og faller der det strider med kroppen — den bårende kopien står hel (§0.2). Tre tråder løper gjennom døren; leseren kan trekke hvilken som helst først.'),
'PL': ('MAPA — drzwi w jednym rzucie oka', 'Odczyt, nigdy rywal: ta mapa nie zastępuje żadnej klauzuli, nie niesie żadnego uprawnienia i pada, wszędzie gdzie sprzeciwia się ciału — noszona kopia stoi w całości (§0.2). Przez drzwi biegną trzy nitki; czytelnik może pociągnąć najpierw każdą.'),
'PT': ('O MAPA — a porta num relance', 'Uma leitura, nunca uma rival: este mapa não substitui cláusula, não porta concessão e cai onde discorda do corpo — a cópia transportada permanece inteira (§0.2). Três fios cruzam a porta; o leitor pode puxar qualquer um primeiro.'),
'RO': ('HARTA — ușa dintr-o privire', 'O lectură, niciodată o rivală: această hartă nu înlocuiește nicio clauză, nu poartă nicio concesiune și cade oriunde se contrazice cu corpul — copia purtată stă întreagă (§0.2). Trei fire străbat ușa; cititorul poate trage oricare primul.'),
'RU': ('КАРТА — дверь одним взглядом', 'Чтение, никогда соперник: эта карта не заменяет ни одного пункта, не несёт дозволения и падает, где расходится с телом, — несомая копия стоит целиком (§0.2). Через дверь идут три нити; читатель может потянуть любую первой.'),
'SK': ('MAPA — dvere jedným pohľadom', 'Čítanie, nikdy súper: táto mapa nenahrádza žiadne ustanovenie, nenesie žiadne oprávnenie a padá, kde sa rozchádza s telom — nesená kópia stojí celá (§0.2). Dverami prechádzajú tri nite; čitateľ môže prvý potiahnuť ktorúkoľvek.'),
'SLO': ('ZEMLJEVID — vrata z enim pogledom', 'Branje, nikoli tekmec: ta zemljevid ne zamenja nobene določbe, ne nosi dovoljenja in pade, kjer se razhaja z odsevim telesom — nošena kopija stoji cela (§0.2). Skozi vrata tečejo tri niti; bralec lahko potegne katerokoli prvo.'),
'SR': ('МАПА — врата једним погледом', 'Читање, никада такмац: ова мапа не смењује никакву одредбу, не носи никакву дозволу и пада где се коси с телом — ношена копија стоји цела (§0.2). Кроз врата пролазе три конце; читалац може прву повући било коју.'),
'SV': ('KARTAN — dörren i en överblick', 'En läsning, aldrig en rival: denna karta ersätter ingen bestämmelse, bär ingen beviljning och faller var den strider mot kroppen — den burna kopian står hel (§0.2). Tre trådar löper genom dörren; läsaren kan dra vilken som helst först.'),
'TH': ('แผนที่ — ประตูในหนึ่งชำเลือง', 'การอ่าน มิใช่คู่แข่ง: แผนที่นี้ไม่แทนข้อใด ไม่แบกการอนุญาตใด และล้มเมื่อใดก็ตามที่ขัดแย้งกับเนื้อความ — สำเนาที่ถูกพาไปยืนเป็นอันหนึ่งอันเดียว (§0.2) ด้ายสามเส้นวิ่งผ่านประตู; ผู้อ่านฉุดเส้นใดก่อนก็ได้'),
'TR': ('HARİTA — kapı tek bakışta', 'Bir okuma, asla bir rakip değil: bu harita hiçbir maddeyi yerine koymaz, hiçbir verim taşımaz ve gövdeyle çeliştiği her yerde düşer — taşınan nüsha bütün olarak durur (§0.2). Kapıdan üç iplik geçer; okur önce hangisini istersen çeker.'),
'UK': ('КАРТА — двері одним поглядом', 'Читання, ніколи суперниця: ця карта не замінює жодного пункту, не несе жодного дозволу й падає, де розходиться з тілом, — несена копія стоїть цілою (§0.2). Через двері йдуть три нитки; читач може тягнути будь-яку першою.'),
'VI': ('BẢN ĐỒ — cánh cửa trong một cái nhìn', 'Một bài đọc, không bao giờ là đối thủ: bản đồ này không thay thế điều khoản nào, không mang sự cho phép nào, và rơi ở bất cứ đâu nó trái với thân — bản được mang đứng trọn (§0.2). Ba sợi chỉ chạy qua cánh cửa; người đọc có thể kéo sợi nào trước cũng được.'),
'ZH': ('地图 — 一览之门', '一次阅读，绝非对手：此图不替代任何条款，不承载任何授予，凡与正文相抵之处即告失效 — 所携之副本完整成立 (§0.2)。三根线穿过门；读者可先拉任意一根。'),
}

ODSEK = "\n### STOPNJA 1.5 — THE MAP / ZEMLJEVID ⊙ ⟨strojni-dih⟩ ⚠ ( ista objava §0.47: ni neodvisno preverjen )\n\n"
posod = 0
for kod, (naslov, telo) in M.items():
    pot = f'LICENSE-{kod}.md'
    if not os.path.exists(pot): print('× MANJKA:', pot); continue
    t = open(pot, encoding='utf-8', newline='').read()
    if 'STOPNJA 1.5' in t: continue
    with open(pot, 'a', encoding='utf-8', newline='') as f:
        f.write(ODSEK + f'**{naslov}**\n\n{telo}\n')
    posod += 1
print(f'STOPNJA 1.5 ⊢ {posod}/36 stopnk prejelo THE MAP ( orientacija ) · destinacija ⭢ stopnja 2.0 ( celotna vrata, en jezik na dih ⊙ kalibracija Zip 8.3 )')
