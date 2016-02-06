"""
This module creates an SBMLDiagram for the given SBML model using graphviz.
"""
from __future__ import print_function, division
import roadrunner
import warnings
import tempfile
import libsbml
from IPython.display import Image, display

try:
    import pygraphviz as pgv
except ImportError as e:
    pgv = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
    warnings.warn("'pygraphviz' could not be imported", ImportWarning, stacklevel=2)


class SBMLDiagram(object):
    """ Create network diagram from a sbml model. """

    def __init__(self, sbml,
                 species={},
                 reactions={},
                 reactants={},
                 products={},
                 modifiers={}):
        """
        :param sbml: SBML string, libsbml.SBMLDocument object, or libsbml.Model object
        :param species:
        :type species:
        :param reactions:
        :type reactions:
        :param reactants:
        :type reactants:
        :param products:
        :type products:
        :param modifiers:
        :type modifiers:
        """
        # load model
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
        # create graph
        self.g = SBMLDiagram._createGraph(self.model,
                                          species=species,
                                          reactions=reactions,
                                          reactants=reactants,
                                          products=products,
                                          modifiers=modifiers)


    @staticmethod
    def _createGraph(model, species={}, reactions={}, reactants={}, products={}, modifiers={}):
        """ Creates the acyclic graph from the given model.

        :param model:
        :type model:
        :param species:
        :type species:
        :param reactions:
        :type reactions:
        :param reactants:
        :type reactants:
        :param products:
        :type products:
        :param modifiers:
        :type modifiers:
        :return:
        :rtype:
        """

        g = pgv.AGraph(strict=False, directed=True)

        # set some default node attributes
        g.node_attr['style'] = 'filled'
        g.node_attr['shape'] = 'circle'
        g.node_attr['fixedsize'] = 'true'
        g.node_attr['fillcolor'] = '#FFFFFF'
        g.node_attr['fontcolor'] = '#000000'
        # g.node_attr['height'] = '40'
        # g.node_attr['width'] = '40'

        # species nodes
        for s in model.species:
            if s.name:
                label = s.name
            else:
                label = s.id
            g.add_node(s.id, label=label, **species)
            n = g.get_node(s.id)

            # boundary species
            if s.boundary_condition is True:
                n.attr['fillcolor'] = '#717FF0'

        for r in model.reactions:
            # reaction nodes
            if r.name:
                label = r.name
            else:
                label = r.id
            g.add_node(r.id, label=label, **reactions)
            n = g.get_node(r.id)
            n.attr['fillcolor'] = '#D1D1D1'
            n.attr['shape'] = 'square'
            # n.attr['height'] = int(int(g.node_attr['height'])/2.0)
            # n.attr['width'] = int(int(g.node_attr['width'])/2.0)

            # edges
            for s in r.reactants:
                g.add_edge(s.getSpecies(), r.getId(), **reactants)
            for s in r.products:
                g.add_edge(r.getId(), s.getSpecies(), **products)
            for s in r.modifiers:
                g.add_edge(s.getSpecies(), r.getId(), **modifiers)
        return g

    def draw(self, layout='neato', **kwargs):
        """ Draw the graph.
        Optional layout=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        :param layout: pygraphviz layout algorithm (default: 'neato')
        :type layout: str
        """
        f = tempfile.NamedTemporaryFile(suffix='.png')
        self.g.layout(prog=layout)
        self.g.draw(f.name)

        i = Image(filename=f.name, **kwargs)
        display(i)
