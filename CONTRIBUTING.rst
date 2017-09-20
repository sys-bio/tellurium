============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs using the `issue tracker <https://github.com/sys-bio/tellurium/issues>`__

If you are reporting a bug, please include:

* Your operating system name and version.
* Your python and tellurium version.
* If you are using the python package, notebook or spyder verion
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub `issues <https://github.com/sys-bio/tellurium/issues>`__
for bugs. Best contact the main contributors and ask questions before you start coding.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub `issues <https://github.com/sys-bio/tellurium/issues>`__
for features. Anything tagged with "enhancement" is open to whoever wants to
implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

tellurium could always use more documentation, whether as part of the official
tellurium docs, in docstrings, or even on the web in blog posts, articles, and
such - all contributions are welcome!

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an
`issue <https://github.com/sys-bio/tellurium/issues>`__.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

If you like tellurium please remember to 'star' our github page (click on the star
at top right corner), that way we also have an idea of who is using tellurium!

Get Started!
------------

Want to contribute a new feature or improvement? Consider starting by raising an
issue and assign it to yourself to describe what you want to achieve. This way,
we reduce the risk of duplicated efforts and you may also get suggestions on how
to best proceed, e.g. there may be half-finished work in some branch that you
could start with.

Here's how to set up `tellurium` for local development to contribute smaller
features or changes that you can implement yourself.

1. Fork the `tellurium` repository on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:<your Github name>/tellurium.git

3. If virtualenvwrapper is not installed,
   `follow the directions <https://virtualenvwrapper.readthedocs.io/en/latest/>`__
   to install virtualenvwrapper.

4. Install your local copy of tellurium into a virtualenv with virtualenvwrapper::

    $ cd tellurium
    $ mkvirtualenv tellurium

   Use the ``--python`` option to select a specific version of Python for the
   virtualenv.

5. Install the required packages for development in the virtualenv using pip install::

    (tellurium)$ pip install --upgrade pip setuptools wheel
    (tellurium)$ pip install -r requirements.txt

6. Check out the branch that you want to contribute to. Most likely that will be
   ``master``::

    (tellurium)$ git checkout master

7. Create a branch for local development based on the previously checked out
   branch (see below for details on the branching model)::

    (tellurium)$ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

8. Setup tellurium for development::

    (tellurium)$ pip install -e .

9. When you are done making changes, check that your changes pass the tests with tox for your local Python version::

     (tellurium)$ tox -e py27
     (tellurium)$ tox -e py34
     (tellurium)$ tox -e py35

10. Commit your changes and push your branch to GitHub::

    (tellurium)$ git add .
    (tellurium)$ git commit -m "Your detailed description of your changes."
    (tellurium)$ git push origin name-of-your-bugfix-or-feature

11. Submit a pull request through the GitHub website. Once you submit a pull
    request your changes will be tested automatically against multiple python
    versions and operating systems. Further errors might appear during those
    tests.

For larger features that you want to work on collaboratively with other tellurium team members,
you may consider to first request to join the sbmlutils developers team to get write access to the
repository so that you can create a branch in the main repository
(or simply ask the maintainer to create a branch for you).
Once you have a new branch you can push your changes directly to the main
repository and when finished, submit a pull request from that branch to ``master``.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests in the ``tellurium/tests``
   directory. Except in rare circumstances, code coverage must
   not decrease (as reported by codecov which runs automatically when
   you submit your pull request)
2. If the pull request adds functionality, the docs should be
   updated. Put your new functionality into a function with a
   docstring and consider creating a notebook that demonstrates the
   usage.
3. The pull request must work for Python 2.7, 3.5 and 3.6.
4. Assign a reviewer to your pull request. If in doubt, assign 0u812, matthiaskoenig and kirichoi.
   Your pull request must be approved by at least one
   reviewer before it can be merged.

Unit tests and benchmarks
-------------------------

tellurium uses `pytest <http://docs.pytest.org/en/latest/>`_ for its
unit-tests and new features should in general always come with new
tests that make sure that the code runs as intended::

    (tellurium)$ pytest

Branching model
---------------

``master``
    Is the branch all pull-requests should be based on.
``{fix, bugfix, doc, feature}/descriptive-name``
    Is the recommended naming scheme for smaller improvements, bugfixes,
    documentation improvement and new features respectively.

Please use concise descriptive commit messages and consider using
``git pull --rebase`` when you update your own fork to avoid merge commits.

1. Tests are in the ``tellurium/tests`` directory. They are automatically run
   through continuous integration services on both python 2 and python 3
   when pull requests are made.
2. Please write tests for new functions. Writing documentation as well
   would also be very helpful.
3. Ensure code will work with both python 2 and python 3. For example,
   instead of ``my_dict.iteritems()`` use ``six.iteritems(my_dict)``

Thank you very much for contributing to tellurium!
