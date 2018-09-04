from general.wplan import WPlan
import os
import secretary


class Export(object):
    def __init__(self, wplan_file, template_file):
        self.wplan_file = wplan_file
        self.wplan = self.initWPlan()

        self.template_file = template_file

        self.output_file = self.initOutputFilename()

    def initOutputFilename(self):
        if '.wplan' in self.wplan_file:
            return self.wplan_file.replace('.wplan', '.odt')
        else:
            return self.wplan_file + '.odt'

    def initWPlan(self):
        if os.path.isfile(self.wplan_file):
            with open(self.wplan_file) as file:
                return WPlan(file.read())
        else:
            return WPlan()

    def convertToPDF(self):
        # TODO: get data to put into the ODT
        workshop = {
            'Title': 'Manu testst den Render!'
        }
        blocks = {}

        if self.renderPDF(workshop, blocks):
            print('Exported.')
        else:
            print('NOT exported !!!')

    def renderPDF(self, workshop, blocks):
        engine = secretary.Renderer()

        # try to replace stuff in the template
        try:
            result = engine.render(
                self.template_file,
                workshop=workshop,
                blocks=blocks
            )

            output = open(self.output_file, 'wb')
            output.write(result)
            output.close()

            return True

        except Exception as e:
            print('Log error: {}'.format(e))
            return False
