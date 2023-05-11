import pytest
from unittest.mock import MagicMock

from helpers.app_overview import AppOverview


@pytest.fixture
def app_overview(main_app):
    return AppOverview(main_app.app_frame, main_app.APPS)


def test_filter_apps(app_overview):
    filter_text = "Adressbuch"
    filtered_apps = app_overview.filter_apps(filter_text)
    assert len(filtered_apps) == 1
    assert filtered_apps[0][0] == "Adressbuch (AB)"


def test_populate_table(app_overview):
    app_overview.populate_table("Adressbuch")
    children = app_overview.table.get_children()
    assert len(children) == 1


def test_update_category_row_bg(app_overview):
    app_overview.update_category_row_bg("dark")
    assert app_overview.table.tag_cget("category", "background") == "#333"
    app_overview.update_category_row_bg("light")
    assert app_overview.table.tag_cget("category", "background") == "#bbb"
