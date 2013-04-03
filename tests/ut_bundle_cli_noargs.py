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
            [sys.executable, "bundler.py"],
            stdout=subprocess.PIPE)

proc.wait()
print proc.stdout.read()