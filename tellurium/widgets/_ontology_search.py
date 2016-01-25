"""
Ontology widgets.
"""
from __future__ import print_function, division
import IPython.html.widgets as w
from IPython.display import display, clear_output
import bioservices


class OntologySearch(object):
    def __init__(self):
        self.ch = bioservices.ChEBI()
        self.kegg = bioservices.KEGG()

        self.widgets = {
            'ontologySelect': w.DropdownWidget(
                description='Ontology:',
                values=['ChEBI', 'KEGG.Reaction']),
            'searchTerm': w.TextWidget(description='Search Term:'),
            'searchButton': w.ButtonWidget(description='Search'),
            'searchResults': w.ContainerWidget(children=[
                w.SelectWidget(description='Results:'),
                w.TextWidget(description='URL:')
            ])
        }
        self.container = w.ContainerWidget(children=[
            self.widgets['ontologySelect'],
            self.widgets['searchTerm'],
            self.widgets['searchButton'],
            self.widgets['searchResults'],
        ])
        self.widgets['searchTerm'].on_submit(self.search)
        self.widgets['searchButton'].on_click(self.search)
        self.widgets['searchResults'].children[0].on_trait_change(self.selectedTerm)
#         self.widgets['selectChebis'].on_trait_change(self.selectChebi)
#         self.widgets['selectModels'].on_trait_change(self.selectedModel)
        display(self.container)
        self.init_display()

    def init_display(self):

        clear_output()
        self.widgets['searchResults'].visible = False

    def show_results(self):
        self.widgets['searchResults'].visible = True

    def search(self, b):
        self.init_display()
        if self.widgets['ontologySelect'].value == 'ChEBI':
            results = self.ch.getLiteEntity(self.widgets['searchTerm'].value)
            choices = [result['chebiId'] for result in results]
            choiceText = ['%s (%s)' % (result['chebiId'], result['chebiAsciiName']) for result in results]
            values = {}
            for choice, text in zip(choices, choiceText):
                values[text] = choice
            self.widgets['searchResults'].children[0].values = values
            self.show_results()
        elif self.widgets['ontologySelect'].value == 'KEGG.Reaction':
            results = self.kegg.find('reaction', self.widgets['searchTerm'].value)
            self.results = results
            lines = [line.split('\t') for line in results.split('\n')]
            values = {}
            for line in lines:
                left = line[0].split('rn:')
                if len(left) == 2:
                    values[line[1]] = left[1]
            self.widgets['searchResults'].children[0].values = values
            self.show_results()

    def selectedTerm(self, trait):
        if trait != 'value':
            return
        if self.widgets['ontologySelect'].value == 'ChEBI':
            chebi_id = self.widgets['searchResults'].children[0].value
            self.widgets['searchResults'].children[1].value = 'http://identifiers.org/chebi/%s' % chebi_id
        elif self.widgets['ontologySelect'].value == 'KEGG.Reaction':
            kegg_id = self.widgets['searchResults'].children[0].value
            self.widgets['searchResults'].children[1].value = 'http://identifiers.org/kegg.reaction/%s' % kegg_id
