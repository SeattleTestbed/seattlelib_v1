"""
Test the extracting of all files in a bundle through the command line.
"""

import bundle_test_helper

TEST_BUNDLE_FN = 'test_readonly.bundle.repy'
TEST_FILENAMES = ['src1', 'src2', 'src3']
TEST_COPY_FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory(TEST_COPY_FILENAMES)

bundle_test_helper.run_program("bundler.py", ["extract-all", TEST_BUNDLE_FN])

bundle_test_helper.run_repy_program('testscript.repy', TEST_FILENAMES)