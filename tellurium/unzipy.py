#**********************************************************************
# Description:
#    Unzips the contents of a zip file into an existing folder
#    Assumes COMBINE archive SED-ML format and returns location of SED-ML file from manifest 
# Arguments:
#  1 - input zip file
#  2 - output folder - pathname to folder that will contain the contents of the zip file
#**********************************************************************
#!/usr/bin/env python
import sys, zipfile, os, traceback
from os.path import isdir, join, normpath, split

def main(args):
  script = args[0]
  scriptDirectory = sys.path[0]
  inFile = args[1]
  outFolder = args[2]
  workingDirectory = os.getcwd()     # the current working directory

  # Create the zipfile handle for reading and unzip it
  zip = zipfile.ZipFile(inFile, 'r')
  unZip(outFolder, zip)
  zip.close()


def unZip(path, zip):
  # If the output location does not yet exist, create it
  if not isdir(path):
    os.makedirs(path)    

  for each in zip.namelist():
    print("Extracting " + os.path.basename(each) + " ...")
    # check if the item includes a subdirectory
    # if it does, create the subdirectory in the output folder and write the file
    # otherwise, just write the file to the output folder
    if not each.endswith('/'): 
      root, name = split(each)
      directory = normpath(join(path, root))
      if not isdir(directory):
        os.makedirs(directory)
      file(join(directory, name), 'wb').write(zip.read(each))


def readManifest(manifestPathName):
  import xml.etree.ElementTree as et
  tree = et.parse(manifestPathName)
  root = tree.getroot()
  print root
  for child in root:
    #print(child.tag, child.attrib)
    format = child.attrib['format']
    if(format.endswith("sed-ml")):
      return(child.attrib['location'])
  print("# Bad .sedx file format.")
  return(null)


if __name__ == '__main__':

  main(sys.argv)
  #main(["unzipy", "C:/dan/temp/pysedmltmp/lorenz.zip", "C:/dan/temp/pyout"])
