"""
A programm for converting .wplan to .pdf

Author: Manuel Senfft (www.tagirijus.de)
"""

from general.settings import Settings
from general.export import Export


def main(settings):
    """Run the programm."""
    wplan_file = settings.args.file
    template_file = settings.args.template
    E = Export(wplan_file, template_file)
    E.convertToPDF()


if __name__ == '__main__':
    main(Settings())
