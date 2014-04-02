cp -Rv spyderlib/* ../installer/windows/spyder/spyderlib/
cp -Rv scripts/* ../installer/windows/spyder/scripts/
cp -Rv img_src/* ../installer/windows/spyder/img_src/
cp -Rv setup.py ../installer/windows/spyder/setup.py
cd ../installer/windows/spyder
python setup.py bdist --formats=wininst --dist-dir ../spyder_dependencies

