"""
Test the extracting of all files in a bundle through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')

TEST_BUNDLE_FN = 'test_readonly.bundle.repy'
FILENAMES = ['src1', 'src2', 'src3']

# Make sure the extracted files don't exist
bundle_test_helper.remove_files_from_directory([FILENAMES])

# src1copy ... src3copy is extracted
bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
bundle.extract_all()
bundle.close()

# Check that the extracted files make sense
bundle_test_helper.run_repy_program('testscript.repy', FILENAMES)
