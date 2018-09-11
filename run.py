"""
A programm for converting .wplan to .odt or .md

Author: Manuel Senfft (www.tagirijus.de)
"""

from general.settings import Settings
from general.export import Export


def main(settings):
    """Run the programm."""
    E = Export(
        settings.args.file,
        settings.args.template
    )

    if settings.args.markdown:
        E.convertToMD()
    else:
        E.convertToODT()


if __name__ == '__main__':
    main(Settings())
