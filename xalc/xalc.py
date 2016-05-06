# -*- coding: utf-8 -*-

from IPython.terminal.embed import InteractiveShellEmbed
from traitlets.config import Config


def main():
    c = Config()
    c.InteractiveShell.confirm_exit = False

    ipshell = InteractiveShellEmbed(config=c, banner1='')
    ipshell.extension_manager.load_extension('xalc')
    ipshell()

if __name__ == '__main__':
    main()
