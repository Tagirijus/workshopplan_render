from general.wplan import WPlan
import os
import secretary
import datetime


class Export(object):
    def __init__(self, wplan_file, template_file):
        self.wplan_file = wplan_file
        self.wplan = self.initWPlan()

        self.template_file = template_file

    def outputFilename(self, ext):
        if '.wplan' in self.wplan_file:
            return self.wplan_file.replace('.wplan', ext)
        else:
            return self.wplan_file + ext

    def initWPlan(self):
        if os.path.isfile(self.wplan_file):
            with open(self.wplan_file) as file:
                return WPlan(file.read())
        else:
            return WPlan()

    def convertToODT(self):
        if self.renderODT():
            print('Exported to ODT.')
        else:
            print('NOT exported to ODT !!!')

    def renderODT(self):
        engine = secretary.Renderer()

        # try to replace stuff in the template
        try:
            result = engine.render(
                self.template_file,
                workshop=self.wplan.Workshop,
                blocks=self.wplan.Blocks
            )

            output = open(
                self.outputFilename('.odt'),
                'wb'
            )
            output.write(result)
            output.close()

            return True

        except Exception as e:
            print('Log error: {}'.format(e))
            return False

    def convertToMD(self):
        if self.renderMD():
            print('Exported to Markdown-presentation.')
        else:
            print('NOT exported to Markdown-presentation !!!')

    def renderMD(self):
        try:
            result = self.generateMD()

            output = open(
                self.outputFilename('.md'),
                'w'
            )
            output.write(result)
            output.close()

            return True

        except Exception as e:
            print('Log error: {}'.format(e))
            return False

    def generateMD(self):
        self.wplan.Workshop['YEAR'] = datetime.datetime.now().year
        header = (
            '% {Workshop}\n% {Author}\n% {YEAR}\n\n'
            '# {Workshop}\n\n### {Author}\n\n#### {YEAR}\n\n---\n\n'
        ).format(
            **self.wplan.Workshop
        )

        content = self.generateMDContent()

        return header + content

    def generateMDContent(self):
        block = []
        for x in self.wplan.Blocks:
            block.append(
                '## {Title}\n\n_({Type})_'.format(**x)
            )
        return '\n\n---\n\n'.join(block)
