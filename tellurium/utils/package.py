"""
Provides trivial wrappers around pip and functionality
working with packages.
"""

from __future__ import print_function, absolute_import
import sys, subprocess

def searchPackage(name):
    """ Search pip package for package name.

    :param name: package name
    :return:
    """
    subprocess.check_call([sys.executable, '-m', 'pip', 'search', name])


def installPackage(name):
    """ Install pip package.
    This has the advantage you don't have to
    manually track down the currently running
    Python interpreter and switch to the command line
    (useful e.g. in the Tellurium notebook viewer).

    :param name: package name
    :return:
    """
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])


def upgradePackage(name):
    """ Upgrade pip package.

        :param name: package name
        :return:
        """
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', name])


def uninstallPackage(name):
    """ Uninstall pip package.

        :param name: package name
        :return:
        """
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', name])
