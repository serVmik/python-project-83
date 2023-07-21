import re
from playwright.sync_api import Page, expect


def test_homepage(page: Page):
    page.goto('http://127.0.0.1:5000')

    # Ожидайте, что заголовок "содержит" подстроку.
    # <title>Анализатор страниц</title>
    expect(page).to_have_title(re.compile('Анализатор страниц'))

    # создать локатор
    # get_started = page.get_by_role("link", name="Get started")

    # Expect an attribute "to be strictly equal" to the value.
    # expect(get_started).to_have_attribute("href", "/docs/intro")

    # # Click the get started link.
    # get_started.click()
    #
    # # Expects the URL to contain intro.
    # expect(page).to_have_url(re.compile(".*intro"))
