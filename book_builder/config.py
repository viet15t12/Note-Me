"""Quản lý cấu hình sách."""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BookConfig:
    """Cấu hình một cuốn sách."""
    title: Optional[str] = None
    subtitle: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None

    @classmethod
    def load(cls, book_dir: Path) -> "BookConfig":
        """Đ đọc cấu hình từ book.json."""
        cfg_path = book_dir / "book.json"
        if cfg_path.exists():
            try:
                data = json.loads(cfg_path.read_text(encoding="utf-8"))
                return cls(**data)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"️  Lỗi đọc book.json: {e}")
        return cls()

    def save(self, book_dir: Path) -> None:
        """Lưu cấu hình vào book.json."""
        cfg_path = book_dir / "book.json"
        data = {k: v for k, v in asdict(self).items() if v is not None}
        cfg_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def merge_with_args(
        self,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        author: Optional[str] = None,
        date: Optional[str] = None,
    ) -> "BookConfig":
        """Gộp với tham số từ CLI (CLI ưu tiên hơn)."""
        return BookConfig(
            title=title or self.title,
            subtitle=subtitle or self.subtitle,
            author=author or self.author,
            date=date or self.date,
        )
