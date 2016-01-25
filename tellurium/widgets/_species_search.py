"""
Form for searching by species.

Textboxes can be formated via
    output_box = widgets.Textarea()
    output_box.height = '400px'
    output_box.font_family = 'monospace'
    output_box.color = '#AAAAAA'
    output_box.background_color = 'black'
    output_box.width = '800px'
"""
from __future__ import print_function, division

import ipywidgets as w
from IPython.display import display, clear_output
import bioservices


class SearchBySpeciesForm(object):
    def __init__(self):
        self.s = bioservices.BioModels()
        self.ch = bioservices.ChEBI()

        self.widgets = {
            'searchTerm': w.Text(description='Search biomodels by species:'),
            'searchButton': w.Button(description='Search'),
            'selectChebis': w.Select(description='Matching ChEBI:'),
            'selectModels': w.Select(description='Matching BioModels:'),
            'selectedModel': w.FlexBox(children=[
                w.Textarea(description='Model ID:'),
                w.Textarea(description='Install Code:'),
                w.Textarea(description='Import module code:'),
                w.Textarea(description='Model SBML:')

            ])
        }
        self.container = w.FlexBox(children=[
            self.widgets['searchTerm'],
            self.widgets['searchButton'],
            self.widgets['selectChebis'],
            self.widgets['selectModels'],
            self.widgets['selectedModel']
        ])
        # functionality of widgets

        self.widgets['searchButton']
        self.widgets['searchButton'].on_click(self.search)
        self.widgets['selectChebis'].on_trait_change(self.selectChebi)
        self.widgets['selectModels'].on_trait_change(self.selectedModel)

        display(self.container)
        self.init_display()

    def init_display(self):
        """ Display the search form. """
        clear_output()
        self.widgets["searchTerm"].value = "D-glucose"
        for key, widg in self.widgets.iteritems():
            widg.visible = True

    def search(self, b):
        """ Search Chebi.

        :param b: ?
        :type b: ?
        """
        term = self.widgets['searchTerm'].value
        print("searchTerm:", term)
        results = self.ch.getLiteEntity(term)
        choices = [res.chebiId for res in results]
        choiceText = ['%s (%s)' % (res.chebiId, res.chebiAsciiName) for res in results]

        options = {}
        for choice, text in zip(choices, choiceText):
            options[text] = choice
        self.widgets['selectChebis'].options = options

    def selectChebi(self, trait):
        """ Action happening on selection of Chebi Term.
        Search of corresponding BioModels.
        :param trait: Chebi term
        :type trait: str
        """
        if trait == 'value':
            chebi = self.widgets['selectChebis'].value
            print("selected Chebi:", chebi)
            modelIds = self.s.getModelsIdByChEBIId(chebi)
            options = {}
            if modelIds is not None:
                for mid in modelIds:
                    options[mid] = mid
            self.widgets['selectModels'].options = options

    def selectedModel(self, trait):
        if trait == 'value':
            modelId = self.widgets['selectModels'].value
            print("selected Model:", modelId)
            sbml = self.s.getModelById(modelId)
            self.widgets['selectedModel'].children[0].value = modelId
            self.widgets['selectedModel'].children[1].value = 'pip install git+https://github.com/biomodels/%s.git' % modelId
            self.widgets['selectedModel'].children[2].value = 'import %s' % modelId
            self.widgets['selectedModel'].children[3].value = sbml
