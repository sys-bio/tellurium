# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:15:16 2014

@author: mgaldzic
"""

import tellurium as te

# Generating different waveforms
model = '''
  model waveforms()
     # All waves have the following amplitude and period
     amplitude = 1
     period = 10

     # These events set the 'UpDown' variable to 1 or 0 according to the period.
     UpDown=0
     at sin(2*pi*time/period) >  0, t0=false: UpDown = 1
     at sin(2*pi*time/period) <= 0, t0=false: UpDown = 0

     # Simple Sine wave with y displaced by 3
     SineWave := amplitude/2*sin(2*pi*time/period) + 3

     # Square wave with y displaced by 1.5
     SquareWave := amplitude*UpDown + 1.5

     # Triangle waveform with given period and y displaced by 1
     TriangleWave = 1
     TriangleWave' = amplitude*2*(UpDown - 0.5)/period

     # Saw tooth wave form with given period
     SawTooth = amplitude/2
     SawTooth' = amplitude/period
     at UpDown==0: SawTooth = 0

     # Simple ramp
     Ramp := 0.03*time
  end
'''

r = te.loadAntimonyModel(model)

r.selections = ['time', 'SineWave', 'SquareWave', 'SawTooth', 'TriangleWave', 'Ramp']
result = r.simulate (0, 90, 500)

te.plotArray(result)