# ---------------------------------------------------------------------
# neobots 1.0.5 -------------------------------------------------------
# Made by txtsd -------------------------------------------------------
# Based on raredaredevil's/DarkByte's HabiBot/NeoAuto -----------------
# Open Source Neopets Automation --------------------------------------
# ---------------------------------------------------------------------

# Imports -------------------------------------------------------------
import urllib2
import pyamf
import time
import sys
from pyamf.remoting.client import RemotingService
from classes.NeoAccount import NeoAccount
from classes.habi import habi
# End Imports ---------------------------------------------------------

debugmode = 1

# Settings ------------------------------------------------------------
neouser = ""  # Neopets Username
neopass = ""  # Neopets Password
proxyaddress = ""  # Optional proxy eg. "127.0.0.1:8888", leave at "" for none

housecount = 2  # How many houses we will build in our map
nestcount = 3  # How many nests we will build in our map
storagecount = 15  # How many storage centers we will build in our map
hospitalcount = 4  # How many hospitals we will build in our map
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
habiopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(acc.session.cookies))
if proxyaddress != "":
    habiopener.setproxy = proxyaddress
lastlogintime = time.time()
pyamfhandler = RemotingService(
    'http://habitarium.neopets.com/amfphp/gateway.php',
    amf_version=pyamf.AMF3,
    user_agent="Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1951.5 Safari/537.36",
    opener=habiopener.open)
# Setup habi hander module
habihandler = habi(acc, pyamfhandler, housecount, nestcount, storagecount, hospitalcount)
test = 1
while test == 1:
    try:
        habihandler.DoLoop()
        time.sleep(10)
    except KeyboardInterrupt:
        print "\n------------------"
        print "neobots was interrupted via keyboard"
        print "------------------"
        sys.exit()
