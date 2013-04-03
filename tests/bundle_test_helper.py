"""
Common test routines for the bundle test
"""

import os
import sys
import subprocess
import repyhelper
repyhelper.translate_and_import('bundle.repy')


def prepare_test_sourcefiles():
  test_filenames = ['src1', 'src2', 'src3']
  test_copy_filenames = ['src1copy', 'src2copy', 'src3copy']
  
  # Make copies of the test files with names as specified by test_copy_filenames.
  for i in xrange(len(test_filenames)):
    _bundle_copy_file(test_filenames[i], test_copy_filenames[i])


def remove_files_from_directory(files):
  for file in files:
    if file in os.listdir('.'):
      os.remove(file)


def run_program(programname, args=None):
  if args is None:
    args = []

  proc = subprocess.Popen(
              [sys.executable, programname] + args,
              stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

  proc.wait()

  # Print out the subprocess might have printed out
  # We cannot use print because it will print out extraneous whitespace that will
  # trigger false positives on UTF.
  sys.stdout.write(proc.stdout.read())
  sys.stderr.write(proc.stderr.read())


def run_repy_program(programname, args=None):
  if args is None:
    args = []

  run_program('repy.py', ['restrictions.test', programname] + args)