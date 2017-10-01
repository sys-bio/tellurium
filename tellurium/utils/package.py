"""
Provides trivial wrappers around pip and functionality
working with packages.
"""

from __future__ import print_function, absolute_import
import pip


def searchPackage(name):
    """ Search pip package for package name.

    :param name: package name
    :return:
    """

    pip.main(['search', name])


def installPackage(name):
    """ Install pip package.
    This has the advantage you don't have to
    manually track down the currently running
    Python interpreter and switch to the command line
    (useful e.g. in the Tellurium notebook viewer).

    :param name: package name
    :return:
    """
    pip.main(['install', name])


def upgradePackage(name):
    """ Upgrade pip package.

        :param name: package name
        :return:
        """
    pip.main(['install', '--upgrade', name])


def uninstallPackage(name):
    """ Uninstall pip package.

        :param name: package name
        :return:
        """
    pip.main(['uninstall', '-y', name])
