"""
Test the extracting of a single file to a string in a bundle through the API.
"""

import repyhelper
repyhelper.translate_and_import('bundle.repy')

TEST_BUNDLE_FN = 'test_readonly.bundle.repy'
FILENAMES = ['src1copy', 'src2copy', 'src3copy']

bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
file_contents = bundle.extract_to_string(FILENAMES[0])
bundle.close()

if file_contents != open('src1', 'rb').read():
  print "Unexpected extracted string:"
  print file_contents