
# tellurium
[![Documentation Status](https://readthedocs.org/projects/tellurium/badge/?version=latest)](http://tellurium.readthedocs.org/en/latest/?badge=latest)

Copyright 2014-2016
Kiri Choi, J Kyle Medley, Matthias König, Kaylene Stocking, Caroline Cannistra, Michal Galdzicki, and Herbert Sauro

![Parameter scan demo](http://tellurium.readthedocs.org/en/latest/_images/parameter_scan_2_0.png)

*Parmeter scan example courtesy of Matthias König*

## Introduction

Tellurium is a python environment based on the [Spyder2 IDE](https://github.com/spyder-ide/spyder) for building, simulating, and analysing models of biochemical networks, including gene regulatory networks, metabolic networks, and signaling pathways. It combines state-of-the-art scientific Python libraries, such as [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/), and includes special-purpose systems biology Python tools. Out of the box, Tellurium includes [libRoadRunner](https://github.com/sys-bio/roadrunner), [Antimony](http://antimony.sourceforge.net/), [PhraSED-ML](http://phrasedml.sf.net/), [libSBML](http://sbml.org/Software/libSBML) (via its [Python bindings](http://sbml.org/Software/libSBML/5.12.0/docs/formatted/python-api/)), and [libSED-ML](https://github.com/fbergmann/libSEDML).

The Tellurium project is funded from the NIH/NIGMS (GM081070).

## Install

Tellurium is availlable as a self-contained installer or as an installable collection of packages via the Anaconda package manager.

It is recommended that you try the conventional installers first. On windows, download the installer, run the installer and follow the instructions. For the Mac, download the dmg file, then:

1. Double click the .dmg to make its content available (name will show up in the Finder sidebar), usually a window opens showing the content as well.
2. Drag the application from the .dmg window into /Applications to install (may need an administrator password)

On some older hardware we have noticed that the Mac distribution fails, if this happens to you then we recommend using the Anaconda package manager, see below. 

#### Conventional installers:

* [Download Tellurium for Windows](https://sourceforge.net/projects/pytellurium/files/Tellurium-1.3/1.3.4/Tellurium-1.3.4-Python-2.7-win32-portable-setup.exe/download)
* [Download Tellurium for Mac OS X 10.10 or later](https://github.com/sys-bio/tellurium/releases/download/1.3.5-rc1/Tellurium-1.3.5-Spyder-2.3.8-OSX.dmg)

#### Anaconda package (Linux/OSX) instructions:

Binaries for Tellurium are available via the Anaconda package manager, which is the most straight-forward installation option for users who do not wish to be locked-in to the full Spyder IDE. Tellurium requires the libsbml Python package to be installed. This package is available on Anaconda via the SBMLTeam channel. The following instructions can be used to install Tellurium and libsbml on both Linux and OS X:

```
conda install -c sys-bio tellurium
conda install -c SBMLTeam python-libsbml 
```

For further information we refer the reader to the [conda installation instructions.](http://conda.pydata.org/docs/using/pkgs.html) 

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

## Legal

The source code for the Tellurium Python package is hosted at https://github.com/sys-bio/tellurium and is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Tellurium uses third-party dependencies which may be licensed under different terms. Consult the documentation for the respective third-party packages for more details.

TELLURIUM AND ALL SOFTWARE BUNDLED WITH TELLURIUM (HEREAFTER "THE SOFTWARE") IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

