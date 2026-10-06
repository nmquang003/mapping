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
let history = [], busy = false;

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
  block.scrollIntoView({block: 'nearest'});
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
  block.scrollIntoView({block: 'nearest'});
}
async function ask(question) {
  if (busy || !question.trim()) return;
  busy = true;
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
    const response = await fetch(apiBase + '/api/chat', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, signal: controller.signal,
      body: JSON.stringify({question, dataset_id: select.value || null, history: history.slice(-6)})
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Atlas chưa xử lý được câu hỏi.');
    pending.remove();
    renderAnswer(result);
    history.push({role: 'user', content: question}, {role: 'assistant', content: result.answer.slice(0, 4000)});
    history = history.slice(-6);
  } catch (error) {
    pending.remove();
    errorBox.textContent = error.name === 'AbortError' ? 'API đang phản hồi chậm. Bạn có thể thử lại.' : (error.message === 'Failed to fetch' ? 'Chưa kết nối được backend RAG. Hãy chạy máy chủ theo hướng dẫn.' : error.message);
    errorBox.hidden = false;
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
document.querySelector('#chat-toggle').addEventListener('click', () => {if (!panel.hidden) {syncDataset(); input.focus();}});
window.addEventListener('hashchange', syncDataset);
syncDataset();
try {
  const response = await fetch(apiBase + '/api/status');
  if (!response.ok) throw new Error();
  const status = await response.json();
  statusLabel.textContent = status.ready ? `RAG · ${status.documents} tư liệu có nguồn` : 'RAG chưa sẵn sàng';
  if (!status.ready) {
    errorBox.textContent = status.startup_error || 'Cần tạo chỉ mục và cấu hình API ở backend.';
    errorBox.hidden = false;
  }
} catch {
  statusLabel.textContent = 'Chưa kết nối backend RAG';
}
