"""
Test to check that wiping with an output file works as expected (on CLI)
"""

import sys
import subprocess

# We make a local copy of the test bundle so that we
# don't affect the execution of other tests
ORIGINAL_BUNDLE_FN = 'test_readonly.bundle.repy'
TEST_BUNDLE_FN = 'test.bundle.repy'
OUTPUT_BUNDLE_FN = 'bundle_wipetest.output'

# Make a copy of the test file
# This must be done in binary mode.  Otherwise, differences of filesize due to
# \r\n and \n on different OSes will cause the bundler to look for data at the
# wrong places.
test_bundle_contents = open(ORIGINAL_BUNDLE_FN, 'rb').read()
open(TEST_BUNDLE_FN, 'wb').write(test_bundle_contents)

proc = subprocess.Popen(
            [sys.executable, "bundler.py", "wipe", TEST_BUNDLE_FN, OUTPUT_BUNDLE_FN],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

proc.wait()

# Print out the subprocess might have printed out
# We cannot use print because it will print out extraneous whitespace that will
# trigger false positives on UTF.
sys.stdout.write(proc.stdout.read())
sys.stderr.write(proc.stderr.read())

# Make sure the output is empty
# If something is printed, then UTF will flag it as an error 
sys.stdout.write(open(OUTPUT_BUNDLE_FN, 'rb').read())