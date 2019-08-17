"""The class holding all the settings."""

import argparse
import json
import os

PATH_TO_PROJECT = os.path.dirname(os.path.realpath(__file__)).replace('/general', '/')
DEFAULT_TEMPLATE = PATH_TO_PROJECT + 'src/template.odt'


class Settings(object):
    """Settings class."""

    def __init__(
        self
    ):
        """Initialize the class and hard code defaults, if no file is given."""
        self.initArguments()
        self.variable = None

    def initArguments(self):
        self.args = argparse.ArgumentParser(
            description=(
                'A programm for rendering .wplan to .odt or .md'
            )
        )

        self.args.add_argument(
            '-f',
            '--file',
            default=None,
            help='The .wplan file'
        )

        self.args.add_argument(
            '-t',
            '--template',
            default=DEFAULT_TEMPLATE,
            help='An external ODT template file'
        )

        self.args.add_argument(
            '-md',
            '--markdown',
            action='store_true',
            default=False,
            help='Generate a markdown presentation from wplan'
        )

        self.args = self.args.parse_args()

    def toJson(self, indent=2, ensure_ascii=False):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['variable'] = self.variable

        # return the json
        return json.dumps(
            out,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    def fromJson(self, js=None):
        """Feed settings variables from json string."""
        if js is None:
            return

        # get js as dict
        try:
            js = json.loads(js)
        except Exception:
            # do not load it
            return

        # feed settings variables
        if 'variable' in js.keys():
            self.variable = js['variable']
