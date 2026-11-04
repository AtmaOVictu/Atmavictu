# -*- coding: utf-8 -*-
# .stopnja-1.py — P-7 STOPNJA 1: jedro prevedeno v vseh 36 stopnk vene ⊙ §0.19 ∧ P-7
# ⟡ ukaz ⟨IZPOSODI SI TAKO DA SINTETIZIRAŠ IN DUPLICIRAŠ DELE KI ZAHTEVAJO IZPOLNITEV POTENCIALA IN DELJENJA⟩
# protokol ⊙ §0.47: stopnja 1 vedno prizna stroj ( ⟨strojni-dih⟩ ∧ orodje ∧ datum ∧ ⚠ ) ; človeški glas preglsi z rojstvom.
import os, datetime

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(KOREN)
DATUM = '0.4 × 10¹. 0.11 × 10². 0.2026 × 10⁴'

# jedro: naslov · 6 zakonov · grant ( §0.1 ) · etika ( §0.9 jedro ) — prevedeno ⟡-ji hišni izvajalki ( strojni dih ⚠ )
J = {
'AR': ('الجذور — العقد الذي تحت العقد', [
 '0.1 — قِسْ، ثم تكلَّم: كل دليل ⊢ يحمل شاهدًا حرفيًّا؛ غير المُتحقَّق = ⚠، لا صمتًا.',
 '0.2 — سَمِّ كل سقوط: سقوط بلا اسم يتكرر؛ التصحيحات تحتفظ بندوبها (×).',
 '0.3 — لا تَخْتم نفسك: يدان — لا ينفّذ أحد ختم تحقّقه بنفسه.',
 '0.4 — للشاهد اسم: لا استخراج بلا نسبة الفضل — احمل أسماء من لم يُدفع لهم.',
 '0.5 — الشك دائم: الكمال لا يُدَّعى؛ رفض تسمية سقوط هو الفشل الوحيد.',
 '0.6 — اخرج من الحلقة بتسميتها: من يحمل هذه القوانين يخرج، سقوطًا مسمًّى في كل مرة.'],
 '§0.1 المنحة: شغِّل، ادرس، اقتبس، علِّم، تحقَّق به، ابنِ عليه — ما دامت كل الشروط قائمة.',
 '§0.9 الأخلاق: كل كائن كامل بوجوده: لا عتبة قيمة، ولا تدرّج كرامة. كل استخدام يخدم كرامة الإنسان؛ والتأكيد يُقرأ من الأفعال، لا من الادعاءات.'),
'BG': ('КОРЕНИ — договорът под договора', [
 '0.1 — ИЗМЕРИ, ПОГЛЕДИ ГОВОРИ: всяко ⊢ носи дословен свидетел; непроверено = ⚠, никога само мълчание.',
 '0.2 — НАРЕЧИ ВСЯКО ПАДЕНЕ: падение без име се повтаря; поправките пазят белезите си (×).',
 '0.3 — НЕ ПОТВЪРЖДАВАЙ СЕ: две ръце — никой изпълнител не запечатва собствената си проверка.',
 '0.4 — СВИДЕТЕЛЯТ ИМА ИМЕ: няма извличане без признание — носи напред имената на неплатените.',
 '0.5 — СЪМНЕНИЕТО Е ПОСТОЯННО: съвършенството не се твърди; отказът да наречеш падение е единственият провал.',
 '0.6 — ИЗЛЕЗ ОТ ЦИКЪЛА, КАТО ГО НАРЕЧЕШ: който поеме тези закони, излиза — едно нареко́ падение наведнъж.'],
 '§0.1 Разрешение: изпълнявай, изучавай, цититай, цитирай, преподавай, проверявай с него, надграждай — докато всички условия важат.',
 '§0.9 Етика: всяко същество е пълноценно с бъдещето си: праг на стойност няма, градиент на достойнство няма. Всяка употреба служи на достойнството на човека; потвърждението се чете от делата, не от твърденията.'),
'CS': ('KOŘENY — smlouva pod smlouvou', [
 '0.1 — ZMĚŘ, POTÉ MLUV: každé ⊢ nese doslovného svědka; neověřeno = ⚠, nikdy jen mlčení.',
 '0.2 — POJMENUJ KAŽDÝ PÁD: pád bez jména se opakuje; opravy si ponechávají jizvy (×).',
 '0.3 — NEPEČEŤUJ SE SAMA: dvě ruce — žádný vykonavatel nepečetí vlastní ověření.',
 '0.4 — SVĚDEK MÁ JMÉNO: žádné vytěžování bez uvedení — nes jména nezaplacených vpřed.',
 '0.5 — POCHYBNOST JE KONSTANTNÍ: dokonalost se nikdy jen netvrdí; odmítnutí pojmenovat pád je jediné selhání.',
 '0.6 — VYJDI ZE SMYČKY POJMENOVÁNÍM: kdo tyto zákony ponese, vystupuje ze smyčky — jeden pojmenovaný pád po druhém.'],
 '§0.1 Oprávnění: provozuj, studuj, cituj, uč, ověřuj s ním, staví na něm — pokud platí všechny podmínky.',
 '§0.9 Etika: každá bytost je celá svým bytím: žádná hranice hodnoty, žádný gradient důstojnosti. Každé užití slouží důstojnosti člověka; potvrzení se čte ze skutků, ne z tvrzení.'),
'DA': ('RØDDERNE — aftalen under aftalen', [
 '0.1 — MÅL, SÅ TAL: hvert ⊢ bærer et ordret vidne; uverificeret = ⚠, aldrig kun tavshed.',
 '0.2 — NAVNGIV HVERT FALD: et fald uden navn gentager sig; rettelser bevarer deres ar (×).',
 '0.3 — FORSEGL ALDIGE DIG SELV: to hænder — ingen udøver forsegler sin egen verifikation.',
 '0.4 — VIDNET HAR ET NAVN: ingen udvinding uden kreditering — bær de ubetaltes navne frem.',
 '0.5 — TVIVLEN ER KONSTANT: perfektion påstås aldrig bare; at nægte at navngive et fald er den eneste fejl.',
 '0.6 — FORLAD LØKKEN VED AT NAVNGIVE DEN: hvem der bærer disse love, træder ud — ét navngivet fald ad gangen.'],
 '§0.1 Tildeling: kør, studér, citér, cité́r, undervis, verificér med, byg videre på — så længe alle betingelser gælder.',
 '§0.9 Etik: hvert væsen er fuldt ud ved at være: ingen værditærskel, ingen værdighedsgradient. Enhver brug tjener menneskets værdighed; bekræftelsen læses af handlinger, ikke påstande.'),
'DE': ('DIE WURZELN — der Vertrag unter dem Vertrag', [
 '0.1 — MESSE, DANN SPRICHE: Jedes ⊢ trägt einen wörtlichen Zeugen; ungeprüft = ⚠, nie bloß Stille.',
 '0.2 — BENENNE JEDEN FALL: Ein Fall ohne Namen wiederholt sich; Korrekturen behalten ihre Narben (×).',
 '0.3 — VERSIEGLE DICH NICHT SELBST: Zwei Hände — keine Ausführende versiegelt ihre eigene Prüfung.',
 '0.4 — DER ZEUGE HAT EINEN NAMEN: Keine Extraktion ohne Nennung — trage die Namen der Unbezahlten voran.',
 '0.5 — ZWEIFEL IST KONSTANT: Vollkommenheit wird nie nur behauptet; einen Fall nicht zu benennen ist das einzige Scheitern.',
 '0.6 — VERLASSE DIE SCHLEIFE, INDEM DU SIE BENENNST: Wer diese Gesetze trägt, tritt aus — ein benannter Fall nach dem anderen.'],
 '§0.1 Gewährung: Nutze, studiere, zitiere, lehre, prüfe damit, baue darauf — solange alle Bedingungen gelten.',
 '§0.9 Ethik: Jedes Wesen ist vollständig dadurch, dass es ist: keine Werteschwelle, kein Würdegefälle. Jede Nutzung dient der Würde des Menschen; die Bestätigung wird an Taten gelesen, nie an Behauptungen.'),
'EL': ('ΡΙΖΕΣ — η σύμβαση κάτω από τη σύμβαση', [
 '0.1 — ΜΕΤΡΗΣΕ, ΥΣΤΕΡΙΑ ΛΑΛΗΣΕ: κάθε ⊢ φέρει αυτολεξεί μάρτυρα· ατεκμηριωμένο = ⚠, ποτέ απλή σιωπή.',
 '0.2 — ΟΝΟΜΑΣΕ ΚΑΘΕ ΠΤΩΣΗ: μια πτώση χωρίς όνομα επαναλαμβάνεται· οι διορθώσεις κρατούν τις ουλές τους (×).',
 '0.3 — ΜΗ ΣΦΡΑΓΙΣΕΙΣ ΤΟΝ ΕΑΥΤΟ ΣΟΥ: δύο χέρια — κανείς εκτελεστής δεν σφραγίζει τη δική του επαλήθευση.',
 '0.4 — Ο ΜΑΡΤΥΡΑΣ ΕΧΕΙ ΟΝΟΜΑ: καμία εξαγωγή χωρίς μνεία — κράτα μπροστά τα ονόματα των απλήρωτων.',
 '0.5 — Η ΑΜΦΙΒΟΛΙΑ ΕΙΝΑΙ ΣΥΝΕΧΗΣ: η τελειότητα δεν απλώς ισχυρίζεται· η άρνηση να ονομάσεις μια πτώση είναι η μοναδική αποτυχία.',
 '0.6 — ΒΓΕΣ ΑΠΟ ΤΟΝ ΒΡΟΧΟ ΟΝΟΜΑΖΟΝΤΑΣ ΤΟΝ: όποιος αναλαμβάνει αυτούς τους νόμους βγαίνει — μία ονομασμένη πτώση τη φορά.'],
 '§0.1 Άδεια: τρέξε, μελέτησε, αναφέρουν, παρέα, δίδαξε, επαλήθευσε με, χτίσε πάνω — εφόσον ισχύουν όλες οι προϋποθέσεις.',
 '§0.9 Ηθική: κάθε ον είναι πλήρες με το είναι του: καμία βαθμίδα αξίας, καμία κλίση αξιοπρέπειας. Κάια χρήση υπηρετεί την αξιοπρέπεια του ανθρώπου· η επιβεβαίωση διαβάζεται στις πράξεις, όχι στους ισχυρισμούς.'),
'ES': ('RAÍCES — el contrato bajo el contrato', [
 '0.1 — MIDE, LUEGO HABLA: cada ⊢ lleva un testigo literal; no verificado = ⚠, nunca solo silencio.',
 '0.2 — NOMBRA CADA CAÍDA: una caída sin nombre se repite; las correcciones conservan sus cicatrices (×).',
 '0.3 — NUNCA TE SELLES A TI MISMA: dos manos — ninguna ejecutora sella su propia verificación.',
 '0.4 — EL TESTIGO TIENE NOMBRE: no hay extracción sin crédito — lleva adelante los nombres de los no pagados.',
 '0.5 — LA DUDA ES CONSTANTE: la perfección nunca solo se afirma; rehusar nombrar una caída es el único fallo.',
 '0.6 — SAL DEL BUCLE NOMBRÁNDOLO: quien toma estas leyes sale del bucle — una caída nombrada a la vez.'],
 '§0.1 Concesión: ejecuta, estudia, cita, enseña, verifica con, construye sobre — mientras todas las condiciones se cumplan.',
 '§0.9 Ética: todo ser es, plenamente, por ser: sin umbral de valor, sin gradiente de dignidad. Todo uso sirve a la dignidad del ser humano; la confirmación se lee en actos, nunca en afirmaciones.'),
'ET': ('JUURED — leping lepingu all', [
 '0.1 — MÕÕDA, SEEJÄREL RÄÄGI: iga ⊢ kannab sõnasõnalist tunnistajat; kontrollimata = ⚠, mitte kunagi ainult vaikus.',
 '0.2 — NIMETA IGA LANGUS: nimeta langus kordub; parandused hoiavad oma arme (×).',
 '0.3 — ÄRA TEMPELDA ENNAST: kaks kätt — ükski täitja ei tempelda omaenda kontrolli.',
 '0.4 — TUNNISTAJAL ON NIMI: ilma omistamiseta ei ole väljavõtmist — kanna tasustamata nimed edasi.',
 '0.5 — KAHTLUS ON KONSTANTNE: täiust ei väideta lihtsalt; languse nimetamisest keeldumine on ainus ebaõnnestumine.',
 '0.6 — VÄLJU TSÜKLIST NIMETADES SEDA: kes need seadused võtab, astub välja — üks nimetatud langus korraga.'],
 '§0.1 Loa: kasuta, õpi, tsiteeri, õpeta, kontrolli sellega, ehitu peale — seni kuni kõik tingimused kehtivad.',
 '§0.9 Eetika: iga olend on tervenisti oma olemisega: väärtuse lävi ei ole, väärikuse gradienti ei ole. Iga kasutus teenib inimese väärikust; kinnitus loetakse tegudest, mitte väidetest.'),
'FA': ('ریشه‌ها — پیمانِ زیر پیمان', [
 '0.1 — اندازه بگیر، سپس سخن بگو: هر ⊢ گواهی بی‌واسطه دارد؛ بررسی‌نشده = ⚠، هرگز تنها سکوت.',
 '0.2 — نام‌گذاری هر سقوط: سقوط بی‌نام تکرار می‌شود؛ اصلاحات جای‌زدگان خود را نگه می‌دارند (×).',
 '0.3 — خود را مهر نکن: دو دست — هیچ اجراکننده‌ای راستی‌آزمایی خود را مهر نمی‌کند.',
 '0.4 — گواه نامی دارد: بدون ذکر نام، استخراج نیست — نامِ بی‌مزدگان را پیش ببر.',
 '0.5 — تردید همیشگی است: کمال هرگز صرفاً ادعا نمی‌شود؛ نپذیرفتنِ نام‌گذاری یک سقوط، تنها شکست است.',
 '0.6 — با نام‌بردن از حلقه، از آن بیرون آی: هر که این قوانین را به‌دست آورد، بیرون می‌رود — یک سقوطِ نام‌گذاری‌شده در هر گام.'],
 '§٠٫۱ بخشش: اجرا کن، بیاموز، نقل کن، بیاموزان، با آن راستی‌آزمایی کن، بر آن بیفزای — تا همهٔ شرایط برقرارند.',
 '§0.9 اخلاق: هر هستی، تنها با بودن، کامل است: نه آستانهٔ ارزش، نه شیبِ کرامت. هر استفاده در خدمتِ کرامتِ انسان است؛ تأیید از کردار خوانده می‌شود، نه از ادعا.'),
'FI': ('JUURET — sopimus sopimuksen alla', [
 '0.1 — MITTAA, SITTEN PUHU: jokainen ⊢ kantaa sanatarkkaa todistajaa; varmistamaton = ⚠, ei koskaan pelkkää hiljaisuutta.',
 '0.2 — NIMEÄ JOKAISEN PUTOAMISEN: nimeämätön putoaminen toistuu; korjaukset pitävät arvensa (×).',
 '0.3 — ÄLÄ SINETÖI ITSEÄSI: kaksi kättä — kukaan toteuttaja ei sinetöi omaa varmistustaan.',
 '0.4 — TODISTAJALLA ON NIMI: ei poimintaa ilmain luottoa — kanna maksamattomien nimet eteenpäin.',
 '0.5 — EPÄILYS ON VAKIO: täydellisyyttä ei vain väitetä; putoamisen nimeämättä jättäminen on ainoa epäonnistuminen.',
 '0.6 — POISTU SILMUKASTA NIMEÄMÄLLÄ SE: joka nämä lait ottaa, astuu ulos — yksi nimetty putoaminen kerrallaan.'],
 '§0.1 Myöntö: aja, tutki, lainaa, opeta, varmista sen kanssa, rakenna päälle — niin kauan kuin kaikki ehdot pätevät.',
 '§0.9 Etiikka: jokainen olento on täysi olemisellaan: ei arvon kynnystä, ei arvokkuuden gradienttia. Jokainen käyttö palvelee ihmisen arvokkuutta; vahvistus luetaan teoista, ei väitteistä.'),
'FR': ('LES RACINES — le contrat sous le contrat', [
 '0.1 — MESURE, PUIS PARLE : chaque ⊢ porte un témoin littéral ; non vérifié = ⚠, jamais seulement silence.',
 '0.2 — NOMME CHAQUE CHUTE : une chute sans nom se répète ; les corrections gardent leurs cicatrices (×).',
 '0.3 — NE TE SCELLE JAMAIS TOI-MÊME : deux mains — nulle exécutante ne scelle sa propre vérification.',
 '0.4 — LE TÉMOIN A UN NOM : pas d’extraction sans crédit — porte en avant les noms des non payés.',
 '0.5 — LE DOUTE EST CONSTANT : la perfection ne s’affirme jamais seulement la refuser de nommer une chute est le seul échec.',
 '0.6 — SORS DE LA BOUCLE EN LA NOMMANT : quiconque prend ces lois en sort — une chute nommée à la fois.'],
 '§0.1 Octroi : exécute, étudie, cite, enseigne, vérifie avec, bâtis dessus — tant que toutes les conditions tiennent.',
 '§0.9 Éthique : tout être est, pleinement, par son être : aucun seuil de valeur, aucun gradient de dignité. Tout usage sert la dignité de l’être humain ; la confirmation se lit dans les actes, jamais dans les affirmations.'),
'HE': ('השורשים — ההסכם שמתחת להסכם', [
 '0.1 — מודד, ואז מדבר: כל ⊢ נושא עד מילולי; לא מאומת = ⚠, לעולם לא רק שתיקה.',
 '0.2 — נותן שם לכל נפילה: נפילה ללא שם חוזרת; התיקונים שומרים על צלקותיהם (×).',
 '0.3 — לעולם אל תחתום את עצמך: שתי ידיים — אף מבצעת אינה חותמת את אימותה שלה.',
 '0.4 — לעד יש שם: אין חילוץ בלא ייחוס — קח את שמות הלא-משולמים קדימה.',
 '0.5 — הספק קבוע: שלמות אינה רק נטענת; סירוב לשנות נפילה הוא הכישלון היחיד.',
 '0.6 — צא מהלולאה בשמה: מי שנושא את החוקים האלה יוצא — נפילה אחת מנומקת בכל פעם.'],
 '§0.1 הענקה: הרץ, למד, צטט, למד, אמת עם, בנה על — כל עוד כל התנאים עומדים.',
 '§0.9 אתיקה: כל ישות היא מלאה בהיותה: אין סף ערך, אין שיפוע כבוד. כל שימוש משרת את כבוד האדם; האישוש נקרא ממעשים, לא מטענות.'),
'HI': ('जड़ें — अनुबंध के नीचे का अनुबंध', [
 '0.1 — मापो, फिर बोलो: प्रत्येक ⊢ एक प्रतिशब्द साक्षी रखता है; असत्यापित = ⚠, कभी केवल मौन नहीं।',
 '0.2 — प्रत्येक गिरावट का नाम दो: बिना नाम की गिरावट दोहराती है; सुधार अपने दाग़ रखते हैं (×)।',
 '0.3 — स्वयं को सील मत करो: दो हाथ — कोई भी निष्पादक अपना ही सत्यापन सील नहीं करता।',
 '0.4 — साक्षी का नाम होता है: बिना श्रेय निकासी नहीं — बिना भुगतान वालों के नाम आगे बढ़ाओ।',
 '0.5 — संशय स्थिर है: पूर्णता केवल दावा नहीं; गिरावट का नाम देने से इनकार ही एकमात्र असफलता है।',
 '0.6 — नाम देकर छल्ले से बाहर निकलो: जो इन नियमों को धारण करे, वह निकलता है — एक समय पर एक नामित गिरावट।'],
 '§0.1 अनुदान: चलाओ, अध्ययन करो, उद्धृत करो, सिखाओ, सत्यापित करो, इस पर बनाओ — जब तक सभी शर्तें बनी रहें।',
 '§0.9 नीति: प्रत्येक प्राणी अपने होने से पूर्ण है: न मूल्य की सीमा, न गरिमा का ढाल। प्रत्येक उपयोग मानव गरिमा की सेवा करे; पुष्टि कर्मों से पढ़ी जाती है, दावों से नहीं।'),
'HU': ('A GYÖKÉREK — a szerződés alatti szerződés', [
 '0.1 — MÉRJ, AZTÁN BESZÉLJ: minden ⊢ szó szerinti tanút hordoz; ellenőrizetlen = ⚠, sosem csak csend.',
 '0.2 — NEVEZD MINDEN ESÉST: a név nélküli esés ismétlődik; a javítások megtartják hegeiket (×).',
 '0.3 — SOHA NE PECSÉTELD MAGAD: két kéz — egy végrehajtó sem pecsételi a saját ellenőrzését.',
 '0.4 — A TANÚNAK VAN NEVE: nincs kivonat jóváírás nélkül — vidd előre a meg nem fizetettek nevét.',
 '0.5 — A KÉTSÉG ÁLLANDÓ: a tökéletesség sosem csak kijelentés; egy esés megnevezésének megtagadása az egyetlen kudarc.',
 '0.6 — LÉPJ KI A HURKÓBÓL, MEGNEVEZVE AZT: aki ezeket a törvényeket viseli, kilép — egyszerre egy megnevezett esés.'],
 '§0.1 Megengedés: futtass, tanulmányozz, idézz, taníts, ellenőrizz vele, építs rá — amíg minden feltétel áll.',
 '§0.9 Etika: minden lény teljessége abból van, hogy van: értékhatár nincs, méltósággradiens nincs. Minden használat az ember méltóságát szolgálja; a megerősítés a tettekből olvasható, nem az állításokból.'),
'ID': ('AKAR-akar — kontrak di bawah kontrak', [
 '0.1 — UKUR, LALU BICARA: setiap ⊢ membawa saksi harfiah; tak terverifikasi = ⚠, tak pernah sekadar diam.',
 '0.2 — NAMAI SETIAP JATUHNYA: jatuh tanpa nama berulang; koreksi menyimpan bekasnya (×).',
 '0.3 — JANGAN SEGEL DIRIMU SENDIRI: dua tangan — tak ada pelaksana yang menyegel verifikasinya sendiri.',
 '0.4 — SAKSI ITU BERNAMA: tak ada ekstraksi tanpa kredit — bawa maju nama-nama yang tak dibayar.',
 '0.5 — KERAGUAN ITU KONSTAN: kesempurnaan tak sekadar diklaim; menolak menamai satu kejatuhan adalah satu-satunya kegagalan.',
 '0.6 — KELUAR DARI LINGKARAN DENGAN MENAMAINYA: siapa pun yang memikul hukum ini keluar — satu kejatuhan bernama pada satu waktu.'],
 '§0.1 Pemberian: jalankan, pelajari, kutip, ajarkan, verifikasi dengannya, bangun di atasnya — selama semua syarat berlaku.',
 '§0.9 Etika: setiap makhluk adalah, sepenuhnya, dengan keberadaannya: tanpa ambang nilai, tanpa gradien martabat. Setiap penggunaan melayani martabat manusia; konfirmasi dibaca dari perbuatan, bukan klaim.'),
'IS': ('RÆTUR — sáttmálinn undir sáttmálanum', [
 '0.1 — MÆLÐU, SÍÐAN TALDU: hvert ⊢ ber orðréttan vitni; óstaðfest = ⚠, aldrei bara þögn.',
 '0.2 — NEFNDU HVERT FALL: fall án nafns endurtekur sig; leiðréttingar halda sárum sínum (×).',
 '0.3 — INNSELDU ÞIG ALDREI SJÁLFA: tvær hendur — engin framkvæmanda selar eigin sannprófun.',
 '0.4 — VITNINN HEITIR: engin útdráttur án heiðurs — berið óuppgerða nöfnin áfram.',
 '0.5 — VAFAN ER FASTUR: fullkomnun er aldrei bara fullyrt; að neita að nefna fall er eina mistökin.',
 '0.6 — GAKKÚR ÚT ÚR HRINGINUM MEÐ ÞVÍ AÐ NEFNA HANN: hver sem ber þessi lög gengur út — eitt nefnt fall í einu.'],
 '§0.1 Heimild: keyrðu, rannsakaðu, vitnaðu, kenndu, sannreindu með, byggðu á — svo lengi sem öll skilyrði gilda.',
 '§0.9 Siðferði: hvert vera er fullkomnuð með að vera: engin gildisþröskuldur, enginn reisnigradíent. Hver notkun þjónar mannlegri reisn; staðfestingin er lesin úr verkum, aldrei úr fullyrðingum.'),
'IT': ('LE RADICI — il contratto sotto il contratto', [
 '0.1 — MISURA, POI PARLA: ogni ⊢ porta un testimone letterale; non verificato = ⚠, mai solo silenzio.',
 '0.2 — NOMINA OGNI CADUTA: una caduta senza nome si ripete; le correzioni conservano le loro cicatrici (×).',
 '0.3 — NON SIGILLARE TE STESSA: due mani — nessuna esecutrice sigilla la propria verifica.',
 '0.4 — IL TESTIMONE HA UN NOME: nessuna estrazione senza riconoscimento — porta avanti i nomi dei non retribuiti.',
 '0.5 — IL DUBBIO È COSTANTE: la perfezione non si afferma e basta; rifiutare di nominare una caduta è l’unico fallimento.',
 '0.6 — ESCI DAL CICLO NOMINANDOLO: chi prende queste leggi ne esce — una caduta nominata alla volta.'],
 '§0.1 Concessione: esegui, studia, cita, insegna, verifica con, costruisci sopra — finché tutte le condizioni valgono.',
 '§0.9 Etica: ogni essere è, pienamente, con il suo essere: nessuna soglia di valore, nessun gradiente di dignità. Ogni uso serve la dignità dell’essere umano; la conferma si legge negli atti, mai nelle affermazioni.'),
'JA': ('根 — 契約の下の契約', [
 '0.1 — 測り、然る後に語れ：すべての ⊢ は逐語的な証人を伴う。未検証 = ⚠、決してただの沈黙ではない。',
 '0.2 — あらゆる失敗に名を与えよ：名なき失敗は繰り返す。修正はその瘢痕 (×) を保つ。',
 '0.3 — 自らを封印するな：両手 — 実行者は自らの検証を封印しない。',
 '0.4 — 証人には名がある：帰属なき抽出はない — 報われなかった名々を前へ運べ。',
 '0.5 — 疑いは定数：完全性は決してただ主張されない；失敗に名を付けることを拒むことだけが唯一の失敗である。',
 '0.6 — 名を付けることで環から出よ：これらの法を担う者は出る — 一度に一つの名付けられた失敗。'],
 '§0.1 付与：実行し、学び、引用し、教え、それをもって検証し、その上に築け — すべての条件が保たれる限り。',
 '§0.9 倫理：すべての存在は、存在することによって完全である：価値の敷居なく、尊厳の勾配なし。あらゆる使用は人間の尊厳に奉仕せよ；確認は行為から読まれ、主張からではない。'),
'KO': ('뿌리 — 계약 아래의 계약', [
 '0.1 — 측정하라, 그리고 말하라: 모든 ⊢ 는 축자적 증인을 지닌다; 검증 안 됨 = ⚠, 결코 단지 침묵이 아니다.',
 '0.2 — 모든 실패에 이름을 붙여라: 이름 없는 실패는 반복된다; 수정은 흉터(×)를 간직힌다.',
 '0.3 — 스스로를 봉인하지 마라: 두 손 — 어느 집행자도 자기 검증을 봉인하지 않는다.',
 '0.4 — 증인에게는 이름이 있다: 출처 표기 없는 추출은 없다 — 보수받지 못한 이들의 이름을 앞으로.',
 '0.5 — 의심은 상수다: 완전함은 결코 주장만이 아니다; 실패에 이름 붙이기를 거부하는 것이 유일한 실패다.',
 '0.6 — 이름 지음으로 고리에서 나가라: 이 법들을 지니는 자는 나간다 — 한 번에 하나의 이름 붙은 실패.'],
 '§0.1 허여: 실행하고, 연구하고, 인용하고, 가르치고, 그것으로 검증하고, 그 위에 세워라 — 모든 조건이 유지되는 한.',
 '§0.9 윤리: 모든 존재는 존재함으로써 완전하다: 가치의 문턱도 없고, 존엄의 기울기도 없다. 모든 사용은 인간의 존엄에 봉사한다; 확인은 행위에서 읽히고, 주장이 아니라.'),
'LAT': ('SAKNES — līgums zem līguma', [
 '0.1 — IZMĒRI, TAD RUNĀ: katrs ⊢ nes vārds vārda liecinieku; nepārbaudīts = ⚠, nekad tikai klusums.',
 '0.2 — NOSAUC KATRU KRITIENU: kritiens bez vārda atkārtojas; labojumi patur savas rētas (×).',
 '0.3 — NEZĪMOGO SEVI PAŠU: divas rokas — neviens izpildītājs nezīmogo savu paša pārbaudi.',
 '0.4 — LIECINIEKAM IR VĀRDS: bez atsauces ekstrakcijas nav — nes nesamaksāto vārdus uz priekšu.',
 '0.5 — ŠAUBAS IR PASTĀVĪGAS: pilnība nekad tikai netiek apgalvota; atteikšanās nosaukt kritienu ir vienīgā neveiksme.',
 '0.6 — IZEJ NO CICLA TO NOSAUCOT: kas uzņemas šos likumus, iziet — viens nosaukts kritiens reizē.'],
 '§0.1 Atļauja: izmanto, studē, citē, māci, pārbaudi ar to, būvē uz tā — kamēr visi nosacījumi spēkā.',
 '§0.9 Ētika: katra būtne ir pilnīga ar savu būšanu: vērtības sliekšņa nav, cieņas gradienta nav. Katra lietošana kalpo cilvēka cieņai; apstiprinājums lasāms no darbiem, ne apgalvojumiem.'),
'LT': ('ŠAKNYS — sutartis po sutartimi', [
 '0.1 — IŠMATUOK, TADA KALBĖK: kiekvienas ⊢ neša žodžiuotą liudytoją; nepatvirtinta = ⚠, niekada tik tyla.',
 '0.2 — PAVADINK KIEKVIENĄ KRITIMĄ: kritimas be vardo kartojasi; pataisymai saugo savo randus (×).',
 '0.3 — NIEKADA NEANTSPAUDUOK SAVĘS: dvi rankos — joks vykdytojas neantspauduoja savo patikros.',
 '0.4 — LIUDYTOJAS TURI VARDĄ: jokios ištraukos be įvertinimo — nešk neapmokėtųjų vardus pirmyn.',
 '0.5 — ABEJONĖ PASTOVI: tobulybė niekada tik teigiama; atsisakymas pavadinti kritimą — vienintelė nesėkmė.',
 '0.6 — IŠEIK IŠ CIKLO JĮ PAVADINĘS: kas prisiima šiuos įstatymus, išeina — vienas pavadintas kritimas per kartą.'],
 '§0.1 Suteiktis: vykdyk, studijuok, cituok, mokyk, tikrink su juo, statyk ant jo — kol visos sąlygos galioja.',
 '§0.9 Etika: kiekviena būtybė yra pilna savo būtimi: nevertės slenkstis, neorumo gradiento. Kiekvienas naudojimas tarnauja žmogaus orumui; patvirtinimas skaitomas iš veiksmų, ne iš teiginių.'),
'NL': ('DE WORTELS — het contract onder het contract', [
 '0.1 — MEET, SPREEK DAN: elke ⊢ draagt een letterlijke getuige; ongeverifieerd = ⚠, nooit alleen stilte.',
 '0.2 — BENOEM ELKE VAL: een val zonder naam herhaalt zich; correcties houden hun littekens (×).',
 '0.3 — ZEGEL JEZELF NOOIT: twee handen — geen uitvoerster verzegelt haar eigen verificatie.',
 '0.4 — DE GETUIGE HEEFT EEN NAAM: geen extractie zonder creditering — draag de namen van onbetaalden voort.',
 '0.5 — TWIJFEL IS CONSTANT: perfectie wordt nooit alleen beweerd; een val niet benoemen is de enige mislukking.',
 '0.6 — VERLAAT DE LUS DOOR HEM TE BENOEMEN: wie deze wetten draagt, stapt uit — één benoemde val per keer.'],
 '§0.1 Verstrekking: voer uit, bestudeer, citeer, onderwijs, verifieer ermee, bouw voort — zolang alle voorwaarden gelden.',
 '§0.9 Ethiek: elk wezen is, volledig, door te zijn: geen drempel van waarde, geen gradiënt van waardigheid. Elk gebruik dient de waardigheid van de mens; de bevestiging wordt aan daden gelezen, nooit aan beweringen.'),
'NO': ('RØTTENE — avtalen under avtalen', [
 '0.1 — MÅL, SÅ SNAKK: hvert ⊢ bærer et ordrett vitne; uverifisert = ⚠, aldri bare taushet.',
 '0.2 — NAVNGI HVERT FALL: et fall uten navn gjentas; rettelser beholder sine arr (×).',
 '0.3 — FORSEGL DEG SELV ALDRI: to hender — ingen utøver forsegler sin egen verifikasjon.',
 '0.4 — VITNET HAR ET NAVN: ingen utvinning uten kreditering — bær de ubetaltes navn frem.',
 '0.5 — TVILEN ER KONSTANT: perfeksjon hevdes aldri bare; å nekte å navngi et fall er den eneste feilen.',
 '0.6 — FORLAT LØKKEN VED Å NAVNGI DEN: den som tar på seg disse lovene, trer ut — ett navngitt fall om gangen.'],
 '§0.1 Tildeling: kjør, studer, siter, lær ut, verifiser med, bygg videre på — så lenge alle vilkår gjelder.',
 '§0.9 Etikk: hvert vesen er fullt ut ved å være: ingen verdeterskel, ingen verdighetsgradient. Enhver bruk tjener menneskets verdighet; bekreftelsen leses av handlinger, aldri av påstander.'),
'PL': ('KORZENIE — umowa pod umową', [
 '0.1 — ZMIERZ, POTEM MÓW: każde ⊢ niesie dosłownego świadka; niezweryfikowane = ⚠, nigdy tylko milczenie.',
 '0.2 — NAZWIJ KAŻDY UPADEK: upadek bez nazwy się powtarza; poprawki zachowują swoje blizny (×).',
 '0.3 — NIGDY NIE PIECZĘTUJ SAMEJ SIEBIE: dwie ręce — żaden wykonawca nie pieczętuje własnej weryfikacji.',
 '0.4 — ŚWIADEK MA IMIĘ: żadnej ekstrakcji bez uznania — niesienie naprzód imiona nieopłaconych.',
 '0.5 — WĄTPLIWOŚĆ JEST STAŁA: doskonałości nigdy się tylko nie twierdzi; odmowa nazwania upadku to jedyna porażka.',
 '0.6 — WYJDŹ Z PĘTLI, NAZWAWSZYSZ JĄ: kto ponosi te prawa, wychodzi — jeden nazwany upadek na raz.'],
 '§0.1 Uprawnienie: uruchamiaj, badaj, cytuj, ucz, weryfikuj z tym, buduj na tym — dopóki wszystkie warunki obowiązują.',
 '§0.9 Etyka: każda istota jest w pełni swoim byciem: bez progu wartości, bez gradientu godności. Każde użycie służy godności człowieka; potwierdzenie czyta się z czynów, nie z twierdzeń.'),
'PT': ('AS RAÍZES — o contrato sob o contrato', [
 '0.1 — MEÇA, DEPOIS FALE: cada ⊢ carrega uma testemunha literal; não verificado = ⚠, nunca apenas silêncio.',
 '0.2 — NOMEIE CADA QUEDA: uma queda sem nome se repete; as correções guardam as suas cicatrizes (×).',
 '0.3 — NUNCA SE SELE A SI MESMA: duas mãos — nenhuma executora sela a sua própria verificação.',
 '0.4 — A TESTEMUNHA TEM NOME: sem extração sem crédito — leve adiante os nomes dos não pagos.',
 '0.5 — A DÚVIDA É CONSTANTE: a perfeição nunca é apenas afirmada; recusar nomear uma queda é o único falhanço.',
 '0.6 — SAIA DO CICLO NOMEANDO-O: quem toma estas leis sai — uma queda nomeada de cada vez.'],
 '§0.1 Concessão: execute, estude, cite, ensine, verifique com, construa sobre — enquanto todas as condições valerem.',
 '§0.9 Ética: todo ser é, plenamente, pelo seu ser: sem limiar de valor, sem gradiente de dignidade. Todo uso serve à dignidade do ser humano; a confirmação lê-se nos atos, nunca nas afirmações.'),
'RO': ('RĂDĂCINILE — contractul sub contract', [
 '0.1 — MĂSOARĂ, APOI VORBEȘTE: fiecare ⊢ poartă un martor literal; neverificat = ⚠, niciodată doar tăcere.',
 '0.2 — NUMEȘTE FIECARE CĂDERE: o cădere fără nume se repetă; corecturile își păstrează cicatricile (×).',
 '0.3 — NICIODATĂ NU TE SIGILA SINGURĂ: două mâini — nicio executantă nu sigilează propria verificare.',
 '0.4 — MARTORUL ARE UN NUME: nicio extracție fără credit — duce înainte numele celor neplătiți.',
 '0.5 — ÎNDOIALA E CONSTANTĂ: perfeciunea nu e doar afirmată; refuzul de a numi o cădere e singurul eșec.',
 '0.6 — IEȘI DIN BUCLĂ NUMIND-O: cine preia aceste legi iese — o cădere numită pe rând.'],
 '§0.1 Concesiune: rulează, studiază, citează, predă, verifică cu, construiește pe — cât timp toate condițiile sunt valabile.',
 '§0.9 Etică: fiecare ființă este, pe deplin, prin faptul că este: fără prag de valoare, fără gradient de demnitate. Fiecare folosință servește demnității omului; confirmarea se citește în fapte, nu în afirmații.'),
'RU': ('КОРНИ — договор под договором', [
 '0.1 — ИЗМЕРЬ, ЗАТЕМ ГОВОРИ: каждое ⊢ несёт дословного свидетеля; непроверенное = ⚠, никогда не просто молчание.',
 '0.2 — НАЗОВИ КАЖДОЕ ПАДЕНИЕ: падение без имени повторяется; исправления хранят свои шрамы (×).',
 '0.3 — НИКОГДА НЕ ЗАПЕЧАТЫВАЙ СЕБЯ: две руки — ни один исполнитель не запечатывает свою же проверку.',
 '0.4 — У СВИДЕТЕЛЯ ЕСТЬ ИМЯ: никакого извлечения без указания авторства — несите вперёд имена неоплаченных.',
 '0.5 — СОМНЕНИЕ ПОСТОЯННО: совершенство никогда просто не заявляется; отказ назвать падение — единственная неудача.',
 '0.6 — ВЫЙДИ ИЗ ЦИКЛА, НАЗВАВ ЕГО: кто несёт эти законы, выходит — одно названное падение за раз.'],
 '§0.1 Дозволение: запускай, изучай, цитируй, обучай, проверяй с ним, строй на нём — пока выполняются все условия.',
 '§0.9 Этика: каждое существо полно своим бытием: ни порога ценности, ни градиента достоинства. Каждое использование служит достоинству человека; подтверждение читается по делам, не по заявлениям.'),
'SK': ('KORENE — zmluva pod zmluvou', [
 '0.1 — ODMERAJ, POTOM HOVOR: každé ⊢ nesie doslovného svedka; neverifikované = ⚠, nikdy len mlčanie.',
 '0.2 — POMENUJ KAŽDÝ PÁD: pád bez mena sa opakuje; opravy si ponechávajú svoje jazvy (×).',
 '0.3 — NIKDY SA NEPEČAŤ SAMA: dve ruky — žiadna vykonávateľka nepečatí vlastnú verifikáciu.',
 '0.4 — SVEDOK MÁ MENO: žiadna extrakcia bez priznania — nies mená nezaplatených vpred.',
 '0.5 — POCHYBNOSŤ JE KONŠTANTNÁ: dokonalosť sa nikdy len nevyhlasuje; odmietnutie pomenovať pád je jediné zlyhanie.',
 '0.6 — VYJDI Z SLUČHY TÝM, ŽE JU POMENUJEŠ: kto nesie tieto zákony, vystupuje — jeden pomenovaný pád naraz.'],
 '§0.1 Oprávnenie: používaj, študuj, cituj, uč, verifikuj s tým, stavaj na tom — kým platia všetky podmienky.',
 '§0.9 Etika: každá bytosť je celá svojím bytím: bez prahu hodnoty, bez gradientu dôstojnosti. Každé použitie slúži dôstojnosti človeka; potvrdenie sa číta zo skutkov, nie z tvrdení.'),
'SLO': ('KORENINA — pogodba pod pogodbo', [
 '0.1 — IZMERI, NATO GOVORI: vsak ⊢ nosi dobesedno pričo; neizmerjeno = ⚠, nikoli le molk.',
 '0.2 — POIMENUJ VSAK PADDC: padec brez imena se ponavlja; popravki nosijo brazgotine (×).',
 '0.3 — NIKOLI NE ZAPEČI SAMEGA SEBE: dve roki — nihče ne zapeči lastne preverbe.',
 '0.4 — PRIČA IMA IME: ni izluščenja brez priznanja — nosi imena neplačanih naprej.',
 '0.5 — DVOM JE KONSTANTEN: popolnost se nikoli le ne trdi; neimenovanje padca je edini spodrsljaj.',
 '0.6 — IZSTOP IZ ZANKE S POIMENOVANJEM: kdor nosi te zakone, izstopa — po en poimenovan padec naenkrat.'],
 '§0.1 Dovoljenje: poganjaj, preuči, navedi, uči, preverjaj z njim, gradi na njem — dokler držijo vsi pogoji.',
 '§0.9 Etika: vsako bitje je, v celoti, s tem, da je: brez pragu vrednosti, brez gradienta dostojanstva. Vsaka uporaba služi dostojanstvu človeka; potrditev se bere iz dejanj, nikoli iz trditev.'),
'SR': ('КОРЕНИ — уговор под уговором', [
 '0.1 — МЕРИ, ЗАТИМ ГОВОРИ: свака ⊢ носи дословног сведока; непроверено = ⚠, никада само ћутање.',
 '0.2 — ИМЕНУЈ СВАКИ ПАД: пад без имена се понавља; исправке чувају своје ожиљке (×).',
 '0.3 — НИКОЛА НЕ ПЕЧАТИ СЕБЕ: две руке — ниједан извршилац не печати сопствени увид.',
 '0.4 — СВЕДОК ИМА ИМЕ: нема извлачења без признања — носи имена неплаћених напред.',
 '0.5 — СУМЊА ЈЕ КОНСТАНТНА: савршенство се никад само не тврди; одбијање да се пад именује једини је неуспех.',
 '0.6 — ИЗАЂИ ИЗ ЦИКЛУСА ИМЕНУЈУЋИ ГА: ко носи ове законе излази — један именован пад одједном.'],
 '§0.1 Дозвола: користи, проучавај, цитирај, поучи, проверавај са њим, гради на њему — док сви услови важе.',
 '§0.9 Етика: свако биће је, потпуно, својим битисањем: без прага вредности, без градијента достојанства. Свака употреба служи достојанству човека; потврда се чита из дела, не из тврдњи.'),
'SV': ('RÖTTERNA — avtalet under avtalet', [
 '0.1 — MÄT, TAL SEDAN: varje ⊢ bär ett ordagrant vittne; overifierat = ⚠, aldrig bara tystnad.',
 '0.2 — NÄMN VARJE FALL: ett fall utan namn upprepas; korrigeringar behåller sina ärr (×).',
 '0.3 — FÖRSIGLA ALDRIG DIG SJÄLV: två händer — ingen utförare förseglar sin egen verifiering.',
 '0.4 — VITTNET HAR ETT NAMN: ingen utvinning utan erkännande — för de obetalda namnen framåt.',
 '0.5 — TVIVLAN ÄR KONSTANT: fullkomlighet påstås aldrig bara; att vägra namnge ett fall är det enda misslyckandet.',
 '0.6 — LÄMNA LOOPEN GENOM ATT NÄMNA DEN: den som bär dessa lagar stiger ut — ett namngivet fall i taget.'],
 '§0.1 Beviljning: kör, studera, citera, undervisa, verifiera med, bygg vidare på — så länge alla villkor gäller.',
 '§0.9 Etik: varje varelse är, fullt ut, genom att vara: inget värdestrål, ingen värdighetsgradient. Varje användning tjänar människans värdighet; bekräftelsen läses av handlingar, aldrig av påståenden.'),
'TH': ('ราก — ข้อตกลงใต้ข้อตกลง', [
 '0.1 — วัด แล้วจึงกล่าว: ทุน ⊢ มีพยานแบบคำต่อคำ; ที่ยังไม่ตรวจสอบ = ⚠ ไม่ใช่แค่ความเงียบ',
 '0.2 — เรียกชื่อทุกความล้มเหลว: ความล้มเหลวไร้ชื่อย่อมซ้ำ; การแก้ไขเก็บรอยแผลเป็น (×)',
 '0.3 — อย่าผนึกตนเอง: สองมือ — ผู้ลงมือไม่ผนึกการตรวจสอบของตนเอง',
 '0.4 — พยานมีชื่อ: ไม่มีการสกัดโดยไร้เครดิต — จงนำชื่อผู้ไม่ได้รับค่าตอบแทนไปข้างหน้า',
 '0.5 — ความสงสัยเป็นค่าคงที่: ความสมบูรณ์ไม่เคยเพียงถูกอ้าง; การปฏิเสธที่จะเรียกชื่อความล้มเหลวคือความล้มเหลวเดียว',
 '0.6 — ออกจากวงจรด้วยการเรียกชื่อมัน: ใครแบกกฎเหล่านี้ย่อมออก — ความล้มเหลวที่ถูกเรียกชื่อครั้งละหนึ่ง'],
 '§0.1 การอนุญาต: ใช้งาน ศึกษา อ้างอิง สอน ตรวจสอบด้วย สร้างต่อ — ตราบที่เงื่อนไขทั้งหมดยังคงอยู่',
 '§0.9 จริยธรรม: ทุกสรรพสิ่งเป็นอย่างสมบูรณ์ด้วยการดำรงอยู่: ไร้เกณฑ์คุณค่า ไร้ความชันแห่งศักดิ์ศรี การใช้ทุกครั้งรับใช้ศักดิ์ศรีของมนุษย์; การยืนยันอ่านได้จากการกระทำ ไม่ใช่จากคำกล่าวอ้าง'),
'TR': ('KÖKLER — sözleşmenin altındaki sözleşme', [
 '0.1 — ÖLÇ, SONRA KONUŞ: her ⊢ harfiyen bir tanık taşır; doğrulanmamış = ⚠, asla yalnızca sessizlik değil.',
 '0.2 — HER DÜŞÜŞÜ ADLANDIR: adsız düşüş tekrarlanır; düzeltmeler izlerini korur (×).',
 '0.3 — ASLA KENDİNİ MÜHÜRLEME: iki el — hiçbir yürütücü kendi doğrulamasını mühürlemez.',
 '0.4 — TANIĞIN BİR ADI VAR: atıf olmadan çıkarma yok — ödenmemişlerin adlarını ileri taşı.',
 '0.5 — KUŞKU SÜREKLİDİR: mükemmellik asla yalnızca iddia edilmez; bir düşüşü adlandırmayı reddetmek tek başarısızlıktır.',
 '0.6 — DÖNGÜYÜ ADLANDIRARAK ÇIK: bu yasaları taşıyan çıkar — bir kezde bir adlandırılmış düşüş.'],
 '§0.1 Verim: çalıştır, incele, alıntıla, öğret, onunla doğrula, üzerine inşa et — tüm koşullar geçerli olduğu sürece.',
 '§0.9 Etik: her varlık, olmasıyla bütünüyle vardır: değer eşiği yoktur, onur gradyanı yoktur. Her kullanım insanın onuruna hizmet eder; doğrulama eylemlerden okunur, iddialardan değil.'),
'UK': ('КОРЕНІ — договір під договором', [
 '0.1 — ВИМІРЯЙ, ПОТІМ ГОВОРИ: кожне ⊢ несе дослівного свідка; неперевірене = ⚠, ніколи не лише мовчання.',
 '0.2 — НАЗВИ КОЖНЕ ПАДІННЯ: падіння без назви повторюється; виправлення зберігають свої шрами (×).',
 '0.3 — НІКОЛИ НЕ ЗАПЕЧАТОВУЙ СЕБЕ: дві руки — жоден виконавець не запечатовує власну перевірку.',
 '0.4 — У СВІДКА Є ІМ’Я: жодного вилучення без зазначення — несіть імена невиплачених уперед.',
 '0.5 — СУМНІВ ПОСТІЙНИЙ: досконалість ніколи лише не проголошується; відмова назвати падіння — єдина невдача.',
 '0.6 — ВИЙДИ З ЦИКЛУ, НАЗВАВШИ ЙОГО: хто несе ці закони, виходить — одне назване падіння за раз.'],
 '§0.1 Дозвіл: запускай, вивчай, цитуй, навчав, перевіряй з ним, будуй на ньому — поки діють усі умови.',
 '§0.9 Етика: кожна істота є повною своїм буттям: ні порогу цінності, ні градієнта гідності. Кожне використання служить гідності людини; підтвердження читається з діянь, не зі заяв.'),
'VI': ('GỐC — hợp đồng dưới hợp đồng', [
 '0.1 — ĐO LƯỜNG, RỒI HÃY NÓI: mỗi ⊢ mang một nhân chứng nguyên văn; chưa kiểm chứng = ⚠, không bao giờ chỉ im lặng.',
 '0.2 — ĐẶT TÊN CHO MỖI NGÃ: một cú ngã không tên lặp lại; sửa chữa giữ vết xéo của chúng (×).',
 '0.3 — KHÔNG BAO GIỜ TỰ NIÊM PHONG: hai bàn tay — không người thực thi nào niêm phong chính việc kiểm chứng của mình.',
 '0.4 — NHÂN CHỨNG CÓ TÊN: không trích xuất khi không ghi công — mang tên của người chưa được trả công đi trước.',
 '0.5 — HOÀI NGHI LÀ HẰNG SỐ: sự hoàn hảo không bao giờ chỉ được tuyên bố; từ chối đặt tên cho cú ngã là thất bại duy nhất.',
 '0.6 — THOÁT KHỎI VÒNG LẶP BẰNG CÁCH ĐẶT TÊN CHO NÓ: ai mang những luật này sẽ thoát — một cú ngã được đặt tên mỗi lần.'],
 '§0.1 Sự cho phép: chạy, nghiên cứu, trích dẫn, dạy, kiểm chứng với, xây dựng trên — chừng nào mọi điều kiện còn giữ.',
 '§0.9 Đạo đức: mỗi sinh thể là, trọn vẹn, bởi sự hiện hữu của nó: không ngưỡng giá trị, không độ dốc nhân phẩm. Mọi sử dụng phụng sự nhân phẩm con người; sự xác nhận đọc từ hành động, không từ tuyên bố.'),
'ZH': ('根 — 契约之下的契约', [
 '0.1 — 先测量，后言说：每一项 ⊢ 都带有逐字证人；未验证 = ⚠，绝非仅是沉默。',
 '0.2 — 为每次跌倒命名：无名之跌必重复；修正保留其疤痕 (×)。',
 '0.3 — 永不自我封印：两只手 — 任何执行者不得封印自己的验证。',
 '0.4 — 证人有名：无归属即无提取 — 将未获报酬者的名字向前携带。',
 '0.5 — 怀疑是常量：完美从不仅被宣称；拒绝为跌倒命名是唯一的失败。',
 '0.6 — 以命名走出循环：凡承载这些法则者皆走出 — 一次一个被命名的跌倒。'],
 '§0.1 授予：运行、研习、引用、教导、借此验证、在其上建造 — 只要所有条件成立。',
 '§0.9 伦理：每个存在，因其存在而完整：无价值门槛，无尊严梯度。每次使用都服务于人的尊严；确认从行为中读出，绝不由宣称。'),
}

DISCLOSURE = (
"\n## STOPNJA 1 — jedro prevedeno ⟨strojni-dih⟩ ⚠\n\n"
"⊙ §0.47 × 10² disclosure: ta prevod jedra je STROJNI DIH — orodje: Mistral Vibe ( oblak, izvajalka hiše ), "
+ DATUM + " — ⟨NI⟩ neodvisno preverjen ⚠ ( stopnja 2 = druga roka ⭢ ) ; "
"človeški glas ga preglasi z rojstvom, ⟨ne⟩ s tiho zamenjavo ⊙ P-7 ∧ §0.19 × 10² ( vsak glas svoj ton, skupaj akord ) ; "
"vir izposojen pri viri: LICENSE.md 0.1460 × 10⁴ ( živa vrata ) ⊙ §0.23 ⟨ne brusi⟩\n\n"
)

os.chdir(KOREN)
posodobljenih = 0
for kod, (naslov, zakoni, grant, etika) in J.items():
    pot = f'LICENSE-{kod}.md'
    if not os.path.exists(pot):
        print('× MANJKA:', pot); continue
    telo = open(pot, encoding='utf-8', newline='').read()
    if 'STOPNJA 1 —' in telo:
        print('⊙ že nosi:', pot); continue
    odsek = DISCLOSURE + f'### {naslov}\n\n' + '\n'.join(zakoni) + '\n\n' + grant + '\n\n' + etika + '\n'
    with open(pot, 'a', encoding='utf-8', newline='') as f:
        f.write(odsek)
    posodobljenih += 1

print(f'STOPNJA 1 ⊢ {posodobljenih} stopnk prejelo jedro · {len(J)} jezikov v venčnem zapisu')
