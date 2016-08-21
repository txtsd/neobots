# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

from datetime import datetime
import random
import re


class Dailies:

    LINKS = {
        'freebies': {
            'adventCalendar': '/winter/adventcalendar.phtml',
            'anchorManagement': '/pirates/anchormanagement.phtml',
            'appleBobbing': (
                '/halloween/applebobbing.phtml',
                '/halloween/applebobbing.phtml?bobbing=1'
            ),
            'bankInterest': (
                '/bank.phtml',
                '/process_bank.phtml',
            ),
            'coltzanShrine': '/desert/shrine.phtml',
            'councilChamber': '/altador/council.phtml',
            'dailyPuzzle': '/community/',
            'darkCave': '/magma/darkcave.phtml',
            'deadlyDice': '/worlds/deadlydice.phtml',
            'desertedTomb': (
                '/worlds/geraptiku/tomb.phtml',
                '/worlds/geraptiku/process_tomb.phtml',
            ),
            'faerieCrossword': '/games/crossword/index.phtml',
            'forgottenShore': '/games/treasure.phtml?type=shore',
            'fruitMachine': (
                '/desert/fruitmachine.phtml',
                '/desert/fruit/index.phtml',
            ),
            'giantJelly': '/jelly/jelly.phtml',
            'giantOmelette': '/prehistoric/omelette.phtml',
            'graveDanger': '/halloween/gravedanger/',
            'grumpyOldKing': (
                '/medieval/grumpyking.phtml',
                '/medieval/grumpyking2.phtml',
            ),
            'healingSprings': '/faerieland/springs.phtml',
            'kikoPop': (
                '/worlds/kiko/kpop/',
                '/worlds/kiko/kpop/ajax/difficulty.php',
                '/worlds/kiko/kpop/ajax/prize.php',
                'http://images.neopets.com/games/dart/popup.png',
                'http://images.neopets.com/games/dart/buttons/close_x.png',
            ),
            'lunarTemple': '/shenkuu/lunar/',
            'magmaPool': '/magma/pool.phtml',
            'meteor': '/moon/meteor.phtml',
            'moltaraQuarry': '/magma/quarry.phtml',
            'moneyTree': '/donations.phtml',
            'monthlyFreebies': '/freebies/',
            'movieCentral': '/moviecentral/index.phtml',
            'mysteriousNeggCave': '/shenkuu/neggcave/',
            'qasalanExpellibox': (
                '/games/giveaway/process_giveaway.phtml',
                'http://images.neopets.com/games/g905_v3_99390.swf',
            ),
            'richSlorg': '/shop_of_offers.phtml?slorg_payout=yes',
            'rubbishDump': '/medieval/rubbishdump.phtml',
            'secondhandShoppe': '/thriftshoppe/index.phtml',
            'snowager': (
                '/winter/snowager.phtml',
                '/winter/snowager2.phtml',
            ),
            'soupKitchen': '/soupkitchen.phtml',
            'shopTill': '/market.phtml?type=till',
            'symolHole': '/medieval/symolhole.phtml',
            'tarlasTreasures': '/freebies/tarlastoolbar.phtml',
            'tdmbgpop': '/faerieland/tdmbgpop.phtml',
            'tombola': (
                '/island/tombola2.phtml',
                '/island/tombola.phtml',
            ),
            # Check
            'trudySurprise': '/trudys_surprise.phtml',
            'turmaculus': '/medieval/turmaculus.phtml',
            'wiseOldKing': (
                '/medieval/wiseking.phtml',
                '/medieval/process_wiseking.phtml',
            ),
            'yeOldFishingVortex': '/water/fishing.phtml',
        },
        'scratchcards': {
            'desert': '/desert/sc/kiosk.phtml',
            'hauntedFairgrounds': '/halloween/scratch.phtml',
            'iceCaves': '/winter/kiosk.phtml',
        },
        'wheels': {
            'excitement': '/faerieland/wheel.phtml',
            'extravagance': '/desert/extravagance.phtml',
            'knowledge': '/medieval/knowledge.phtml',
            'mediocrity': '/prehistoric/mediocrity.phtml',
            'misfortune': '/halloween/wheel/index.phtml',
            'monotony': '/prehistoric/monotony/monotony.phtml',
        },
        'quests': {
            'brainTree': '/halloween/braintree.phtml',
            'edna': '/halloween/witchtower.phtml',
            'esophagor': '/halloween/esophagor.phtml',
            'faerie': '/quests.phtml',
            'illusensGlade': '/medieval/earthfaerie.phtml',
            'jhudorasBluff': '/faerieland/darkfaerie.phtml',
            'kitchen': '/island/kitchen.phtml',
            'taelia': '/winter/snowfaerie.phtml',
            'theCoincidence': '/space/coincidence.phtml',
        },
        'someNP': {
            'almostAbandonedAttic': '/halloween/garage.phtml',
            'bagatelle': (
                '/halloween/process_bagatelle.phtml?r=%d',
                '/halloween/bagatelle.phtml',
            ),
            'buriedTreasure': '/pirates/buriedtreasure/index.phtml',
            'cheeseroller': '/medieval/cheeseroller.phtml',
            'coconutShy': (
                '/halloween/process_cocoshy.phtml?coconut=1&r=%d',
                '/halloween/coconutshy.phtml',
            ),
            'corkGunGallery': '/halloween/corkgun.phtml',
            'employmentAgency': '/faerieland/employ/employment.phtml',
            'faerieCaverns': '/faerieland/caverns/index.phtml',
            'foodClub': '/pirates/foodclub.phtml?type=bet',
            'iglooGarageSale': '/winter/igloo.phtml',
            'leverOfDoom': '/space/strangelever.phtml',
            'neolodge': '/neolodge.phtml',
            'neopianLottery': '/games/process_lottery.phtml',
            'pickYourOwn': '/medieval/pickyourown_index.phtml',
            'poogleRacing': '/faerieland/poogleracing.phtml',
            'stockMarket': (
                '/stockmarket.phtml?type=portfolio',
                '/stockmarket.phtml?type=list&full=true',
                '/stockmarket.phtml?type=profile&company_id=%d',
                '/stockmarket.phtml?type=buy&ticker=%s',
                '/process_stockmarket.phtml',
            ),
            'stockMarketBargain': '/stockmarket.phtml?type=list&bargain=true',
            'tarlaShopOfMystery': '/winter/shopofmystery.phtml',
            'testYourStrength': (
                '/halloween/strtest/index.phtml',
                # Check
                '/halloween/strtest/process_strtest.phtml?r=2379&lang=en&r=3381&scriptURL=http:%2F%2Fwww.neopets.com%2Fhalloween%2Fstrtest%2Fprocess_strtest.phtml&prizeScriptURL=http:%2F%2Fwww.neopets.com%2Fhalloween%2Fstrtest%2Fstrtestprize.phtml&FUIComponentClass=[type+Function]&FScrollBarClass=[type+Function]&total=613323&loaded=613323&percent=100%25&msg=&getScript=[type+Function]&attachHammer=[type+Function]&moved=0&ended=0&clicked=0&speed5_set=0&speed4_set=0&speed3_set=0&speed2_set=0&speed1_set=0&sent=0&feedback=&hammer_type=hammer_wood_mc',
            ),
            'turdleRacing': '/medieval/turdleracing.phtml',
            'tyrannianTicketBooth': '/prehistoric/ticketbooth.phtml',
        },
        'train': {
            'mysteryIsland': '/island/training.phtml',
            'secretNinjaSchool': '/island/fight_training.phtml',
            'swashBucklingAcademy': '/pirates/academy.phtml',
        },
        'others': {
            'battledome': '/dome/',
            'guessMarrowWeight': '/medieval/guessmarrow.phtml',
            'haiku': '/island/haiku/haiku.phtml',
            'hiddenTower': '/faerieland/hiddentower938.phtml',
            'islandMystic': '/island/mystichut.phtml',
            'labRay': '/lab.phtml',
            'petpetLabRay': '/petpetlab.phtml',
            'kadoatery': '/games/kadoatery/index.phtml?',
            'tyrannianBattleground': '/prehistoric/battleground/',
            'wishingWell': '/wishing.phtml',
        }
    }

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
        if re.search('come back tomorrow and try again', result.content):
            print('You\'ve already spun today!')
            return
        csrf = re.search('name="ck" value="(.+?)">', result.content).group(1)
        result = self.accounturbator.post(
            '/desert/fruit/index.phtml',
            data={
                'spin': '1',
                'ck': csrf,
            },
            referer='/desert/fruit/index.phtml'
        )
        self.saveHTML('fruitMachine', result.content)
        if re.search('is not a winning spin', result.content):
            print('Got nothing.')
        elif re.search('Paint Brush', result.content) and \
                re.search('Faerie', result.content):
            print(
                '[[random] NP]',
                '[[random] Paint Brush]',
                '3x [[random] faerie]',
                '[STR boost]',
                '[LVL boost]'
            )
        elif re.search('Puntec Fruit', result.content):
            print(
                '[2500 NP]',
                '[Puntec Fruit]'
            )
        elif re.search('<b>20[,]?000 NP</b>', result.content):
            print(
                '[20000 NP]',
                '[[random] Battle Muffin]',
                '[[random] Paint Brush]'
            )
        elif re.search('Ptolymelon', result.content):
            print(
                '[1000 NP]',
                '[Ptolymelon]'
            )
        elif re.search('Muffin', result.content):
            print(
                '[15000 NP]',
                '[[random] Battle Muffin]'
            )
        elif re.search('Cheops Plant', result.content):
            print(
                '[750 NP]',
                '[Cheops Plant]'
            )
        elif re.search('<b>5[,]?000 NP</b>', result.content):
            print(
                '[5000 NP]',
                '[[random] petpet]'
            )
        elif re.search('Ummagine', result.content):
            print(
                '[500 NP]',
                '[Ummagine]'
            )
        elif re.search('<b>2[,]?500 NP</b>', result.content):
            print('[2500 NP]')
        elif re.search('Tchea Fruit', result.content):
            print(
                '[250 NP]',
                '[Tchea Fruit]'
            )
        elif re.search('<b>1[,]?000 NP</b>', result.content):
            print('[1000 NP]')
        elif re.search('Bagguss', result.content):
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
