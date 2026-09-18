"""Dựng PDF từ các file Typst."""
from __future__ import annotations
import shutil
import subprocess
from pathlib import Path


class BookBuilder:
    """Dựng PDF sách từ các file Typst."""

    def __init__(self, template_path: Path, verbose: bool = False):
        self.template_path = template_path
        self.verbose = verbose

    def create_main_typ(
        self,
        build_dir: Path,
        typ_files: list[str],
        title: str,
        subtitle: str | None = None,
        author: str | None = None,
        date: str | None = None,
    ) -> Path:
        """Tạo file main.typ."""
        template_name = self.template_path.name

        lines = [
            f'#import "{template_name}": book',
            "",
            "#show: book.with(",
            f'  title: "{title}",',
        ]

        if subtitle:
            lines.append(f'  subtitle: "{subtitle}",')
        if author:
            lines.append(f'  author: "{author}",')
        if date:
            lines.append(f'  date: "{date}",')

        lines.append(")")
        lines.append("")

        for typ_file in typ_files:
            lines.append(f'#include "{typ_file}"')

        main_path = build_dir / "main.typ"
        main_path.write_text("\n".join(lines), encoding="utf-8")
        return main_path

    def compile_to_pdf(self, main_typ: Path, output_pdf: Path) -> None:
        """Biên dịch file Typst sang PDF."""
        if self.verbose:
            print(f"  🔄 Đang biên dịch PDF...")

        # Thử dùng typst CLI trước
        if shutil.which("typst"):
            subprocess.run(
                ["typst", "compile", str(main_typ), str(output_pdf)],
                check=True,
                capture_output=not self.verbose,
            )
            return

        # Thử dùng Python package
        try:
            import typst as typst_pkg
            typst_pkg.compile(str(main_typ), output=str(output_pdf))
        except ImportError:
            raise RuntimeError(
                "Không tìm thấy Typst. Cài đặt:\n"
                "  - CLI: https://github.com/typst/typst#installation\n"
                "  - Python: pip install typst"
            )

    def build(
        self,
        book_dir: Path,
        typ_files: list[str],
        title: str,
        subtitle: str | None = None,
        author: str | None = None,
        date: str | None = None,
        output_pdf: Path | None = None,
        keep_build_dir: bool = False,
    ) -> Path:
        """
        Dựng PDF hoàn chỉnh.

        Returns:
            Path đến file PDF đã tạo.
        """
        build_dir = book_dir / "build"

        # Các file chương đã được ChapterConverter ghi vào build_dir trước
        # khi hàm này được gọi. Vì vậy không được xóa cả thư mục ở đây,
        # nếu không các file được liệt kê trong typ_files sẽ biến mất trước
        # lúc Typst biên dịch.
        build_dir.mkdir(parents=True, exist_ok=True)

        # Copy template
        shutil.copy(self.template_path, build_dir / self.template_path.name)

        # Tạo main.typ
        main_typ = self.create_main_typ(
            build_dir=build_dir,
            typ_files=typ_files,
            title=title,
            subtitle=subtitle,
            author=author,
            date=date,
        )

        # Xác định output path
        if output_pdf is None:
            safe_name = "".join(c for c in title if c.isalnum() or c in " -_").strip()
            output_pdf = book_dir / f"{safe_name or book_dir.name}.pdf"

        # Compile
        self.compile_to_pdf(main_typ, output_pdf)

        # Dọn dẹp
        if not keep_build_dir:
            shutil.rmtree(build_dir)
        elif self.verbose:
            print(f"  💾 Đã giữ lại thư mục build: {build_dir}")

        return output_pdf
