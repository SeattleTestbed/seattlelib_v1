"""
Test the removing of a single file in a bundle through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')

ORIGINAL_BUNDLE_FN = 'test_readonly.bundle.repy'
TEST_BUNDLE_FN = 'test.bundle.repy'
FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# We make a local copy of the test bundle so that we
# don't affect the execution of other tests

# This must be done in binary mode.  Otherwise, differences of filesize due to
# \r\n and \n on different OSes will cause the bundler to look for data at the
# wrong places.
_bundle_copy_file(ORIGINAL_BUNDLE_FN, TEST_BUNDLE_FN)

bundle = bundle_Bundle(TEST_BUNDLE_FN, 'a')
bundle.remove(FILENAMES[0])
bundle.close()

# We shouldn't see 'src1' in this list...
#pragma out {'src3copy': 461, 'src2copy': 100}
bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
print bundle.list()
bundle.close()

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN)