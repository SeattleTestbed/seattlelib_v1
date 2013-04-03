"""
Test the creation of new bundles without embedded files through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')


TEST_BUNDLE_FN = 'test.bundle.repy'

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

bundle_Bundle(TEST_BUNDLE_FN, 'w')

# We should be able to re-open the same bundle without issue
bundle_Bundle(TEST_BUNDLE_FN, 'r')

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN)