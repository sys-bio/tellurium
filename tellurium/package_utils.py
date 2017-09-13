"""
Provides trivial wrappers around pip.
"""
from __future__ import print_function, division, absolute_import
import pip

def searchPackage(name):
    """ Search pip package.

    :param name: package name
    :return:
    """

    pip.main(['search', name])


def installPackage(name):
    """ Install pip package.

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
