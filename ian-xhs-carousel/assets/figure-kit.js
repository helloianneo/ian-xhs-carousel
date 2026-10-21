// 代码画图的小工具：颜色、画布准备、箭头、标注、图片采样
(function () {
  // 颜色每次现读 xhs.css 的变量，深色版（body[data-theme="dark"]）跟着换
  // 渲染脚本加 --theme dark 时，主题是页面加载完才切的，画图函数用 onTheme 包一下才会重画
  function readInk() {
    const cs = getComputedStyle(document.body);
    const v = (name) => cs.getPropertyValue(name).trim();
    return {
      strong: v('--text-strong'),
      body: v('--text-body'),
      muted: v('--text-muted'),
      faint: v('--text-faint'),
      line: v('--line'),
      hairline: v('--line-soft'),
      fill: v('--fill'),
      fillStrong: v('--fill-strong'),
      surface: v('--surface'),
      accent: v('--orange'),
      accentSoft: v('--orange-200'),
      green: v('--green'),
    };
  }
  const FONT = '"PingFang SC", sans-serif';
  const NOTE_SIZE = 24;
  const ARROW_HEAD = 8;

  // 按元素实际大小和设备像素比设好画布，之后都用 CSS 像素画
  function prepare(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    const w = Math.round(rect.width);
    const h = Math.round(rect.height);
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    return { ctx, w, h };
  }

  function arrow(ctx, x0, y0, x1, y1, { color = readInk().muted, width = 2 } = {}) {
    const angle = Math.atan2(y1 - y0, x1 - x0);
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x1, y1);
    ctx.moveTo(x1 - ARROW_HEAD * Math.cos(angle - Math.PI / 6), y1 - ARROW_HEAD * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(x1, y1);
    ctx.lineTo(x1 - ARROW_HEAD * Math.cos(angle + Math.PI / 6), y1 - ARROW_HEAD * Math.sin(angle + Math.PI / 6));
    ctx.stroke();
    ctx.restore();
  }

  function label(ctx, text, x, y, { color = readInk().muted, align = 'center', baseline = 'middle', weight = 400 } = {}) {
    ctx.save();
    ctx.font = `${weight} ${NOTE_SIZE}px ${FONT}`;
    ctx.fillStyle = color;
    ctx.textAlign = align;
    ctx.textBaseline = baseline;
    ctx.fillText(text, x, y);
    ctx.restore();
  }

  // 把一张已加载的图（img / canvas）采样成 rows×cols 的亮度格，值 0 到 1，透明当 0
  function sampleImage(img, cols, rows = cols) {
    const off = document.createElement('canvas');
    off.width = cols;
    off.height = rows;
    const c = off.getContext('2d', { willReadFrequently: true });
    c.drawImage(img, 0, 0, cols, rows);
    const { data } = c.getImageData(0, 0, cols, rows);
    return Array.from({ length: rows }, (_, r) =>
      Array.from({ length: cols }, (_, col) => {
        const i = (r * cols + col) * 4;
        const lum = (0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2]) / 255;
        return lum * (data[i + 3] / 255);
      }),
    );
  }

  // 主题切换后重画：FigureKit.onTheme(draw)，页面加载时先画一次
  function onTheme(draw) {
    draw();
    new MutationObserver(draw).observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
  }

  window.FigureKit = { get INK() { return readInk(); }, prepare, arrow, label, sampleImage, onTheme };
})();
