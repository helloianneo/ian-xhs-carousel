"""把 HTML 里的每个 .slide 渲染成 1080x1440 PNG，顺带查版式规则，最后出总览。

用法：python3 render.py <index.html> [输出文件夹] [--theme dark]
输出：01.png … NN.png、总览.png（默认和 HTML 同一个文件夹）
--theme dark：渲染前给 <body> 加 data-theme="dark"，出深色版
"""
import argparse
import glob
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

SLIDE_W, SLIDE_H = 1080, 1440
VIEWPORT = {"width": SLIDE_W + 100, "height": SLIDE_H + 60}
DEFAULT_WAIT_MS = 800
SETTLE_MS = 1500
SHEET_BG = {"light": "#e4e4e7", "dark": "#3a3a40"}
SHEET_INK = {"light": "#18181b", "dark": "#f4f4f5"}

# 页面里的规则检查：返回这一页的问题列表
# [data-art] 和 .code 里面是图或代码，不查字号颜色；[data-accent] 里的橙色算同一处
LINT_JS = """
(slide) => {
  const SIZES = new Set([88, 64, 40, 32, 26, 24, 22]);
  const probe = document.createElement('i');
  probe.style.color = 'var(--orange)';
  slide.appendChild(probe);
  const ORANGE = getComputedStyle(probe).color;
  probe.remove();

  const issues = [];
  const box = slide.getBoundingClientRect();
  const skip = (el) => el.closest('[data-art], canvas, svg, .ph, .code');
  const textEls = [...slide.querySelectorAll('*')].filter((el) =>
    !skip(el) && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()));
  for (const el of textEls) {
    const cs = getComputedStyle(el);
    const text = el.textContent.trim().slice(0, 12);
    const size = Math.round(parseFloat(cs.fontSize));
    if (!SIZES.has(size)) issues.push(`字号 ${size}px 不在字号表里：「${text}」`);
    if (!/PingFang|Inter|Geist Mono/.test(cs.fontFamily)) issues.push(`字体不对：「${text}」`);
    const r = el.getBoundingClientRect();
    if (r.width && (r.left < box.left - 1 || r.right > box.right + 1 || r.top < box.top - 1 || r.bottom > box.bottom + 1))
      issues.push(`文字超出画布：「${text}」`);
    else if (r.width && r.bottom > box.bottom - 40)
      issues.push(`文字贴到画布底边了：「${text}」`);
    if (el.scrollWidth > el.clientWidth + 1 && cs.overflow !== 'visible')
      issues.push(`文字被截断：「${text}」`);
  }

  const spots = new Set();
  slide.querySelectorAll('*').forEach((el) => {
    if (el.closest('[data-art], .code')) return;
    const cs = getComputedStyle(el);
    if (cs.color === ORANGE && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()) ||
        cs.backgroundColor === ORANGE)
      spots.add(el.closest('[data-accent]') || el);
  });
  if (spots.size > 1) issues.push(`用了 ${spots.size} 处橙，一页最多一处（同一组标注外面包 data-accent）`);
  if (slide.querySelector('.ph')) issues.push('还有没换掉的占位 .ph');
  return issues;
}
"""

# 字体是按需加载的，没用到的不算；@import 整个失败时 document.fonts 里根本没有 Inter
FONT_CHECK_JS = """
() => {
  const faces = [...document.fonts];
  const bad = faces.filter((f) => f.status === 'error').map((f) => f.family);
  if (!faces.some((f) => f.family.replace(/"/g, '') === 'Inter')) bad.push('Inter、Geist Mono');
  return [...new Set(bad)];
}
"""


# 总览图标签用的中文字体：先找苹方，不在 Mac 上就找思源黑体
FONT_GLOBS = [
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font*/*/AssetData/PingFang.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/**/NotoSansCJK*.tt[cf]",
    "/usr/share/fonts/**/NotoSansSC*.[ot]t[cf]",
    "C:/Windows/Fonts/msyh.tt[cf]",
]


def find_font():
    for pattern in FONT_GLOBS:
        hits = glob.glob(pattern, recursive=True)
        if hits:
            return hits[0]
    return None


def render(html: Path, out: Path, theme: str):
    out.mkdir(parents=True, exist_ok=True)
    pages = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=2)
        page.on("console", lambda m: m.type in ("error", "warning") and print(f"  console {m.type}: {m.text}"))
        page.on("pageerror", lambda e: print(f"  页面报错: {e}"))
        page.goto(html.resolve().as_uri())
        if theme == "dark":
            page.evaluate("document.body.dataset.theme = 'dark'")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(SETTLE_MS)
        missing = page.evaluate(FONT_CHECK_JS)
        if missing:
            print(f"  注意：{', '.join(missing)} 没加载上（要联网拉 Google Fonts），数字和代码会退回苹方 / SF Mono")
        for n, el in enumerate(page.query_selector_all(".slide"), start=1):
            name = f"{n:02d}"
            layout = el.get_attribute("data-layout") or ""
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(300)
            el.evaluate("s => s.querySelectorAll('[data-poke]').forEach(e => e.dispatchEvent(new Event('poke')))")
            hover = el.get_attribute("data-hover")
            target = el.query_selector(hover) if hover else None
            if hover and not target:
                print(f"  {name}: data-hover 找不到 {hover}")
            if target:
                b = target.bounding_box()
                page.mouse.move(b["x"] + b["width"] * 0.3, b["y"] + b["height"] * 0.4)
                page.mouse.move(b["x"] + b["width"] * 0.55, b["y"] + b["height"] * 0.45, steps=20)
            else:
                page.mouse.move(2, 2)
            page.wait_for_timeout(int(el.get_attribute("data-wait") or DEFAULT_WAIT_MS))
            raw = out / f"_{name}@2x.png"
            el.screenshot(path=str(raw))
            Image.open(raw).resize((SLIDE_W, SLIDE_H), Image.LANCZOS).save(out / f"{name}.png", optimize=True)
            raw.unlink()
            issues = el.evaluate(LINT_JS)
            print(f"{name}  {layout or '(没写 data-layout)'}  {'OK' if not issues else ''}")
            for issue in issues:
                print(f"    ! {issue}")
            pages.append((name, layout))
        browser.close()
    return pages


def overview(out: Path, pages, theme: str):
    cols = 3 if len(pages) <= 9 else 4
    w, h, pad, lab = 360, 480, 40, 56
    rows = (len(pages) + cols - 1) // cols
    sheet = Image.new("RGB", (pad + cols * (w + pad), pad + rows * (h + lab + pad)), SHEET_BG[theme])
    draw = ImageDraw.Draw(sheet)
    path = find_font()
    font = ImageFont.truetype(path, 22, index=0) if path else ImageFont.load_default()
    for k, (name, layout) in enumerate(pages):
        r, c = divmod(k, cols)
        x, y = pad + c * (w + pad), pad + r * (h + lab + pad)
        sheet.paste(Image.open(out / f"{name}.png").resize((w, h), Image.LANCZOS), (x, y + lab))
        draw.text((x, y + 14), f"{name}  {layout}", fill=SHEET_INK[theme], font=font)
    sheet.save(out / "总览.png", optimize=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="把 .slide 渲染成小红书 3:4 PNG")
    parser.add_argument("html", type=Path)
    parser.add_argument("out", type=Path, nargs="?")
    parser.add_argument("--theme", choices=["light", "dark"], default="light")
    args = parser.parse_args()
    if not args.html.is_file():
        parser.exit(1, f"找不到 {args.html}\n")
    dest = args.out or args.html.parent
    result = render(args.html, dest, args.theme)
    if not result:
        parser.exit(1, "页面里没有 .slide\n")
    overview(dest, result, args.theme)
    print(f"已输出 {len(result)} 页和 总览.png 到 {dest}")
