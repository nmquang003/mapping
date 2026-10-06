const panel = document.querySelector('#chat-panel');
const form = document.querySelector('#chat-form');
const input = document.querySelector('#chat-question');
const select = document.querySelector('#chat-dataset');
const log = document.querySelector('#chat-messages');
const errorBox = document.querySelector('#chat-error');
const statusLabel = document.querySelector('#chat-status');
const submit = document.querySelector('#chat-submit');
const localPreview = ['127.0.0.1', 'localhost'].includes(location.hostname) && location.port === '4321';
const apiBase = localPreview ? `http://${location.hostname}:4322` : '';
let history = [], busy = false, connected = false, healthRequest = null;
const imageDialog = document.querySelector('#chat-image-dialog');
let imageTrigger = null;
const connectionError = 'Chưa kết nối được máy chủ chatbot. Vui lòng thử kết nối lại; nếu vẫn lỗi, tải lại trang.';
function showError(text, reconnect = false) {
  errorBox.replaceChildren(document.createTextNode(text));
  if (reconnect) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'chat-reconnect';
    button.textContent = 'Kết nối lại';
    button.addEventListener('click', () => refreshConnection());
    errorBox.append(' ', button);
  }
  errorBox.hidden = false;
}
async function requestJSON(path, options = {}) {
  const response = await fetch(apiBase + path, {cache: 'no-store', ...options});
  const type = response.headers.get('Content-Type') || '';
  if (!type.toLowerCase().includes('application/json')) {
    connected = false;
    throw new Error(connectionError);
  }
  let result;
  try {result = await response.json();} catch {
    connected = false;
    throw new Error(connectionError);
  }
  if (!result || typeof result !== 'object' || Array.isArray(result)) throw new Error(connectionError);
  if (!response.ok) throw new Error(typeof result.error === 'string' ? result.error : 'Máy chủ chatbot tạm thời chưa xử lý được câu hỏi.');
  return result;
}
async function refreshConnection() {
  if (healthRequest) return healthRequest;
  healthRequest = (async () => {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    try {
      const status = await requestJSON('/api/status', {signal: controller.signal});
      if (typeof status.ready !== 'boolean' || !Number.isInteger(status.documents)) throw new Error(connectionError);
      connected = status.ready && status.api_configured;
      statusLabel.textContent = connected ? 'Sẵn sàng cùng bạn khám phá' : 'Đang chờ kết nối';
      panel.classList.toggle('is-connected', !!connected);
      if (connected) {
        if (errorBox.querySelector('.chat-reconnect')) errorBox.hidden = true;
      } else showError(status.startup_error || 'Cần cấu hình API key và chỉ mục ở backend.', true);
      return connected;
    } catch {
      connected = false;
      statusLabel.textContent = 'Chưa kết nối được hướng dẫn viên';
      panel.classList.remove('is-connected');
      showError(connectionError, true);
      return false;
    } finally {clearTimeout(timeout);}
  })();
  try {return await healthRequest;} finally {healthRequest = null;}
}

function scrollToLatest() {
  requestAnimationFrame(() => {const body = panel.querySelector('.chat-body'); body.scrollTop = body.scrollHeight;});
}
function openChat() {
  panel.hidden = false;
  document.querySelector('#chat-toggle').setAttribute('aria-expanded', 'true');
  input.focus();
}
function currentDataset() {
  return location.hash.match(/^#\/dia-phuong\/([a-z-]+)/)?.[1] || '';
}
function syncDataset() {
  const id = currentDataset();
  if ([...select.options].some(option => option.value === id)) select.value = id;
}
function message(role, text) {
  const block = document.createElement('div');
  block.className = 'chat-message ' + role;
  const meta = document.createElement('div');
  meta.className = 'chat-message-meta';
  meta.textContent = role === 'user' ? 'Bạn' : '✧ Atlas';
  const content = document.createElement('div');
  content.className = 'chat-message-content';
  const p = document.createElement('p');
  p.textContent = text;
  content.append(p);
  block.append(meta, content);
  log.append(block);
  scrollToLatest();
  return block;
}
function renderIllustrations(content, illustrations) {
  const images = (Array.isArray(illustrations) ? illustrations : []).filter(image =>
    image && typeof image.src === 'string' && /^assets\/ai\/[a-z0-9/-]+\.(webp|jpg|png)$/.test(image.src)
    && typeof image.name === 'string' && typeof image.alt === 'string').slice(0, 3);
  if (!images.length) return;
  const gallery = document.createElement('div');
  gallery.className = 'chat-gallery';
  gallery.setAttribute('aria-label', 'Ảnh minh họa địa danh');
  for (const image of images) {
    const figure = document.createElement('figure');
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'chat-image-button';
    button.setAttribute('aria-label', `Xem ảnh lớn ${image.name}`);
    const img = document.createElement('img');
    img.src = image.src;
    img.alt = image.alt;
    img.loading = 'lazy';
    img.decoding = 'async';
    const badge = document.createElement('span');
    badge.className = 'chat-image-badge';
    badge.textContent = 'Ảnh minh họa AI';
    const zoom = document.createElement('span');
    zoom.className = 'chat-image-zoom';
    zoom.textContent = '↗';
    zoom.setAttribute('aria-hidden', 'true');
    button.append(img, badge, zoom);
    const caption = document.createElement('figcaption');
    const name = document.createElement('strong');
    name.textContent = image.name;
    const note = document.createElement('span');
    note.textContent = 'Không phải ảnh tư liệu · Bấm để xem lớn';
    caption.append(name, note);
    figure.append(button, caption);
    img.addEventListener('error', () => {
      button.disabled = true;
      img.hidden = true;
      zoom.textContent = 'Ảnh tạm thời chưa tải được';
      zoom.classList.add('chat-image-unavailable');
    }, {once: true});
    button.addEventListener('click', () => {
      imageTrigger = button;
      document.querySelector('#chat-image-full').src = image.src;
      document.querySelector('#chat-image-full').alt = image.alt;
      document.querySelector('#chat-image-title').textContent = image.name;
      imageDialog.showModal();
    });
    gallery.append(figure);
  }
  content.append(gallery);
}
function renderAnswer(result) {
  const block = message('assistant', result.claims?.length ? '' : result.answer);
  const content = block.querySelector('.chat-message-content');
  const sources = new Map((result.sources || []).map(s => [s.id, s]));
  const sourceNumbers = new Map([...sources.keys()].map((id, index) => [id, index + 1]));
  if (result.claims?.length) {
    content.replaceChildren();
    for (const claim of result.claims) {
      const p = document.createElement('p');
      p.textContent = claim.text + ' ';
      for (const sourceId of claim.source_ids || []) {
        const source = sources.get(sourceId);
        if (!source || !/^https?:\/\//i.test(source.url)) continue;
        const link = document.createElement('a');
        link.href = source.url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.className = 'chat-citation';
        link.textContent = `[${sourceNumbers.get(sourceId)}]`;
        link.title = source.title;
        p.append(link, ' ');
      }
      content.append(p);
    }
  }
  renderIllustrations(content, result.illustrations);
  if (typeof result.illustration_note === 'string') {
    const note = document.createElement('p');
    note.className = 'chat-illustration-note';
    note.textContent = result.illustration_note;
    content.append(note);
  }
  if (sources.size) {
    const details = document.createElement('details');
    details.className = 'chat-sources';
    const summary = document.createElement('summary');
    summary.textContent = `Xem ${sources.size} nguồn tham khảo`;
    details.append(summary);
    for (const source of sources.values()) {
      if (!/^https?:\/\//i.test(source.url)) continue;
      const p = document.createElement('p');
      const link = document.createElement('a');
      link.href = source.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = `${sourceNumbers.get(source.id)}. ${source.title}`;
      p.append(link, document.createElement('br'), `${source.publisher} · Đọc nguồn: ${source.accessed_on || 'chưa rõ'}`);
      details.append(p);
    }
    content.append(details);
  }
  requestAnimationFrame(() => {
    const body = panel.querySelector('.chat-body');
    body.scrollTop += block.getBoundingClientRect().top - body.getBoundingClientRect().top - 12;
  });
}
async function ask(question) {
  if (busy || !question.trim()) return;
  busy = true;
  if (!connected && !await refreshConnection()) {
    busy = false;
    return;
  }
  submit.disabled = true;
  input.disabled = true;
  errorBox.hidden = true;
  message('user', question);
  input.value = '';
  const pending = message('assistant', 'Đang tìm tư liệu và đối chiếu câu trả lời…');
  pending.classList.add('pending');
  const dots = document.createElement('span');
  dots.className = 'chat-typing';
  dots.setAttribute('aria-hidden', 'true');
  for (let index = 0; index < 3; index++) dots.append(document.createElement('i'));
  pending.querySelector('.chat-message-content').prepend(dots);
  document.querySelector('#chat-destinations').hidden = true;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 240000);
  try {
    const result = await requestJSON('/api/chat', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, signal: controller.signal,
      body: JSON.stringify({question, dataset_id: select.value || null, history: history.slice(-6)})
    });
    if (typeof result.answer !== 'string' || !Array.isArray(result.claims) || !Array.isArray(result.sources)) throw new Error(connectionError);
    statusLabel.textContent = 'Đang đồng hành cùng bạn';
    pending.remove();
    renderAnswer(result);
    history.push({role: 'user', content: question}, {role: 'assistant', content: result.answer.slice(0, 4000)});
    history = history.slice(-6);
  } catch (error) {
    pending.remove();
    const lostConnection = error.message === 'Failed to fetch' || error.message === connectionError;
    if (lostConnection) {connected = false; statusLabel.textContent = 'Chưa kết nối được hướng dẫn viên'; panel.classList.remove('is-connected');}
    showError(error.name === 'AbortError' ? 'API đang phản hồi chậm. Bạn có thể thử lại.' : (lostConnection ? connectionError : error.message), lostConnection);
    input.value = question;
  } finally {
    clearTimeout(timeout);
    busy = false;
    submit.disabled = false;
    input.disabled = false;
    input.focus();
  }
}
form.addEventListener('submit', event => {event.preventDefault(); ask(input.value.trim());});
input.addEventListener('keydown', event => {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {event.preventDefault(); form.requestSubmit();}
});
document.addEventListener('click', event => {
  const askButton = event.target.closest('[data-ask-atlas]');
  const suggestion = event.target.closest('[data-chat-question]');
  if (askButton) {
    select.value = askButton.dataset.chatProvince;
    openChat();
    input.value = `Giới thiệu về ${askButton.dataset.askAtlas}.`;
  }
  if (suggestion) {openChat(); ask(suggestion.dataset.chatQuestion);}
});
document.querySelector('#chat-toggle').addEventListener('click', () => {if (!panel.hidden) {syncDataset(); input.focus(); refreshConnection();}});
window.addEventListener('hashchange', syncDataset);
window.addEventListener('resize', () => {if (!panel.hidden) scrollToLatest();});
syncDataset();
refreshConnection();

const expand = document.querySelector('#chat-expand');
expand.addEventListener('click', () => {
  const expanded = panel.classList.toggle('is-expanded');
  expand.setAttribute('aria-pressed', String(expanded));
  expand.setAttribute('aria-label', expanded ? 'Thu gọn khung chat' : 'Mở rộng khung chat');
});
imageDialog.querySelector('.chat-image-close').addEventListener('click', () => imageDialog.close());
imageDialog.addEventListener('close', () => imageTrigger?.focus());
imageDialog.addEventListener('click', event => {
  if (event.target !== imageDialog) return;
  const rect = imageDialog.getBoundingClientRect();
  if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) imageDialog.close();
});
