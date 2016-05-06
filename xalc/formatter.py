# -*- coding: utf-8 -*-

import re

import bitstring
import blessed


class Cursed:

    def __init__(self):
        pass

    def __getattr__(self, s):
        return ''


class XalcFormatter(object):

    def __init__(self):
        self.last_binval = None
        self.last_hexval = None
        self.cursed = Cursed()
        self.t = blessed.Terminal()

    def format_size(self, sz):
        sizes = [(1024 * 1024 * 1024, 'Gi'),
                 (1024 * 1024, 'Mi'),
                 (1024, 'Ki'),
                 (1, '')]
        parts = []
        for size, name in sizes:
            if sz and sz >= size:
                parts.append('{} {}'.format(sz / size, name))
                sz -= (sz / size) * size

        return ' + '.join(parts)

    def diff_strings(self, a, b):
        diffs = []

        if len(a) != len(b):
            return diffs

        for i in range(len(a)):
            if a[i] != b[i]:
                diffs.append(i)

        return diffs

    def highlight_diff(self, s, last):
        if last:
            diffs = self.diff_strings(last, s)

            # Many diffs probably means this calculation is completely
            # unrelated from the previous one -- don't bother highlighting
            # diffs in that case
            if diffs and len(diffs) < len(s) / 2:
                parts = list(s)
                for pos in diffs:
                    fmt = '{t.underline}{b}{t.no_underline}'
                    parts[pos] = fmt.format(t=self.t, b=parts[pos])
                s = ''.join(parts)

        return s

    def format_int(self, n, p, cycle):
        decfmt = ' {t.bold}{n:}{t.normal}'
        hexfmt = ' {t.bold_blue}0x{hexval}{t.normal}'

        if n >= 0:
            hexn = n
            hexval = '{n:08x}'.format(n=hexn)
        else:
            hexn = int(bitstring.BitArray('int:32={}'.format(n)).hex, 16)
            hexval = '{n:08x}'.format(n=hexn)

        fits32bits = hexn <= 0xffffffff

        decstr = decfmt.format(t=self.cursed, n=n)
        hexstr = hexfmt.format(t=self.cursed, hexval=hexval)

        declen = len(decstr)
        hexlen = len(hexstr)
        maxlen = max(declen, hexlen) + 4

        decfmt += ' ' * (maxlen - declen) + '│'
        if fits32bits:
            markers = ''.join(['{:2d}─╮ '.format(i)
                               for i in range(28, -1, -4)])
            decfmt += '  {t.white}{markers}{t.normal}'.format(
                t=self.t, markers=markers)

        hexfmt += ' ' * (maxlen - hexlen) + '│'

        if fits32bits:
            rawbinval = ' '.join(re.findall('.{4}', '{:032b}'.format(hexn)))
            binval = self.highlight_diff(rawbinval, self.last_binval)
            self.last_binval = rawbinval
            hexfmt += '  {t.magenta}{binval}{t.normal}'.format(
                t=self.t, binval=binval)
        else:
            self.last_binval = None
            hexfmt += '  {t.magenta}> 32 bits{t.normal}'.format(t=self.t)

        rawhexval = hexval
        hexval = self.highlight_diff(rawhexval, self.last_hexval)
        self.last_hexval = rawhexval

        p.text(decfmt.format(t=self.t, n=n) + '\n')
        p.text(hexfmt.format(t=self.t, hexval=hexval))

        if n and n > 1024:
            p.text('\n {t.yellow}{sz:10}{t.normal}'.format(
                t=self.t, sz=self.format_size(n)))
