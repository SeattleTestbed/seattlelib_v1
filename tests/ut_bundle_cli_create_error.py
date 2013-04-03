"""
Test to ensure we display a meaningful message when user gives bad input
for creating a bundle on the command line.
"""

import bundle_test_helper

#pragma out Expected Arguments: {source_filename} bundle_filename
bundle_test_helper.run_program("bundler.py", ["create"])