"""
This module creates an SBMLDiagram for the given SBML model using graphviz.
"""

from __future__ import print_function, division, absolute_import
import roadrunner
import warnings
import tempfile
try:
    import tesbml as libsbml
except ImportError:
    import libsbml
from six import string_types

try:
    from IPython.display import Image, display
except ImportError:
    pass
import os


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
        if isinstance(sbml, string_types):
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

        try:
            import pygraphviz as pgv
        except ImportError as e:
            pgv = None
            roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))
            warnings.warn("'pygraphviz' could not be imported, cannot draw network diagrams", ImportWarning, stacklevel=2)

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
        for s in (model.getSpecies(k) for k in range(model.getNumSpecies())):
            if s.getName():
                label = s.getName()
            else:
                label = s.getId()
            g.add_node(s.getId(), label=label, width=0.15*len(label), **species)
            n = g.get_node(s.getId())

            # boundary species
            if s.isSetBoundaryCondition() and s.getBoundaryCondition() == True:
                n.attr['fillcolor'] = '#717FF0'

        for r in (model.getReaction(k) for k in range(model.getNumReactions())):
            # reaction nodes
            if r.getName():
                label = r.getName()
            else:
                label = r.getId()
            g.add_node(r.getId(), label=label, width=0.15*len(label), **reactions)
            n = g.get_node(r.getId())
            n.attr['fillcolor'] = '#D1D1D1'
            n.attr['shape'] = 'square'
            # n.attr['height'] = int(int(g.node_attr['height'])/2.0)
            # n.attr['width'] = int(int(g.node_attr['width'])/2.0)

            # edges
            for s in (r.getReactant(k) for k in range(r.getNumReactants())):
                g.add_edge(s.getSpecies(), r.getId(), **reactants)
            for s in (r.getProduct(k) for k in range(r.getNumProducts())):
                g.add_edge(r.getId(), s.getSpecies(), **products)
            for s in (r.getModifier(k) for k in range(r.getNumModifiers())):
                g.add_edge(s.getSpecies(), r.getId(), **modifiers)
        return g

    def draw(self, layout='neato', **kwargs):
        """ Draw the graph.
        Optional layout=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        :param layout: pygraphviz layout algorithm (default: 'neato')
        :type layout: str
        """
        f, filePath = tempfile.mkstemp(suffix='.png')
        self.g.layout(prog=layout)
        self.g.draw(filePath)
        
        i = Image(filename=filePath)
        display(i)
        os.close(f)
        os.remove(filePath)
