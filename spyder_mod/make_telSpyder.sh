cp -Rv spyderlib/* ~/src/spyder-mgaldzic/spyderlib/
cp -Rv scripts/* ~/src/spyder-mgaldzic/scripts/
cd ~/src/spyder-mgaldzic/
python setup.py bdist --formats=wininst --dist-dir ../tellurium/installer/windows/spyder_dependencies

