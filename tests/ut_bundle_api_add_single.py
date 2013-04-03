"""
Test adding a single file through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')


TEST_BUNDLE_FN = 'test.bundle.repy'
FILENAMES = ['src1', 'src2', 'src3']
COPY_FILENAMES = ['src1copy', 'src2copy', 'src3copy']

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

bundle = bundle_Bundle(TEST_BUNDLE_FN, 'w')
bundle.add(COPY_FILENAMES[0])
bundle.close()

# # Make sure the added file is inside the bundle
# bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
# if not COPY_FILENAMES[0] in bundle.list():
#   print "Added file not found when listing bundle contents"

# # Make sure added file matches original file contents
# added_file_contents = bundle.extract_to_string(COPY_FILENAMES[0])
# if added_file_contents != open(COPY_FILENAMES[0]).read():
#   print "Added file contents does not match file contents"

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN, [FILENAMES[0]])