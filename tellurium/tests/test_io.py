"""
Test the latex export.
"""
import unittest
import tempfile
import shutil
import os.path


class ExportTestCase(unittest.TestCase):
    def test_latex_export(self):
        """Test latex export. """
        temp_dir = tempfile.mkdtemp()
        # export is writing files which have to be handeled in temp_dir
        try:
            tmp_f = tempfile.NamedTemporaryFile()

            import tellurium as te
            newModel = '''
                   $Xo -> S1; k1*Xo;
                   S1 -> S2; k2*S1;
                   S2 -> $X1; k3*S2;

                   Xo = 50; X1=0.0; S1 = 0; S2 = 0;
                   k1 = 0.2; k2 = 0.4; k3 = 2;
            '''

            rr = te.loadAntimonyModel(newModel)
            result = rr.simulate(0, 30)

            p = te.LatexExport(rr,
                     color=['blue', 'green'],
                     legend=['S1', 'S2'],
                     xlabel='Time',
                     ylabel='Concentration',
                     exportComplete=True,
                     saveto=temp_dir,
                     fileName='Model')
            p.saveToFile(result)

            # test that the files were written
            # writing data document: /tmp/tmpi722ME/Model_data1.txt
            # writing data document: /tmp/tmpi722ME/Model_data2.txt
            # writing latex document: /tmp/tmpi722ME/Model_code.txt
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model_data1.txt')))
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model_data2.txt')))
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model_code.txt')))

            # test without result
            p.saveToFile()
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model_data1.txt')))
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model_data2.txt')))
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model_code.txt')))

        finally:
            shutil.rmtree(temp_dir)

    def test_latex_export2(self):
        """Test latex export. """
        temp_dir = tempfile.mkdtemp()
        # export is writing files which have to be handeled in temp_dir
        try:
            tmp_f = tempfile.NamedTemporaryFile()

            import tellurium as te
            newModel = '''
                   $Xo -> S1; k1*Xo;
                   S1 -> S2; k2*S1;
                   S2 -> $X1; k3*S2;

                   Xo = 50; X1=0.0; S1 = 0; S2 = 0;
                   k1 = 0.2; k2 = 0.4; k3 = 2;
            '''

            rr = te.loadAntimonyModel(newModel)
            result = rr.simulate(0, 30)
            p = te.LatexExport(rr,
                     color=['blue', 'green'],
                     legend=['S1', 'S2'],
                     xlabel='Time',
                     ylabel='Concentration',
                     exportComplete=True,
                     saveto=temp_dir,
                     fileName='Model')
            p.saveToOneFile(result)
            # test that file was written
            self.assertTrue(os.path.isfile(os.path.join(temp_dir, 'Model.txt')))

        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
