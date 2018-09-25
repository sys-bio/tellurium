import unittest
import matplotlib


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        self.backend = matplotlib.rcParams['backend']
        matplotlib.pyplot.switch_backend("Agg")

    def tearDown(self):
        matplotlib.pyplot.switch_backend(self.backend)

    def test_plot2DParameterScan(self):
        """Test plot2DParameterScan."""
        import tellurium as te
        from tellurium.analysis.parameterscan import ParameterScan2D
        r = te.loada("""
        model test
           J0: S1 -> S2; Vmax * (S1/(Km+S1))
            S1 = 10; S2 = 0;
            Vmax = 1; Km = 0.5;
        end
        """)
        s = r.simulate(0, 50, 101)
        # r.plot(s)

        import numpy as np
        p = ParameterScan2D(r,
                            p1='Vmax', p1Range=np.linspace(1, 10, num=5),
                            p2='Vmax', p2Range=np.linspace(0.1, 1.0, num=5),
                            start=0, end=50, points=101)
        p.plot2DParameterScan()


if __name__ == '__main__':
    unittest.main()
