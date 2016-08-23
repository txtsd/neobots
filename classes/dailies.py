# ---------------------------------------------------------------------
# ---------------------------- neobots --------------------------------
# ------------------------------txtsd----------------------------------
# ---------------------------------------------------------------------

from urllib import parse
import random
import time
import re


class Dailies:
    """Handles the dailies"""

    def __init__(self, accounturbator, configurator):
        self.accounturbator = accounturbator
        self.configurator = configurator
        if configurator['neobots']['randomMethod'].lower() in ['gauss', 'normal']:
            self.random = random.gauss
        else:
            self.random = random.uniform

    # Freebies
    def process_adventCalendar(self):
        pass

    def process_anchorManagement(self):
        result = self.accounturbator.get(
            '/pirates/anchormanagement.phtml'
        )
        html = result.content
        if re.search('already done your share', html):
            print('You\'ve already cannonballed today!')
            return
        # 'type="hidden" value="(.+?)">(?:\s)*?</form>'
        csrf = re.search('type="hidden" value="(.+?)"></form>', html).group(1)
        result = self.accounturbator.post(
            '/pirates/anchormanagement.phtml',
            data={
                'action': csrf,
            },
            referer='/pirates/anchormanagement.phtml'
        )
        html = result.content
        self.configurator.saveHTML('anchorManagement', html)
        item = re.search('class="prize-item-name">(.+?)</span>', html)
        if item:
            print('[%s]' % item.group(1))
        else:
            print('Unforeseen result. Check logs.')

    def process_appleBobbing(self):
        result = self.accounturbator.get(
            '/halloween/applebobbing.phtml'
        )
        html = result.content
        if re.search('Think I\'m blind underneath', html):
            print('You\'ve already bobed today.')
            return
        result = self.accounturbator.get(
            '/halloween/applebobbing.phtml',
            params={
                'bobbing': '1',
            },
            referer='/halloween/applebobbing.phtml'
        )
        html = result.content
        self.configurator.saveHTML('appleBobbing', html)
        item = re.search(
            'bob_middle\'>[\S\s]*<br><b>(.+?)</b></center><br>[\S\s]*<div id=\'bob_bottom', html)
        if re.search('decide to skip bobbing', html):
            print('Got nothing.')
        elif item:
            print('[%s]' % item.group(1))
        else:
            print('Unforeseen result. Check logs.')

    def process_bankInterest(self):
        pass

    def process_coltzanShrine(self):
        result = self.accounturbator.get(
            '/desert/shrine.phtml'
        )
        html = result.content
        if re.search('you should wait a while', html):
            print('You\'ve already been to the shrine today!')
            return
        result = self.accounturbator.post(
            '/desert/shrine.phtml',
            data={
                'type': 'approach',
            },
            referer='/desert/shrine.phtml'
        )
        html = result.content
        self.configurator.saveHTML('coltzanShrine', html)
        levels = re.search('Your pet has gained (\d)+ level', html)
        if re.search('Awww, nothing happened.', html):
            print('Got nothing.')
        elif levels:
            print('[%s]' % levels.group(0))
        else:
            print('Unforeseen result. Check logs.')

    def process_councilChamber(self):
        result = self.accounturbator.get(
            '/altador/council.phtml'
        )
        html = result.content
        if re.search('is a monument to the great legends of Altador', html):
            print('You have not completed the Altador Plot yet.')
            return
        csrf = re.search('prhv=(.+?)"></MAP>')
        result = self.accounturbator.post(
            '/altador/council.phtml',
            data={
                'prhv': csrf.group(1),
                'collect': '1',
            },
            referer='/altador/council.phtml'
        )
        html = result.content
        self.configurator.saveHTML('councilChamber', html)
        item = re.search('<BR><B>(.+?)</B></DIV>', html)
        if item:
            print('[%s]' % item.group(1))
        elif re.search('King Altador frowns at you as you enter', html):
            print('You\'ve already collected today\'s prize.')
        else:
            print('Unforeseen result. Check logs.')

    def process_dailyPuzzle(self):
        pass

    def process_darkCave(self):
        pass

    def process_deadlyDice(self):
        pass

    def process_desertedTomb(self):
        result = self.accounturbator.get(
            '/worlds/geraptiku/tomb.phtml'
        )
        # Check if there's an intermediate POST here
        result = self.accounturbator.get(
            '/worlds/geraptiku/process_tomb.phtml',
            referer='/worlds/geraptiku/tomb.phtml'
        )
        html = result.content
        self.configurator.saveHTML('desertedTomb', html)
        if re.search('had enough excitement for one day', html):
            print('You\'ve already visited the tomb today!')
        elif re.search('After being lost in the tomb for two', html):
            print('Got nothing.')
        elif re.search('You happen upon a flight of stairs that leads', html):
            print('Got nothing.')
        elif re.search('never seen so many traps in', html):
            print('Your pet loses some HP. Check logs.')
        elif re.search('passed that same carving at least', html):
            print('You got a prize and possibly the avatar. Check logs.')
        elif re.search('Your mum would be proud', html):
            print('You got a prize and possibly the avatar. Check logs.')
        else:
            print('Unforeseen result. Check logs.')

    def process_faerieCrossword(self):
        pass

    def process_forgottenShore(self):
        result = self.accounturbator.get(
            '/pirates/forgottenshore.phtml'
        )
        html = result.content
        if re.search('Located about 80 miles south of Mystery Island', html):
            print('No access to the Forgotten Shore yet.')
            return
        csrf = re.search('?confirm=1&_ref_ck=(.+?)\'><', html)
        result = self.accounturbator.get(
            '/pirates/forgottenshore.phtml',
            data={
                'confirm': '1',
                '_ref_ck': csrf.group(1),
            },
            referer='/pirates/forgottenshore.phtml'
        )
        html = result.content
        self.configurator.saveHTML('forgottenShore', html)
        print('Unforeseen result. Check logs.')

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
        self.configurator.saveHTML('fruitMachine', html)
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
        result = self.accounturbator.get(
            '/jelly/jelly.phtml'
        )
        html = result.content
        if re.search('cannot take more than one', html):
            print('You\'ve already taken a jelly today!')
            return
        result = self.accounturbator.get(
            '/jelly/jelly.phtml',
            params={
                'type': 'get_jelly',
            },
            referer='/jelly/jelly.phtml'
        )
        html = result.content
        self.configurator.saveHTML('giantJelly', html)
        item = re.search('some <b>(.+?)</b>!', html)
        if item:
            print('[%s]' % item.group(1))
        else:
            print('Unforeseen result. Check logs.')

    def process_giantOmelette(self):
        result = self.accounturbator.get(
            '/prehistoric/omelette.phtml',
            params={
                'type': 'get_omelette'
            }
        )
        html = result.content
        self.configurator.saveHTML('giantOmellete', html)
        if re.search('more than one slice per day'):
            print('You\'ve already taken a slice today.')
        else:
            print('Unforeseen result. Check logs.')

    def process_graveDanger(self):
        # Do not use until pets can be shuffled
        result = self.accounturbator.get(
            '/halloween/gravedanger/index.phtml'
        )
        html = result.content
        self.configurator.saveHTML('graveDanger', html)
        if re.search('Your Petpet has returned', html):
            result = self.accounturbator.post(
                '/halloween/gravedanger/index.phtml',
                data={
                    'again': '1',
                },
                referer='/halloween/gravedanger/index.phtml'
            )
            html = result.content
            self.configurator.saveHTML('graveDanger', html)
        active_pet = re.search('href="/quickref.phtml"><b>(.+?)</b></a>', html)
        result = self.accounturbator.post(
            '/halloween/gravedanger/index.phtml',
            data={
                'neopet': active_pet,
                'equipped': '0',
            },
            referer='/halloween/gravedanger/index.phtml'
        )
        html = result.content
        self.configurator.saveHTML('graveDanger', html)

    def process_grumpyOldKing(self):
        result = self.accounturbator.get(
            '/medieval/grumpyking.phtml'
        )
        html = result.content
        if re.search('already told me a joke today', html):
            print('You\'ve already told a joke today!')
            return
        for i in range(2):
            result = self.accounturbator.post(
                '/medieval/grumpyking2.phtml',
                data={
                    'qp1': 'What',
                    'qp2': 'do',
                    'qp3': 'you do if',
                    'qp4': '',
                    'qp5': 'fierce',
                    'qp6': 'Peophins',
                    'qp7': '',
                    'qp8': 'has eaten too much',
                    'qp9': '',
                    'qp10': 'tin of olives',
                    'ap1': 'You',
                    'ap2': 'offering',
                    'ap3': 'them a',
                    'ap4': 'tin of',
                    'ap5': '',
                    'ap6': 'what what what',
                    'ap7': '',
                    'ap8': '',
                },
                referer='/medieval/grumpyking.phtml'
            )
            html = result.content
            self.configurator.saveHTML('grumpyOldKing', html)
            if re.search(
                    'It looks like your joke had no effect', html):
                print('Got nothing.')
            else:
                print('Unforeseen result. Check logs.')

    def process_healingSprings(self):
        result = self.accounturbator.get(
            '/faerieland/springs.phtml'
        )
        html = result.content
        if re.search('My magic is not fully restored yet', html):
            print('You\'ve been here in the past 30 minutes.')
            return
        result = self.accounturbator.get(
            '/faerieland/springs.phtml',
            params={
                'type': 'heal',
            },
            referer='/faerieland/springs.phtml'
        )
        html = result.content
        self.configurator.saveHTML('healingSprings', html)
        print('Unforeseen result. Check logs.')

    def process_kikoPop(self):
        pass

    def process_lunarTemple(self):
        # choice[phase]
        choice = [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7, 8]
        result = self.accounturbator.get(
            '/shenkuu/lunar/'
        )
        html = result.content
        self.configurator.saveHTML('lunarTemple', html)
        if re.search('You may only attempt my challenge once per day', html):
            print('You\'ve already attempted the puzzle today.')
            return
        result = self.accounturbator.get(
            '/shenkuu/lunar/',
            params={
                'show': 'puzzle'
            },
            referer='/shenkuu/lunar/'
        )
        html = result.content
        self.configurator.saveHTML('lunarTemple', html)
        angle = re.search('&angleKreludor=(\d+?)&viewID=', html)
        angle_final = math.ceil(float(angle))
        phase = int(round(angle / 22.5))
        phase_choice = str(choice[phase])
        result = self.accounturbator.post(
            '/shenkuu/lunar/results.phtml',
            data={
                'submitted': 'false',
                'phase_choice': phase_choice,
            },
            referer='/shenkuu/lunar/?show=puzzle'
        )
        html = result.content
        self.configurator.saveHTML('lunarTemple', html)
        print('Unforeseen result. Check logs.')

    def process_magmaPool(self):
        pass

    def process_meteor(self):
        result = self.accounturbator.get(
            '/moon/meteor.phtml'
        )
        result = self.accounturbator.get(
            '/moon/meteor.phtml',
            params={
                'getclose': '1',
            },
            referer='/moon/meteor.phtml'
        )
        result = self.accounturbator.post(
            '/moon/process_meteor.phtml',
            data={
                'pickstep': '1',
                'meteorsubmit': 'Submit',
            },
            referer='/moon/meteor.phtml?getclose=1'
        )
        html = result.content
        self.configurator.saveHTML('meteor', html)
        print('Unforeseen result. Check logs.')

    def process_moltaraQuarry(self):
        result = self.accounturbator.get(
            '/magma/quarry.phtml'
        )
        html = result.content
        self.configurator.saveHTML('moltaraQuarry', html)
        if re.search('An angry Shoyru flies over', html):
            print('You\'ve already collected today\'s Obsidian')
        elif re.search('Shiny Obsidian', html):
            print('[Shiny Obsidian]')
        else:
            print('Unforeseen result. Check logs.')

    def process_moneyTree(self):
        pass

    def process_monthlyFreebies(self):
        result = self.accounturbator.get(
            '/freebies/'
        )
        html = result.content
        self.configurator.saveHTML('monthlyFreebies', html)
        print('Unforeseen result. Check logs.')

    def process_movieCentral(self):
        pass

    def process_mysteriousNeggCave(self):
        pass

    def process_qasalanExpellibox(self):
        random = str(random.randrange(1000, 100000))
        result = self.accounturbator.get(
            '/games/giveaway/process_giveaway.phtml',
            params={
                'r': random,
            },
            referer='ncmall.neopets.com/mall/shop.phtml?page=giveaway'
        )
        html = result.content
        parsed = parse.unquote_plus(html)
        self.configurator.saveHTML('qasalanExpellibox', parsed)
        print('Unforeseen result. Check logs.')

    def process_richSlorg(self):
        result = self.accounturbator.get(
            '/shop_of_offers.phtml',
            params={
                'slorg_payout': 'yes',
            }
        )
        html = result.content
        self.configurator.saveHTML('richSlorg', html)
        item = re.search('You have received <strong>([\d,]+?)</strong>')
        if item:
            print('[%s NP]' % item.group(1))

    def process_rubbishDump(self):
        pass

    def process_secondhandShoppe(self):
        pass

    def process_snowager(self):
        result = self.accounturbator.get(
            '/winter/snowager.phtml'
        )
        if re.search('The snowager is awake', html):
            print('Snowager is awake.')
            return
        result = self.accounturbator.get(
            '/winter/snowager2.phtml',
            referer='/winter/snowager.phtml'
        )
        html = result.content
        self.configurator.saveHTML('snowager', html)
        item = re.search('pick up a (?:cool )?(.+) from the', html)
        outcome = re.search('rears up and fires', html)
        if item:
            print('[%s]' % item.group(1))
        elif outcome:
            print('You got attacked. Check logs.')
        else:
            print('Unforeseen result. Check logs.')

    def process_soupKitchen(self):
        pass

    def process_shopTill(self):
        pass

    def process_symolHole(self):
        result = self.accounturbator.get(
            '/medieval/symolhole.phtml'
        )
        random = str(random.randrange(0, 5))
        result = self.accounturbator.post(
            '/medieval/symolhole.phtml',
            data={
                'type': 'goin',
                'goin': random,
            },
            referer='/medieval/symolhole.phtml'
        )
        html = result.content
        self.configurator.saveHTML('symolHole', html)
        if re.search('e=[067]', result.url):
            print('Got nothing.')
        elif re.search('e=[123]', result.url):
            print('[Something] Check logs.')
        elif re.search('e=4', result.url):
            print('Your petpet gained a level. Check logs.')
        elif re.search('e=5', result.url):
            print('[some NP] Check logs.')
        else:
            print('Unforeseen result. Check logs.')

    def process_tarlasTreasures(self):
        pass

    def process_tdmbgpop(self):
        result = self.accounturbator.get(
            '/faerieland/tdmbgpop.phtml'
        )
        html = result.content
        if re.search('appreciates your attention', html):
            print('You\'ve already been here today.')
            return
        result = self.accounturbator.post(
            '/faerieland/tdmbgpop.phtml',
            data={
                'talkto': '1',
            },
            referer='/faerieland/tdmbgpop.phtml'
        )
        html = result.content
        self.configurator.saveHTML('tdmbgpop', html)
        if re.search('but nothing seems to happen.', html):
            print('Got nothing.')
        else:
            print('Unforeseen result. Check logs.')

    def process_tombola(self):
        result = self.accounturbator.get(
            '/island/tombola.phtml'
        )
        html = result.content
        if re.search('Back in an hour', html):
            print('Try again in an hour. Check logs.')
            return
        result = self.accounturbator.get(
            '/island/tombola2.phtml',
            referer='/island/tombola.phtml'
        )
        html = result.content
        self.configurator.saveHTML('tombola', html)
        item = re.search('<b>Your Prize - (.*)</b><center>', html)
        if item:
            print('[%s]' % item.group(1))
        else:
            print('Unforeseen result. Check logs.')

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
        self.configurator.saveHTML('weltrudesToyChest', html)
        item = re.search('type=inventory">(.*)</A></B><BR>', html)
        if re.search('already collected your prize today', html):
            print('You\'ve already collected today\'s prize.')
        elif item:
            print('[%s]' % item.group(1))
        else:
            print('Unforeseen result. Check logs.')

    def process_wiseOldKing(self):
        result = self.accounturbator.get(
            '/medieval/wiseking.phtml'
        )
        html = result.content
        if re.search('It seems you have already', html):
            print('You\'ve already told a joke today!')
            return
        result = self.accounturbator.post(
            '/medieval/process_wiseking.phtml',
            data={
                'qp1': 'One should never assume that',
                'qp2': 'beauty',
                'qp3': 'is comparable to',
                'qp4': 'the courage of',
                'qp5': 'an',
                'qp6': 'coconut',
                'qp7': 'Baby Fireball',
            },
            referer='/medieval/wiseking.phtml'
        )
        html = result.content
        self.configurator.saveHTML('wiseOldKing', html)
        if re.search('That didn\'t make any sense at all.', html):
            print('Got nothing.')
        else:
            print('Unforeseen result. Check logs.')

    def process_yeOldFishingVortex(self):
        result = self.accounturbator.get(
            '/water/fishing.phtml'
        )
        # Handle fishing for all pets instead of just one
        result = self.accounturbator.post(
            '/water/fishing.phtml',
            data={
                'go_fish': '1',
            },
            referer='/water/fishing.phtml'
        )
        html = result.content
        self.configurator.saveHTML('yeOldFishingVortex', html)
        print('Unforeseen result.  Check logs.')

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
        self.configurator.saveHTML('slime', html)
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
        result = self.accounturbator.get(
            '/halloween/bagatelle.phtml'
        )
        html = result.content
        self.configurator.saveHTML('bagatelle', html)
        while True:
            random = str(random.randrange(10083, 49083))
            result = self.accounturbator.get(
                '/halloween/process_bagatelle.phtml',
                params={
                    'r': random,
                },
                referer='/halloween/bagatelle.phtml'
            )
            html = result.content
            unquoted = parse.unquote_plus(html)
            self.configurator.saveHTML('bagatelle', html)
            NP = re.search('ints=(\d+?)', unquoted)
            if re.search('We have a loser', unquoted):
                print('Got nothing.')
            elif NP:
                print('[%s]' % NP.group(1))
            elif re.search('afford to play', unquoted):
                print('No neopoints. Check logs.')
                return
            elif re.search('let somebody else', unquoted):
                print('No more remaining. Check logs.')
                return
            else:
                print('Unforeseen result. Check logs.')

    def process_buriedTreasure(self):
        random_1 = random.randrange(50, 400)
        random_2 = random.randrange(50, 400)
        result = self.accounturbator.get(
            '/pirates/buriedtreasure/buriedtreasure.phtml?%d,%d' %
            (random_1, random_2)
        )
        html = result.content
        self.configurator.saveHTML('buriedTreasure', html)
        if re.search('http://images.neopets.com/pirates/map_blank_scroll.gif', html):
            print('Got nothing.')
        elif re.search('http://images.neopets.com/pirates/map_prize1.gif', html):
            print('[500 NP] Check logs.')
        elif re.search('http://images.neopets.com/pirates/map_prize6.gif', html):
            print('[1000-20000 NP] Check logs.')
        elif re.search('http://images.neopets.com/pirates/map_prize_booby.gif', html):
            print('[Booby prize] Check logs.')
        elif re.search('http://images.neopets.com/pirates/map_prize_dub.gif', html):
            print('[One Dubloon Coin] Check logs.')
        elif re.search('http://images.neopets.com/pirates/map_prize_jackpot.gif', html):
            print('[Jackpot] Check logs.')
        else:
            print('You\'ve already been here in the last 3 hours!')

    def process_cheeseroller(self):
        pass

    def process_coconutShy(self):
        result = self.accounturbator.get(
            'halloween/coconutshy.phtml'
        )
        html = result.content
        self.configurator.saveHTML('coconutShy', html)
        while True:
            random = str(random.randrange(70083, 79083))
            result = self.accounturbator.get(
                '/halloween/process_cocoshy.phtml',
                params={
                    'coconut': '1',
                    'r': random,
                },
                referer='halloween/coconutshy.phtml'
            )
            html = result.content
            unquoted = parse.unquote_plus(html)
            self.configurator.saveHTML('coconutShy', html)
            if re.search('No more throws', unquoted):
                print('No more throws. Check logs.')
                return
            elif re.search('No Neopoints', unquoted):
                print('No neopoints. Possible throws remaining. Check logs.')
                return
            else:
                print('Unforeseen result. Check logs.')

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
        result = self.accounturbator.get(
            '/medieval/guessmarrow.phtml'
        )
        random = str(random.randrange(201, 800))
        result = self.accounturbator.post(
            '/medieval/process_guessmarrow.phtml',
            data={
                'guess': random,
            },
            referer='/medieval/guessmarrow.phtml'
        )
        html = result.content
        if re.search('WRONG', html):
            print('Got nothing.')
        else:
            print('Unforeseen result. Check logs.')

    def process_haiku(self):
        result = self.accounturbator.get(
            '/island/haiku/haiku.phtml'
        )
        html = result.content
        self.configurator.saveHTML('haiku', html)
        if re.search('You are now eligible to use', html):
            print('Got the avatar.')
        else:
            print('Unforeseen result. Check logs.')

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

    # Games
    def process_potatoCounter(self):
        result = self.accounturbator.get(
            '/medieval/potatocounter.phtml'
        )
        html = result.content
        self.configurator.saveHTML('potatoCounter', html)
        # Sneaky bastards
        htmlfix = re.sub('<!--\s<td(.+?)</td>-->', '', html)
        counter = 0
        potato = 'http://images.neopets.com/medieval/potato%d.gif'
        potato_re = '(%s)|(%s)|(%s)|(%s)' % \
            (
                potato % 1,
                potato % 2,
                potato % 3,
                potato % 4
            )
        for x in re.finditer(potato_re, htmlfix):
            counter += 1
        time.sleep(random.gauss(11, 2))
        result = self.accounturbator.post(
            '/medieval/potatocounter.phtml',
            data={
                'type': 'guess',
                'guess': str(counter),
            },
            referer='/medieval/potatocounter.phtml'
        )
        html = result.content
        if re.search('you win', html):
            print('Won. Check logs.')
        else:
            print('Unforeseen result. Check logs.')
