Install additional packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are using Tellurium notebook or Tellurium Spyder, you can install additional package using ``installPackage`` function. In Tellurium Spyder, you can also install packages using included command Prompt. For more information, see `Running Command Prompt for Tellurium Spyder <https://tellurium.readthedocs.io/en/latest/walkthrough.html#running-command-prompt-for-tellurium-spyder>`_.

.. autofunction:: tellurium.installPackage

.. code-block:: python

    import tellurium as te
    # install cobra (https://github.com/opencobra/cobrapy)
    te.installPackage('cobra')
    # update cobra to latest version
    te.upgradePackage('cobra')
    # remove cobra
    # te.removePackage('cobra')
