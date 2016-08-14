# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

"""Handles the configuration file"""

from collections import OrderedDict
import json
import os


class Config:

    dir_data = 'data'
    dir_logs = 'logs'
    file_config = 'config.json'
    file_accounts = 'accounts.txt'

    DEFAULT_CONFIG = OrderedDict(
        {
            'account': {
                'username': '',
                'password': '',
                'proxy': '',
                'neoPin': '',
            },
            'freebies': {
                'adventCalendar': True,
                'anchorManagement': True,
                'appleBobbing': True,
                'bankInterest': True,
                'coltzanShrine': True,
                'councilChamber': True,
                'dailyPuzzle': True,
                'darkCave': True,
                'deadlyDice': False,
                'desertedTomb': True,
                'faerieCrossword': True,
                'forgottenShore': True,
                'fruitMachine': True,
                'giantJelly': True,
                'giantOmelette': True,
                'graveDanger': True,
                'grumpyOldKing': True,
                'haiku': True,
                'healingSprings': True,
                'islandMystic': True,
                'kikoPop': True,
                'lunarTemple': True,
                'magmaPool': False,
                'meteor': True,
                'moltaraQuarry': True,
                'moneyTree': False,
                'monthlyFreebies': True,
                'movieCentral': True,
                'mysteriousNeggCave': True,
                'qasalanExpellibox': True,
                'richSlorg': True,
                'rubbishDump': False,
                'secondhandShoppe': False,
                'snowager': True,
                'soupKitchen': True,
                'shopTill': True,
                'symolHole': True,
                'tarlasTreasures': False,
                'tdmbgpop': True,
                'tombola': True,
                'trudySurprise': True,
                'turmaculus': True,
                'wiseOldKing': True,
                'yeOldFishingVortex': True,
            },
            'scratchcards': {
                'desert': False,
                'hauntedFairgrounds': False,
                'iceCaves': False,
            },
            'wheels': {
                'excitement': False,
                'extravagance': False,
                'knowledge': False,
                'mediocrity': False,
                'misfortune': False,
                'monotony': False,
            },
            'quests': {
                'brainTree': False,
                'edna': False,
                'esophagor': False,
                'faerie': False,
                'illusensGlade': False,
                'jhudorasBluff': False,
                'kitchen': False,
                'taelia': False,
                'coincidence': False,
            },
            'someNP': {
                'almostAbandonedAttic': False,
                'bagatelle': False,
                'buriedTreasure': False,
                'cheeseroller': False,
                'coconutShy': False,
                'corkGunGallery': False,
                'employmentAgency': False,
                'faerieCaverns': False,
                'foodClub': False,
                'iglooGarageSale': False,
                'leverOfDoom': False,
                'neolodge': False,
                'neopianLottery': False,
                'pickYourOwn': False,
                'poogleRacing': False,
                'stockMarket': False,
                'stockMarketBargain': False,
                'tarlaShopOfMystery': False,
                'testYourStrength': False,
                'turdleRacing': False,
                'tyrannianTicketBooth': False,
            },
            'train': {
                'mysteryIsland': False,
                'secretNinjaAcademy': False,
                'swashBucklingAcademy': False,
            },
            'others': {
                'battledome': False,
                'guessMarrowWeight': False,
                'hiddenTower': False,
                'labRay': False,
                'petpetLabRay': False,
                'kadoatery': False,
                'tyrannianBattleground': False,
                'wishingWell': False,
            }
        }
    )

    def __init__(self, account):
        self.config = None
        self.refresh()

    def get(self, key):
        try:
            return self.config[key]
        except KeyError:
            return False

    def set(self, key, value):
        try:
            self.config[key] = value
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

    def _create_config(self):
        with open(Config.file_config, 'w') as file:
            json.dump(Config.DEFAULT_CONFIG, file, indent=2)
        self.refresh()
