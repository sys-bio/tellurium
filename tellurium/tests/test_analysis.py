import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # switch the backend of matplotlib, so plots can be tested
        import matplotlib
        matplotlib.pyplot.switch_backend("Agg")

    def test_plot2DParameterScan(self):
        import tellurium as te
        from tellurium.analysis.parameterscan import plot2DParameterScan
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
        plot2DParameterScan(r,
                            p1='Vmax', p1Range=np.linspace(1, 10, num=5),
                            p2='Vmax', p2Range=np.linspace(0.1, 1.0, num=5),
                            start=0, end=50, points=101)


if __name__ == '__main__':
    unittest.main()
