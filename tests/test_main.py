import pytest
from unittest.mock import MagicMock

from main import MainApp, APPS_NAMES
from helpers.app_overview import AppOverview


@pytest.fixture
def main_app():
    app = MainApp()
    app.mainloop = MagicMock()  # Um die mainloop zu verhindern
    return app


def test_load_app(main_app):
    main_app.load_app(AppOverview)
    assert isinstance(main_app.app_frame.current_app, AppOverview)


def test_toggle_theme(main_app):
    current_theme = main_app.theme_switch_var.get()
    main_app.toggle_theme()
    new_theme = main_app.theme_switch_var.get()
    assert current_theme != new_theme
