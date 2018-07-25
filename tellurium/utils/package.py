"""
Provides trivial wrappers around pip and functionality
working with packages.
"""

from __future__ import print_function, absolute_import
import sys, subprocess

def check_macos_ver():
    import sys,platform
    if sys.platform == 'darwin':
        vstr, _, _ = platform.mac_ver()
        from distutils.version import LooseVersion
        import warnings
        v = LooseVersion(vstr)
        oldest_str = '10.9.0'
        if v < LooseVersion(oldest_str):
            warnings.warn('Your OS version is older than the oldest supported version ({} < {}). The operation may fail.'.format(vstr,oldest_str))

def searchPackage(name):
    """ Search pip package for package name.

    :param name: package name
    :return:
    """
    check_macos_ver()
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
    check_macos_ver()
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])


def upgradePackage(name):
    """ Upgrade pip package.

        :param name: package name
        :return:
        """
    check_macos_ver()
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', name])


def uninstallPackage(name):
    """ Uninstall pip package.

        :param name: package name
        :return:
        """
    check_macos_ver()
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', name])
