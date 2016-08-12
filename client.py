# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

import sys
from classes.NeoAccount import NeoAccount

neouser = ''  # Neopets Username
neopass = ''  # Neopets Password
proxyaddress = ''  # Optional proxy eg. '127.0.0.1:8888', leave at '' for none

if len(sys.argv) == 4:
    neouser = sys.argv[1]  # Get args from commandline
    neopass = sys.argv[2]  # Get args from commandline
    proxyaddress = sys.argv[3]  # Get args from commandline
elif len(sys.argv) == 3:
    neouser = sys.argv[1]  # Get args from commandline
    neopass = sys.argv[2]  # Get args from commandline


account = NeoAccount(neouser, neopass, proxyaddress)
account.login()
