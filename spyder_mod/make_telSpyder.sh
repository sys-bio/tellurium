cp -Rv spyderlib/* ../installer/windows/spyder/spyderlib/
cp -Rv scripts/* ../installer/windows/spyder/scripts/
cd ../installer/windows/spyder
python setup.py bdist --formats=wininst --dist-dir ../spyder_dependencies

