"""
Test for adding multiple files to bundles on the command line
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')

TEST_BUNDLE_FN = "testresult.bundle.repy"
TEST_FILENAMES = ['src1', 'src2', 'src3']
TEST_COPY_FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

bundle_test_helper.prepare_test_sourcefiles()

# First create the bundle
bundle_test_helper.run_program("bundler.py", ["create", TEST_BUNDLE_FN])

# Add multiple files
bundle_test_helper.run_program("bundler.py", ["add", TEST_BUNDLE_FN] + TEST_COPY_FILENAMES)

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN, TEST_FILENAMES)