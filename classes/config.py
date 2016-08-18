# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

"""Handles the configuration file"""

from collections import OrderedDict
import json
import sys
import os


class Config:

    dir_data = 'data'
    dir_logs = 'logs'
    file_config = 'config.json'
    file_accounts = 'accounts.txt'

    # OrderedDict of a list of tuples to maintain order while saving
    # and loading from JSON, and to access data like dictionaries
    DEFAULT_CONFIG = OrderedDict(
        [
            ('neopets', OrderedDict(
                [
                    ('username', ''),
                    ('password', ''),
                    ('proxy', ''),
                    ('pin', ''),
                ]
            )),
            ('freebies', OrderedDict(
                [
                    ('adventCalendar', True),
                    ('anchorManagement', True),
                    ('appleBobbing', True),
                    ('bankInterest', True),
                    ('coltzanShrine', True),
                    ('councilChamber', True),
                    ('dailyPuzzle', True),
                    ('darkCave', True),
                    ('deadlyDice', False),
                    ('desertedTomb', True),
                    ('faerieCrossword', True),
                    ('forgottenShore', True),
                    ('fruitMachine', True),
                    ('giantJelly', True),
                    ('giantOmelette', True),
                    ('graveDanger', True),
                    ('grumpyOldKing', True),
                    ('healingSprings', True),
                    ('kikoPop', True),
                    ('lunarTemple', True),
                    ('magmaPool', False),
                    ('meteor', True),
                    ('moltaraQuarry', True),
                    ('moneyTree', False),
                    ('monthlyFreebies', True),
                    ('movieCentral', True),
                    ('mysteriousNeggCave', True),
                    ('qasalanExpellibox', True),
                    ('richSlorg', True),
                    ('rubbishDump', False),
                    ('secondhandShoppe', False),
                    ('snowager', True),
                    ('soupKitchen', True),
                    ('shopTill', True),
                    ('symolHole', True),
                    ('tarlasTreasures', False),
                    ('tdmbgpop', True),
                    ('tombola', True),
                    ('trudySurprise', True),
                    ('turmaculus', True),
                    ('wiseOldKing', True),
                    ('yeOldFishingVortex', True),
                ]
            )),
            ('scratchcards', OrderedDict(
                [
                    ('desert', False),
                    ('hauntedFairgrounds', False),
                    ('iceCaves', False),
                ]
            )),
            ('wheels', OrderedDict(
                [
                    ('excitement', False),
                    ('extravagance', False),
                    ('knowledge', False),
                    ('mediocrity', False),
                    ('misfortune', False),
                    ('monotony', False),
                ]
            )),
            ('quests', OrderedDict(
                [
                    ('brainTree', False),
                    ('edna', False),
                    ('esophagor', False),
                    ('faerie', False),
                    ('illusensGlade', False),
                    ('jhudorasBluff', False),
                    ('kitchen', False),
                    ('taelia', False),
                    ('theCoincidence', False),
                ]
            )),
            ('someNP', OrderedDict(
                [
                    ('almostAbandonedAttic', False),
                    ('bagatelle', False),
                    ('buriedTreasure', False),
                    ('cheeseroller', False),
                    ('coconutShy', False),
                    ('corkGunGallery', False),
                    ('employmentAgency', False),
                    ('faerieCaverns', False),
                    ('foodClub', False),
                    ('iglooGarageSale', False),
                    ('leverOfDoom', False),
                    ('neolodge', False),
                    ('neopianLottery', False),
                    ('pickYourOwn', False),
                    ('poogleRacing', False),
                    ('stockMarket', False),
                    ('stockMarketBargain', False),
                    ('tarlaShopOfMystery', False),
                    ('testYourStrength', False),
                    ('turdleRacing', False),
                    ('tyrannianTicketBooth', False),
                ]
            )),
            ('train', OrderedDict(
                [
                    ('mysteryIsland', False),
                    ('secretNinjaSchool', False),
                    ('swashBucklingAcademy', False),
                ]
            )),
            ('others', OrderedDict(
                [
                    ('battledome', False),
                    ('guessMarrowWeight', False),
                    ('haiku', True),
                    ('hiddenTower', False),
                    ('islandMystic', True),
                    ('labRay', False),
                    ('petpetLabRay', False),
                    ('kadoatery', False),
                    ('tyrannianBattleground', False),
                    ('wishingWell', False),
                ]
            )),
        ]
    )

    DEFAULT_ACCOUNTS = """# Possible formats:
#    neouser|neopass|proxy:port|PIN
#    neouser|neopass|proxy:port|
#    neouser|neopass||PIN
#    neouser|neopass||
# proxy:port and PIN are optional
# Example proxy:port:
#    localhost:8888
#    8.8.4.4:8080
"""

    def __init__(self, account):
        self.config = None
        self.refresh()

    def get(self, key1, key2):
        try:
            return self.config[key1][key2]
        except KeyError:
            return False

    def set(self, key1, key2, value):
        try:
            self.config[key1][key2] = value
            return True
        except:
            return False

    def refresh(self):
        if os.path.isfile(Config.file_config):
            with open(Config.file_config, 'r') as file:
                self.config = json.load(file, object_pairs_hook=OrderedDict)
        else:
            self.config = self._create_config()

    def sync(self):
        with open(Config.file_config, 'w') as file:
            json.dump(self.config, file, indent=2)

    def readAccounts():
        try:
            account_lines = None
            valid_account_lines = []
            with open(
                '%s/%s' %
                (Config.dir_data, Config.file_accounts),
                'r'
            ) as file:
                account_lines = file.read().split('\n')
            if account_lines == Config.DEFAULT_ACCOUNTS.split('\n'):
                Config._advice_exit()
            for line in account_lines:
                if len(line) != 0:
                    if line.strip(' ').strip('\t')[0] != '#':
                        valid_account_lines.append(line)
            if len(valid_account_lines) == 0:
                Config._advice_exit()
            print(valid_account_lines)
            return valid_account_lines
        except FileNotFoundError:
            with open(
                '%s/%s' %
                (Config.dir_data, Config.file_accounts),
                'w'
            ) as file:
                file.write(Config.DEFAULT_ACCOUNTS)
            Config._advice_exit()

    def _create_config(self):
        with open(Config.file_config, 'w') as file:
            json.dump(Config.DEFAULT_CONFIG, file, indent=2)
        self.refresh()

    def _advice_exit():
        print(
            'Configure %s/%s and run again.' %
            (Config.dir_data, Config.file_accounts)
        )
        sys.exit()
