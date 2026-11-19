# -*- coding: utf-8 -*-

from .transformer import XalcInputTransformer, echo
from .formatter import XalcFormatter


def load_ipython_extension(ip):
    ip.input_transformers_cleanup.extend([XalcInputTransformer(), echo])

    formatter = ip.display_formatter.formatters['text/plain']
    formatter.for_type(int, XalcFormatter().format_int)
