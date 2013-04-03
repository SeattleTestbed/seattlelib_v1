"""
Test the removing of multiple files in a bundle through the command line.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')

ORIGINAL_BUNDLE_FN = 'test_readonly.bundle.repy'

# We make a local copy of the test bundle so that we
# don't affect the execution of other tests
TEST_BUNDLE_FN = 'test.bundle.repy'
FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# This must be done in binary mode.  Otherwise, differences of filesize due to
# \r\n and \n on different OSes will cause the bundler to look for data at the
# wrong places.
_bundle_copy_file(ORIGINAL_BUNDLE_FN, TEST_BUNDLE_FN)

bundle_test_helper.run_program("bundler.py", ["remove", TEST_BUNDLE_FN] + FILENAMES)

# We shouldn't see ANY files in this list...
#pragma out {}
bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
print bundle.list()
bundle.close()

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN)