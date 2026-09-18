"""Chuyển đổi Markdown sang Typst."""
from __future__ import annotations
from pathlib import Path
import md2typ


class ChapterConverter:
    """Chuyển đổi các chương Markdown sang Typst."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def convert_chapter(self, md_path: Path) -> str:
        """Chuyển đổi một file Markdown sang Typst."""
        md_text = md_path.read_text(encoding="utf-8")
        return md2typ.convert(md_text)

    def convert_chapters(self, chapters: list[Path], output_dir: Path) -> list[str]:
        """
        Chuyển đổi nhiều chương và lưu vào thư mục đích.
        Trả về danh sách tên file Typst đã tạo.
        """
        typ_files = []
        output_dir.mkdir(parents=True, exist_ok=True)

        for i, ch in enumerate(chapters, 1):
            typ_text = self.convert_chapter(ch)
            out_name = ch.with_suffix(".typ").name
            out_path = output_dir / out_name
            out_path.write_text(typ_text, encoding="utf-8")
            typ_files.append(out_name)

            if self.verbose:
                print(f"  ✓ [{i}/{len(chapters)}] {ch.name} → {out_name}")

        return typ_files
