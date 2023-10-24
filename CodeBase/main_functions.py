from bs4 import BeautifulSoup, Tag, ResultSet
from time import sleep
import requests


def content_text(article_: Tag, atr: str, desc: str = None, id_: str = None) -> str or None:

    text_object = article_.find_all(atr)
    if len(text_object) == 0:
        try:
            text = article_.text
        except AttributeError:
            text = ' \r '

        if atr == 'h2':
            return text.split('\r')[0].replace('\n', '').strip()
        return text.split('\r')[1].replace('\n', '').strip()

    try:
        data_ = ''.join(val.text for val in text_object)
        return data_
    except AttributeError:
        print(f'No {desc} for article {id_}')
        return ''


def get_id_from_main_page(article_: Tag):
    article_response = requests.get(article_.get('href'))
    article_id = (BeautifulSoup(article_response.content, 'lxml')
                  .find('main', id='main').find('article').get('id'))
    return article_id


def get_article_id(article_: Tag):
    article_id = ''
    try:
        article_id = article_.find('article').get('id')
    except AttributeError:
        try:
            article_id = get_id_from_main_page(article_)
        except AttributeError:
            pass
    finally:
        return article_id


def check_if_article_is_premium(article_: Tag) -> bool:
    if article_.find('article', class_='entry locked-paywalled__item'):
        return True
    return False


def get_single_article_data(article_: Tag) -> dict:
    article_id = get_article_id(article_)
    article_content_link = article_.get('href')
    article_title = content_text(article_, atr='h2', desc='title', id_=article_id)
    article_description = content_text(article_, atr='p', desc='description', id_=article_id)
    premium_article = check_if_article_is_premium(article_)

    # load information to dictionary
    data_ = {
        'article_id': article_id,
        'title': article_title,
        'description': article_description,
        'premium': premium_article,
        'url': article_content_link,
    }
    return data_


def find_page_articles(soup: BeautifulSoup) -> ResultSet:
    main_container = soup.find('main', id='main')
    articles = main_container.find_all('a', class_='entry__link')
    return articles


def nr_pages_within_page_scope(soup: BeautifulSoup, nr_pages: int) -> int:
    nav_links = soup.find('div', class_='nav-links')
    all_links = nav_links.find_all('a', class_='page-numbers')
    max_count = int(all_links[-2].text)

    if nr_pages > max_count:
        print(f'nr_pages exceeds page limit, trunating to max of {max_count}...')
        nr_pages = max_count
    return nr_pages


def get_page(url: str) -> BeautifulSoup:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    sleep(1)
    return soup


def run_single_page_pipe(soup: BeautifulSoup) -> list:
    articles = find_page_articles(soup)
    article_data = [get_single_article_data(article) for article in articles]
    return article_data
