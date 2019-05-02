#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 13:40:40 2019

@author: mikaelapisanileal
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 16:01:57 2019

@author: mikaelapisanileal
"""

import sys
import getopt
from APIs import import_data

def info():
    print('main.py -p <path>')

def main(argv):
   path_zipcodes = ''
   try:
      opts, args = getopt.getopt(argv,'hp:',['path_zipcodes='])
   except getopt.GetoptError:
      info()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         info()
         sys.exit()
      elif opt in ('-p', '--path_zipcodes'):
         path_zipcodes = arg
        
   import_data(path_zipcodes)
   
if __name__ == "__main__":
    main(sys.argv[1:])
