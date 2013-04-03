"""
Test adding a string through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')


TEST_BUNDLE_FN = 'test.bundle.repy'

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

TEST_STRING = 'this is a test string'
TEST_STRING_FN = 'teststring'

bundle = bundle_Bundle(TEST_BUNDLE_FN, 'w')
bundle.add_string(TEST_STRING_FN, TEST_STRING)
bundle.close()

# Make sure the added file is inside the bundle
bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')
if not TEST_STRING_FN in bundle.list():
  print "Added string not found when listing bundle contents"

# Make sure added file matches original file contents
added_file_contents = bundle.extract_to_string(TEST_STRING_FN)
if added_file_contents != TEST_STRING:
  print "Added string contents does not match string contents"

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN)