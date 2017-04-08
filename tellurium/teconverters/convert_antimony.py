from __future__ import print_function, division, absolute_import

class antimonyConverter:
    def checkAntimonyReturnCode(self, code):
        """Negative return code (usu. -1) from Antimony signifies error"""
        return (code < 0)

    def sbmlToAntimony(self, sbml):
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
        return (module, sb_source)

    def sbmlFileToAntimony(self, sbml_path):
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
        return (module, sb_source)

    def antimonyToSBML(self, sb_str):
        """ Converts an Antimony string to raw SBML.

        :param sb_str: The raw Antimony string
        :returns: A 2-tuple (module_name, raw_sbml)
        """

        import antimony as sb
        # try to load the Antimony code`
        code = sb.loadAntimonyString(sb_str)

        # if errors, bail
        if self.checkAntimonyReturnCode(code):
            errors = sb.getLastError()
            raise RuntimeError('Errors encountered when trying to load model:\n{}'.format(errors))

        module = sb.getMainModuleName()
        sbml = sb.getSBMLString(module)
        return (module, sbml)
