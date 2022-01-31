from common import *
import sys

if len(sys.argv) != 2:
    errorMessage("usage: Reboot.py number_loops")
    testFailedMessage()
loops = int(sys.argv[1])
for i in range(loops):
    infoMessage("Rebot number " + str(i))
    reboot()
testResultMessage()