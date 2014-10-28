# ---------------------------------------------------------------------
# neobots 1.0.5 -------------------------------------------------------
# Made by txtsd -------------------------------------------------------
# Based on raredaredevil's/DarkByte's HabiBot/NeoAuto -----------------
# Open Source Neopets Automation --------------------------------------
# ---------------------------------------------------------------------

# Imports -------------------------------------------------------------
import urllib2
import sys
import pyamf
import time
from pyamf.remoting.client import RemotingService
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
habiopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(acc.session.cookies))
if proxyaddress != "":
    habiopener.setproxy = proxyaddress
lastlogintime = time.time()
pyamfhandler = RemotingService(
    'http://habitarium.neopets.com/amfphp/gateway.php',
    amf_version=pyamf.AMF3,
    user_agent="Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
    opener=habiopener.open)

try:
    player_service = pyamfhandler.getService('PlayerService')
    inventory_service = pyamfhandler.getService('InventoryService')
    itembag = inventory_service.itemBag()
    for x in itembag:
        inventory_service.deleteItem(str(x[1]['m_id']))
        print "Deleted item"
    print "Resetting player"
    player_service.reset()
    print "Player has been reset"
    print "You may now run client.py as usual"
except:
    print "Something went wrong. Run this program again."
    print "If it doesn't work at all, contact txtsd"
