import pytest
import jupytext
from jupytext.compare import compare, compare_notebooks


@pytest.fixture()
def text():
    return '''A short
Markdown file
'''


def test_crlf(text):
    nb = jupytext.reads(text, 'md')
    assert 'use_crlf' not in nb.metadata['jupytext']

    text_crlf = '\r\n'.join(text.splitlines()) + '\r\n'
    nb_crlf = jupytext.reads(text_crlf, 'md')
    assert nb_crlf.metadata['jupytext']['use_crlf'] is True
    compare_notebooks(nb_crlf, nb)


def test_lf_file(tmpdir, text):
    tmp_md = str(tmpdir.join('file.md'))
    with open(tmp_md, 'w', newline='\n') as fp:
        fp.write(text)

    nb = jupytext.read(tmp_md)
    assert 'use_crlf' not in nb.metadata['jupytext']

    jupytext.write(nb, tmp_md)
    with open(tmp_md) as fp:
        compare(fp.read(), text)


def test_crlf_file(tmpdir, text):
    tmp_md = str(tmpdir.join('file.md'))
    with open(tmp_md, 'w', newline='\r\n') as fp:
        fp.write(text)

    nb = jupytext.read(tmp_md)
    assert nb.metadata['jupytext']['use_crlf'] is True

    jupytext.write(nb, tmp_md)
    with open(tmp_md, newline='') as fp:
        compare(fp.read(), text.replace('\n', '\r\n'))
