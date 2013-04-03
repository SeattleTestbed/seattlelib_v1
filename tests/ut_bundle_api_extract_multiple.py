"""
Test the extracting of multiple files in a bundle through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')

TEST_BUNDLE_FN = 'test_readonly.bundle.repy'
FILENAMES = ['src1', 'src2', 'src3']
COPY_FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# Make sure the extracted files don't exist
bundle_test_helper.remove_files_from_directory([COPY_FILENAMES])

bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
bundle.extract_files(COPY_FILENAMES)
bundle.close()

# Check that the extracted files make sense
bundle_test_helper.run_repy_program('testscript.repy', FILENAMES)