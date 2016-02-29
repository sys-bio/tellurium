from __future__ import print_function

import re
xpath = '/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id="ps_a"]/@value'
m = re.findall(r'id="(.*?)"', xpath)

print(m[0])