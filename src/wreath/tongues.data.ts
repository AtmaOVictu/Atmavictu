export interface WreathTongue {
  code: string;
  language: string;
  slot: string;
  canon: string;
  connotation: string;
  status: 'slot' | 'issued';
}

export const REGISTRY: WreathTongue[] = [
  { code: 'AR', language: 'Arabščina', slot: 'LICENSE-AR.md', canon: 'šahada priča', connotation: 'glas brez lastnika', status: 'slot' },
  { code: 'BG', language: 'Bolgarščina', slot: 'LICENSE-BG.md', canon: 'istina', connotation: 'svedok, ne vrata', status: 'slot' },
  { code: 'CS', language: 'Češčina', slot: 'LICENSE-CS.md', canon: 'pravda', connotation: 'svědek, nikdy dveře', status: 'slot' },
  { code: 'DA', language: 'Danščina', slot: 'LICENSE-DA.md', canon: 'sandhed', connotation: 'vidne, aldrig døren', status: 'slot' },
  { code: 'DE', language: 'Nemščina', slot: 'LICENSE-DE.md', canon: 'Ordnung', connotation: 'struktura členov, logika', status: 'slot' },
  { code: 'EL', language: 'Grščina', slot: 'LICENSE-EL.md', canon: 'aletheia', connotation: 'martyrías, ochi i porta', status: 'slot' },
  { code: 'EN', language: 'Angleščina (vir licence)', slot: 'LICENSE.md', canon: 'the door is born sewn in', connotation: 'živa vrata, edina grant-nosilna izdaja', status: 'issued' },
  { code: 'ES', language: 'Španščina', slot: 'LICENSE-ES.md', canon: 'Rigor', connotation: 'strogo, natančno', status: 'slot' },
  { code: 'ET', language: 'Estonščina', slot: 'LICENSE-ET.md', canon: 'tõde', connotation: 'tunnistaja, mitte uks', status: 'slot' },
  { code: 'FA', language: 'Farsi', slot: 'LICENSE-FA.md', canon: 'šohudat', connotation: 'goāh, har gaz dar nist', status: 'slot' },
  { code: 'FI', language: 'Finska', slot: 'LICENSE-FI.md', canon: 'totuus', connotation: 'todistaja, ei koskaan ovi', status: 'slot' },
  { code: 'FR', language: 'Francoščina', slot: 'LICENSE-FR.md', canon: 'Précision', connotation: 'natančnost', status: 'slot' },
  { code: 'HE', language: 'Hebrejščina', slot: 'LICENSE-HE.md', canon: 'emet', connotation: 'ed, le-olam lo delet', status: 'slot' },
  { code: 'HI', language: 'Hindščina', slot: 'LICENSE-HI.md', canon: 'satya', connotation: 'gavāh, kabhī dvār nahīṁ', status: 'slot' },
  { code: 'HU', language: 'Madžarščina', slot: 'LICENSE-HU.md', canon: 'igazság', connotation: 'tanú, sosem az ajtó', status: 'slot' },
  { code: 'ID', language: 'Indonezijščina', slot: 'LICENSE-ID.md', canon: 'kejujuran', connotation: 'saksi, bukan pintu', status: 'slot' },
  { code: 'IS', language: 'Islandščina', slot: 'LICENSE-IS.md', canon: 'sönn', connotation: 'vottur, aldrei dyrrin', status: 'slot' },
  { code: 'IT', language: 'Italijanščina', slot: 'LICENSE-IT.md', canon: 'Correttezza', connotation: 'pravilnost', status: 'slot' },
  { code: 'JA', language: 'Japonščina', slot: 'LICENSE-JA.md', canon: 'kotowari', connotation: 'shōnin, kesshite tobira dewa nai', status: 'slot' },
  { code: 'KO', language: 'Korejščina', slot: 'LICENSE-KO.md', canon: 'jinje', connotation: 'jeungin, geuollo mun-i anida', status: 'slot' },
  { code: 'LAT', language: 'Latinščina', slot: 'LICENSE-LAT.md', canon: 'veritas', connotation: 'testis, numquam ianua', status: 'slot' },
  { code: 'LT', language: 'Litva', slot: 'LICENSE-LT.md', canon: 'teisybė', connotation: 'liudytojas, niekada durys', status: 'slot' },
  { code: 'NL', language: 'Nizozemščina', slot: 'LICENSE-NL.md', canon: 'waarheid', connotation: 'getuige, nooit de deur', status: 'slot' },
  { code: 'NO', language: 'Norveščina', slot: 'LICENSE-NO.md', canon: 'sannhet', connotation: 'vitne, aldri døren', status: 'slot' },
  { code: 'PL', language: 'Poljščina', slot: 'LICENSE-PL.md', canon: 'prawda', connotation: 'świadek, nigdy drzwi', status: 'slot' },
  { code: 'PT', language: 'Portugalska', slot: 'LICENSE-PT.md', canon: 'verdade', connotation: 'testemunha, nunca a porta', status: 'slot' },
  { code: 'RO', language: 'Romunščina', slot: 'LICENSE-RO.md', canon: 'adevăr', connotation: 'martor, nu ușa', status: 'slot' },
  { code: 'RU', language: 'Rusščina', slot: 'LICENSE-RU.md', canon: 'pravda', connotation: 'svidetel, ne dverʹ', status: 'slot' },
  { code: 'SK', language: 'Slovaščina', slot: 'LICENSE-SK.md', canon: 'pravda', connotation: 'svedok, nikdy dvere', status: 'slot' },
  { code: 'SLO', language: 'Slovenščina (tla korpusa)', slot: 'LICENSE-SLO.md', canon: 'tla korpusa', connotation: 'strojni dih 1–1.6, brez druge roke ⚠', status: 'slot' },
  { code: 'SR', language: 'Srbohrvaščina', slot: 'LICENSE-SR.md', canon: 'istina', connotation: 'svedok, nikad vrata', status: 'slot' },
  { code: 'SV', language: 'Švedščina', slot: 'LICENSE-SV.md', canon: 'sanning', connotation: 'vittne, aldrig dörren', status: 'slot' },
  { code: 'TH', language: 'Tajščina', slot: 'LICENSE-TH.md', canon: 'sat', connotation: 'phayan, mai chai pra-tu', status: 'slot' },
  { code: 'TR', language: 'Turščina', slot: 'LICENSE-TR.md', canon: 'gerçek', connotation: 'tanık, asla kapı', status: 'slot' },
  { code: 'UK', language: 'Ukrajinščina', slot: 'LICENSE-UK.md', canon: 'pravda', connotation: 'svidok, ne dverі', status: 'slot' },
  { code: 'VI', language: 'Vijetnamščina', slot: 'LICENSE-VI.md', canon: 'sự thật', connotation: 'chứng nhân, không bao giờ là cửa', status: 'slot' },
  { code: 'ZH', language: 'Kitajščina', slot: 'LICENSE-ZH.md', canon: 'zhēn', connotation: 'jiànzhèng zhě, juédì fēishì mén', status: 'slot' },
];
