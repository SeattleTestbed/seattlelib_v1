"""
Test for creating bundles on the command line
"""

import bundle_test_helper

TEST_BUNDLE_FN = "testresult.bundle.repy"

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

bundle_test_helper.run_program("bundler.py", ["create", TEST_BUNDLE_FN])

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN)