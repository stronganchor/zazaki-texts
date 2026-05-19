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

const publication = {
  'ali-agha-ladi-kelhani': {
    public_summary_tr: "Kelhan'ın oğlu Ali Ağa'nın Karbegan çevresindeki gücünü, Qasım Ağa ile Weşinli Hasan Ağa'nın kurduğu tuzağı, Ali Ağa'nın ailesinin öldürülmesini ve cenazelerin defnedilmesini anlatan bir kan davası hikayesi.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Ali Ağa; Qasım Ağa; Weşinli Hasan Ağa; Ahmed; Eysan; Mela Qasım; Ramedan Ağa; Memed Ağa; Hasan Kalan; Mela Resa.',
    places_tr: 'Karbegan/Karabegan; Narbêş; Syeraçur; Sivan/Servi; Weşin; Desmun; Merzyelê; Ğêytê.',
    historical_context_tr: "Bu metin Karbegan/Karabegan ve Sivan/Servi çevresindeki yerel güç ilişkilerini yansıtan bir kan davası anlatısıdır. 1870-1871 Diyarbakır salnamesinde Karabegan nahiyesinin Sivan'a bağlı köylerle birlikte anılması, Karbegan adını aynı Palu-Genç/Servi tarihî coğrafyası içinde düşünmeyi destekler. Şimdilik kesin tarih verilmemelidir; metin, Lerch'in 1856'da Roslavl'da savaş esirlerinden derlediği Zazaca malzemenin parçası olarak yayınlanmaktadır.",
    editorial_note_tr: "Karbegan/Karabegan ile Sivan/Servi bağlantısı kaynakla desteklenir; Narbêş, Syeraçur, Desmun, Merzyelê ve Ğêytê için modern yer karşılıkları hâlâ çalışma konusudur.",
  },
  'degirmenci-ve-tilki': {
    public_summary_tr: "Bir tilki değirmencinin ununu çalarken yakalanır ve canını kurtarmak için değirmenciyi Mısır Paşası'nın kızıyla evlendireceğini söyler. Kurnazlık, kimlik uydurma ve pazarlık üzerine kurulu bir masaldır.",
    content_warning_tr: '',
    people_tr: '',
    places_tr: '',
    historical_context_tr: "Masal türündedir; belirli kişi veya yerler için tarihsel kimlik iddiası eklenmemiştir. MF03 satırındaki köşeli parantezli bölüm Lerch tarafından çevrilmemiştir; mevcut çeviri, interlinear ve bağlamdan çıkarılmış çalışma yorumudur.",
    editorial_note_tr: "Çemçequ Paşa adı ve MF03'teki sel/fırtına bölümü sonraki karşılaştırmalarla yeniden gözden geçirilebilir.",
  },
  'gespraech-mit-hassan': {
    public_summary_tr: "Hassan ile yapılan kısa soru-cevap söyleşisi Sivan aşiretinin köyleri, Kasan/Kassau/Kaschan, bahçeler, yayla yaşamı ve Hassan'ın gördüğü kan davalarına değinir.",
    content_warning_tr: '',
    people_tr: 'Hassan; Avdula Beg; Mistefa Ali; Ali Beg Aldun; Ahmed Beg.',
    places_tr: 'Sivan/Servi; Kasan/Kassau/Kaschan/Günkondu; Gewel/Gevil; Aldun/Alaaddin; Talek; Weşin; Karbegan/Karabegan; Hyêni/Hêni/Hani; Nyêrib/Nerib/Kuyular; Kavare; Gowman.',
    historical_context_tr: "Bu söyleşi, Lerch'in ana Zaza kaynağı Hassan hakkında en doğrudan bilgiyi veren metindir. Hassan'ın Sivan dediği çerçeve, 1841 Palu nüfus defterinde 42 köylü Sivan nahiyesi olarak görünen ve daha sonra Genç'e bağlanıp Servi adıyla anılan bölgeyle örtüşür. Kasan/Kassau/Kaschan için en güçlü çalışma karşılığı, Sivan köy listesinde Kasan/Kâsan olarak verilen bugünkü Günkondu'dur.",
    editorial_note_tr: "Hassan/Hasan yazımı Lerch'in biçimine göre korunur. Köy eşleştirmeleri çalışma notudur: Kasan/Günkondu, Horsik/Saklıca, Aldun/Alaaddin ve bazı diğer Sivan köyleri kaynakla desteklenir; Weşin, Talek, Kavare ve Gowman gibi adlar için daha fazla yerel kontrol gerekir.",
  },
  'goin-puhu-kusunun-hikayesi': {
    public_summary_tr: "Üvey annesinin öldürdüğü kardeşini rüyasında gören bir kız, aile içi çatışmanın ardından Allah'tan kendisini go'in/puhu kuşuna çevirmesini ister.",
    content_warning_tr: 'şiddet; çocuk ölümü',
    people_tr: '',
    places_tr: '',
    historical_context_tr: "Dönüşüm ve kuş motifi etrafında gelişen folklorik bir anlatıdır; belirli tarihsel kişi veya yer bilgisi eklenmemiştir.",
    editorial_note_tr: "Go'in/puhu kuşu kimliği çalışma yorumudur ve kuş adı sonraki folklor/diyalekt karşılaştırmalarıyla yeniden değerlendirilebilir.",
  },
  'kauge-nyerib-u-hyeni': {
    public_summary_tr: "Nyêrib'den bir adamın Hyêni toprağında bir hizmetçiyi öldürmesiyle başlayan anlatı, Xalef Ağa ile Daqma Bey arasında savaşa dönüşür ve Ziriki ağalarının arabuluculuğuyla barışla biter.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Xalef Ağa; Daqma Bey; Temir Beg; Mela Haseynê Mûğara; Wesman Ağa; Mêhmêt Ağa; Ziriki ağaları; Bayraktar.',
    places_tr: 'Nyêrib/Nerib/Kuyular; Hyêni/Hêni/Hani/Khini; Dawz; Küçük Nyêrib; Deştê Henzi; Ziriki.',
    historical_context_tr: "Hyêni/Hêni adı dış kaynaklardaki Hani/Khini ile, Nyêrib/Nerib adı da 19. yüzyıl yer adı notlarında Hani ilçesindeki Kuyular/Nerib ile eşleştirilebilir. Hikâyede ordunun Temir Beg'in evi önünde toplanması önemlidir: bu kişi Hani beylerinden Timur/Temir Bey ise, dış kaynaklarda 1819'da Hani ileri geleni, 1835'te Hani emini olarak görünmesi ve aynı yıl yenilip Edirne'ye sürgün edilmesi olay için en makul üst sınırı 1835'e çeker. Bu kesin tarihleme değil, tarihsel kimlik varsayımına dayalı çalışma notudur.",
    editorial_note_tr: "Temir Beg = Timur/Temir Bey of Hani eşleştirmesi güçlü ama kesin değildir. Nyêrib/Kuyular ve Hyêni/Hani eşleştirmeleri dış kaynakla desteklenir; Dawz, Deştê Henzi ve Küçük Nyêrib için daha ayrıntılı yerel kontrol gerekir.",
  },
  'kauge-nyerib-u-sivani': {
    public_summary_tr: "Nyêrib'den bir gencin Horsig'de hırsızlık yapması ve öldürülmesiyle başlayan anlatı, Xalef Ağa ile Avdulah Ağa arasında tehditler, çatışma ve sonunda barışa uzanan bir kan davasını anlatır.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Xalef Ağa; Avdulah Ağa; Mela Ahmed/Qafon; Huseyin; Hayder Ağa; Sele.',
    places_tr: 'Nyêrib/Nerib/Kuyular; Sivan/Servi; Horsig/Horsik/Saklıca; Deştê Henzi; Şeynan; Hêni/Hyêni/Hani; Kelan.',
    historical_context_tr: "Bu anlatı Sivan/Servi-Palu hattı ile Nyêrib/Hani hattı arasındaki yerel çatışma hafızasını birleştirir. Horsig adı, Sivan köy listesinde Horsik (bugünkü Saklıca) olarak görünen yerle büyük olasılıkla aynıdır. Metindeki Xalef Ağa'ya 'Hyêni'de kavga ettin' uyarısı, bunu Nyêrib-Hyêni kavgasından sonra konumlandıran iç ipucudur; bu nedenle çalışma aralığı kabaca 1820-1853 olarak tutulur, üst sınır ise Lerch'in Kırım Savaşı dönemindeki kayıt bağlamıdır.",
    editorial_note_tr: "Sivan/Servi, Horsig/Horsik/Saklıca ve Nyêrib/Nerib/Kuyular eşleştirmeleri kaynakla desteklenir. Deştê Henzi, Şeynan ve Kelan için modern karşılıklar henüz kesinleştirilmemiştir; anlatılar arası kronoloji çalışma hipotezi olarak verilmelidir.",
  },
  'uc-kardes-masali': {
    public_summary_tr: "Hasanek, Qasım ve Şaban adlı üç kardeşin bir devle karşılaşmasını, Hasanek'in mektupları değiştirerek devi kandırmasını ve sonunda devi öldürmesini anlatan masal.",
    content_warning_tr: 'şiddet; yetişkin tema',
    people_tr: '',
    places_tr: '',
    historical_context_tr: 'Masal türündedir; belirli tarihsel kişi veya yer bilgisi eklenmemiştir.',
    editorial_note_tr: 'Hasanek adı, Qasım/Qasim yazımı ve bazı masal motifleri sonraki folklor karşılaştırmalarıyla gözden geçirilebilir.',
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
  if (data.public_summary_tr) {
    metadata.excerpt = data.public_summary_tr;
  }
  writeJson(metadataPath, metadata);

  const payload = readJson(payloadPath);
  payload.metadata = payload.metadata && typeof payload.metadata === 'object' ? payload.metadata : {};
  payload.metadata.publication = data;
  if (data.public_summary_tr) {
    payload.metadata.excerpt = data.content_warning_tr
      ? `${data.public_summary_tr} İçerik uyarısı: ${data.content_warning_tr}.`
      : data.public_summary_tr;
  }
  writeJson(payloadPath, payload);
}

console.log(`Updated publication metadata for ${Object.keys(publication).length} Lerch texts.`);
