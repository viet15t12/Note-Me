"""Giao diện TUI tương tác."""

from __future__ import annotations

from pathlib import Path

import questionary
from questionary import Choice
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table

from .scanner import BookInfo

console = Console()

MENU_STYLE = questionary.Style(
    [
        ("qmark", "fg:#38bdf8 bold"),
        ("question", "bold"),
        ("answer", "fg:#22c55e bold"),
        ("pointer", "fg:#22c55e bold"),
        ("highlighted", "fg:#38bdf8 bold"),
        ("selected", "fg:#22c55e"),
        ("checked", "fg:#22c55e bold"),
    ]
)


def select_book(books: list[BookInfo]) -> BookInfo | None:
    """Menu chọn sách."""
    if not books:
        return None

    choices = [
        Choice(
            title=f"{book}",
            value=book,
        )
        for book in books
    ]

    return questionary.select(
        "📚 Chọn sách cần dựng:",
        choices=choices,
        style=MENU_STYLE,
    ).ask()


def select_chapters(book: BookInfo) -> list | None:
    """Menu chọn chương (checkbox)."""
    choices = [Choice(title=f"📖 {ch.name}", value=ch) for ch in book.chapters]

    # Thêm option chọn tất cả
    choices.insert(0, Choice(title="✨ Chọn TẤT CẢ", value="ALL"))

    selected = questionary.checkbox(
        "📑 Chọn chương (SPACE để chọn, ENTER để xác nhận):",
        choices=choices,
        style=MENU_STYLE,
    ).ask()

    if selected is None:
        return None

    if "ALL" in selected:
        return book.chapters

    return selected


def quick_build_menu() -> str:
    """Menu chọn chế độ dựng nhanh."""
    return questionary.select(
        "⚡ Chế độ dựng:",
        choices=[
            Choice(title="🚀 Dựng ngay (chọn tất cả chương)", value="quick_all"),
            Choice(title="🎯 Chọn chương cụ thể", value="select_chapters"),
            Choice(title="❌ Thoát", value="exit"),
        ],
        style=MENU_STYLE,
    ).ask()


def confirm_keep_typst() -> bool:
    """Hỏi người dùng có muốn giữ các file Typst trung gian không."""
    answer = questionary.confirm(
        "💾 Giữ lại file Typst (.typ) sau khi dựng?",
        default=True,
        style=MENU_STYLE,
    ).ask()
    return bool(answer)


def show_build_info(
    book: BookInfo,
    chapter_count: int,
    title: str,
    author: str | None = None,
) -> None:
    """Hiển thị thông tin trước khi dựng."""
    details = Table.grid(padding=(0, 2))
    details.add_column(style="dim", justify="right")
    details.add_column(style="bold white")
    details.add_row("Dự án", escape(book.name))
    details.add_row("Tác giả", escape(author or "Chưa thiết lập"))
    details.add_row("Chương", f"{chapter_count}/{book.chapter_count}")

    console.print(
        Panel.fit(
            details,
            title=f"[bold cyan]{escape(title)}[/bold cyan]",
            subtitle="[dim]Sẵn sàng để dựng[/dim]",
            border_style="cyan",
            padding=(1, 3),
        )
    )


def show_progress(message: str) -> Progress:
    """Tạo progress bar."""
    return Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn(f"[bold cyan]{escape(message)}[/bold cyan]"),
        BarColumn(bar_width=28, complete_style="green", finished_style="green"),
        TaskProgressColumn(),
        console=console,
    )


def success_message(pdf_path: Path, typst_dir: Path | None = None) -> None:
    """Hiển thị thông báo thành công."""
    details = (
        f"[bold green]✓ PDF đã sẵn sàng[/bold green]\n"
        f"[dim]{escape(str(pdf_path.absolute()))}[/dim]"
    )
    if typst_dir is not None:
        details += (
            "\n\n[bold cyan]Typst[/bold cyan]\n"
            f"[dim]{escape(str(typst_dir.absolute()))}[/dim]"
        )

    console.print(
        Panel.fit(
            details,
            title="[bold green]Hoàn tất[/bold green]",
            border_style="green",
            padding=(1, 3),
        )
    )


def error_message(message: str) -> None:
    """Hiển thị thông báo lỗi."""
    console.print(f"[bold red]❌ {message}[/bold red]")
