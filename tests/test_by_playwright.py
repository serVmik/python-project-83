import re
from playwright.sync_api import (
    expect,
    sync_playwright,
)

from page_analyzer import db
from page_analyzer.app import CONN_STRING
from tests.conftest import drop_tables


with sync_playwright() as p:
    page_home = 'http://127.0.0.1:5000'
    url_entered = 'https://ru.hexlet.io/my'
    url_name = 'https://ru.hexlet.io'
    page_next1 = 'http://127.0.0.1:5000/urls/1'

    print('\n\n' + 'Run sync_playwright ...')

    connection = db.connect(CONN_STRING)
    drop_tables(connection)
    db.close(connection)
    print('tables of db dropped!')

    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # Home page
    print(f'go to page_home "{page_home}"')
    page.goto(page_home)
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile('Анализатор страниц'))
    expect(page.get_by_role("heading", name='Анализатор страниц')).to_be_visible()

    print(f'fill in the textbox with url_entered "{url_entered}"')
    page.get_by_role('textbox').fill(url_entered)
    print('click button "Проверить"')
    page.get_by_role('button', name='Проверить').click()

    # urls
    print(f'testing have url_next1 "{page_next1}"')
    expect(page).to_have_url(re.compile(page_next1))

    page.get_by_role('button').click()

    page.get_by_text('Сайты').click()

    page.get_by_text('https://ru.hexlet.io').click()

    page.get_by_text('Анализатор страниц').click()

    browser.close()
    print('... sync_playwright completed!' + '\n')
