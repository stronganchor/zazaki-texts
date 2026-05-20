#!/usr/bin/env node
/* eslint-disable no-console */

const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const textsRoot = path.join(repoRoot, 'texts', 'lerch');

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function maps(query) {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;
}

function place(name, modern, query = null) {
  const item = { name, modern };
  if (query) {
    item.url = maps(query);
  }
  return item;
}

const unresolvedModern = 'modern adı kesinleşmedi';

const publication = {
  'ali-agha-ladi-kelhani': {
    title: "Kelhan'ın Oğlu Ali Ağa",
    public_summary_tr: "Kelhan'ın oğlu Ali Ağa'nın Karbegan çevresindeki gücünü, Qasım Ağa ile Weşinli Hasan Ağa'nın kurduğu tuzağı, Ali Ağa'nın ailesinin öldürülmesini ve cenazelerin defnedilmesini anlatan bir kan davası hikayesi.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Ali Ağa; Qasım Ağa; Weşinli Hasan Ağa; Ahmed; Eysan; Mela Qasım; Ramedan Ağa; Memed Ağa; Hasan Kalan; Mela Resa.',
    places_tr: 'Karbegan/Karabegan; Narbêş; Syeraçur; Sivan/Servi; Weşin; Desmun; Merzyelê; Ğêytê.',
    place_links: [
      place('Karbegan/Karabegan', 'Arıcak', 'Arıcak, Elazığ'),
      place('Narbêş', 'Yoğunbilek', 'Yoğunbilek, Arıcak, Elazığ'),
      place('Syeraçur/Sêraçur', 'Güllüce', 'Güllüce, Palu, Elazığ'),
      place('Sivan', 'Servi', 'Servi, Genç, Bingöl'),
      place('Weşin/Wısheyn', 'Erimli', 'Erimli, Alacakaya, Elazığ'),
      place('Desmun', 'Küplüce', 'Küplüce, Arıcak, Elazığ'),
      place('Merzyelê/Merzil', 'Erbağı', 'Erbağı, Arıcak, Elazığ'),
      place('Ğêytê/Ğeyd', 'Karcı', 'Karcı, Genç, Bingöl'),
    ],
    historical_context_tr: "Bu metin Karbegan/Karabegan ve Sivan/Servi çevresindeki yerel güç ilişkilerini yansıtan bir kan davası anlatısıdır. 1870-1871 Diyarbakır salnamesinde Karabegan nahiyesinin Sivan'a bağlı köylerle birlikte anılması, Karbegan adını aynı Palu-Genç/Servi tarihî coğrafyası içinde düşünmeyi destekler. Metin, Lerch'in 1856'da Roslavl'da savaş esirlerinden derlediği Zazaca malzemenin parçası olarak yayınlanmaktadır.",
    editorial_note_tr: "Narbêş, Syeraçur, Desmun, Merzyelê ve Ğêytê adları anlatının yerel coğrafyasını gösterir; Karbegan/Karabegan ile Sivan/Servi bağlantısı dış kaynaklarla da desteklenir.",
  },
  'degirmenci-ve-tilki': {
    public_summary_tr: "Bir tilki değirmencinin ununu çalarken yakalanır ve canını kurtarmak için değirmenciyi Mısır Paşası'nın kızıyla evlendireceğini söyler. Kurnazlık, kimlik uydurma ve pazarlık üzerine kurulu bir masaldır.",
    content_warning_tr: '',
    people_tr: '',
    places_tr: 'Mısr/Mısır.',
    place_links: [
      place('Mısr/Mısır', 'Mısır', 'Egypt'),
    ],
    historical_context_tr: '',
    editorial_note_tr: "MF03 satırındaki köşeli parantezli bölüm Lerch tarafından çevrilmemiştir; yayındaki anlam, Zazaca metin çözümlemesi ve bağlam üzerinden verilmiştir.",
  },
  'gespraech-mit-hassan': {
    public_summary_tr: "Hassan ile yapılan kısa soru-cevap söyleşisi Sivan aşiretinin köyleri, Kasan/Kassau/Kaschan, bahçeler, yayla yaşamı ve Hassan'ın gördüğü kan davalarına değinir.",
    content_warning_tr: '',
    people_tr: 'Hassan; Avdula Beg; Mistefa Ali; Ali Beg Aldun; Ahmed Beg.',
    places_tr: 'Sivan/Servi; Kasan/Kassau/Kaschan/Günkondu; Gewel/Gevil; Aldun/Alaaddin; Talek; Weşin; Karbegan/Karabegan; Hyêni/Hêni/Hani; Nyêrib/Nerib/Kuyular; Kavare; Gowman.',
    place_links: [
      place('Sivan', 'Servi', 'Servi, Genç, Bingöl'),
      place('Kasan/Kassau/Kaschan', 'Günkondu', 'Günkondu, Genç, Bingöl'),
      place('Fatrakom', 'Yatansöğüt', 'Yatansöğüt, Genç, Bingöl'),
      place('Hopsor/Hapsor', 'Ericek', 'Ericek, Genç, Bingöl'),
      place('Tenik/Tinik', 'Doludere', 'Doludere, Genç, Bingöl'),
      place('Rezuan/Rızvan', 'Harmancık', 'Harmancık, Genç, Bingöl'),
      place('Zımag/Zimak', 'Bahçebaşı', 'Bahçebaşı, Genç, Bingöl'),
      place('Horsig/Horsik', 'Saklıca', 'Saklıca, Genç, Bingöl'),
      place('Bılıkê/Bılıko', 'Yolaçtı', 'Yolaçtı, Genç, Bingöl'),
      place('Melêkang/Melekan', 'Sarıbudak', 'Sarıbudak, Genç, Bingöl'),
      place('Mark/Mukriyan', 'Anıl', 'Anıl, Hani, Diyarbakır'),
      place('Aldun/Aldûn', 'Alaaddin', 'Alaaddin, Genç, Bingöl'),
      place('Gewel/Gevil', 'Görülü', 'Görülü, Genç, Bingöl'),
      place('Hoena/Huynu', 'Eskibağ', 'Eskibağ, Genç, Bingöl'),
      place('Şekara/Şekaron', 'Şekeran Yaylası', 'Şekeran Yaylası, Genç, Bingöl'),
      place('Hêylang/Heylan', 'Gerçekli', 'Gerçekli, Genç, Bingöl'),
      place('Bazyang/Bazian', 'Dereköy', 'Dereköy, Genç, Bingöl'),
      place('Mala İbrahiman', 'Mollaibrahiman', 'Mollaibrahiman, Genç, Bingöl'),
      place('Avdêlang/Avdelan', 'Sırmalıova', 'Sırmalıova, Genç, Bingöl'),
      place('Mıstang/Mıstan', 'Bulgurluk', 'Bulgurluk, Genç, Bingöl'),
      place('Sayêrê/Sayer', 'Yazılı', 'Yazılı, Genç, Bingöl'),
      place('Abasa/Abason', 'Damlapınar', 'Damlapınar, Palu, Elazığ'),
      place('Wis’hêyn/Weşin', 'Erimli', 'Erimli, Alacakaya, Elazığ'),
      place('Haspêg/Hasbeg', 'Hasbey', 'Hasbey, Palu, Elazığ'),
      place('Sêraçyori/Sêraçur', 'Güllüce', 'Güllüce, Palu, Elazığ'),
      place('Akêragi/Akerag', 'Burgudere', 'Burgudere, Palu, Elazığ'),
      place('Letang/Letan', 'Gürpınar', 'Gürpınar, Genç, Bingöl'),
      place('Ğahar/Gahar', 'Göründü', 'Göründü, Arıcak, Elazığ'),
      place('Ğoêmang/Gowman', 'Yalnızdamlar', 'Yalnızdamlar, Alacakaya, Elazığ'),
      place('Kavarê/Kavar', 'Yazkonağı', 'Yazkonağı, Genç, Bingöl'),
      place('Talek/Tolek', 'Gümeçbağlar', 'Gümeçbağlar, Palu, Elazığ'),
      place('Karbegan/Karabegan', 'Arıcak', 'Arıcak, Elazığ'),
      place('Hyêni/Hêni', 'Hani', 'Hani, Diyarbakır'),
      place('Nyêrib/Nerib', 'Kuyular', 'Kuyular, Hani, Diyarbakır'),
      place('Hêmek/Hamek', 'Yeniler (Güzeldere)', 'Yeniler, Güzeldere, Genç, Bingöl'),
      place('Sama/Sema', unresolvedModern),
      place('Emêra/Emera', 'Servi bölgesinde büyük köy; modern adı kesinleşmedi'),
    ],
    historical_context_tr: "Bu söyleşi, Lerch'in ana Zaza kaynağı Hassan hakkında en doğrudan bilgiyi veren metindir. Hassan'ın Sivan dediği çerçeve, 1841 Palu nüfus defterinde 42 köylü Sivan nahiyesi olarak görünen ve daha sonra Genç'e bağlanıp Servi adıyla anılan bölgeyle örtüşür. Kasan/Kassau/Kaschan için en güçlü çalışma karşılığı, Sivan köy listesinde Kasan/Kâsan olarak verilen bugünkü Günkondu'dur.",
    editorial_note_tr: "Hassan/Hasan yazımı Lerch'in biçimine göre korunur. Kasan/Günkondu, Horsik/Saklıca, Aldun/Alaaddin ve Hêmek/Hamek/Yeniler gibi Sivan köyleri kaynakla desteklenir; Weşin, Talek, Kavare ve Gowman gibi adlar anlatının yerel coğrafyasını belgeleyen diğer adlardır.",
  },
  'goin-puhu-kusunun-hikayesi': {
    public_summary_tr: "Üvey annesinin öldürdüğü kardeşini rüyasında gören bir kız, aile içi çatışmanın ardından Allah'tan kendisini go'in/puhu kuşuna çevirmesini ister.",
    content_warning_tr: 'şiddet; çocuk ölümü',
    people_tr: '',
    places_tr: '',
    historical_context_tr: '',
    editorial_note_tr: '',
  },
  'kauge-nyerib-u-hyeni': {
    title: "Nyêrib ile Hyêni'nin Kavgası",
    public_summary_tr: "Nyêrib'den bir adamın Hyêni toprağında bir hizmetçiyi öldürmesiyle başlayan anlatı, Xalef Ağa ile Daqma Bey arasında savaşa dönüşür ve Ziriki ağalarının arabuluculuğuyla barışla biter.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Xalef Ağa; Daqma Bey; Temir Beg; Mela Haseynê Mûğara; Wesman Ağa; Mêhmêt Ağa; Ziriki ağaları; Bayraktar.',
    places_tr: 'Nyêrib/Nerib/Kuyular; Hyêni/Hêni/Hani/Khini; Dawz; Küçük Nyêrib; Deştê Henzi; Ziriki.',
    place_links: [
      place('Nyêrib/Nerib', 'Kuyular', 'Kuyular, Hani, Diyarbakır'),
      place('Hyêni/Hêni/Khini', 'Hani', 'Hani, Diyarbakır'),
      place('Dawz/Cauz/Cewzê', 'Gürbüz', 'Gürbüz, Hani, Diyarbakır'),
      place('Deştê Henzi', 'Henzi Ovası', 'Henzi Ovası, Hani, Diyarbakır'),
      place('Küçük Nyêrib', 'Nerib hattındaki küçük köy; modern karşılığı kesinleşmedi'),
      place('Dûzê Hemyê', 'Hani/Nerib çevresinde mevki; modern adı kesinleşmedi'),
    ],
    historical_context_tr: "Hyêni/Hêni adı dış kaynaklardaki Hani/Khini ile, Nyêrib/Nerib adı da 19. yüzyıl yer adı notlarında Hani ilçesindeki Kuyular/Nerib ile eşleşir. Hikâyede ordunun Temir Beg'in evi önünde toplanması önemlidir: bu kişi büyük olasılıkla kaynaklarda 1819'da Hani ileri geleni, 1835'te Hani emini olarak görünen ve aynı yıl yenilip Edirne'ye sürgün edilen Timur/Temir Bey'dir. Bu bağlantı, olayın muhtemelen 1819-1835 aralığında gerçekleştiğini gösterir.",
    editorial_note_tr: "Nyêrib/Kuyular ve Hyêni/Hani eşleştirmeleri dış kaynakla desteklenir. Küçük Nyêrib adı, Hani çevresindeki Nêrib köyleri kümesine bağlı bir küçük yerleşimi gösteriyor olmalıdır; Dûzê Hemyê ise aynı çevrede bir ova veya mevki adı gibi görünür.",
  },
  'kauge-nyerib-u-sivani': {
    title: "Nyêrib ve Sivan'ın Kavgası",
    public_summary_tr: "Nyêrib'den bir gencin Horsig'de hırsızlık yapması ve öldürülmesiyle başlayan anlatı, Xalef Ağa ile Avdulah Ağa arasında tehditler, çatışma ve sonunda barışa uzanan bir kan davasını anlatır.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Xalef Ağa; Avdulah Ağa; Mela Ahmed/Qafon; Huseyin; Hayder Ağa; Sele.',
    places_tr: 'Nyêrib/Nerib/Kuyular; Sivan/Servi; Horsig/Horsik/Saklıca; Deştê Henzi; Şeynan; Hêni/Hyêni/Hani; Kelan.',
    place_links: [
      place('Nyêrib/Nerib', 'Kuyular', 'Kuyular, Hani, Diyarbakır'),
      place('Sivan', 'Servi', 'Servi, Genç, Bingöl'),
      place('Horsig/Horsik', 'Saklıca', 'Saklıca, Genç, Bingöl'),
      place('Deştê Henzi', 'Henzi Ovası', 'Henzi Ovası, Hani, Diyarbakır'),
      place('Şeynan/Şeynon', 'Çukurköy', 'Çukurköy, Hani, Diyarbakır'),
      place('Hyêni/Hêni', 'Hani', 'Hani, Diyarbakır'),
      place('Dait/Caıt', 'Sergen', 'Sergen, Hani, Diyarbakır'),
      place('Şelê/Sele deresi', 'Yukarı Turalı / Aşağı Turalı', 'Yukarı Turalı Aşağı Turalı Hani Diyarbakır'),
      place('Qotwesan/Qotweson', 'Arıcak', 'Arıcak, Elazığ'),
      place('Kelan', 'Doğanlı? (Kelahsı/Kelaxsi)', 'Doğanlı, Genç, Bingöl'),
      place('Tawricyê/Taurıcye', unresolvedModern),
    ],
    historical_context_tr: "Bu anlatı Sivan/Servi-Palu hattı ile Nyêrib/Hani hattı arasındaki yerel çatışma hafızasını birleştirir. Horsig adı, Sivan köy listesinde Horsik (bugünkü Saklıca) olarak görünen yerle büyük olasılıkla aynıdır. Metindeki Xalef Ağa'ya 'Hyêni'de kavga ettin' uyarısı, bu anlatıyı Nyêrib-Hyêni kavgasından sonra konumlandırır; bu nedenle en uygun tarih aralığı yaklaşık 1820-1853'tür.",
    editorial_note_tr: "Sivan/Servi, Horsig/Horsik/Saklıca ve Nyêrib/Nerib/Kuyular eşleştirmeleri kaynakla desteklenir. Şelê adı bu anlatıda Hani tarafındaki Şelli/Turalı köyleriyle daha iyi örtüşür. Kelan için en güçlü aday, Sivan köy listelerindeki Kelahsı/Kelaxsi, bugünkü Doğanlı'dır; Tawricyê için modern karşılık henüz kesinleşmemiştir.",
  },
  'uc-kardes-masali': {
    public_summary_tr: "Hasanek, Qasım ve Şaban adlı üç kardeşin bir devle karşılaşmasını, Hasanek'in mektupları değiştirerek devi kandırmasını ve sonunda devi öldürmesini anlatan masal.",
    content_warning_tr: 'şiddet; yetişkin tema',
    people_tr: '',
    places_tr: '',
    historical_context_tr: '',
    editorial_note_tr: '',
  },
};

const titleUnits = {
  'kauge-nyerib-u-hyeni': {
    id: 'title',
    source: "Kawğê Nyêrib û Hyêni",
    translations: {
      tr: "Nyêrib ile Hyêni'nin Kavgası",
      en: "The Feud Between Nyêrib and Hyêni",
      de: "Die Feindseligkeiten zwischen Nyêrib und Hyêni",
    },
  },
  'kauge-nyerib-u-sivani': {
    id: 'title',
    source: "Kawğê Nyêrib û Sivani",
    translations: {
      tr: "Nyêrib ve Sivan'ın Kavgası",
      en: "The Feud Between Nyêrib and Sivan",
      de: "Die Feindseligkeiten zwischen Nyêrib und Sivan",
    },
  },
};

for (const [slug, data] of Object.entries(publication)) {
  const dir = path.join(textsRoot, slug);
  const metadataPath = path.join(dir, 'metadata.json');
  const payloadPath = path.join(dir, 'text-document.json');
  if (!fs.existsSync(metadataPath) || !fs.existsSync(payloadPath)) {
    throw new Error(`Missing metadata or payload for ${slug}`);
  }

  const metadata = readJson(metadataPath);
  metadata.publication = data;
  if (data.title) {
    metadata.title = data.title;
  }
  if (data.public_summary_tr) {
    metadata.excerpt = data.public_summary_tr;
  }
  writeJson(metadataPath, metadata);

  const payload = readJson(payloadPath);
  if (data.title) {
    payload.title = data.title;
  }
  payload.metadata = payload.metadata && typeof payload.metadata === 'object' ? payload.metadata : {};
  payload.metadata.publication = data;
  if (data.title) {
    payload.metadata.title_tr = data.title;
  }
  if (titleUnits[slug] && Array.isArray(payload.reading_units)) {
    payload.reading_units = [
      titleUnits[slug],
      ...payload.reading_units.filter((unit) => unit && unit.id !== 'title'),
    ];
    if (payload.summary && typeof payload.summary === 'object') {
      payload.summary.reading_units = payload.reading_units.length;
    }
  }
  if (data.public_summary_tr) {
    payload.metadata.excerpt = data.content_warning_tr
      ? `${data.public_summary_tr} İçerik uyarısı: ${data.content_warning_tr}.`
      : data.public_summary_tr;
  }
  writeJson(payloadPath, payload);
}

console.log(`Updated publication metadata for ${Object.keys(publication).length} Lerch texts.`);
