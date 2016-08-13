# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

from classes.neoaccount import NeoAccount

neouser = ''  # Neopets Username
neopass = ''  # Neopets Password
proxyaddress = ''  # Optional proxy eg. '127.0.0.1:8888', leave at '' for none

account = NeoAccount(neouser, neopass, proxyaddress)
account.login()
