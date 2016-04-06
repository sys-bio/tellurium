"""
Export utilities.
Write to latex.
"""

from __future__ import print_function, division
import os.path


class LatexExport(object):
    """ Class for exporting simulation to latex. """
    def __init__(self, rr,
                 color=['blue', 'green', 'red', 'black'],
                 xlabel='x',
                 ylabel='y',
                 legend=None,
                 exportComplete=False,
                 coorPerRow=6,
                 saveto=None,
                 exportType='pgfplot',
                 fileName='Model',
                 exportString=''):
        """ Creating the export object with given settings.

        :param rr: roadrunner instance (used for data loading if no result)
        :type rr: roadrunner.RoadRunner
        :param color:
        :type color: list
        :param xlabel: x-axis label
        :type xlabel: str
        :param ylabel: y-axis label
        :type ylabel: str
        :param legend:
        :type legend:
        :param exportComplete:
        :type exportComplete:
        :param coorPerRow:
        :type coorPerRow:
        :param saveto:
        :type saveto:
        :param exportType:
        :type exportType:
        :param fileName:
        :type fileName:
        :param exportString:
        :type exportString:
        """
        self.rr = rr
        self.color = color
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.legend = legend
        self.exportComplete = exportComplete
        self.coorPerRow = coorPerRow
        self.saveto = saveto
        self.exportType = exportType
        self.fileName = fileName
        self.exportString = exportString

    def _getPath(self, suffix, count=''):
        """ File path from suffix and count.
        Uses fileName and saveto information to create a file path.

        :param suffix: suffix for file generation
        :type suffix: str
        :param count: suffix2 (iterator of file)
        :type count: int
        :return: path of latex file
        :rtype: str
        """
        path = '{}{}{}.txt'.format(self.fileName, suffix, str(count))
        if self.saveto is not None:
            path = os.path.join(self.saveto, path)
        return path

    def saveToFile(self, result=None):
        """Creates .tex and .txt files for plotting result of simulation with LaTeX.
        Outputs one file with code to be pasted into LaTeX, and one data file
        for each variable in results after the first.

        Takes two arguments, results of simulation and name of file to be created.
        Setting self.exportClipboard to True also copies LaTeX code to clipboard, while 
        setting self.exportComplete to True adds necessary code to build doc right away. 
        
        result = rr.simulate(0, 6, 20, ['Time', 'S1', 'S2'])
        p.export(result, model1)
        """
        if result is None:
            result = self.rr.getSimulationData()

        # write one data file per column
        Ncol = result.shape[1] - 1
        if len (self.color) < Ncol:
           raise StandardError ('The number of specified colors does not match the number of data columns') 
        for i in range(Ncol):
            dataPath = self._getPath(suffix='_data', count=i+1)
            print("writing data document: " + dataPath)

            with open(dataPath, 'w') as f:
                r = result[:, [0, (i+1)]]
                for row in r:
                    row.tolist()
                    row = ' '.join(str(e) for e in row)
                    f.write("{0}\n".format(row))

        # write one latex document
        latexPath = self._getPath(suffix='_code').replace('txt', 'tex')
        print("writing latex document: " + latexPath)

        with open(latexPath, 'w') as f:
            if self.exportComplete:
                f.write('\\documentclass{article}\n')
                f.write('\\usepackage[usenames,dvipsnames]{color}\n')
                f.write('\\usepackage{pgfplots}\n')
                f.write('\\begin{document}\n\n')
                
            f.write('\\begin{tikzpicture}[scale = 1.0]\n')
            f.write('\\begin{{axis}}[xlabel=${}$, ylabel=${}$, axis lines = middle, xlabel near ticks,'
                    ' ylabel near ticks]\n'.format(self.xlabel, self.ylabel))
            for i in range(Ncol):
                f.write('\\addplot[%s, thin] table {%s_data%s.txt};\n' 
                        % (self.color[i], dataPath, (i + 1)))
                
            if self.legend is not None:
                f.write('\\legend{')
                for i in range(Ncol - 1):
                    f.write('%s,' % self.legend[i])
                    f.write('%s}\n' % self.legend[i])
                    
            f.write('\\end{axis}\n')
            f.write('\\end{tikzpicture}\n\n')
            
            if self.exportComplete:
                f.write('\\end{document}')

    def saveToOneFile(self, result=None):
        """ Creates one .txt file with LaTeX code and results.
        Takes two arguments, results of
        simulation and name of file to be created. Same options as for saveToFile method.
        """
        if result is None:
            result = self.rr.getSimulationData()

        Ncol = result.shape[1] - 1
        if len (self.color) < Ncol:
           raise StandardError ('The number of specified colors does not match the number of data columns') 
        latexPath = self._getPath(suffix='')
        print("writing latex document: " + latexPath)
        with open(latexPath, 'w') as f:
            if self.exportComplete is True:
                f.write('\\documentclass{article}\n')
                f.write('\\usepackage[usenames,dvipsnames]{color}\n')
                f.write('\\usepackage{pgfplots}\n')
                f.write('\\begin{document}\n\n')
                
            f.write('\\begin{tikzpicture}[scale = 1.0]\n')
            f.write('\\begin{{axis}}[xlabel=${}$, ylabel=${}$, axis lines = middle, xlabel near'
                    ' ticks, ylabel near ticks]\n'.format(self.xlabel, self.ylabel))
            for i in range(Ncol):
                f.write('\\addplot[line width = 2pt, %s] coordinates {\n' % (self.color[i]))
                r = result[:, [0,(i + 1)]]
                count = 1
                for row in r:
                    row.tolist()
                    coor = ', '.join(str(e) for e in row)
                    coor = '({})'.format(coor)
                    if count % self.coorPerRow == 0:
                        f.write('{}\n'.format(coor))
                    else:
                        f.write('{}'.format(coor))
                    count += 1
                f.write('\n};\n')
            f.write('\\end{axis}\n')
            f.write('\\end{tikzpicture}\n\n')
            if self.exportComplete is True:
                f.write('\\end{document}')
