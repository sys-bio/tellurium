<h1><img title="tellurium logo" src="./docs/images/tellurium_logo.png" height="50" />&nbsp;&nbsp;tellurium</h1>

<!-- These badges come from shield.io, zenodo or travis -->

<table style="width:100%">
  <tr>
    <td><img alt="Github version", src="https://travis-ci.com/sys-bio/tellurium.svg?branch=master"></td>
    <td><img alt="Read the Docs" src="https://img.shields.io/readthedocs/tellurium"></td>
    <td><a href="https://badge.fury.io/gh/sys-bio%2Ftellurium"><img src="https://badge.fury.io/gh/sys-bio%2Ftellurium.svg" alt="GitHub version" height="18"></a></td>
  </tr>
</table> 

 <table style="width:100%">
  <tr>
    <td><img alt="Licence", src="https://img.shields.io/hexpm/l/tellurium"</td>
    <td><img alt="PyPI - Downloads", src="https://img.shields.io/pypi/dm/tellurium"></td>
    <td><img alt="Funding", src="https://img.shields.io/badge/Funding-NIGMS%20(GM123032)-blue"></td>
    <td><img alt="Funding", src="https://img.shields.io/badge/Funding-NIBIB%20(EB028887)-blue"></td>
    <td><a href="https://badge.fury.io/py/tellurium"><img src="https://badge.fury.io/py/tellurium.svg" alt="PyPI version" height="18"></a> </td>
   </tr>
</table> 

 <table style="width:100%">
  <tr>
    <td><a href="https://doi.org/10.5281/zenodo.2548944"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2548944.svg" alt="DOI"></a></td>
  </tr>
</table>

Copyright 2014-2023
Kiri Choi, J Kyle Medley, Matthias König, Kaylene Stocking, Caroline Cannistra, Michal Galdzicki, Ciaran Welsh, Lucian Smith, Adel Heydarabadipour, and Herbert Sauro

## Introduction

Tellurium is a python environment for reproducible dynamical modeling of biological networks. 
Tellurium provides the interfacial code to convert between standard formats and utilize powerful 
libraries without requiring technical expertise, allowing you to focus on what’s important: 
building better models. Tellurium also provides first-class support for exchangeability via 
[COMBINE archives](http://co.mbine.org/documents/archive), allowing you to share your models 
and simulations with other tools.

Tellurium combines state-of-the-art scientific Python libraries, such 
as [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/), 
and includes special-purpose systems biology Python tools. Out of the box, 
Tellurium includes [libroadrunner](https://github.com/sys-bio/roadrunner), 
[antimony](http://antimony.sourceforge.net/), [phrasedml](http://phrasedml.sf.net/), 
[libsbml](http://sbml.org/Software/libSBML), and [libsedml](https://github.com/fbergmann/libSEDML).

The Tellurium (and libroadrunner project) project is funded from the NIH/NIGMS (GM081070) and NIH/NIBIB U24EB028887.

## Documentation 
* General: http://tellurium.readthedocs.org/en/latest/
* API: http://tellurium.readthedocs.io/en/latest/_apidoc/tellurium.html
* Webpage: http://tellurium.analogmachine.org/

## Usage Example

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

![Tellurium front page demo](./docs/images/tellurium-front-page-image.png)

## Installation Instructions

:exclamation:**Attention to those using Python 2.7 :**
**[Python 2.7 reached EOL on January 1st, 2020](https://www.python.org/doc/sunset-python-2/). Support for Python 2.7 has been dropped, though previous releases will continue to be available.**

Tellurium can be installed as a Python package, with a front-end (Notebook, IDE), or in a cloud environment (Google Colab):

A. [Python package (pip)](#install-via-pip-no-front-end)  
B. [IDE front-end](#front-end-1-spyder-for-tellurium-ide) based on [Spyder](https://www.spyder-ide.org/)  
C. [Notebook front-end](#front-end-2-tellurium-notebook)  
D. [Google Colab](#google-colab)  

We recommend first-time users choose one of the front-ends, while developers looking to integrate Tellurium use the pip package. All python desktop IDE graphical front-ends should work. We know for certain that telluirum will work from Spyder, pyCharm and Visual Studio Code.

The IDE front-end provides a MATLAB like experience with a code editor and Python console. 
The notebook front-end provides a notebook interface similar to [Jupyter](http://jupyter.org/), 
and features notebook cells for inline OMEX, a human-readable representation of COMBINE archives.

For any issues with installation and setup, please check [FAQ](https://github.com/sys-bio/tellurium/wiki/FAQ) or [contact us](#contact-us). 

-------

### Install via pip
[![PyPI version](https://badge.fury.io/py/tellurium.svg)](https://badge.fury.io/py/tellurium)

If you have a version of Python in an environment you're comfortable with, you can add Tellurium with pip:

```
pip install tellurium
```	

Tellurium itself is Python-only, and is available for any version of Python 3.  Its main binary dependency, roadrunner, should be installed with Tellurium, and should be available for the latest three or four versions of Python (currently 3.8, 3.9, 3.10, and 3.11), for Windows, Mac (both Intel and ARM), and Linux. 

For those using Anaconda, we currently do not have a separate Anaconda version of Tellurium, so you'll need to install it via pip, as above.

:exclamation:**For detailed instructions on how to setup Tellurium on Anaconda distributions, 
see [this page](https://github.com/sys-bio/tellurium/wiki/FAQ#i-would-like-to-use-tellurium-on-anaconda-what-should-i-do).** 


For developers, the latest stable version from the repository can be installed via
```
pip install git+https://github.com/sys-bio/tellurium.git
```

-------


### Front-end 1: Spyder for Tellurium IDE
The Tellurium Spyder installers are tested with Windows 10 and 11, and come with a choice of Python versions.

**For those who wish to use Tellurium with Spyder IDE on Mac OS X or Linux, we suggest you to install through [Anaconda](https://www.anaconda.com/) by 
following the instructions on [this page](https://github.com/sys-bio/tellurium/wiki/FAQ#i-would-like-to-use-tellurium-on-anaconda-what-should-i-do).**

<img align="left" width="32px" id="windows" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/windows.png">
<h4>Windows</h4>
<br style="clear:both"/>

:exclamation:**Attention to those upgrading to Tellurium Spyder IDE from an older version :** 
We strongly suggest you to completely remove the older version of Tellurium Spyder IDE prior to installing the latest version.

1. Download Tellurium Spyder for Windows:
    * [Python 3.7](https://sourceforge.net/projects/pytellurium/files/Tellurium-2.3/2.3.5/Tellurium-2.3.5-Python-3.7-win64-setup.exe/download)
    * [Python 3.8](https://sourceforge.net/projects/pytellurium/files/Tellurium-2.3/2.3.5/Tellurium-2.3.5-Python-3.8-win64-setup.exe/download)
    * [Python 3.10](https://sourceforge.net/projects/pytellurium/files/Tellurium-2.4/2.4.0/Tellurium-2.4.0-Python-3.10-win64-setup.exe/download)
    * [Python 3.11](https://sourceforge.net/projects/pytellurium/files/Tellurium-2.4/2.4.0/Tellurium-2.4.0-Python-3.11-win64-setup.exe/download)
2. Double-click the installer to start the installation
3. Follow the instructions

If you wish to use a different version of Python, you'll need to install Tellurium from the windows command line by using the command: pip install tellurium


NOTE: Installation requires administrative rights. It is recommended to accept the default settings.

<img align="left" width="32px" id="mac-osx" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/macos.png">
<h4>Mac OS X</h4>
<br style="clear:both"/>

Mac OS X users can install Tellurium and the Spyder IDE through Anaconda:

1. [Download the Anaconda distribution for Mac OS X.](https://www.anaconda.com/download). 

2. [Follow the installer instructions.](https://docs.anaconda.com/anaconda/install/linux). The installer will install Spyder as part of the installation process. If you customize the installation, you will have a chance to select which packages to install - ensure Spyder is selected.
3. When prompted, add Anaconda to your PATH (optional, but this will make the following steps easier).
4. [Open a Terminal](https://www.wikihow.com/Open-a-Terminal-Window-in-Mac) and run the command:
```
conda install msgpack-python
```
Next, install Tellurium itself:
```
pip install tellurium
```
If this fails, try using the default absolute path to Anaconda, which will probably be something like:
```
/Users/<your-user>/opt/anaconda3/bin/pip install tellurium
```
5. Launch the Anaconda Navigator via Launchpad. In Anaconda Navigator, run Spyder and then try `import tellurium` within the Spyder editor or console.

<img align="left" width="32px" id="mac-osx" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/macos.png">
<h4>Mac OS X (Legacy)</h4>
<br style="clear:both"/>

Currently, only a legacy version of the Mac Spyder IDE is available. We recommend using the Notebook front-end on Mac.

1. [Download Tellurium IDE for Mac OS X 10.10 or later](https://github.com/sys-bio/tellurium/releases/download/1.3.5-rc3/Tellurium-1.3.5-Spyder-2.3.8-OSX.dmg)
2. Double-click the .dmg file to open a new window
3. Double-click the Spyder icon

-------

### Front-end 2: Tellurium Notebook
The Tellurium notebook is no longer being updated, but is still available.  It was tested with Windows 10, Mac OS X 10.10+, Debian 8+, and Fedora 22+.
The notebook viewer comes with Python 3.6 (64-bit).

<img align="left" width="32px" id="windows" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/windows.png">
<h4>Windows</h4>
<br style="clear:both"/>

1. [Download Tellurium Notebook for Windows](https://sourceforge.net/projects/pytellurium/files/notebook/Tellurium%20Setup%202.1.1.exe/download)
2. Double-click the installer `*.exe` to start the installation
3. Follow the instructions

<img align="left" width="32px" id="mac-osx" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/macos.png">
<h4>Mac OS X</h4>
<br style="clear:both"/>

1. [Download Tellurium Notebook for Mac OS X 10.10 or later](https://sourceforge.net/projects/pytellurium/files/notebook/Tellurium-2.1.1.dmg/download)
2. You may need to [disable Gatekeeper](https://github.com/sys-bio/tellurium/wiki/FAQ#on-mac-after-downloading-tellurium-i-cant-open-it-because-it-is-from-an-unidentified-developer)
3. Double-click the `*.dmg` file to open a new window
4. Drag the Tellurium icon to your Applications
5. You can now launch Tellurium from Spotlight or directly from your applications folder

<img align="left" width="32px" id="redhat" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/redhat.png">
<h4>Linux (RedHat)</h3>
<br style="clear:both"/>

1. [Download Tellurium Notebook (.rpm)](https://sourceforge.net/projects/pytellurium/files/notebook/Tellurium-2.1.1.rpm/download)
2. Install the package using `dnf install Tellurium-2.1.1.rpm`
3. You should be able to launch Tellurium from your activities pane. If not, log out and in again or run `tellurium` from the terminal.

<img align="left" width="32px" id="debian" src="https://raw.githubusercontent.com/wiki/sys-bio/tellurium/img/debian.png">
<h4>Linux (Debian)</h4>
<br style="clear:both"/>

1. [Download Tellurium Notebook (.deb)](https://sourceforge.net/projects/pytellurium/files/notebook/Tellurium_2.1.1_amd64.deb/download)
2. Install the package using `dpkg -i Tellurium_2.1.1_amd64.deb`
3. You should be able to launch Tellurium from your activities pane. If not, log out and in again or run `/opt/Tellurium/tellurium` from the terminal.

<br>

:question:Looking for old releases? [You can find them here.](https://sourceforge.net/projects/pytellurium/files/notebook) To install an old release over a new release, you will need to [manually wipe the data directory.](https://github.com/sys-bio/tellurium/wiki/FAQ#how-do-i-uninstall-tellurium-notebook)

<br>

-------

### Google Colab
Tellurium can be used entirely in a browser using [Google Colab](https://colab.research.google.com/).  Ideally, it will work with the following steps (updated May 2023)
  
1. run a cell with ```!apt-get install libncurses5```
2. run a cell with ```!pip install -q tellurium==2.2.8```
3. (Very important) Restart the runtime (From the menu: 'Runtime / Restart runtime')
4. Test by typing ```import telluirum as te```
  
The Python version behind Colab changes periodically, so what worked one day may stop working the next, but the following Colab notebook worked when used at ICSB 2022:  https://colab.research.google.com/drive/1wddLftHNhetbozZY29r2HRkzQLl1F_fs#scrollTo=l1bCgW46-adR and will hopefully be instructive.


  
## Citing

If you use Tellurium in your research, we would appreciate following citations in any works you publish:

Medley et al. (2018). ["Tellurium notebooks—An environment for reproducible dynamical modeling in systems biology."](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006220) *PLoS Computational Biology*, 14(6), e1006220.

Choi et al. (2018). ["Tellurium: An extensible python-based modeling environment for systems and synthetic biology."](https://www.sciencedirect.com/science/article/pii/S0303264718301254) *Biosystems*, 171, 74-79.

## Contact Us

For general questions, requesting help, or reporting bugs, feel free to use the [GitHub issue tracker](https://github.com/sys-bio/tellurium/issues).  You can also post to the  [Tellurium-discuss](https://groups.google.com/d/forum/tellurium-discuss) mailing list.

## Legal

The source code for the Tellurium Python package is hosted at https://github.com/sys-bio/tellurium and is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Tellurium uses third-party dependencies which may be licensed under different terms. Consult the documentation for the respective third-party packages for more details.

TELLURIUM AND ALL SOFTWARE BUNDLED WITH TELLURIUM (HEREAFTER "THE SOFTWARE") IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
