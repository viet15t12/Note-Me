#!/usr/bin/env python3
"""
build_book.py — Entry point cho Book Builder
Công cụ dựng PDF sách kỹ thuật từ Markdown + Typst
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from book_builder import ui
from book_builder.builder import BookBuilder
from book_builder.config import BookConfig
from book_builder.converter import ChapterConverter
from book_builder.scanner import BookScanner

ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = ROOT / "template.typ"


def build_interactive() -> None:
    """Chế độ tương tác với TUI."""
    # 1. Quét sách
    scanner = BookScanner(ROOT)
    books = scanner.find_books()

    if not books:
        ui.error_message("Không tìm thấy sách nào trong thư mục hiện tại.")
        sys.exit(1)

    # 2. Chọn sách
    book = ui.select_book(books)
    if not book:
        sys.exit("Đã hủy.")

    # 3. Chọn chế độ dựng
    mode = ui.quick_build_menu()
    if mode == "exit" or not mode:
        sys.exit("Đã hủy.")

    # 4. Chọn chương
    if mode == "quick_all":
        chapters = book.chapters
    else:
        chapters = ui.select_chapters(book)
        if not chapters:
            sys.exit("Chưa chọn chương nào.")

    # 5. Chọn có giữ lại nguồn Typst hay không
    keep_build_dir = ui.confirm_keep_typst()

    # 6. Đọc config
    config = BookConfig.load(book.path)
    title = config.title or book.name
    author = config.author

    # 7. Hiển thị thông tin
    ui.show_build_info(
        book=book,
        chapter_count=len(chapters),
        title=title,
        author=author,
    )

    # 8. Build
    try:
        # Progress của Rich đã đảm nhiệm phần hiển thị trong chế độ TUI;
        # tắt log dòng để giao diện không bị chen ngang.
        converter = ChapterConverter(verbose=False)
        builder = BookBuilder(TEMPLATE_PATH, verbose=False)

        with ui.show_progress("Đang chuyển đổi Markdown → Typst...") as progress:
            task = progress.add_task("convert", total=len(chapters))
            typ_files = converter.convert_chapters(chapters, book.path / "build")
            progress.update(task, completed=len(chapters))

        with ui.show_progress("Đang biên dịch PDF...") as progress:
            task = progress.add_task("compile", total=1)
            pdf_path = builder.build(
                book_dir=book.path,
                typ_files=typ_files,
                title=title,
                subtitle=config.subtitle,
                author=author,
                date=config.date,
                keep_build_dir=keep_build_dir,
            )
            progress.update(task, completed=1)

        ui.success_message(
            pdf_path,
            typst_dir=book.path / "build" if keep_build_dir else None,
        )

    except Exception as e:
        ui.error_message(f"Lỗi khi dựng sách: {e}")
        sys.exit(1)


def build_cli(args: argparse.Namespace) -> None:
    """Chế độ CLI (không tương tác)."""
    scanner = BookScanner(ROOT)
    books = scanner.find_books()

    if not books:
        ui.error_message("Không tìm thấy sách nào.")
        sys.exit(1)

    # Tìm sách theo tên
    if args.book:
        matches = [b for b in books if b.name == args.book]
        if not matches:
            ui.error_message(f"Không tìm thấy sách '{args.book}'")
            sys.exit(1)
        book = matches[0]
    else:
        book = books[0] if len(books) == 1 else None
        if not book:
            ui.error_message("Cần chỉ định tên sách khi dùng chế độ CLI")
            sys.exit(1)

    # Chọn chương
    if args.chapters == "all":
        chapters = book.chapters
    elif args.chapters:
        indices = []
        for part in args.chapters.split(","):
            part = part.strip()
            if "-" in part:
                a, b = map(int, part.split("-", 1))
                indices.extend(range(a, b + 1))
            else:
                indices.append(int(part))
        chapters = [
            book.chapters[i - 1] for i in indices if 1 <= i <= len(book.chapters)
        ]
    else:
        chapters = book.chapters

    # Load config
    config = BookConfig.load(book.path).merge_with_args(
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        date=args.date,
    )

    # Build
    try:
        converter = ChapterConverter(verbose=args.verbose)
        builder = BookBuilder(TEMPLATE_PATH, verbose=args.verbose)

        typ_files = converter.convert_chapters(chapters, book.path / "build")

        pdf_path = builder.build(
            book_dir=book.path,
            typ_files=typ_files,
            title=config.title or book.name,
            subtitle=config.subtitle,
            author=config.author,
            date=config.date,
            output_pdf=args.output,
            keep_build_dir=args.keep_build_dir,
        )

        ui.success_message(
            pdf_path,
            typst_dir=book.path / "build" if args.keep_build_dir else None,
        )

    except Exception as e:
        ui.error_message(f"Lỗi: {e}")
        sys.exit(1)


def main() -> None:
    """Entry point chính."""
    parser = argparse.ArgumentParser(
        description="📖 Dựng PDF sách từ Markdown + Typst",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  # Chế độ tương tác (TUI)
  python build_book.py

  # Chế độ CLI
  python build_book.py "THE LINUX COMMAND LINE" --chapters all
  python build_book.py "THE LINUX COMMAND LINE" --chapters 1,2,3
  python build_book.py "THE LINUX COMMAND LINE" --chapters 1-5 --output mybook.pdf
        """,
    )

    parser.add_argument(
        "book",
        nargs="?",
        help="Tên thư mục sách (bỏ qua để dùng TUI)",
    )
    parser.add_argument(
        "--chapters",
        help="Chương cần dựng: 1,2,3 | 1-5 | all",
    )
    parser.add_argument("--title", help="Tiêu đề sách")
    parser.add_argument("--subtitle", help="Phụ đề")
    parser.add_argument("--author", help="Tác giả")
    parser.add_argument("--date", help="Ngày xuất bản")
    parser.add_argument("--output", type=Path, help="File PDF đầu ra")
    parser.add_argument(
        "--keep-build-dir",
        action="store_true",
        help="Giữ lại thư mục .build",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Hiển thị chi tiết",
    )

    args = parser.parse_args()

    # Chọn chế độ
    if args.book or args.chapters:
        build_cli(args)
    else:
        build_interactive()


if __name__ == "__main__":
    main()
