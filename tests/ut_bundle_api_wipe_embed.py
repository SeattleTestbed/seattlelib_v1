"""
Test wiping of a bundle that does has an embedded script (on API)
"""

import os
import sys
import repyhelper
repyhelper.translate_and_import('bundle.repy')

ORIGINAL_BUNDLE_FN = 'test_embedded_readonly.bundle.repy'
TEST_BUNDLE_FN = 'test.bundle.repy'
# The original file that was embedded into the bundle
EMBED_SCRIPT_FN = 'testscript.repy'

# We make a local copy of the test bundle so that we
# don't affect the execution of other tests

# This must be done in binary mode.  Otherwise, differences of filesize due to
# \r\n and \n on different OSes will cause the bundler to look for data at the
# wrong places.
_bundle_copy_file(ORIGINAL_BUNDLE_FN, TEST_BUNDLE_FN)

bundle_clear_bundle_from_file(TEST_BUNDLE_FN)

# Make sure the output matches the test script
output = open(TEST_BUNDLE_FN, 'rb').read()
if output != open(EMBED_SCRIPT_FN, 'rb').read():
  print "Wiped bundle does not match expected output:"
  print "Got:"
  print output