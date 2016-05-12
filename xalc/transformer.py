# -*- coding: utf-8 -*-

import re

from IPython.core.inputtransformer import InputTransformer

tests = [
    ('m0', '(1)'),
    ('m15', '((1 << 15))'),
    ('m1_2_31', '((1 << 1) | (1 << 2) | (1 << 31))'),
    ('m4t6', '((0x7 << 4))'),
    ('m6t4', '((0x7 << 4))'),
    ('m5@1', '((0x1f << 1))'),
    ('m2@0_5_8t9_29_31t31', '(0x3 | (1 << 5) | (0x3 << 8) | (1 << 29) | (1 << 31))'),

    ('cafe $ m4t7', '(((0xcafe) & (0xf << 4)) >> 4)'),
    ('beef $ m2@11', '(((0xbeef) & (0x3 << 11)) >> 11)'),
    ('dead $ m3@6_2_3', '(((0xdead) & (1 << 2)) >> 2) | (((0xdead) & (1 << 3)) >> 2) | (((0xdead) & (0x7 << 6)) >> 4)'),

    ('n1010', '0b1010'),
    ('b01a', '0xb01a'),
    ('110b', '0x110b'),

    ('0xabc', '0xabc'),
    ('xabcg', 'xabcg'),
    ('0000zx', '0000zx'),
    ('x01', '0x01'),
    ('fx', '0xf'),

    ('9m', '0x%x' % (9 * 1024 * 1024)),
    ('50k', '0x%x' % (50 * 1024)),
    ('128k', '0x%x' % (128 * 1024)),
    ('20g', '0x%x' % (20 * 1024 * 1024 * 1024)),

    ('0123', '0123'),
    ('a', '0xa'),
    ('12A3', '0x12A3'),
    ('123e', '0x123e'),
    ('abcg', 'abcg'),
    ('BEEF', '0xBEEF'),
]


class XalcInputTransformer(InputTransformer):

    def bitpos(self, pos):
        if 't' in pos:
            start, end = pos.split('t')
            start = int(start)
            end = int(end)
            if start > end:
                start, end = end, start
        elif '@' in pos:
            width, start = pos.split('@')
            start = int(start)
            width = int(width)
            end = start + width - 1
        else:
            start = end = int(pos)

        val = ((1 << (end - start + 1)) - 1)
        val = ('0x{:x}' if val > 1 else '{}').format(val)

        if start > 0:
            expr = '({} << {})'.format(val, start)
        else:
            expr = val

        return expr

    def replace_bit(self, match):
        poses = [self.bitpos(pos) for pos in match.group(1).split('_')]
        return '(%s)' % ' | '.join(poses)

    def get_mask_shift(self, mask):
        b = bin(eval(mask))[2:][::-1]
        return (b.index('1'), b.rindex('1'))

    def replace_extract(self, match):
        expr = match.group(1).rstrip()
        masks = [self.bitpos(pos) for pos in match.group(2).split('_')]

        maskshifts = []
        lastend = 0
        for m in sorted(masks, key=lambda m:self.get_mask_shift(m)[0]):
            start, end = self.get_mask_shift(m)
            shift = start - lastend
            maskshifts.append((m, shift))
            lastend = end - shift + 1

        fmt = '((({expr}) & {mask}) >> {shift})'

        return ' | '.join([fmt.format(expr=expr,
            mask=mask, shift=shift) for mask, shift in maskshifts])

    def replace_size(self, match):
        sz = int(match.group(1))
        unit = match.group(2).lower()

        if unit == 'k':
            sz *= 1024
        elif unit == 'm':
            sz *= 1024 * 1024
        elif unit == 'g':
            sz *= 1024 * 1024 * 1024

        return '0x%x' % sz

    def hexrep(self, match):
        return '0x' + match.group(1)

    def binrep(self, match):
        return '0b' + match.group(1)

    def do_subs(self, line):
        reps = [
            (r'(.*)\$ m([0-9t@_]+)\b', self.replace_extract),
            (r'\bm([0-9t@_]+)\b', self.replace_bit),

            (r'\b(?=[0-9]*[a-fA-F]+[0-9]*)([0-9a-fA-F]+)\b', self.hexrep),

            (r'\bn([01]+)\b', self.binrep),
            (r'\b([01]+)n\b', self.binrep),

            (r'\b([0-9]+)([kKmMgG])\b', self.replace_size),

            (r'\bx([0-9a-fA-F]+)\b', self.hexrep),
            (r'\b([0-9a-fA-F]+)x\b', self.hexrep),
        ]

        for regex, rep in reps:
            line = re.sub(regex, rep, line)

        print line
        return line

    def push(self, line):
        return self.do_subs(line)

    def reset(self):
        pass
