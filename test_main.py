import main
import pytest
from datetime import datetime, timedelta, timezone
from collections.abc import Generator


def test_convert_pages(article_path):
    page = main.convert_pages(article_path)
    assert page['title'] == "吾輩は猫である"
    assert page['date'] == datetime(2020, 1, 1, 0, 0, 0, tzinfo=get_jst())
    assert page['summary'] == "吾輩わがはいは猫である。名前はまだ無い。"
    assert page['category'] == "夏目漱石"
    assert page['text'] == """\
<h2>どこで生れたかとんと見当けんとうがつかぬ。</h2>
<p>何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。</p>\
"""
    assert page['output_file_name'] == "2020-01-01"
    assert page['link'] == "https://yoshiken.dev" "/articles/2020-01-01"


def get_jst():
    return timezone(timedelta(hours=+9), 'JST')


@pytest.fixture
def article_path(tmpdir) -> Generator[str, None, None]:
    tmpfile = tmpdir.join('2020-01-01.md')

    article_text = """\
Title: 吾輩は猫である
Date: 2020-01-01 00:00:00
Category: 夏目漱石
Summary: 吾輩わがはいは猫である。名前はまだ無い。

## どこで生れたかとんと見当けんとうがつかぬ。

何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。
"""

    try:
        with tmpfile.open('w') as f:
            f.write(article_text)
    except OSError as e:
        raise e
    yield str(tmpfile)
    tmpfile.remove()
