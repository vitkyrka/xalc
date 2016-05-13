# -*- coding: utf-8 -*-

import argparse
import sys

from IPython.terminal.embed import InteractiveShellEmbed
from traitlets.config import Config

from transformer import tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', nargs='*',
                        help='run this command and exit')
    args = parser.parse_args()

    c = Config()
    c.InteractiveShell.confirm_exit = False

    if args.cmd:
        c.PromptManager.out_template = ''
        c.HistoryAccessor.enabled = False

    ipshell = InteractiveShellEmbed(config=c, banner1='')
    ipshell.extension_manager.load_extension('xalc')

    if args.cmd:
        ipshell.run_cell(' '.join(args.cmd), store_history=False)
        sys.exit()

    print 'xalc examples/tests:'
    for inp, out in tests:
        print ' {:10s} => {:10s}'.format(inp, out)

    ipshell()

if __name__ == '__main__':
    main()
