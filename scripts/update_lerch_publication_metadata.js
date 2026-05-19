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
    places_tr: 'Karbegan; Narbêş; Syeraçur; Sivan; Weşin; Desmun; Merzyelê; Ğêytê.',
    historical_context_tr: "Sivan/Karbegan çevresiyle ilişkili bir yerel güç ve kan davası anlatısıdır. Şimdilik kesin tarih verilmemelidir; metin, Lerch'in 1856'da Roslavl'da savaş esirlerinden derlediği Zazaca malzemenin parçası olarak yayınlanmaktadır.",
    editorial_note_tr: 'Çalışma yayınıdır; kişi ve yer adlarının bazı modern karşılıkları ek araştırma gerektirir.',
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
    places_tr: 'Sivan; Kasan/Kassau/Kaschan; Gewel; Aldun; Talek; Weşin; Karbegan; Hyêni/Hêni; Nyêrib; Kavare; Gowman.',
    historical_context_tr: "Bu söyleşi, Lerch'in ana Zaza kaynağı Hassan hakkında en doğrudan bilgiyi veren metindir. Yerel çalışma notlarına göre Hassan Sivan aşiretindendi ve Palu yakınındaki Kasan/Kassau/Kaschan köyüyle bağlantılıydı.",
    editorial_note_tr: 'Hassan/Hasan yazımı ve Kasan yerinin kesin modern karşılığı daha fazla dış kaynakla kontrol edilmelidir.',
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
    places_tr: 'Nyêrib; Hyêni/Hêni/Hani; Dawz; Küçük Nyêrib; Deştê Henzi; Ziriki.',
    historical_context_tr: "Temir Beg adı, Hani/Hyêni begi Timur/Temir Bey ile bağlantılıysa olay için en güçlü çalışma aralığı yaklaşık 1819-1835'tir. Bu aralık, Timur Bey'in 1819'da Hani ileri geleni olarak görünmesi ve 1835'te yenilgi/sürgün bağlamıyla sınırlıdır; kesin tarih olarak değil, araştırma notu olarak kullanılmalıdır.",
    editorial_note_tr: "Hyêni/Hani/Khini adı, Temir/Daqma Bey bağlamı ve yer adları dış kaynaklarla yeniden kontrol edilmelidir.",
  },
  'kauge-nyerib-u-sivani': {
    public_summary_tr: "Nyêrib'den bir gencin Horsig'de hırsızlık yapması ve öldürülmesiyle başlayan anlatı, Xalef Ağa ile Avdulah Ağa arasında tehditler, çatışma ve sonunda barışa uzanan bir kan davasını anlatır.",
    content_warning_tr: 'şiddet; ölüm',
    people_tr: 'Xalef Ağa; Avdulah Ağa; Mela Ahmed/Qafon; Huseyin; Hayder Ağa; Sele.',
    places_tr: 'Nyêrib; Sivan; Horsig; Deştê Henzi; Şeynan; Hêni/Hyêni; Kelan.',
    historical_context_tr: "Bu anlatı, Nyêrib-Hyêni kavgasından sonra anlatılan veya onu ima eden bir Sivan-Nyêrib kavgası gibi görünür. Çalışma notu olarak kabaca 1820-1853 aralığı önerilebilir; üst sınır, metnin Kırım Savaşı sırasında Lerch tarafından kaydedilmiş olmasıdır.",
    editorial_note_tr: 'Sivan/Nyêrib yer adları, kişi adları ve anlatılar arası kronoloji çalışma notu olarak tutulmalıdır.',
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
