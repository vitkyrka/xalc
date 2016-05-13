# -*- coding: utf-8 -*-

from IPython.terminal.embed import InteractiveShellEmbed
from traitlets.config import Config

from transformer import tests


def main():
    c = Config()
    c.InteractiveShell.confirm_exit = False

    ipshell = InteractiveShellEmbed(config=c, banner1='')
    ipshell.extension_manager.load_extension('xalc')

    print 'xalc examples/tests:'
    for inp, out in tests:
        print ' {:10s} => {:10s}'.format(inp, out)

    ipshell()

if __name__ == '__main__':
    main()
