from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.webkit.launch()
    page = browser.new_page()
    page.goto('https://python-page-analyzer-ru.hexlet.app')
    page.screenshot(path='fixtures/screenshots/index.png')
    page.goto('https://python-page-analyzer-ru.hexlet.app/url')
    page.screenshot(path='fixtures/screenshots/url.png')
    page.goto('https://python-page-analyzer-ru.hexlet.app/urls')
    page.screenshot(path='fixtures/screenshots/urls.png')
    browser.close()
