"""
Form for searching by species.
"""
from __future__ import print_function, division

import IPython.html.widgets as w
from IPython.display import display, clear_output
import bioservices

class SearchBySpeciesForm(object):
    def __init__(self):
        self.s = bioservices.BioModels()
        self.ch = bioservices.ChEBI()
        self.widgets = {
            'searchTerm': w.TextWidget(description='Search biomodels by species:'),
            'searchButton': w.ButtonWidget(description='Search'),
            'selectChebis': w.SelectWidget(description='Matching ChEBI:'),
            'selectModels': w.SelectWidget(description='Matching BioModels:'),
            'selectedModel': w.ContainerWidget(children=[
                w.TextWidget(description='Model ID:'),
                w.TextWidget(description='Install Code:'),
                w.TextWidget(description='Import module code:'),
                w.TextareaWidget(description='Model SBML:')

            ])
        }
        self.container = w.ContainerWidget(children=[
            self.widgets['searchTerm'],
            self.widgets['searchButton'],
            self.widgets['selectChebis'],
            self.widgets['selectModels'],
            self.widgets['selectedModel']
        ])
        self.widgets['searchTerm'].on_submit(self.search)
        self.widgets['searchButton'].on_click(self.search)
        self.widgets['selectChebis'].on_trait_change(self.selectChebi)
        self.widgets['selectModels'].on_trait_change(self.selectedModel)

        display(self.container)
        self.init_display()

    def init_display(self):
        clear_output()
        for key, widg in self.widgets.iteritems():
            widg.visible = False

        self.widgets['searchTerm'].visible = True
        self.widgets['searchButton'].visible = True


    def search(self, b):
        self.init_display()
        results = self.ch.getLiteEntity(self.widgets['searchTerm'].value)
        choices = [result['chebiId'] for result in results]
        choiceText = ['%s (%s)' % (result['chebiId'], result['chebiAsciiName']) for result in results]

        values = {}
        for choice, text in zip(choices, choiceText):
            values[text] = choice

        self.widgets['selectChebis'].values = values
        self.widgets['selectChebis'].visible = True


    def selectChebi(self, trait):
        if trait == 'value':
            self.widgets['selectModels'].visible = False
            self.widgets['selectedModel'].visible = False
            chebi = self.widgets['selectChebis'].value
            modelIds = self.s.getModelsIdByChEBIId(chebi)
            values = {}
            if modelIds is not None:
                for id in modelIds:
                    values[id] = id
            self.widgets['selectModels'].values = values
            self.widgets['selectModels'].visible = True

    def selectedModel(self, trait):
        if trait == 'value':
            self.widgets['selectedModel'].visible = False
            modelId = self.widgets['selectModels'].value
            sbml = self.s.getModelById(modelId)
            self.widgets['selectedModel'].children[0].value = modelId
            self.widgets['selectedModel'].children[1].value = 'pip install git+https://github.com/biomodels/%s.git' % modelId
            self.widgets['selectedModel'].children[2].value = 'import %s' % modelId
            self.widgets['selectedModel'].children[3].value = sbml
            self.widgets['selectedModel'].visible = True
