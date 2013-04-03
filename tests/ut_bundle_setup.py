"""
Performs initialization for the bundle unit tests.

It should create bundles that contains 3 files: src1, src2, and src3.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')

# Tests shouldn't modify this file directly
# They should make a copy if they need to modify this file.

TEST_BUNDLE_FN = 'test_readonly.bundle.repy'
TEST_EMBED_BUNDLE_FN = 'test_embedded_readonly.bundle.repy'
EMBED_SCRIPT_FN = 'testscript.repy'
TEST_FILENAMES = ['src1', 'src2', 'src3']
TEST_COPY_FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

bundle_test_helper.prepare_test_sourcefiles()


test_bundle = bundle_Bundle(TEST_BUNDLE_FN, 'w')
test_bundle.add_files(TEST_COPY_FILENAMES)
test_bundle.close()

test_bundle = bundle_Bundle(TEST_EMBED_BUNDLE_FN, 'w', srcfn=EMBED_SCRIPT_FN)
test_bundle.add_files(TEST_COPY_FILENAMES)
test_bundle.close() 