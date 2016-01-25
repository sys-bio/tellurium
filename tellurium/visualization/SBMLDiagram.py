"""
SBMLDiagram extension via graphviz.
"""
from __future__ import print_function, division
import roadrunner
import os
import tempfile
import libsbml
from IPython.display import Image, display

try:
    # FIXME: this should always be packed
    import pygraphviz as pgv
except ImportError as e:
    pgv = None
    roadrunner.Logger.log(roadrunner.Logger.LOG_WARNING, str(e))


class SBMLDiagram(object):
    """ Create a network diagram from a sbml model. """

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

        self.G = pgv.AGraph(strict=False, directed=True)

        for i, s in enumerate(self.model.species):
            if s.getName():
                label = s.getName()
            else:
                label = s.getId()
            self.G.add_node(s.getId(), label=label, **species)
        for i, r in enumerate(self.model.reactions):
            if r.getName():
                label = r.getName()
            else:
                label = r.getId()
            self.G.add_node(r.getId(), label=label, **reactions)
            for s in r.reactants:
                self.G.add_edge(s.getSpecies(), r.getId(), **reactants)
            for s in r.products:
                self.G.add_edge(r.getId(), s.getSpecies(), **products)
            for s in r.modifiers:
                self.G.add_edge(s.getSpecies(), r.getId(), **modifiers)

    def draw(self, layout='neato'):
        """ Draw the graph.
        Optional layout=['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']
        will use specified graphviz layout method.

        :param layout: pygraphviz layout algorithm (default: 'neato')
        :type layout: str
        """
        f = tempfile.NamedTemporaryFile()
        fname = f.name + '.png'
        self.G.layout(prog=layout)
        self.G.draw(fname)

        i = Image(filename=fname)
        display(i)
        os.remove(fname)
