import { GIFEncoder, quantize, applyPalette } from './gifenc.esm.js';

const MAX = 6; // segundos: acima disso o WhatsApp trata como vídeo
const $ = s => document.querySelector(s);
const form = $('#form'), link = $('#link'), msg = $('#msg'), escolha = $('#escolha');
const editor = $('#editor'), video = $('#video'), inicio = $('#inicio');
const resultado = $('#resultado'), gifImg = $('#gif'), barra = $('#barra');
let urlVideo = null, urlGif = null, blobGif = null;

const avisa = (t, erro) => { msg.textContent = t; msg.classList.toggle('erro', !!erro); };
const fmt = s => s.toFixed(1).replace('.', ',') + 's';

function idDoLink(t) {
  const m = String(t).match(/(?:twitter\.com|x\.com|fxtwitter\.com|vxtwitter\.com|fixupx\.com)\/[^/]+\/status(?:es)?\/(\d+)/i)
    || String(t).match(/^\s*(\d{10,25})\s*$/);
  return m && m[1];
}

async function json(u) {
  const r = await fetch(u);
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return r.json();
}

// Procura os vídeos/GIFs do post, primeiro no FxTwitter e depois no vxTwitter.
async function midias(id) {
  try {
    const d = await json(`https://api.fxtwitter.com/i/status/${id}`);
    const t = d.tweet || {};
    const vs = (t.media && t.media.videos) || [];
    if (vs.length) return vs.map(v => ({ url: leve(v), capa: v.thumbnail_url, dur: v.duration }));
    if (t.media) return [];
  } catch (e) { console.warn('fxtwitter', e); }
  const d = await json(`https://api.vxtwitter.com/i/status/${id}`);
  return (d.media_extended || []).filter(m => m.type === 'video' || m.type === 'gif')
    .map(m => ({ url: m.url, capa: m.thumbnail_url, dur: (m.duration_millis || 0) / 1000 }));
}

// A figurinha tem no máximo 512px: não precisa baixar a versão em alta.
function leve(v) {
  const mp4 = (v.variants || []).filter(x => /mp4/.test(x.content_type || x.url) && x.bitrate)
    .sort((a, b) => a.bitrate - b.bitrate);
  const ok = mp4.find(x => x.bitrate >= 800000) || mp4[mp4.length - 1];
  return (ok && ok.url) || v.url;
}

async function baixa(u) {
  const r = await fetch(u);
  if (!r.ok) throw new Error('HTTP ' + r.status);
  return r.blob();
}

function carrega(blob) {
  if (urlVideo) URL.revokeObjectURL(urlVideo);
  urlVideo = URL.createObjectURL(blob);
  video.src = urlVideo;
  resultado.hidden = true;
  return new Promise((ok, falha) => {
    video.onloadedmetadata = () => {
      const d = video.duration;
      inicio.max = Math.max(0, d - MAX).toFixed(1);
      inicio.value = 0;
      $('#trecho').hidden = d <= MAX;
      $('#aviso-corte').hidden = d <= MAX;
      $('#dur-txt').textContent = 'vídeo: ' + fmt(d);
      trecho();
      editor.hidden = false;
      video.play().catch(() => {});
      ok();
    };
    video.onerror = () => falha(new Error('Não deu para abrir esse vídeo.'));
  });
}

function trecho() {
  const a = +inicio.value, b = Math.min(video.duration || 0, a + MAX);
  $('#trecho-txt').textContent = `trecho: ${fmt(a)} a ${fmt(b)}`;
  return [a, b];
}
inicio.addEventListener('input', () => { video.currentTime = +inicio.value; });
video.addEventListener('timeupdate', () => {
  const [a, b] = trecho();
  if (video.currentTime >= b - 0.05 || video.currentTime < a - 0.2) video.currentTime = a;
});

async function escolhe(m) {
  avisa('Baixando o vídeo…');
  try {
    await carrega(await baixa(m.url));
    avisa('');
    editor.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (e) {
    console.error(e);
    avisa('Não consegui baixar o vídeo desse post. Salve o vídeo no celular e use "Enviar um vídeo do celular".', true);
  }
}

form.addEventListener('submit', async ev => {
  ev.preventDefault();
  escolha.hidden = true; escolha.innerHTML = '';
  const id = idDoLink(link.value);
  if (!id) return avisa('Esse link não parece de um post do X. Ele tem que ter /status/ e um número.', true);
  $('#buscar').disabled = true;
  avisa('Procurando o vídeo do post…');
  try {
    const ms = await midias(id);
    if (!ms.length) return avisa('Esse post não tem vídeo nem GIF.', true);
    if (ms.length === 1) return await escolhe(ms[0]);
    avisa('Esse post tem mais de um vídeo. Toque no que você quer:');
    ms.forEach((m, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.setAttribute('aria-label', 'Vídeo ' + (i + 1));
      b.style.backgroundImage = `url("${m.capa}")`;
      b.onclick = () => { escolha.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b)); escolhe(m); };
      escolha.append(b);
    });
    escolha.hidden = false;
  } catch (e) {
    console.error(e);
    avisa('Não consegui encontrar esse post. Ele pode ser privado ou ter sido apagado. Se tiver o vídeo salvo, use "Enviar um vídeo do celular".', true);
  } finally { $('#buscar').disabled = false; }
});

$('#arquivo').addEventListener('change', async e => {
  const f = e.target.files[0];
  if (!f) return;
  escolha.hidden = true;
  try { await carrega(f); avisa(''); editor.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  catch (err) { avisa(err.message, true); }
});

const espera = (el, ev) => new Promise(ok => el.addEventListener(ev, ok, { once: true }));
async function vaiPara(t) {
  if (Math.abs(video.currentTime - t) < 0.001) return;
  const p = espera(video, 'seeked');
  video.currentTime = t;
  await p;
}

$('#gerar').addEventListener('click', async () => {
  const lado = +$('#tamanho').value, fps = +$('#fps').value;
  const [a, b] = trecho();
  const vw = video.videoWidth, vh = video.videoHeight;
  const k = Math.min(1, lado / Math.max(vw, vh));
  const w = Math.max(2, Math.round(vw * k)), h = Math.max(2, Math.round(vh * k));
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const n = Math.max(1, Math.floor((b - a) * fps));
  const atraso = Math.round(1000 / fps);
  const gerar = $('#gerar');
  gerar.disabled = true; barra.hidden = false; barra.firstElementChild.style.width = '0';
  video.pause();
  try {
    const gif = GIFEncoder();
    for (let i = 0; i < n; i++) {
      await vaiPara(Math.min(b - 0.01, a + i / fps));
      cx.drawImage(video, 0, 0, w, h);
      const { data } = cx.getImageData(0, 0, w, h);
      const pal = quantize(data, 256, { format: 'rgb565' });
      gif.writeFrame(applyPalette(data, pal, 'rgb565'), w, h, { palette: pal, delay: atraso, repeat: 0 });
      barra.firstElementChild.style.width = ((i + 1) / n * 100) + '%';
      gerar.textContent = `Criando… ${Math.round((i + 1) / n * 100)}%`;
      await new Promise(r => setTimeout(r));
    }
    gif.finish();
    blobGif = new Blob([gif.bytes()], { type: 'image/gif' });
    if (urlGif) URL.revokeObjectURL(urlGif);
    urlGif = URL.createObjectURL(blobGif);
    gifImg.src = urlGif;
    $('#baixar').href = urlGif;
    const kb = blobGif.size / 1024;
    $('#peso').textContent = `${w}×${h} · ${fmt(n / fps)} · ${kb > 1024 ? (kb / 1024).toFixed(1).replace('.', ',') + ' MB' : Math.round(kb) + ' KB'}`
      + (kb > 1500 ? ' · ficou pesada: se o WhatsApp reclamar, tente o tamanho Pequeno ou o movimento Econômico.' : '');
    const arq = new File([blobGif], 'figurinha-fendas.gif', { type: 'image/gif' });
    $('#compartilhar').hidden = !(navigator.canShare && navigator.canShare({ files: [arq] }));
    resultado.hidden = false;
    resultado.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (e) {
    console.error(e);
    avisa('Deu um erro ao criar a figurinha: ' + e.message, true);
  } finally {
    gerar.disabled = false; gerar.textContent = 'Criar figurinha'; barra.hidden = true;
    video.currentTime = a; video.play().catch(() => {});
  }
});

$('#compartilhar').addEventListener('click', () => {
  const arq = new File([blobGif], 'figurinha-fendas.gif', { type: 'image/gif' });
  navigator.share({ files: [arq] }).catch(() => {});
});

$('#nova').addEventListener('click', () => {
  resultado.hidden = true; editor.hidden = true; link.value = ''; avisa('');
  video.pause(); window.scrollTo({ top: 0, behavior: 'smooth' }); link.focus();
});

// Aceita link vindo pela URL (?u=...) ou pelo compartilhamento.
const p = new URLSearchParams(location.search).get('u');
if (p) { link.value = p; form.requestSubmit(); }
