# tellurium
<img title="tellurium logo" src="./docs/images/tellurium_logo.png" height="50" />
[![Documentation Status](https://readthedocs.org/projects/tellurium/badge/?version=latest)](http://tellurium.readthedocs.org/en/latest/?badge=latest)

Copyright 2014-2016
Kiri Choi, J Kyle Medley, Matthias König, Kaylene Stocking, Caroline Cannistra, Michal Galdzicki, and Herbert Sauro

![Parameter scan demo](http://tellurium.readthedocs.org/en/latest/_images/parameter_scan_2_0.png)

*Parmeter scan example*

## Introduction

Tellurium is a python environment based on the [Spyder2 IDE](https://github.com/spyder-ide/spyder) for building, simulating, and analysing models of biochemical networks, including gene regulatory networks, metabolic networks, and signaling pathways. It combines state-of-the-art scientific Python libraries, such as [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/), and includes special-purpose systems biology Python tools. Out of the box, Tellurium includes [libRoadRunner](https://github.com/sys-bio/roadrunner), [Antimony](http://antimony.sourceforge.net/), [PhraSED-ML](http://phrasedml.sf.net/), [libSBML](http://sbml.org/Software/libSBML) (via its [Python bindings](http://sbml.org/Software/libSBML/5.12.0/docs/formatted/python-api/)), and [libSED-ML](https://github.com/fbergmann/libSEDML).

The Tellurium project is funded from the NIH/NIGMS (GM081070).

## Installation Instructions

Tellurium is availlable via two distributions:

1. As a Windows setup file / Apple disk image which includes the Spyder IDE and all Tellurium packages
2. As a Python meta-package which can be installed via the Anaconda package manager

Option 1. does not modify or conflict with any previous Python installation. Option 2. allows you to use Tellurium from within a pre-existing Anaconda installation, including via a notebook. If you are a new user, it is recommended that you try option 1. first.

### Option 1: IDE installer

#### Windows

1. [Download Tellurium for Windows](https://sourceforge.net/projects/pytellurium/files/Tellurium-1.3/1.3.5/Tellurium-1.3.5-Python-2.7-win32-portable-setup.exe/download)
2. Double-click the installer to start the installation
3. Follow the instructions

NOTE: Installation requires administrative rights. It is recommended to accept the default settings.

#### Mac OSX

1. [Download Tellurium for Mac OS X 10.10 or later](https://sourceforge.net/projects/pytellurium/files/Tellurium-1.3/1.3.5/Tellurium-1.3.5-Spyder-2.3.8-OSX.dmg/download)
2. Double-click the .dmg file to open a new window
3. Double-click the Spyder icon

NOTE: On some older hardware we have noticed that the .dmg sometimes fails. If this happens, we recommend using the Anaconda package manager (see below).

### Option 2: Anaconda package (Linux/OSX only):

Binaries for Tellurium are available via the [Anaconda](https://www.continuum.io/downloads) package manager for **Python 2.7**. Neither the IDE plugins for Spyder nor SBOL functionality is available when using this method. To install Tellurium and the necessary packages on both Linux and OS X, type the following into a terminal:

```
conda install -c sys-bio tellurium
conda install jinja2 ipython
conda install -c SBMLTeam python-libsbml 
```

Detailed instructions for using the `conda` package manager are available [here.](http://conda.pydata.org/docs/using/pkgs.html) 

## System Requirements

The [Spyder IDE](https://github.com/sys-bio/tellurium#installation-instructions) installers are tested with Windows 7+ and Mac OS X 10.9+. Some older Macs cannot run Spyder, regardless of whether the operating system is up-to-date. Anaconda packages are tested on RHEL 6.6, Debian 8, Ubuntu 14.04, and Mac OS X 10.10.

## Usage

```{python}
import tellurium as te

rr = te.loada('''
    model example0
      S1 -> S2; k1*S1
      S1 = 10
      S2 = 0
      k1 = 0.1
    end
''')

result = rr.simulate(0, 40, 500) 
te.plotArray(result)
```

![Tellurium front page demo](https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/tellurium-front-page-image.png)

## API documentation 

http://tellurium.readthedocs.org/en/latest/

## Known Issues

### Python support

**Python 2** is the highest supported Python version at the time of writing, due to the fact that not all packages included in Tellurium are Python 3 compatible.

## Legal

The source code for the Tellurium Python package is hosted at https://github.com/sys-bio/tellurium and is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Tellurium uses third-party dependencies which may be licensed under different terms. Consult the documentation for the respective third-party packages for more details.

TELLURIUM AND ALL SOFTWARE BUNDLED WITH TELLURIUM (HEREAFTER "THE SOFTWARE") IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

