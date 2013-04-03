"""
Test the creation of new bundles when the specified file is already a bundle
with bundled files
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')


# We make a local copy of the test bundle so that we
# don't affect the execution of other tests
ORIGINAL_BUNDLE_FN = 'test_embedded_readonly.bundle.repy'
TEST_BUNDLE_FN = 'test.bundle.repy'

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

# This must be done in binary mode.  Otherwise, differences of filesize due to
# \r\n and \n on different OSes will cause the bundler to look for data at the
# wrong places.
_bundle_copy_file(ORIGINAL_BUNDLE_FN, TEST_BUNDLE_FN)

# This should be an empty bundle
#pragma out {}
print bundle_Bundle(TEST_BUNDLE_FN, 'w').list()

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN)