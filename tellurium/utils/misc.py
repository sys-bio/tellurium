from __future__ import print_function, division, absolute_import

import functools
import os
import sys
import warnings

# ---------------------------------------------------------------------
# Simple File Read and Store Utilities
# ---------------------------------------------------------------------
def saveToFile(filePath, str):
    """ Save string to file.

    see also: :func:`readFromFile`

    :param filePath: file path to save to
    :param str: string to save
    """
    with open(filePath, 'w') as f:
        f.write(str)


def readFromFile(filePath):
    """ Load a file and return contents as a string.

    see also: :func:`saveToFile`

    :param filePath: file path to read from
    :returns: string representation of the contents of the file
    """
    with open(filePath, 'r') as f:
        string = f.read()
    return string


# ---------------------------------------------------------------------
# Deprecated warning
# ---------------------------------------------------------------------
def deprecated(func):
    """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used.
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1
        )
        return func(*args, **kwargs)
    return new_func

# ---------------------------------------------------------------------
# Running external tools
# ---------------------------------------------------------------------
def runTool (toolFileName):
    """ Call an external application called toolFileName.
        Note that .exe extension may be omitted for windows applications.

        Include any arguments in arguments parameter.

        Example:
        returnString = te.runTool (['myplugin', 'arg1', 'arg2'])

              If the external tool writes to stdout, this will be captured and returned.

        :param arguments to external tool
        :return String return by external tool, if any.
        """
    import subprocess
    try:
        p = os.path.dirname(sys.executable)
        root, waste = os.path.split(p)
        toolFileName[0] = root + '\\telluriumTools\\' + toolFileName[0] + '\\' + toolFileName[0] + '.exe'
        return subprocess.check_output(toolFileName)
    except subprocess.CalledProcessError as e:
        raise Exception('Tool failed to run correctly or could not be found')
        
# ---------------------------------------------------------------------
# ODE extraction methods
# ---------------------------------------------------------------------        

def getODEsFromSBMLFile (fileName):
    """ Given a SBML file name, this function returns the model 
    as a string of rules and ODEs
    
    eg te.getODEsFromSBMLFile ('mymodel.xml')
    """
    sbmlStr = te.readFromFile (fileName)
    extractor = ODEExtractor (sbmlStr)
    return extractor.toString()
    
def getODEsFromSBMLString (sbmlStr):
    """ Given a SBML string this fucntion returns the model 
    as a string of rules and ODEs
      
    eg te.getODEsFromSBMLString (sbmlStr)
    """
    
    extractor = ODEExtractor (sbmlStr)
    return extractor.toString()
  
def getODEsFromModel (sbmlModel):
    """Given a roadrunner instance this function returns
    a string of rules and ODEs
    
    eg
     
    r = te.loada ('S1 -> S2; k1*S1; k1=1')
    te.getODEsFromModel (r)
    """       
    from roadrunner import RoadRunner
    if type (sbmlModel) == RoadRunner:
       extractor = ODEExtractor (sbmlModel.getSBML())
    else:
       raise RuntimeError('The argument to getODEsFromModelAsString should be a roadrunner variable')
           
    return extractor.toString()
    
class Accumulator:
    def __init__(self, species_id):
        self.reaction_map = {}
        self.reactions = []
        self.species_id = species_id

    def addReaction(self, reaction, stoich):
        rid = reaction.getId()
        if rid in self.reaction_map:
            self.reaction_map[rid]['stoich'] += stoich
        else:
            self.reaction_map[rid] = {
                'reaction': reaction,
                'id': rid,
                'formula': self.getFormula(reaction),
                'stoich': stoich,
            }
            self.reactions.append(rid)

    def getFormula(self, reaction):
        return reaction.getKineticLaw().getFormula()

    def toString(self, use_ids=False):
        lhs = 'd{}/dt'.format(self.species_id)
        terms = []
        for rid in self.reactions:
            if abs(self.reaction_map[rid]['stoich']) == 1:
                stoich = ''
            else:
                stoich = str(abs(self.reaction_map[rid]['stoich'])) + '*'

            if len(terms) > 0:
                if self.reaction_map[rid]['stoich'] < 0:
                    op = ' - '
                else:
                    op = ' + '
            else:
                if self.reaction_map[rid]['stoich'] < 0:
                    op = '-'
                else:
                    op = ''

            if use_ids:
                expr = 'v' + self.reaction_map[rid]['id']
            else:
                expr = self.reaction_map[rid]['formula']

            terms.append(op + stoich + expr)

        rhs = ''.join(terms)
        return lhs + ' = ' + rhs

class ODEExtractor:
    def __init__(self, sbmlStr):
        try:
            import tesbml
        except ImportError:
            raise Exception("Cannot import tesbml. Try tellurium.installPackage('tesbml')")
            
        self.doc = tesbml.readSBMLFromString (sbmlStr)
        self.model = self.doc.getModel()
               
        self.species_map = {}
        self.species_symbol_map = {}
        self.use_species_names = False
        self.use_ids = True

        from collections import defaultdict
        self.accumulators = {}
        self.accumulator_list = []
      
        def reactionParticipant(participant, stoich):
            stoich_sign = 1
            if stoich < 0:
                stoich_sign = -1
            if participant.isSetStoichiometry():
                stoich = participant.getStoichiometry()
            elif participant.isSetStoichiometryMath():
                raise RuntimeError('Stoichiometry math not supported')
            self.accumulators[participant.getSpecies()].addReaction(r, stoich_sign*stoich)

        newReactant = lambda p: reactionParticipant(p, -1)      
        newProduct  = lambda p: reactionParticipant(p, 1)

        for s in (self.model.getSpecies(i) for i in range(self.model.getNumSpecies())):
            self.species_map[s.getId()] = s
            if s.isSetName() and self.use_species_names:
                self.species_symbol_map[s.getId()] = s.getName()
            else:
                self.species_symbol_map[s.getId()] = s.getId()
            a = Accumulator(s.getId())
            self.accumulators[s.getId()] = a
            self.accumulator_list.append(a)

        for r in (self.model.getReaction(i) for i in range(self.model.getNumReactions())):
            for reactant in (r.getReactant(i) for i in range(r.getNumReactants())):
                newReactant(reactant)
            for product in (r.getProduct(i) for i in range(r.getNumProducts())):
                newProduct(product)
        
    def getRules (self):
        r = ''
        for i in range (self.model.getNumRules()): 
            if self.model.getRule(i).getType() == 0:
                r += 'd' + self.model.getRule(i).id + '/dt = ' + self.model.getRule(i).formula + '\n'
            if self.model.getRule(i).getType() == 1:
                r += self.model.getRule(i).id + ' = ' + self.model.getRule(i).formula + '\n'
        return r
    
    def getKineticLaws (self):
        r = ''
        if self.use_ids:
            r += '\n'
            for rx in (self.model.getReaction(i) for i in range(self.model.getNumReactions())):           
                r += 'v' + rx.getId() + ' = ' + rx.getKineticLaw().getFormula().replace(" ", "")  + '\n'
        return r
    
    def getRateOfChange (self, index):
        return self.accumulator_list[index].toString(use_ids=self.use_ids) + '\n'
        
    def getRatesOfChange (self):
        r = '\n'
        for a in self.accumulator_list:
            r += a.toString(use_ids=self.use_ids) + '\n'
        return r
       
    def toString(self):
        r = self.getRules()  
        r = r + self.getKineticLaws() + '\n'
        for index in range (self.model.getNumSpecies()):
            if not self.model.getSpecies (index).boundary_condition:
               r = r + self.getRateOfChange (index)     

        return r