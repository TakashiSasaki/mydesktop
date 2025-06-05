from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Footer

class Developer:
    valid_languages: list[str] = [
        "Python",
        "Java",
        "JavaScript",
        "C",
        "C++",
        "C#",
        "PHP",
        "Swift",
        "Go",
        "Kotlin",
        "Ruby",
        "Rust",
        "TypeScript",
        "Scala",
        "Perl",
        "Lua",
        "Groovy",
        "R",
        "Shell",
        "Objective-C",
        "SQL",
        "HTML/CSS",
    ]

    def __init__(self, name, language) -> None:
        if language not in self.valid_languages:
            raise ValueError(f"{language} is not a valid language.")
        self.name = name
        self.language = language

    def get_info(self) -> str:
        return f"{self.name} is a developer who codes in {self.language}."


def start_coding() -> None:
    print("Start coding in Python today!")


def date() -> datetime:
    current_datetime: datetime = datetime.now()
    return current_datetime


class TextureApp(App):
    """Minimal TUI application with a default screen."""

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+shift+q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static(
            "Press CTRL+Q or CTRL+SHIFT+Q or use the Quit button to exit.",
            id="message",
        )
        yield Button("Quit", id="quit-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit-button":
            self.exit()

def main() -> None:
    TextureApp().run()


if __name__ == "__main__":
    main()
