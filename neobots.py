# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

from classes.neoaccount import NeoAccount
from classes.config import Config

configurator = Config()
account_lines = None
neoaccounts = list()

with open(
    '%s/%s' % (configurator.dir_data, configurator.file_accounts), 'r'
) as file:
    account_lines = file.readlines()

for line in account_lines:
    username, password, proxy, pin = line.split('|')
    neoaccounts.append(
        NeoAccount(username, password, proxy, pin)
    )

# TODO: Add threading to load multiple neoaccounts simultaneously
accounturbator = neoaccounts[0].login()
