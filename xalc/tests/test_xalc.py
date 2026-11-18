import contextlib
import io

from IPython.core.interactiveshell import InteractiveShell
from traitlets.config import Config

from xalc.transformer import tests, XalcInputTransformer


def check_sub(inp, out):
    transformer = XalcInputTransformer()
    print('in {} want {} got {}'.format(inp, out, transformer.do_subs(inp)))
    assert out == transformer.do_subs(inp)


def test_reps():
    for inp, out in tests:
        check_sub(inp, out)


def get_shell():
    c = Config()
    c.HistoryAccessor.enabled = False
    ip = InteractiveShell.instance(config=c)
    ip.extension_manager.load_extension('xalc')
    return ip


def capture(func, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        ret = func(*args)
    return ret, buf.getvalue()


def test_transform_cell():
    ip = get_shell()
    for inp, out in tests:
        assert capture(ip.transform_cell, inp) == (out + '\n', out + '\n')


def test_check_complete():
    ip = get_shell()
    assert capture(ip.check_complete, 'cafe $ m4t7') == (('complete', ''), '')
    assert capture(ip.check_complete, '(cafe $ m4t7') == (('incomplete', ''), '')
    assert capture(ip.check_complete, 'mp3') == (('invalid', ''), '')


def test_run_cell():
    ip = get_shell()
    for _ in range(2):
        result, out = capture(ip.run_cell, 'cafe $ m4t7')
        assert result.result == 0xf
        assert out.startswith('(((0xcafe) & (0xf << 4)) >> 4)\n')
        assert out.count('0xcafe') == 1

    result, out = capture(ip.run_cell, 'mp3')
    assert isinstance(result.error_before_exec, SyntaxError)
