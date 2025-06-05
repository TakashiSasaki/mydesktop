import pytest
from mydesktop.__main__ import TextureApp
from textual.app import App
from textual.widgets import Static


def test_app_is_subclass_of_app():
    assert issubclass(TextureApp, App)


def test_compose_returns_static_widget():
    app = TextureApp()
    widgets = list(app.compose())
    assert len(widgets) == 1
    widget = widgets[0]
    assert isinstance(widget, Static)
    assert widget.renderable == "Hello from Texture!"
