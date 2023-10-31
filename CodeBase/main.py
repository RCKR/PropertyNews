import pandas as pd
import numpy as np
from CodeBase import main_functions as mf


class PropPipe:
    def __init__(self, fv_url):
        self.base_url = fv_url
        self.data = None
        self.current_soup = mf.get_page(fv_url)

    @property
    def get_data(self):
        return self.data

    def _update_soup(self, page_idx):
        if page_idx > 1:
            next_url = f'{self.base_url}/page/{page_idx}/'
            self.current_soup = mf.get_page(next_url)

    def _update_key_word(self, title, word):
        self.data['key_match'] = np.where(
            self.data['title'].str.lower().str.contains(word), word, self.data['key_match']
        )

    def _loop_through_keywords(self, list_of_words):
        self.data['key_match'] = np.nan
        for word in list_of_words:
            word = word.lower()
            self._update_key_word(title='title', word=word)
            self._update_key_word(title='description', word=word)

    def find_keywords(self, list_of_words):
        if self.data is None:
            raise AttributeError('No data to work on, please run "run_pipeline"')

        self._loop_through_keywords(list_of_words)
        result = self.data[self.data['key_match'] != 'nan'].copy()

        self.data.drop(columns='key_match', inplace=True)
        return result

    def run_pipeline(self, inplace=False, nr_pages: int = 1):
        # extract first page and check page criteria
        nr_pages = mf.nr_pages_within_page_scope(self.current_soup, nr_pages=nr_pages)
        main_data_source = []

        # loop through pages with (small) articles
        for page_idx in range(1, nr_pages + 1):
            print(f'processing page: {page_idx}...')

            # get url to next page
            self._update_soup(page_idx)
            article_data = mf.run_single_page_pipe(self.current_soup)
            main_data_source += article_data

        self.data = pd.DataFrame(main_data_source)

        if not inplace:
            return main_data_source


if __name__ == '__main__':
    fv_url_ = 'https://www.fastighetsvarlden.se/'
    pipe = PropPipe(fv_url=fv_url_)
    pipe.run_pipeline(nr_pages=3, inplace=True)


