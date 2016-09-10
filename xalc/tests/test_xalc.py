from xalc.transformer import tests, XalcInputTransformer


def check_sub(inp, out):
    transformer = XalcInputTransformer()
    print('in {} want {} got {}'.format(inp, out, transformer.do_subs(inp)))
    assert out == transformer.do_subs(inp)


def test_reps():
    for inp, out in tests:
        yield check_sub, inp, out
