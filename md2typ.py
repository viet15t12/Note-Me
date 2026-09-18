"""
md2typ.py — chuyển đổi Markdown (.md) sang cú pháp Typst (.typ)

Không phụ thuộc thư viện ngoài (không cần pandoc). Xử lý theo khối
(block-level) rồi theo dòng (inline-level). Bao phủ đủ dùng cho sách kỹ
thuật: heading, đoạn văn, in đậm/nghiêng, code inline/code block, link,
ảnh, danh sách có thứ tự/không thứ tự, blockquote, bảng pipe, hr.

Dùng độc lập:
    python md2typ.py chapter_1.md -o chapter_1.typ

Hoặc import:
    from md2typ import convert
    typst_src = convert(markdown_text)
"""

from __future__ import annotations
import re
import sys
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Inline-level conversion (áp dụng cho phần text bên trong 1 đoạn/dòng)
# ---------------------------------------------------------------------------

# Giữ chỗ cho các đoạn code inline / link / ảnh để không bị các rule khác
# (bold, italic...) phá cú pháp bên trong.
_PLACEHOLDER_RE = re.compile(r"\x00(\d+)\x00")


def _protect_inline_code(text: str, store: list[str]) -> str:
    def repl(m: re.Match) -> str:
        store.append(f"`{m.group(1)}`")  # Typst dùng cú pháp backtick giống Markdown
        return f"\x00{len(store) - 1}\x00"

    return re.sub(r"`([^`]+)`", repl, text)


def _convert_images_and_links(text: str, store: list[str]) -> str:
    # Ảnh: ![alt](path)  ->  #image("path", alt: "alt")
    def img_repl(m: re.Match) -> str:
        alt, path = m.group(1), m.group(2)
        alt_esc = alt.replace('"', '\\"')
        store.append(f'#image("{path}", alt: "{alt_esc}")')
        return f"\x00{len(store) - 1}\x00"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img_repl, text)

    # Link: [text](url)  ->  #link("url")[text]
    def link_repl(m: re.Match) -> str:
        label, url = m.group(1), m.group(2)
        store.append(f'#link("{url}")[{label}]')
        return f"\x00{len(store) - 1}\x00"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    return text


def _convert_emphasis(text: str) -> str:
    # Escape các ký tự có ý nghĩa đặc biệt trong Typst mà văn bản thường
    # không cố ý dùng: # (hàm), @ (tham chiếu), $ (toán)
    text = re.sub(r"(?<!\x00)([#@$])", r"\\\1", text)

    # Dùng placeholder tạm để bold đã chuyển đổi không bị pass italic bắt lại
    bold_store: list[str] = []

    def bold_repl(m: re.Match) -> str:
        bold_store.append(f"*{m.group(1)}*")
        return f"\x01{len(bold_store) - 1}\x01"

    # **bold** hoặc __bold__  ->  *bold*   (Typst: *...* = đậm)
    text = re.sub(r"\*\*(.+?)\*\*", bold_repl, text)
    text = re.sub(r"__(.+?)__", bold_repl, text)

    # *italic* hoặc _italic_  ->  _italic_   (Typst: _..._ = nghiêng)
    text = re.sub(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)", r"_\1_", text)
    text = re.sub(r"(?<!_)_(?!_)([^_\n]+?)_(?!_)", r"_\1_", text)

    # khôi phục bold
    def restore_bold(m: re.Match) -> str:
        return bold_store[int(m.group(1))]

    text = re.sub(r"\x01(\d+)\x01", restore_bold, text)

    return text


def _restore_placeholders(text: str, store: list[str]) -> str:
    def repl(m: re.Match) -> str:
        return store[int(m.group(1))]

    prev = None
    while prev != text:
        prev = text
        text = _PLACEHOLDER_RE.sub(repl, text)
    return text


def convert_inline(text: str) -> str:
    store: list[str] = []
    text = _protect_inline_code(text, store)
    text = _convert_images_and_links(text, store)
    text = _convert_emphasis(text)
    text = _restore_placeholders(text, store)
    return text


# ---------------------------------------------------------------------------
# Block-level conversion
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})\s*$")
_UL_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
_OL_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
_QUOTE_RE = re.compile(r"^>\s?(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
_FENCE_RE = re.compile(r"^(```|~~~)(\w*)\s*$")


def _split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def convert(md_text: str) -> str:
    lines = md_text.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # --- code fence: giữ nguyên nội dung (Typst hiểu cùng cú pháp ```lang)
        fence_m = _FENCE_RE.match(line)
        if fence_m:
            fence_char = fence_m.group(1)
            lang = fence_m.group(2)
            out.append(f"```{lang}")
            i += 1
            while i < n and not lines[i].startswith(fence_char):
                out.append(lines[i])
                i += 1
            out.append("```")
            i += 1  # bỏ qua dòng fence đóng
            continue

        # --- bảng pipe
        if "|" in line and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1] or ""):
            header = _split_table_row(line)
            ncols = len(header)
            i += 2  # bỏ qua dòng header + dòng phân cách
            rows = [header]
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_table_row(lines[i]))
                i += 1
            out.append(f"#table(")
            out.append(f"  columns: {ncols},")
            out.append("  table.header(")
            out.append(
                "    " + ", ".join(f"[{convert_inline(c)}]" for c in rows[0]) + ","
            )
            out.append("  ),")
            for row in rows[1:]:
                cells = row + [""] * (ncols - len(row))
                out.append(
                    "  " + ", ".join(f"[{convert_inline(c)}]" for c in cells[:ncols]) + ","
                )
            out.append(")")
            out.append("")
            continue

        # --- heading
        h = _HEADING_RE.match(line)
        if h:
            level = len(h.group(1))
            out.append("=" * level + " " + convert_inline(h.group(2).strip()))
            i += 1
            continue

        # --- hr
        if _HR_RE.match(line):
            out.append("#line(length: 100%)")
            i += 1
            continue

        # --- blockquote (gộp các dòng liên tiếp bắt đầu bằng '>')
        if _QUOTE_RE.match(line):
            buf = []
            while i < n and (_QUOTE_RE.match(lines[i]) or lines[i].strip() == ""):
                if lines[i].strip() == "":
                    if buf and buf[-1] != "":
                        buf.append("")
                    i += 1
                    continue
                buf.append(_QUOTE_RE.match(lines[i]).group(1))
                i += 1
            content = " ".join(b for b in buf if b != "").strip()
            out.append(f"#quote(block: true)[{convert_inline(content)}]")
            out.append("")
            continue

        # --- danh sách không thứ tự
        if _UL_RE.match(line):
            while i < n and (_UL_RE.match(lines[i]) or (lines[i].strip() == "" and i + 1 < n and _UL_RE.match(lines[i + 1] or ""))):
                if lines[i].strip() == "":
                    i += 1
                    continue
                m = _UL_RE.match(lines[i])
                indent = len(m.group(1))
                depth = indent // 2  # 2 spaces = 1 cấp lồng, tuỳ chỉnh nếu cần
                out.append("  " * depth + "- " + convert_inline(m.group(2)))
                i += 1
            out.append("")
            continue

        # --- danh sách có thứ tự
        if _OL_RE.match(line):
            while i < n and (_OL_RE.match(lines[i]) or (lines[i].strip() == "" and i + 1 < n and _OL_RE.match(lines[i + 1] or ""))):
                if lines[i].strip() == "":
                    i += 1
                    continue
                m = _OL_RE.match(lines[i])
                indent = len(m.group(1))
                depth = indent // 2
                out.append("  " * depth + "+ " + convert_inline(m.group(2)))
                i += 1
            out.append("")
            continue

        # --- dòng trống
        if line.strip() == "":
            out.append("")
            i += 1
            continue

        # --- đoạn văn thường: gộp các dòng liên tục thành 1 đoạn
        buf = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not _HEADING_RE.match(lines[i]) \
                and not _UL_RE.match(lines[i]) and not _OL_RE.match(lines[i]) \
                and not _QUOTE_RE.match(lines[i]) and not _FENCE_RE.match(lines[i]) \
                and not _HR_RE.match(lines[i]):
            buf.append(lines[i])
            i += 1
        out.append(convert_inline(" ".join(buf)))
        out.append("")

    # gộp nhiều dòng trống liên tiếp thành 1
    result_lines: list[str] = []
    for l in out:
        if l == "" and result_lines and result_lines[-1] == "":
            continue
        result_lines.append(l)

    return "\n".join(result_lines).strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Chuyển đổi 1 file Markdown sang Typst")
    ap.add_argument("input", type=Path, help="File .md đầu vào")
    ap.add_argument("-o", "--output", type=Path, help="File .typ đầu ra (mặc định: cùng tên, đổi đuôi)")
    args = ap.parse_args()

    md_text = args.input.read_text(encoding="utf-8")
    typ_text = convert(md_text)

    out_path = args.output or args.input.with_suffix(".typ")
    out_path.write_text(typ_text, encoding="utf-8")
    print(f"Đã ghi: {out_path}")


if __name__ == "__main__":
    main()
