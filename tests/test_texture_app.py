import pytest
from mydesktop.__main__ import TextureApp
from textual.app import App
from textual.widgets import Static, Button, Footer
from unittest.mock import MagicMock


def test_app_is_subclass_of_app():
    assert issubclass(TextureApp, App)


def test_bindings_contain_quit_shortcuts():
    assert ("ctrl+q", "quit", "Quit") in TextureApp.BINDINGS
    assert ("ctrl+shift+q", "quit", "Quit") in TextureApp.BINDINGS


def test_compose_contains_widgets():
    app = TextureApp()
    widgets = list(app.compose())
    assert any(isinstance(w, Static) for w in widgets)
    assert any(isinstance(w, Button) for w in widgets)
    assert any(isinstance(w, Footer) for w in widgets)


def test_button_triggers_exit():
    app = TextureApp()
    mock_exit = MagicMock()
    app.exit = mock_exit
    button = Button("Quit", id="quit-button")
    event = Button.Pressed(button)
    app.on_button_pressed(event)
    mock_exit.assert_called_once()
