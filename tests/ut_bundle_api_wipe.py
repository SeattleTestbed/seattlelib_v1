"""
Test wiping of a bundle that does not have an embedded script (on API)
"""

import os
import sys
import repyhelper
repyhelper.translate_and_import('bundle.repy')

# We make a local copy of the test bundle so that we
# don't affect the execution of other tests
ORIGINAL_BUNDLE_FN = 'test_readonly.bundle.repy'
TEST_BUNDLE_FN = 'test.bundle.repy'

# This must be done in binary mode.  Otherwise, differences of filesize due to
# \r\n and \n on different OSes will cause the bundler to look for data at the
# wrong places.
_bundle_copy_file(ORIGINAL_BUNDLE_FN, TEST_BUNDLE_FN)

# Perform action
bundle_clear_bundle_from_file(TEST_BUNDLE_FN)

# Make sure the output is empty
# If something is printed, then UTF will flag it as an error 
sys.stdout.write(open(TEST_BUNDLE_FN, 'rb').read())