"""
Ontology search widget for ipython notebooks.

see example notebook: `tellurium/examples/notebooks/ontology_search.ipynb`
"""
from __future__ import print_function, division
import ipywidgets as w
from IPython.display import display, clear_output
import bioservices


class OntologySearch(object):
    """ ipywidget form for searching in ontologies. """
    def __init__(self):
        self.ch = bioservices.ChEBI()
        self.kegg = bioservices.KEGG()

        self.wOntologySelect = w.Dropdown(description='Ontology:', options=['ChEBI', 'KEGG.Reaction'])
        self.wSearchTerm = w.Text(description='Search Term:', value="glucose")
        self.wSearchTerm.on_submit(self.search)
        self.wSearchButton = w.Button(description='Search')
        self.wSearchButton.on_click(self.search)

        self.wResultsSelect = w.Select(description='Results:', width='100%')
        self.wResultsSelect.on_trait_change(self.selectedTerm)
        self.wResultsURL = w.Textarea(description='URL:', width='100%')
        self.wResults = w.VBox(children=[
                self.wResultsSelect,
                self.wResultsURL
        ], width='100%')
        for ch in self.wResults.children:
            ch.font_family = 'monospace'
            ch.color = '#AAAAAA'
            ch.background_color = 'black'

        # <Container>
        self.wContainer = w.FlexBox(children=[
            self.wOntologySelect,
            self.wSearchTerm,
            self.wSearchButton,
            self.wResults
        ])

        # display the container
        display(self.wContainer)
        self.init_display()

    def init_display(self):
        clear_output()
        self.wResults.visible = False
        self.wSearchButton.visible = True

    def show_results(self):
        self.wResults.visible = True
        self.wSearchButton.visible = True

    def search(self, b):
        """ Search the ontology for the given term.
        Sets the search results.
        :param b: ?
        :type b: ?
        """
        self.init_display()
        options = {}
        term = self.wSearchTerm.value
        self.wSearchButton.visible = False
        print('... querying WebService ...')
        # search ChEBI
        if self.wOntologySelect.value == 'ChEBI':
            results = self.ch.getLiteEntity(term)
            choices = [result['chebiId'] for result in results]
            choiceText = ['%s (%s)' % (result.chebiId, result.chebiAsciiName) for result in results]

            for choice, text in zip(choices, choiceText):
                options[text] = choice
        # search Kegg Reaction
        elif self.wOntologySelect.value == 'KEGG.Reaction':
            # database: can be one of pathway, module, disease, drug,
            # environ, ko, genome, compound, glycan, reaction, rpair, rclass,
            # enzyme, genes, ligand or an organism
            results = self.kegg.find(database='reaction', query=term)
            if isinstance(results, unicode):
                lines = results.split('\n')
                for line in lines:
                    tokens = line.split('\t')
                    if len(tokens) == 2 and tokens[0].startswith('rn:'):
                        options[tokens[0]] = tokens[1]
        self.wResultsSelect.options = options
        self.show_results()

    def selectedTerm(self, trait):
        """ Action on selecting an ontology.
        :param trait: ?
        :type trait: ?
        """
        if trait != 'value':
            return

        url = ''
        sid = self.wResultsSelect.value
        if self.wOntologySelect.value == 'ChEBI':
            url = 'http://identifiers.org/chebi/{}'.format(sid)
        elif self.wOntologySelect.value == 'KEGG.Reaction':
            url = 'http://identifiers.org/kegg.reaction/{}'.format(sid)

        self.wResultsURL.value = url
        print(url)
