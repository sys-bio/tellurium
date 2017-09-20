import libsedml

if __name__ == "__main__":
    path = "test-sedml.xml"
    doc = libsedml.readSedMLFromFile(path)
    print(doc)
