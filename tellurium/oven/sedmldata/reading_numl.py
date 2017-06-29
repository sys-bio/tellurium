from __future__ import absolute_import, print_function
import warnings
import numpy as np
import pandas as pd

try:
    import libsedml
except ImportError:
    import tesedml as libsedml
print('Version:', libsedml.getLibSEDMLDottedVersion())

SOURCE_CSV = "./oscli.csv"
SOURCE_NUML = "./oscli.numl"

import libnuml


def parse_dimension_description(dd):
    """ Parses the dimension information from the dimension description.

          <dimensionDescription>
            <compositeDescription indexType="double" name="time">
              <compositeDescription indexType="string" name="SpeciesIds">
                <atomicDescription valueType="double" name="Concentrations" />
              </compositeDescription>
            </compositeDescription>
          </dimensionDescription>
          <dimension>

    :param dd:
    :return:
    """
    cd_top = dd.getComposiiteDescription()
    print('cd_top', cd_top)

    dim_info = None
    # FIXME: implement
    return dim_info


def load_numl_data(source):
    """ Helper function for loading data files from given source.

    For more information see:
        https://github.com/numl/numl

          <dimensionDescription>
            <compositeDescription indexType="double" name="time">
              <compositeDescription indexType="string" name="SpeciesIds">
                <atomicDescription valueType="double" name="Concentrations" />
              </compositeDescription>
            </compositeDescription>
          </dimensionDescription>

    :param source:
    :return: data matrix
    """
    # FIXME: handle urn/url sources

    doc_numl = libnuml.readNUMLFromFile('./oscil.numl')
    print(doc_numl)

    # reads all the resultComponents from the numl file
    results = []
    print(doc_numl.getNumResultComponents())
    print(libnuml)

    for res_comp in doc_numl.getResultComponents():
        print(type(res_comp))
        dd = res_comp.getDimensionDescription()
        print(dd)
        dimension_info = parse_dimension_description(dd)

        for cvalue in dd.getComponentValues():
            print(cvalue)

    # TODO: figure out the dimensionality, and create np.array
    # if 2D return as pandas DataFrame (Does this work with the slicing?)

    columns = None
    data = None
    df = None
    # TODO: implement
    return df



# load data from sources
df_numl = load_numl_data(SOURCE_NUML)
print(df_numl)
