# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

import re


class Bank:
    """Handles bank operations"""

    def __init__(self, accounturbator, configurator):
        self.accounturbator = accounturbator
        self.configurator = configurator

    def make_account(self):
        result = self.accounturbator.get(
            '/bank.phtml'
        )
        html = result.content
        if re.search('Create a Bank Account', html):
            result = self.accounturbator.post(
                'process_bank.phtml',
                data={
                    'type': 'new_account',
                    'name': self.acc.un,    # max_char: 30
                    'add1': '',             # max_char: 30
                    'add2': '',             # max_char: 30
                    'add3': '',             # max_char: 30
                    'employment': 'Chia Custodian',
                    'salary': '10,000 NP and below',
                    'account_type': '0',
                    'initial_deposit': '1',
                },
                referer='/bank.phtml'
            )

    def deposit(self, np=None):
        pass
