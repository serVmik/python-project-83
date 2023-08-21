import re
from playwright.sync_api import (
    expect,
    Page,
)


def test_page_analyzer(page: Page):
    url_entered1 = 'https://ru.hexlet.io/my'
    url_entered2 = 'https://www.djangoproject.com/download/'
    url_name1 = 'https://ru.hexlet.io'
    url_name2 = 'https://www.djangoproject.com'
    url_empty = ''
    baseurl = 'http://server:8001'
    page_index = f'{baseurl}'
    page_index_title = 'Анализатор страниц'
    page_index_placeholder = 'https://www.example.com'
    page_url_name1 = f'{baseurl}/urls/1'
    page_url_name2 = f'{baseurl}/urls/2'
    page_urls = f'{baseurl}/urls'

    # index
    page.goto(page_index)
    expect(page).to_have_title(re.compile(page_index_title))
    expect(page.get_by_role('heading', name=page_index_title)).to_be_visible()
    placeholder = page.get_by_placeholder(page_index_placeholder)
    expect(placeholder).to_have_attribute('placeholder', page_index_placeholder)
    placeholder.fill(url_entered1)
    page.get_by_role('button', name='Проверить').click()

    # urls/1
    expect(page).to_have_url(re.compile(page_url_name1))
    expect(page.get_by_text('Страница успешно добавлена')).to_be_visible()
    expect(page.get_by_text(f'Сайт: {url_name1}')).to_be_visible()
    page.get_by_role('button').click()
    expect(page.get_by_text('Страница успешно проверена')).to_be_visible()
    page.get_by_text('Сайты').click()

    # urls
    expect(page).to_have_url(re.compile(page_urls))
    page.get_by_text('https://ru.hexlet.io').click()

    # urls/1
    page.get_by_text('Анализатор страниц').click()

    # index
    page.get_by_role('textbox').fill(url_entered1)
    page.get_by_role('button').click()

    # urls/1
    expect(page).to_have_url(re.compile(page_url_name1))
    expect(page.get_by_text('Страница уже существует')).to_be_visible()
    page.get_by_text('Анализатор страниц').click()

    # index
    page.get_by_role('textbox').fill(url_empty)
    page.get_by_role('button').click()
    expect(page.get_by_text('URL обязателен')).to_be_visible()
    expect(page.get_by_text('Некорректный URL')).to_be_visible()
    expect(page).to_have_url(re.compile(page_urls))
    page.get_by_role('textbox').fill(url_entered2)
    page.get_by_role('button').click()

    # urls/2
    expect(page).to_have_url(re.compile(page_url_name2))
    expect(page.get_by_text(f'Сайт: {url_name2}')).to_be_visible()
    page.get_by_text('Сайты').click()

    # urls
    expect(page.get_by_text(url_name1)).to_be_visible()
    expect(page.get_by_text(url_name2)).to_be_visible()
