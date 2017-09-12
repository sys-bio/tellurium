"""
Single UniformTimeCourse.

CVODE uniformTimecourse simulation with plot of concentrations vs. time.
"""
from __future__ import print_function
import os
from tellurium.sedml.case_template import run_case

antimonyStr = """
model case_01
    J0: S1 -> S2; k1*S1;
    S1 = 10.0; S2=0.0;
    k1 = 0.1;
end
"""

phrasedmlStr = """
    model0 = model "case_01"
    sim0 = simulate uniform(0, 10, 100)
    task0 = run sim0 on model0
    plot "UniformTimecourse" task0.time vs task0.S1
    report task0.time vs task0.S1
"""
run_case(os.path.realpath(__file__), antimonyStr, phrasedmlStr)