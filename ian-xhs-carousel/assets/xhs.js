// 版式库的小脚本：把 <i class="ic" data-i="名字"> 换成线框图标，给没填内容的 .ph 标上尺寸
(function () {
  // 32 格，线宽 2.5，圆头圆角，只用线框
  const ICONS = {
    close: '<path d="M8 8L24 24M24 8L8 24"/>',
    check: '<path d="M7 16.5L13 22.5L25 10"/>',
    cross: '<path d="M9 9L23 23M23 9L9 23"/>',
    'arrow-up': '<path d="M16 26V7M8 14L16 6L24 14"/>',
    'chevron-down': '<path d="M9 12.5L16 19.5L23 12.5"/>',
    'chevron-right': '<path d="M12.5 9L19.5 16L12.5 23"/>',
    sparkle: '<path d="M16 5C16.9 10.6 21.4 15.1 27 16C21.4 16.9 16.9 21.4 16 27C15.1 21.4 10.6 16.9 5 16C10.6 15.1 15.1 10.6 16 5Z"/>',
    info: '<circle cx="16" cy="16" r="11"/><path d="M16 15V22M16 10.5V11"/>',
    copy: '<rect x="11" y="11" width="15" height="15" rx="3"/><path d="M21 11V8a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h3"/>',
    paperclip: '<path d="M24 15L15.5 23.5a5 5 0 0 1-7-7L17 8a3.33 3.33 0 0 1 4.7 4.7L13.1 21.3a1.67 1.67 0 0 1-2.4-2.4L18 11.6"/>',
    code: '<path d="M11 10L5 16L11 22M21 10L27 16L21 22"/>',
    search: '<circle cx="14" cy="14" r="8"/><path d="M20 20L26 26"/>',
  };

  document.querySelectorAll('.ic[data-i]').forEach((el) => {
    const body = ICONS[el.dataset.i];
    if (!body) {
      console.warn(`没有这个图标：${el.dataset.i}`);
      return;
    }
    el.innerHTML = `<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;
  });

  // 还没换成真内容的占位，标出实际像素，备图时照着截
  document.querySelectorAll('.ph').forEach((el) => {
    const { width, height } = el.getBoundingClientRect();
    el.dataset.size = width < 120 ? '图' : `图 ${Math.round(width)}×${Math.round(height)}`;
  });

  window.XHS_ICONS = Object.keys(ICONS);
})();
