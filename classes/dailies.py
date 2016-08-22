# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

from datetime import datetime
from urllib import parse
import random
import re


class Dailies:

    def __init__(self, accounturbator, configurator):
        self.accounturbator = accounturbator
        self.configurator = configurator
        if configurator['neobots']['randomMethod'].lower() in ['gauss', 'normal']:
            self.random = random.gauss()
        else:
            self.random = random.uniform()

    # Freebies
    def process_adventCalendar(self):
        pass

    def process_anchorManagement(self):
        pass

    def process_appleBobbing(self):
        pass

    def process_bankInterest(self):
        pass

    def process_coltzanShrine(self):
        pass

    def process_councilChamber(self):
        pass

    def process_dailyPuzzle(self):
        pass

    def process_darkCave(self):
        pass

    def process_deadlyDice(self):
        pass

    def process_desertedTomb(self):
        pass

    def process_faerieCrossword(self):
        pass

    def process_forgottenShore(self):
        pass

    def process_fruitMachine(self):
        result = self.accounturbator.get(
            '/desert/fruit/index.phtml'
        )
        html = result.content
        if re.search('come back tomorrow and try again', html):
            print('You\'ve already spun today!')
            return
        csrf = re.search('name="ck" value="(.+?)">', html).group(1)
        result = self.accounturbator.post(
            '/desert/fruit/index.phtml',
            data={
                'spin': '1',
                'ck': csrf,
            },
            referer='/desert/fruit/index.phtml'
        )
        html = result.content
        self.saveHTML('fruitMachine', html)
        if re.search('is not a winning spin', html):
            print('Got nothing.')
        elif re.search('Paint Brush', html) and \
                re.search('Faerie', html):
            print(
                '[[random] NP]',
                '[[random] Paint Brush]',
                '3x [[random] faerie]',
                '[STR boost]',
                '[LVL boost]'
            )
        elif re.search('Puntec Fruit', html):
            print(
                '[2500 NP]',
                '[Puntec Fruit]'
            )
        elif re.search('<b>20[,]?000 NP</b>', html):
            print(
                '[20000 NP]',
                '[[random] Battle Muffin]',
                '[[random] Paint Brush]'
            )
        elif re.search('Ptolymelon', html):
            print(
                '[1000 NP]',
                '[Ptolymelon]'
            )
        elif re.search('Muffin', html):
            print(
                '[15000 NP]',
                '[[random] Battle Muffin]'
            )
        elif re.search('Cheops Plant', html):
            print(
                '[750 NP]',
                '[Cheops Plant]'
            )
        elif re.search('<b>5[,]?000 NP</b>', html):
            print(
                '[5000 NP]',
                '[[random] petpet]'
            )
        elif re.search('Ummagine', html):
            print(
                '[500 NP]',
                '[Ummagine]'
            )
        elif re.search('<b>2[,]?500 NP</b>', html):
            print('[2500 NP]')
        elif re.search('Tchea Fruit', html):
            print(
                '[250 NP]',
                '[Tchea Fruit]'
            )
        elif re.search('<b>1[,]?000 NP</b>', html):
            print('[1000 NP]')
        elif re.search('Bagguss', html):
            print(
                '[100 NP]',
                '[Bagguss]'
            )
        else:
            print('Unforeseen result. Check logs.')

    def process_giantJelly(self):
        pass

    def process_giantOmelette(self):
        pass

    def process_graveDanger(self):
        pass

    def process_grumpyOldKing(self):
        pass

    def process_healingSprings(self):
        pass

    def process_kikoPop(self):
        pass

    def process_lunarTemple(self):
        pass

    def process_magmaPool(self):
        pass

    def process_meteor(self):
        pass

    def process_moltaraQuarry(self):
        pass

    def process_moneyTree(self):
        pass

    def process_monthlyFreebies(self):
        pass

    def process_movieCentral(self):
        pass

    def process_mysteriousNeggCave(self):
        pass

    def process_qasalanExpellibox(self):
        pass

    def process_richSlorg(self):
        pass

    def process_rubbishDump(self):
        pass

    def process_secondhandShoppe(self):
        pass

    def process_snowager(self):
        pass

    def process_soupKitchen(self):
        pass

    def process_shopTill(self):
        pass

    def process_symolHole(self):
        pass

    def process_tarlasTreasures(self):
        pass

    def process_tdmbgpop(self):
        pass

    def process_tombola(self):
        pass

    def process_trudySurprise(self):
        pass

    def process_turmaculus(self):
        pass

    def process_weltrudesToyChest(self):
        result = self.accounturbator.get(
            '/petpetpark/daily.phtml'
        )
        result = self.accounturbator.post(
            '/petpetpark/daily.phtml',
            data={
                'go': '1',
            },
            referer='/petpetpark/daily.phtml'
        )
        html = result.content
        self.saveHTML('weltrudesToyChest', html)
        item = re.search('type=inventory">(.*)</A></B><BR>', html)
        if re.search('already collected your prize today', html):
            print('You\'ve already collected today\'s prize.')
        elif item:
            print('[%s]' % item.group(1))
        else:
            print('Unforeseen result. Check logs.')

    def process_wiseOldKing(self):
        pass

    def process_yeOldFishingVortex(self):
        pass

    # Scratchcards
    def process_desert(self):
        pass

    def process_hauntedFairgrounds(self):
        pass

    def process_iceCaves(self):
        pass

    # Wheels
    def process_excitement(self):
        pass

    def process_extravagance(self):
        pass

    def process_knowledge(self):
        pass

    def process_mediocrity(self):
        pass

    def process_misfortune(self):
        pass

    def process_monotony(self):
        pass

    def process_slime(self):
        result - self.accounturbator.get(
            '/games/nickwheel/process_wheel.phtml'
        )
        html = result.content
        self.saveHTML('slime', html)
        message = re.search('message="(.+?)"></m', html)
        unquoted = parse.unquote_plus(message)
        print('[%s]' % unquoted)

    # Quests
    def process_brainTree(self):
        pass

    def process_edna(self):
        pass

    def process_esophagor(self):
        pass

    def process_faerie(self):
        pass

    def process_illusensGlade(self):
        pass

    def process_jhudorasBluff(self):
        pass

    def process_kitchen(self):
        pass

    def process_taelia(self):
        pass

    def process_theCoincidence(self):
        pass

    # Some NP Required
    def process_almostAbandonedAttic(self):
        pass

    def process_bagatelle(self):
        pass

    def process_buriedTreasure(self):
        pass

    def process_cheeseroller(self):
        pass

    def process_coconutShy(self):
        pass

    def process_corkGunGallery(self):
        pass

    def process_employmentAgency(self):
        pass

    def process_faerieCaverns(self):
        pass

    def process_foodClub(self):
        pass

    def process_iglooGarageSale(self):
        pass

    def process_leverOfDoom(self):
        pass

    def process_neolodge(self):
        pass

    def process_neopianLottery(self):
        pass

    def process_pickYourOwn(self):
        pass

    def process_poogleRacing(self):
        pass

    def process_stockMarket(self):
        pass

    def process_stockMarketBargain(self):
        pass

    def process_tarlaShopOfMystery(self):
        pass

    def process_testYourStrength(self):
        pass

    def process_turdleRacing(self):
        pass

    def process_tyrannianTicketBooth(self):
        pass

    # Train
    def process_mysteryIsland(self):
        pass

    def process_secretNinjaSchool(self):
        pass

    def process_swashBucklingAcademy(self):
        pass

    # Others
    def process_battledome(self):
        pass

    def process_guessMarrowWeight(self):
        pass

    def process_haiku(self):
        pass

    def process_hiddenTower(self):
        pass

    def process_islandMystic(self):
        pass

    def process_labRay(self):
        pass

    def process_petpetLabRay(self):
        pass

    def process_kadoatery(self):
        pass

    def process_tyrannianBattleground(self):
        pass

    def process_wishingWell(self):
        pass

    def saveHTML(self, method, html):
        user = self.configurator['neopets']['username']
        time = datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S')
        filename = '%s/%s__%s__%s.html' % (
            self.configurator.dir_logs,
            user,
            method,
            time,
        )
        with open(filename, 'wb') as file:
            file.write(html)
