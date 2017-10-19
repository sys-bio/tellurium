# tellurium
<img title="tellurium logo" src="./docs/images/tellurium_logo.png" height="50" />

[![Documentation Status](https://readthedocs.org/projects/tellurium/badge/?version=latest)](http://tellurium.readthedocs.org/en/latest/) 
[![Build Status](https://travis-ci.org/sys-bio/tellurium.svg?branch=master)](https://travis-ci.org/sys-bio/tellurium)


Copyright 2014-2017
Kiri Choi, J Kyle Medley, Matthias König, Kaylene Stocking, Caroline Cannistra, Michal Galdzicki, and Herbert Sauro

## Introduction

Tellurium is a python environment based on the [Spyder2 IDE](https://github.com/spyder-ide/spyder) 
for building, simulating, and analysing models of biochemical networks, 
including gene regulatory networks, metabolic networks, and signaling pathways. 
It combines state-of-the-art scientific Python libraries, such 
as [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/), 
and includes special-purpose systems biology Python tools. Out of the box, 
Tellurium includes [libRoadRunner](https://github.com/sys-bio/roadrunner), 
[Antimony](http://antimony.sourceforge.net/), [PhraSED-ML](http://phrasedml.sf.net/), 
[libSBML](http://sbml.org/Software/libSBML) (via its [Python bindings](http://sbml.org/Software/libSBML/5.12.0/docs/formatted/python-api/)), and [libSED-ML](https://github.com/fbergmann/libSEDML).

The Tellurium project is funded from the NIH/NIGMS (GM081070).

## Installation Instructions

Tellurium can be installed via a front-end which includes all of its constituent packages, or via `pip`:

1. [Notebook front-end](#front-end-1-tellurium-notebook)
2. [IDE front-end](#front-end-2-tellurium-ide)
3. [pip](#pip-installation-no-front-end)

We recommend first-time users choose one of the front-ends, while developers looking to integrate Tellurium use the pip package. The IDE front-end provides a MATLAB like experience with a code editor and Python console. The notebook front-end provides a notebook interface similar to [Jupyter](http://jupyter.org/), and features notebook cells for inline OMEX, a human-readable representation of COMBINE archives.

### Front-end 1: Tellurium Notebook


<img align="left" width="32px" id="windows" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/windows.png">
<h3>Windows</h3>
<br style="clear:both"/>

1. [Download Tellurium notebook for Windows](https://github.com/sys-bio/tellurium/releases/download/2.0.0-alpha4/Tellurium.Setup.2.0.0.exe)
2. Double-click the installer to start the installation
3. Follow the instructions

<img align="left" width="32px" id="mac-osx" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/macos.png">
<h3>Mac OS X</h3>
<br style="clear:both"/>

1. [Download Tellurium notebook for Mac OS X 10.10 or later](https://github.com/sys-bio/tellurium/releases/download/2.0.0-alpha4/Tellurium-2.0.0.dmg)
2. Double-click the .dmg file to open a new window
3. Drag the Tellurium icon to your Applications
4. You can now launch Tellurium from e.g. Spotlight or your Applications folder directly


<img align="left" width="32px" id="redhat" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/redhat.png">
<h3>Linux (RedHat)</h3>
<br style="clear:both"/>

1. TODO: Upload rpm

<img align="left" width="32px" id="debian" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/debian.png">
<h3>Linux (Debian)</h3>
<br style="clear:both"/>

1. [Download Tellurium notebook for Debian](https://github.com/sys-bio/tellurium/releases/download/2.0.0-alpha9/Tellurium_2.0.0_amd64.deb)
2. Install the package using `dpkg -i Tellurium_2.0.0_amd64.deb`
3. You should be able to launch Tellurium from your activities pane. If not, log out and in again or run `tellurium` from the terminal.

### Front-end 2: Tellurium IDE

#### Windows

1. [Download Tellurium IDE for Windows](https://sourceforge.net/projects/pytellurium/files/Tellurium-2.0/2.0.3/Tellurium-2.0.3-Python-2.7-win64-portable-setup.exe/download)
2. Double-click the installer to start the installation
3. Follow the instructions

NOTE: Installation requires administrative rights. It is recommended to accept the default settings.

#### Mac OSX (Legacy)

1. [Download Tellurium IDE for Mac OS X 10.10 or later](https://github.com/sys-bio/tellurium/releases/download/1.3.5-rc3/Tellurium-1.3.5-Spyder-2.3.8-OSX.dmg)
2. Double-click the .dmg file to open a new window
3. Double-click the Spyder icon

NOTE: On some older hardware we have noticed that this front-end sometimes fails. If this happens, we recommend using the Tellurium notebook front-end instead.

### PIP Installation (no front-end)

Binaries wheels for Tellurium are available via the `pip` command. To install Tellurium and the necessary packages on both Linux and OS X, type the following into a terminal:

```bash
pip install tellurium
```

Detailed instructions for using the `conda` package manager are available [here.](http://conda.pydata.org/docs/using/pkgs.html) 

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

## Documentation 

* General: http://tellurium.readthedocs.org/en/latest/
* API: http://tellurium.readthedocs.io/en/latest/_apidoc/tellurium.html


## System Requirements

The Tellurium notebook supports Windows 10, Mac OS X 10.10+, Debian 8+, and Fedora 22+. The [Spyder IDE](https://github.com/sys-bio/tellurium#installation-instructions) installers are tested with Windows 7+ and Mac OS X 10.9+. Some older Macs cannot run Spyder, regardless of whether the operating system is up-to-date. Pip packages are tested on Fedora 22, Debian 8, Ubuntu 14.04, and Mac OS X 10.10.

## Supported Python Versions

The Tellurium PyPI packages support 64-bit Python versions 2.7, 3.4, 3.5, and 3.6 for Windows, Mac, and Linux. The notebook viewer comes with Python 3.6 (64-bit) and the IDE comes with Python 2.7 (64-bit).

## Legal

The source code for the Tellurium Python package is hosted at https://github.com/sys-bio/tellurium and is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Tellurium uses third-party dependencies which may be licensed under different terms. Consult the documentation for the respective third-party packages for more details.

TELLURIUM AND ALL SOFTWARE BUNDLED WITH TELLURIUM (HEREAFTER "THE SOFTWARE") IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

