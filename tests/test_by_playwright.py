import re
from playwright.sync_api import Page, expect, sync_playwright

from page_analyzer import db
from page_analyzer.app import CONN_STRING
from tests.conftest import drop_tables


def test_simple(page: Page) -> None:
    print('\n\n' + 'Run test_simple ...')
    page.goto('http://127.0.0.1:5000')
    expect(page).to_have_title(re.compile('Анализатор страниц'))
    expect(page.get_by_role("heading", name='Анализатор страниц')).to_be_visible()
    print('... test_simple completed!' + '\n')


with sync_playwright() as p:
    page_home = 'http://127.0.0.1:5000'
    url_verified = 'https://ru.hexlet.io/my'
    url_next1 = 'http://127.0.0.1:5000/urls/1'
    indent = ' ' * 4

    print('\n\n' + 'Run sync_playwright ...')

    connection = db.connect(CONN_STRING)
    drop_tables(connection)
    db.close(connection)
    print(f'{indent}tables of db dropped!')

    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    print(f'{indent}go to page_home "{page_home}"')
    page.goto(page_home)
    print(f'{indent}fill in the textbox with url_verified "{url_verified}"')
    page.get_by_role('textbox').fill(url_verified)
    print(f'{indent}click button "Проверить"')
    page.get_by_role('button', name='Проверить').click()

    print(f'{indent}testing have url_next1 "{url_next1}"')
    expect(page).to_have_url(re.compile(url_next1))

    page.get_by_role('button').click()

    page.get_by_text('Сайты').click()

    page.get_by_text('https://ru.hexlet.io').click()

    page.get_by_text('Анализатор страниц').click()

    browser.close()
    print('... sync_playwright completed!' + '\n')
