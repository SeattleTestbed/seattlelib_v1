"""
Test adding multiple files through the API.
"""

import bundle_test_helper
import repyhelper
repyhelper.translate_and_import('bundle.repy')


TEST_BUNDLE_FN = 'test.bundle.repy'
ADD_FILENAMES = ['src1', 'src2', 'src3']

# Make sure the bundle doesn't exist to test bundle creation
bundle_test_helper.remove_files_from_directory([TEST_BUNDLE_FN])

bundle = bundle_Bundle(TEST_BUNDLE_FN, 'w')
bundle.add_files(ADD_FILENAMES)
bundle.close()

# Verification step
bundle = bundle_Bundle(TEST_BUNDLE_FN, 'r')

for addedfile in ADD_FILENAMES:
  # Make sure the added files are inside the bundle
  if not addedfile in bundle.list():
    print "Added file not found when listing bundle contents"
  
  # Make sure added files matches original contents
  added_file_contents = bundle.extract_to_string(addedfile)
  if added_file_contents != open(addedfile).read():
    print "Added file contents does not match file contents"

bundle.close()

# Now run the test script!
bundle_test_helper.run_repy_program(TEST_BUNDLE_FN, ADD_FILENAMES)