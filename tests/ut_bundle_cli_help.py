"""
User should see a readable usage string if they don't provide adequate input
"""

import sys
import subprocess

#pragma out Valid commands:
#pragma out   $ bundle.repy create [source] bundlename
#pragma out   $ bundle.repy wipe bundlename [outputfile]
#pragma out   $ bundle.repy [list | extract-all]
#pragma out   $ bundle.repy [add | extract | remove] bundlename {filename}
#pragma out For more information on how to use a particular command:
#pragma out   $ bundle.repy help [command]
proc = subprocess.Popen(
            [sys.executable, "bundler.py", 'help'],
            stdout=subprocess.PIPE)
proc.wait()
print proc.stdout.read()


#pragma out $ bundle.repy create [source] bundlename
#pragma out 
#pragma out Creates a new bundle at the specified output file.  If no source file is given
#pragma out and the output file already exists, the existing file will be embedded into
#pragma out the bundle.  Otherwise, the existing file will be overwritten.
proc = subprocess.Popen(
            [sys.executable, "bundler.py", 'help', 'create'],
            stdout=subprocess.PIPE)
proc.wait()
print proc.stdout.read()


#pragma out $ bundle.repy add bundlename file_1 [file_2] ... [file_n]
#pragma out 
#pragma out Adds the specified files to the bundle.  You must provide at least one file,
#pragma out and file names must not have any spaces.
proc = subprocess.Popen(
            [sys.executable, "bundler.py", 'help', 'add'],
            stdout=subprocess.PIPE)
proc.wait()
print proc.stdout.read()