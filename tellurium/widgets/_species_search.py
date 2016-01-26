"""
Form for searching BioModels by species information.
Uses the bioservices WebServices to retrieve information.

Search via bioservices is done via
::

    import bioservices
    s = bioservices.BioModels()
    ch = bioservices.ChEBI()
    results = ch.getLiteEntity("D-glucose 6-sulfate")[0:5]
    print(results)
    print(type(results[0]))
    print(results[0].chebiId)

see example notebook: `tellurium/examples/notebooks/species_search.ipynb`
"""
from __future__ import print_function, division

import ipywidgets as w
from IPython.display import display, clear_output
import bioservices


class SearchBySpeciesForm(object):
    """ ipywidgets form for searching biomodels by species."""

    def __init__(self, debug=False):
        """ Creates and displays the search form. """
        self.debug = debug

        self.s = bioservices.BioModels()
        self.ch = bioservices.ChEBI()

        # Define widgets
        # <Search>
        self.wSearchTerm = w.Text(description='Search biomodels by species:', value="CHEBI:17925")
        self.wSearchTerm.on_submit(self.searchChebi)
        self.wSearchButton = w.Button(description='Search')
        self.wSearchButton.on_click(self.searchChebi)
        self.wSearchChebi = w.HBox(children=[
            self.wSearchTerm, self.wSearchButton
        ])

        self.wSelectChebis = w.Select(description='Matching ChEBI:', width='600px', height='250px')
        # FIXME: update the deprecated functions
        self.wSelectChebis.on_trait_change(self.selectChebi)
        self.wSelectModels = w.Select(description='Matching BioModels:', width='200px')
        self.wSelectModels.on_trait_change(self.selectedModel)

        # <Model>
        self.wModelId = w.Text(description='Model ID:', value="No model selected")
        self.wModelCode = w.Text(description='Install Code:')
        self.wModelImport = w.Text(description='Import module code:')
        self.wModelSbml = w.Textarea(description='Model SBML:', width='800px', height='300px')

        # <Container>
        self.wModel = w.FlexBox(children=[
            self.wModelId,
            self.wModelCode,
            self.wSelectModels,
            self.wModelImport,
            self.wModelSbml
        ])
        for ch in self.wModel.children:
            ch.font_family = 'monospace'
            ch.color = '#AAAAAA'
            ch.background_color = 'black'

        self.wContainer = w.FlexBox(children=[
            self.wSearchChebi,
            self.wSelectChebis,
            self.wModel
        ])

        # display the widgets
        display(self.wContainer)
        # clear notebook output
        clear_output()

    def searchChebi(self, b):
        """ Search Chebi with search term and updates the Chebi selection based on results.

        :param b: ?
        :type b: ?
        """
        term = self.wSearchTerm.value
        if self.debug:
            print("searchTerm:", term)
        results = self.ch.getLiteEntity(term)
        choices = [res.chebiId for res in results]
        choiceText = ['%s (%s)' % (res.chebiId, res.chebiAsciiName) for res in results]

        options = {}
        for choice, text in zip(choices, choiceText):
            options[text] = choice
        self.wSelectChebis.options = options

    def selectChebi(self, trait):
        """ Action happening on selection of Chebi Term.
        Search of corresponding BioModels.

        :param trait: ?
        :type trait: str
        """
        if trait == 'value':
            chebi = self.wSelectChebis.value
            if self.debug:
                print("selected Chebi:", chebi)
            modelIds = self.s.getModelsIdByChEBIId(chebi)
            options = {}
            if modelIds is not None:
                for mid in modelIds:
                    options[mid] = mid
            self.wSelectModels.options = options

    def selectedModel(self, trait):
        """ Action happening on selection of Model.
        Update of model information.

        :param trait: ?
        :type trait: str
        """
        if trait == 'value':
            modelId = self.wSelectModels.value
            if self.debug:
                print("selected Model:", modelId)
            sbml = self.s.getModelById(modelId)
            self.wModelId.value = modelId
            self.wModelCode = 'pip install git+https://github.com/biomodels/%s.git' % modelId
            self.wModelImport.value = 'import %s' % modelId
            self.wModelSbml.value = sbml

    def getSBML(self):
        """ Get the SBML string of the current search.
        :return: SBML string
        :rtype: str
        """
        return str(self.wModelSbml.value)
