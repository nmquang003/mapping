// Prepared local copy only: hovering never sends a question to the RAG backend.
const provinceCopy = {
  'ninh-binh': [
    '🛶 Tràng An Ninh Bình có núi đá vôi, hang động và những dòng nước uốn quanh. Bạn muốn khám phá bằng thuyền không?',
    '🏛️ Bạn thích ngắm cảnh Tràng An hay tìm hiểu dấu xưa ở cố đô Hoa Lư?',
    '⛰️ Thử khám phá Tam Cốc, Hang Múa và những câu chuyện non nước Ninh Bình nhé!'
  ],
  'ha-noi': [
    '🏙️ Hồ Hoàn Kiếm, phố cổ và Văn Miếu đang chờ bạn khám phá trong sổ tay Hà Nội.',
    '📜 Bạn muốn nghe chuyện Thăng Long hay khám phá văn hóa phố phường Hà Nội?'
  ],
  'quang-ninh': [
    '🌊 Vịnh Hạ Long mở ra một thế giới núi đá, sóng nước và những câu chuyện làng chài.',
    '🏝️ Bạn muốn khám phá Hạ Long, Yên Tử hay những hòn đảo của Quảng Ninh?'
  ],
  'lao-cai': [
    '🌾 Từ Sa Pa đến những ruộng bậc thang, Lào Cai có nhiều câu chuyện miền núi để khám phá.',
    '☁️ Bạn thích biển mây Fansipan hay sắc màu chợ phiên Bắc Hà?'
  ]
};

export function createProvinceHints(destinations) {
  const bubble = document.querySelector('#province-hint');
  const text = bubble.querySelector('.province-hint-text');
  const panel = document.querySelector('#chat-panel');
  let active = null, dismissed = null, showTimer, hideTimer, cycleTimer;
  let bubbleHovered = false;
  const lastMessages = new Map();

  function nextMessage(key, copy) {
    const previous = lastMessages.get(key);
    const choices = copy.filter(message => message !== previous);
    const message = choices[Math.floor(Math.random() * choices.length)];
    lastMessages.set(key, message);
    return message;
  }

  function stopTimers() {
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    clearInterval(cycleTimer);
  }
  function hide() {
    stopTimers();
    bubble.hidden = true;
    active = null;
    bubbleHovered = false;
  }
  function blocked() {
    return !panel.hidden || !!document.querySelector('dialog[open]');
  }
  function targetFrom(element) {
    if (!(element instanceof Element)) return null;
    const province = element.closest('#country-map [data-province]');
    if (province) return {key: province.dataset.province, name: province.dataset.name,
      destination: destinations.find(d => String(d.province) === province.dataset.province)};
    const marker = element.closest('#country-map [data-open], .destination-card[data-open]');
    const destination = marker && destinations.find(d => d.id === marker.dataset.open);
    return destination ? {key: String(destination.province), name: destination.name, destination} : null;
  }
  function preview(target) {
    clearTimeout(hideTimer);
    if (active?.key === target.key || dismissed === target.key || blocked()) return;
    stopTimers();
    bubble.hidden = true;
    active = target;
    dismissed = null;
    showTimer = setTimeout(() => {
      if (blocked()) { hide(); return; }
      const copy = [
        `👋 Bạn muốn tìm hiểu về ${target.name} à?`,
        ...(provinceCopy[target.destination?.id] || [
          `🧭 Bạn tò mò về cảnh sắc, lịch sử hay ẩm thực ${target.name}?`,
          `💚 Sổ tay ${target.name} đang được chuẩn bị. Hẹn bạn cùng khám phá những câu chuyện nơi đây nhé!`
        ])
      ];
      text.textContent = nextMessage(target.key, copy);
      bubble.hidden = false;
      cycleTimer = setInterval(() => {
        if (blocked()) { hide(); return; }
        text.textContent = nextMessage(target.key, copy);
      }, 4500);
    }, 280);
  }
  function leave() {
    if (bubble.hidden) { hide(); return; }
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    clearInterval(cycleTimer);
    active = null;
    if (!bubbleHovered && !bubble.contains(document.activeElement)) hideTimer = setTimeout(hide, 1800);
  }

  document.addEventListener('pointerover', event => {
    if (event.pointerType === 'touch' || event.buttons) return;
    const target = targetFrom(event.target);
    if (target) preview(target);
  });
  document.addEventListener('pointerout', event => {
    const from = targetFrom(event.target), to = targetFrom(event.relatedTarget);
    if (from && from.key !== to?.key) {
      dismissed = null;
      if (!to) leave();
    }
  });
  document.addEventListener('focusin', event => {
    const target = targetFrom(event.target);
    if (target) preview(target);
    if (bubble.contains(event.target)) clearTimeout(hideTimer);
  });
  document.addEventListener('focusout', event => {
    if (bubble.contains(event.target) && !bubble.contains(event.relatedTarget)) dismissed = null;
    if (!bubble.contains(event.relatedTarget) && (targetFrom(event.target) || bubble.contains(event.target))) leave();
  });
  document.addEventListener('pointerdown', event => {
    if (event.target instanceof Element && event.target.closest('#country-map')) hide();
  });
  document.addEventListener('click', event => {
    if (event.target instanceof Element && event.target.closest('[data-open], [data-province], #chat-toggle')) hide();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !bubble.hidden) { dismissed = active?.key; hide(); }
  });
  bubble.addEventListener('pointerenter', () => { bubbleHovered = true; clearTimeout(hideTimer); });
  bubble.addEventListener('pointerleave', () => { bubbleHovered = false; dismissed = null; leave(); });
  new MutationObserver(() => { if (!panel.hidden) hide(); }).observe(panel, {attributes: true, attributeFilter: ['hidden']});
  new MutationObserver(hide).observe(document.querySelector('main'), {childList: true});
  document.querySelectorAll('dialog').forEach(dialog => {
    new MutationObserver(() => { if (dialog.open) hide(); }).observe(dialog, {attributes: true, attributeFilter: ['open']});
  });
  window.addEventListener('hashchange', hide);
  window.addEventListener('blur', hide);
}
