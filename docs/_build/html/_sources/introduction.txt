===================
Introduction
===================
Tellurium is a cross-platform and open source Python based environment that integrates a variety of useful packages for systems biology modeling. The IDE is based on the spyder2 IDE (https://code.google.com/p/spyderlib/)

**Simple Example** 
::

	import tellurium as te
	r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
	r.simulate(0, 10, 100)
	r.plot()

**More Complex Example** 
::

	import tellurium at te
	r = te.loada ('''
		# A dollar symbol means fix the species concentration
		    $S1 -> S2;  k1*S1; 
		 J2: S2 -> S3;  k2*S2 - k3*S3;
		     S3 -> $S4; k4*S3;
		
		k1 = 0.1; S1 = 10
	''')

	result = r.simulate (0, 10, 100, ['time', 'S1', 'S3', 'J1'])
	rr.plot (result)

**Screen-shot of Tellurium**

.. image:: ./images/tellurium_screenshot.png

