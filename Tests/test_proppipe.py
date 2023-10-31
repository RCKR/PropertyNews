from CodeBase.main import PropPipe
import pandas as pd


def test_find_keywords():
    example_url = 'https://www.fastighetsvarlden.se/'
    pipe = PropPipe(fv_url=example_url)

    fake_data = pd.DataFrame({
        'title': ['not', 'test', 'secbaR', 'debArsA' 'Bar', 'NoT'],
        'description': ['TeSt', 'test', 'sec', 'bar' 'Bar', 'NoT']
    })

    pipe.data = fake_data
    length, width = pipe.find_keywords(['bar']).shape
    assert length == 2
    assert width == 3
