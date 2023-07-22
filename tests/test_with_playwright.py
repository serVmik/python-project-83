from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch(headless=False, slow_mo=800)
    page = browser.new_page()
    page.goto('http://127.0.0.1:5000')

    page.screenshot(path='tests/fixtures/screenshots/index_1.png')
    page.get_by_role('textbox').fill('https://ru.hexlet.io/my')
    page.get_by_role('button').click()

    page.screenshot(path='tests/fixtures/screenshots/urls_1.png')
    page.get_by_role('button').click()
    page.screenshot(path='tests/fixtures/screenshots/urls_2.png')

    page.get_by_text('Сайты').click()
    page.screenshot(path='tests/fixtures/screenshots/urls_3.png')

    page.get_by_text('https://ru.hexlet.io').click()

    page.get_by_text('https://ru.hexlet.io').click()
    page.screenshot(path='tests/fixtures/screenshots/index_2.png')

    page.get_by_text('Анализатор страниц').click()

    browser.close()
