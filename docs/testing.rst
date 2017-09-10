.. _front-ends::

======================
Unit Tests
======================

Tellurium features a unit test suite.

.. code-block:: python

    import tellurium.tests.test_runner as tetest
    runner = tetest.TestRunner()
    runner.te_passes_tests()

If the output is true, Tellurium passed all tests and is working without any errors.

libRoadRunner Test Suite
========================

libRoadRunner also comes with its own test suite, which is part of the Tellurium test suite. To run it, execute the following.

.. code-block:: python

    import roadrunner as rr
    rr.runTests()
