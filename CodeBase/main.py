import pandas as pd
import main_functions as mf

def run_pipeline(fv_url, nr_pages: int = 1) -> list:
    # extract first page and check page criteria
    soup = mf.get_page(fv_url)
    nr_pages = mf.nr_pages_within_page_scope(soup, nr_pages=nr_pages)
    main_data_source = []

    # loop through pages with (small) articles
    for page_idx in range(1, nr_pages+1):
        print(f'processing page: {page_idx}...')
        # get url to next page
        if page_idx > 1:
            next_page_url = f'{fv_url}/page/{page_idx}/'
            soup = mf.get_page(next_page_url)

        # article data from page
        article_data = mf.run_single_page_pipe(soup)
        main_data_source += article_data

    return main_data_source

if __name__ == '__main__':
    fv_url_ = 'https://www.fastighetsvarlden.se/'
    data = run_pipeline(fv_url_, nr_pages=3)
    df = pd.DataFrame(data)


