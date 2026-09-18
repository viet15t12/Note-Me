"""Quét và phát hiện các sách trong thư mục."""
from __future__ import annotations
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class BookInfo:
    """Thông tin một cuốn sách."""
    path: Path
    name: str
    chapters: list[Path]
    chapter_count: int

    def __str__(self) -> str:
        return f"📚 {self.name} ({self.chapter_count} chương)"


class BookScanner:
    """Quét thư mục để tìm các cuốn sách."""

    IGNORE_DIRS = {
        ".git", "__pycache__", ".build", "build", "output", "node_modules", ".venv"
    }

    def __init__(self, root: Path):
        self.root = root

    @staticmethod
    def natural_key(path: Path) -> list:
        """Sắp xếp tự nhiên: chapter_2 trước chapter_10."""
        return [int(t) if t.isdigit() else t.lower()
                for t in re.split(r"(\d+)", path.stem)]

    def find_books(self) -> list[BookInfo]:
        """Tìm tất cả sách trong thư mục gốc."""
        books = []
        for p in sorted(self.root.iterdir()):
            if self._is_book_directory(p):
                chapters = self._find_chapters(p)
                if chapters:
                    books.append(BookInfo(
                        path=p,
                        name=p.name,
                        chapters=chapters,
                        chapter_count=len(chapters)
                    ))
        return books

    def _is_book_directory(self, path: Path) -> bool:
        """Kiểm tra xem thư mục có phải là sách không."""
        if not path.is_dir():
            return False
        if path.name in self.IGNORE_DIRS:
            return False
        if path.name.startswith("."):
            return False
        return True

    def _find_chapters(self, book_dir: Path) -> list[Path]:
        """Tìm tất cả chương (file .md) trong thư mục sách."""
        files = list(book_dir.glob("*.md"))
        return sorted(files, key=self.natural_key)

    def scan_and_display(self) -> None:
        """Quét và hiển thị danh sách sách tìm thấy."""
        books = self.find_books()
        if not books:
            print("❌ Không tìm thấy sách nào.")
            return

        print("\n" + "="*60)
        print(" CÁC SÁCH ĐÃ TÌM THẤY")
        print("="*60)
        for i, book in enumerate(books, 1):
            print(f"  {i}. {book}")
        print("="*60 + "\n")
