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
      statusLabel.textContent = connected ? `RAG · ${status.documents} tư liệu có nguồn` : 'RAG chưa sẵn sàng';
      if (connected) {
        if (errorBox.querySelector('.chat-reconnect')) errorBox.hidden = true;
      } else showError(status.startup_error || 'Cần cấu hình API key và chỉ mục ở backend.', true);
      return connected;
    } catch {
      connected = false;
      statusLabel.textContent = 'Chưa kết nối backend RAG';
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
  const p = document.createElement('p');
  p.textContent = text;
  block.append(p);
  log.append(block);
  scrollToLatest();
  return block;
}
function renderAnswer(result) {
  const block = message('assistant', result.claims?.length ? '' : result.answer);
  const sources = new Map((result.sources || []).map(s => [s.id, s]));
  if (result.claims?.length) {
    block.replaceChildren();
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
        link.textContent = `[${sourceId}]`;
        link.title = source.title;
        p.append(link, ' ');
      }
      block.append(p);
    }
  }
  if (sources.size) {
    const details = document.createElement('details');
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
      link.textContent = `${source.id} · ${source.title}`;
      p.append(link, document.createElement('br'), `${source.publisher} · Đọc nguồn: ${source.accessed_on || 'chưa rõ'}`);
      details.append(p);
    }
    block.append(details);
  }
  scrollToLatest();
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
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 240000);
  try {
    const result = await requestJSON('/api/chat', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, signal: controller.signal,
      body: JSON.stringify({question, dataset_id: select.value || null, history: history.slice(-6)})
    });
    if (typeof result.answer !== 'string' || !Array.isArray(result.claims) || !Array.isArray(result.sources)) throw new Error(connectionError);
    statusLabel.textContent = 'RAG · Trả lời có nguồn';
    pending.remove();
    renderAnswer(result);
    history.push({role: 'user', content: question}, {role: 'assistant', content: result.answer.slice(0, 4000)});
    history = history.slice(-6);
  } catch (error) {
    pending.remove();
    const lostConnection = error.message === 'Failed to fetch' || error.message === connectionError;
    if (lostConnection) {connected = false; statusLabel.textContent = 'Chưa kết nối backend RAG';}
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
