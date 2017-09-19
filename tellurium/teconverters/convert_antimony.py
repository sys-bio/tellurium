from __future__ import print_function, division, absolute_import

from .antimony_sbo import antimonySBOConverter, antimonySBOParser

class antimonyConverter(object):
    def checkAntimonyReturnCode(self, code):
        """Negative return code (usu. -1) from Antimony signifies error"""
        return (code < 0)

    def sbmlToAntimony(self, sbml, addSBO=False):
        """ Converts a raw SBML string to Antimony source.

        :param sbml: The raw SBML string
        :returns: A 2-tuple (module_name, antimony_source)
        """

        import antimony as sb
        # try to load the Antimony code`
        code = sb.loadSBMLString(sbml)

        # if errors, bail
        if self.checkAntimonyReturnCode(code):
            errors = sb.getLastError()
            raise RuntimeError('Errors encountered when trying to load model:\n{}'.format(errors))

        module = sb.getMainModuleName()
        sb_source = sb.getAntimonyString(module)
        if addSBO:
            sb_source = self.tryAddSBOTerms(sb_source, sbml_str=sbml)
        return (module, sb_source)

    def sbmlFileToAntimony(self, sbml_path, addSBO=False):
        """ Converts a SBML file to Antimony source.

        :param sbml_path: The path to the SBML file
        :returns: A 2-tuple (module_name, antimony_source)
        """

        import antimony as sb
        # try to load the Antimony code`
        code = sb.loadSBMLFile(sbml_path)

        # if errors, bail
        if self.checkAntimonyReturnCode(code):
            errors = sb.getLastError()
            raise RuntimeError('Errors encountered when trying to load model:\n{}'.format(errors))

        module = sb.getMainModuleName()
        sb_source = sb.getAntimonyString(module)
        if addSBO:
            sb_source = self.tryAddSBOTerms(sb_source, sbml_file=sbml_path)
        return (module, sb_source)

    def cellmlFileToAntimony(self, sbml_path):
        """ Converts a CellML file to Antimony source.

        :param sbml_path: The path to the CellML file
        :returns: A 2-tuple (module_name, antimony_source)
        """

        import antimony as sb
        # try to load the Antimony code`
        code = sb.loadCellMLFile(sbml_path)

        # if errors, bail
        if self.checkAntimonyReturnCode(code):
            errors = sb.getLastError()
            raise RuntimeError('Errors encountered when trying to load model:\n{}'.format(errors))

        module = sb.getMainModuleName()
        sb_source = sb.getAntimonyString(module)
        return (module, sb_source)

    def antimonyToSBML(self, sb_str, SBO=False):
        """ Converts an Antimony string to raw SBML.

        :param sb_str: The raw Antimony string
        :returns: A 2-tuple (module_name, raw_sbml)
        """

        import antimony as sb

        if not SBO:
            sbo_parser = antimonySBOParser(sb_str)
            try:
                sb_str = sbo_parser.elideSBOTerms()
            except:
                pass

        # try to load the Antimony code`
        code = sb.loadAntimonyString(sb_str)

        # if errors, bail
        if self.checkAntimonyReturnCode(code):
            errors = sb.getLastError()
            raise RuntimeError('Errors encountered when trying to load model into Antimony:\n{}'.format(errors))

        module = sb.getMainModuleName()
        sbml = sb.getSBMLString(module)
        if not SBO:
            sbml = sbo_parser.addSBOsToSBML(sbml)
        return (module, sbml)

    def tryAddSBOTerms(self, antimony_str, sbml_file=None, sbml_str=None):
        """ Attempt to add SBO terms to the Antimony model.
        You must supply one of either sbml_file or sbml_str, not both.
        This method will return the original Antimony string if SBO terms cannot
        be added.
        """
        if not sbml_file and not sbml_str:
            raise RuntimeError('You must supply sbml_file or sbml_str')
        # try:
        if sbml_file:
            converter = antimonySBOConverter.fromSBMLFile(sbml_file)
        elif sbml_str:
            converter = antimonySBOConverter.fromSBMLString(sbml_str)
        return converter.convert(antimony_str)
        # except RuntimeError:
        #     return antimony_str
