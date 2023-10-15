import CodeBase.main_functions as mf
import bs4


def test_get_page():
    test_url =  'https://www.fastighetsvarlden.se/'
    soup = mf.get_page(test_url)
    assert isinstance(soup, bs4.BeautifulSoup)

