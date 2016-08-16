# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

from classes.neoaccount import NeoAccount
from classes.config import Config

account_lines = None
neoaccounts = list()

account_lines = Config.readAccounts()
for line in account_lines:
    username, password, proxy, pin = line.split('|')
    neoaccounts.append(
        NeoAccount(username, password, proxy, pin)
    )

# TODO: Add threading to load multiple neoaccounts simultaneously
neoaccount = neoaccounts[0]
configurator = Config(neoaccount)
login_status = neoaccount.login()
