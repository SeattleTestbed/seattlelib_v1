"""
Test the listing of files in a bundle through the command line.
"""

import bundle_test_helper


TEST_BUNDLE_FN = 'test_readonly.bundle.repy'

bundle_test_helper.run_program("bundler.py", ["list", TEST_BUNDLE_FN])

#pragma out Bundle contents:
#pragma out Filename   Size (bytes)
#pragma out src1copy             87
#pragma out src2copy            100
#pragma out src3copy            461
