"""
Test the getting the listing of files in a bundle through the API.
"""

import os
import repyhelper
repyhelper.translate_and_import('bundle.repy')


TEST_BUNDLE_FN = 'test_readonly.bundle.repy'

# Dict mapping filenames to length of encoded files
EXPECTED_DICT = {'src3copy': 461, 'src2copy': 100, 'src1copy': 87}

actual_contents = bundle_Bundle(TEST_BUNDLE_FN, 'r').list() 
if EXPECTED_DICT != actual_contents:
  print "Unexpected contents in bundle"
  print actual_contents