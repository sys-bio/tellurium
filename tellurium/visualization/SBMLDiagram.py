import networkx as nx
import libsbml
class SBMLDiagram():
    '''
    Create a network diagram from a sbml model.

    '''

    def __init__(self, sbml):
        '''
        sbml -- an SBML string, libsbml.SBMLDocument object, or libsbml.Model object

        '''

        if isinstance(sbml, basestring):
            self.doc = libsbml.readSBMLFromString(sbml)
            self.model = self.doc.getModel()
        elif isinstance(sbml, libsbml.SBMLDocument):
            self.doc = sbml
            self.model = self.doc.getModel()
        elif isinstance(sbml, libsbml.Model):
            self.model = sbml
        else:
            raise Exception('SBML Input is not valid')

        self.G = nx.DiGraph()
        self.labels = {}
        self.species = []
        self.reactions = []
        for i, s in enumerate(self.model.species):
            self.G.add_node(s.getId())
            self.species.append(s.getId())
        for i, r in enumerate(self.model.reactions):
            self.G.add_node(r.getId())
            self.reactions.append(r.getId())
            for s in r.reactants:
                self.G.add_edge(s.getSpecies(), r.getId(), kind='reactant')
            for s in r.products:
                self.G.add_edge(r.getId(), s.getSpecies(), kind='product')
            for s in r.modifiers:
                self.G.add_edge(s.getSpecies(), r.getId(), kind='modifier')

        self.modifier_edges = [key for key, val in nx.get_edge_attributes(self.G, 'kind').items() if val == 'modifier']
        self.product_edges = [key for key, val in nx.get_edge_attributes(self.G, 'kind').items() if val == 'product']
        self.reactant_edges = [key for key, val in nx.get_edge_attributes(self.G, 'kind').items() if val == 'reactant']
        #mass_transfer_edges = [key for key, val in nx.get_edge_attributes(G, 'kind').items() if val != 'modifier']

        # Default drawing options
        self.options = {}
        self.options['species'] = {
            'size': 500,
            'color': 'r',
            'alpha': 0.8,
            'label_size': 16
        }
        self.options


    def draw(self, layout_type='spring_layout'):
        '''
        Draw the graph

        layout_type = The type of layout algorithm (Default = 'spring_layout')
        '''

        import matplotlib.pyplot as plt

        try:
            pos = getattr(nx, layout_type)(self.G)
        except:
            raise Exception('layout_type of %s is not valid' % layout_type)


        nx.draw_networkx_nodes(self.G,pos,
                               nodelist=self.species,
                               node_color=self.options['species']['color'],
                               node_size=self.options['species']['size'],
                               alpha=self.options['species']['alpha'])
        nx.draw_networkx_edges(self.G, pos, edgelist=self.product_edges)
        nx.draw_networkx_edges(self.G, pos, edgelist=self.reactant_edges, arrows=False)
        nx.draw_networkx_edges(self.G, pos, edgelist=self.modifier_edges, style='dashed')

        labels = {}
        for n in self.G.nodes():
            if n in self.species:
                labels[n] = n
        nx.draw_networkx_labels(self.G,pos,labels,font_size=self.options['species']['label_size'])
        plt.axis('off')
        plt.show()
