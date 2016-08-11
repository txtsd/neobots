# ---------------------------------------------------------------------
# neobots 1.0.5 -------------------------------------------------------
# Made by txtsd -------------------------------------------------------
# Based on raredaredevil's/DarkByte's HabiBot/NeoAuto -----------------
# Open Source Neopets Automation --------------------------------------
# ---------------------------------------------------------------------

# Imports -------------------------------------------------------------
import sys
from classes.NeoAccount import NeoAccount
# End Imports ---------------------------------------------------------

debugmode = 1

# Settings ------------------------------------------------------------
neouser = ""  # Neopets Username
neopass = ""  # Neopets Password
proxyaddress = ""  # Optional proxy eg. "127.0.0.1:8888", leave at "" for none
# ---------------------------------------------------------------------

if debugmode == 0:
    if len(sys.argv) == 4:
        neouser = sys.argv[1]  # Get args from commandline
        neopass = sys.argv[2]  # Get args from commandline
        proxyaddress = sys.argv[3]  # Get args from commandline
    elif len(sys.argv) == 3:
        neouser = sys.argv[1]  # Get args from commandline
        neopass = sys.argv[2]  # Get args from commandline
    else:
        print "Debug mode was turned off, but incorrect args sent, so fell back to debug mode."

acc = NeoAccount(neouser, neopass, proxyaddress)
acc.login()
