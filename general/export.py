from general.wplan import WPlan
import os


class Export(object):
    def __init__(self, wplan_file, template_file):
        self.wplan_file = wplan_file
        self.wplan = self.initWPlan()

        self.template_file = template_file
        self.template = self.initTemplate()

        self.output_file = self.initOutputFilename()
        self.temp_file = self.initTempFilename()

    def initTempFilename(self):
        path = os.path.dirname(self.template_file) + '/'
        return path + 'WPLAN_RENDER_TEMP.html'

    def initOutputFilename(self):
        if '.wplan' in self.wplan_file:
            return self.wplan_file.replace('.wplan', '.pdf')
        else:
            return self.wplan_file + '.pdf'

    def initTemplate(self):
        if os.path.isfile(self.template_file):
            with open(self.template_file) as file:
                return file.read()
        else:
            return 'TEMPLATE FILE NOT FOUND ...'

    def initWPlan(self):
        if os.path.isfile(self.wplan_file):
            with open(self.wplan_file) as file:
                return WPlan(file.read())
        else:
            return WPlan()

    def convertToPDF(self):
        self.replaceMeta()
        self.saveHTML()
        # self.renderPDF()
        self.delHTML()

    def replaceMeta(self):
        self.template = self.template.replace(
            '{TITLE}', self.wplan.Workshop['Workshop']
        )
        self.template = self.template.replace(
            '{DESCRIPTION}', self.wplan.Workshop['Description']
        )
        self.template = self.template.replace(
            '{AUTHOR}', self.wplan.Workshop['Author']
        )

    def saveHTML(self):
        with open(self.temp_file, 'w') as file:
            file.write(self.template)

    def delHTML(self):
        os.remove(self.temp_file)
