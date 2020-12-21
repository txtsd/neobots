import logging
import re
import time
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup as bs


class Freebies:

    def __init__(self, account):
        self.account = account
        # self.baseReferer = self.account.domain + '/'
        self.username = account.username
        self.pathString = '.debug'

        # Create debug directory
        self.debugOutput = Path(self.pathString)
        self.debugOutput.mkdir(exist_ok=True)

        # Links
        self.LINK_INDEX = '/index.html'

    def save(self, reply, name, JSON=False):
        timeNow = time.time_ns()
        today = date.today().isoformat()
        filename = '{}/{}-{}-{}-{}.{}'.format(
            self.pathString,
            self.username,
            today,
            name,
            timeNow,
            'json' if JSON else 'html',
        )
        with open(filename, 'wb') as f:
            f.write(reply.content)

    def doTrudy(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Trudy')

        # Constants
        LINK_TRUDY_1 = '/trudys_surprise.phtml'
        LINK_TRUDY_2 = '/trudydaily/slotgame.phtml'
        LINK_TRUDY_3 = '/trudydaily/js/slotsgame.js'
        LINK_TRUDY_4 = '/trudydaily/ajax/claimprize.php'
        PARAMS_TRUDY = {'delevent': 'yes'}
        DATA_TRUDY_1 = {'action': 'beginroll'}
        DATA_TRUDY_2 = {'action': 'prizeclaimed'}
        TEXT_TRUDY = "Trudy's Surprise"
        PATTERN_TRUDY_1 = re.compile(r'(?P<link>/trudydaily/slotgame\.phtml\?id=(?P<id>.*?)&slt=(?P<slt>\d+))')
        PATTERN_TRUDY_2 = re.compile(r'(?P<link>/trudydaily/js/slotsgame\.js\?v=(?P<v>\d+))')

        # Look for Trudy's Surprise event notfif at top of page
        result1 = self.account.get(self.LINK_INDEX)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('#neobdy.en div#main div#header table tr td.eventIcon.sf b')

        # If event exists
        if soup1_match and (soup1_match.get_text() == TEXT_TRUDY):
            result2 = self.account.get(
                LINK_TRUDY_1,
                params=PARAMS_TRUDY,
                referer=self.LINK_INDEX
            )
            soup2 = bs(result2.content, 'lxml')
            soup2_match = soup2.select_one('#frameTest')

            # Check for trudy game link
            if soup2_match:
                soup2_regexmatch = PATTERN_TRUDY_1.search(soup2_match.get('src'))
                result3 = self.account.get(
                    LINK_TRUDY_2,
                    params={
                        'id': soup2_regexmatch['id'],
                        'slt': soup2_regexmatch['slt']
                    },
                    referer=LINK_TRUDY_1
                )
                soup3 = bs(result3.content, 'lxml')
                soup3_matches = soup3.select('script')
                # Select the second script element which has the link we need
                soup3_match = soup3_matches[1]

                # Check for slotsgame link
                if soup3_match:
                    soup3_regexmatch = PATTERN_TRUDY_2.search(soup3_match.get('src'))
                    result4 = self.account.get(
                        LINK_TRUDY_3,
                        params={'v': soup3_regexmatch['v']},
                        referer=soup2_regexmatch['link']
                    )

                    # Start POSTing
                    result5 = self.account.xhr(
                        LINK_TRUDY_4,
                        data={
                            'action': 'getslotstate',
                            'key': soup2_regexmatch['id']
                        },
                        referer=LINK_TRUDY_1
                    )
                    self.save(result5, 'trudy_getslotstate', JSON=True)
                    json5 = result5.json()
                    if not json5['error']:
                        time.sleep(5)
                        # Next POST
                        result6 = self.account.xhr(
                            LINK_TRUDY_4,
                            data=DATA_TRUDY_1,
                            referer=LINK_TRUDY_1
                        )
                        self.save(result6, 'trudy_beginroll', JSON=True)
                        json6 = result6.json()
                        if not json6['error']:
                            # Prize has been won
                            # Display before clicking the modal
                            for prize in json6['prizes']:
                                logger.info('Received: {} {}'.format(prize['value'], prize['name']))
                            result7 = self.account.xhr(
                                LINK_TRUDY_4,
                                data=DATA_TRUDY_2,
                                referer=LINK_TRUDY_1
                            )
                            json7 = result7.json()
                            if not json7['error']:
                                result8 = self.account.get(LINK_TRUDY_1, referer=LINK_TRUDY_1)
                            else:
                                logger.error(json7['error'])
                        else:
                            logger.error(json6['error'])
                    else:
                        logger.error(json5['error'])
                else:
                    logger.error('No slotsgame.js link')
            else:
                logger.error('No slotgame link')
        else:
            logger.info("No Trudy's Surprise notification")

    def doSnowager(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Snowager')

        # Constants
        LINK_SNOWAGER_1 = '/winter/snowager.phtml'
        LINK_SNOWAGER_2 = '/winter/snowager2.phtml'
        TEXT_SNOWAGER = 'Attempt to steal a piece of treasure'
        PATTERN_SNOWAGER_1 = re.compile(r'You carefully walk in and pick up a')
        PATTERN_SNOWAGER_2 = re.compile(r'You carefully walk in and hastily pick up an item')
        PATTERN_SNOWAGER_3 = re.compile(r'You have already collected your prize today.')
        PATTERN_SNOWAGER_4 = re.compile(r'Come back later.')
        PATTERN_SNOWAGER_5 = re.compile(r'The Snowager is awake')
        PATTERN_SNOWAGER_6 = re.compile(r'The Snowager moves slightly in its sleep')
        PATTERN_SNOWAGER_7 = re.compile(r'The Snowager awakes, looks straight at you')
        PATTERN_SNOWAGER_8 = re.compile(r'ROOOOAARRR')

        # Visit snowager page
        result1 = self.account.get(LINK_SNOWAGER_1)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('.content center form input')

        # Probe snowager
        if soup1_match and soup1_match.get('value') == TEXT_SNOWAGER:
            result2 = self.account.get(LINK_SNOWAGER_2, referer=LINK_SNOWAGER_1)
            self.save(result2, 'snowager')
            soup2 = bs(result2.content, 'lxml')
            soup2_match_1 = soup2.select_one('td.content center p')
            soup2_match_1_text = soup2_match_1.get_text()
            if PATTERN_SNOWAGER_1.search(soup2_match_1_text):
                soup2_match_2 = soup2.select_one('td.content center p b')
                if soup2_match_2:
                    logger.info('Received: {}'.format(soup2_match_2.get_text()))
            elif PATTERN_SNOWAGER_2.search(soup2_match_1_text):
                soup2_match_2 = soup2.select_one('td.content center p b')
                if soup2_match_2:
                    logger.info('Received an exclusive prize: {}'.format(soup2_match_2.get_text()))
            elif PATTERN_SNOWAGER_3.search(soup2_match_1_text):
                logger.info('[Advent] The Snowager has been visited today')
            elif PATTERN_SNOWAGER_4.search(soup2_match_1_text):
                logger.info('The Snowager has been visited already')
            elif PATTERN_SNOWAGER_5.search(soup2_match_1_text):
                logger.info('The Snowager is awake!')
            elif PATTERN_SNOWAGER_6.search(soup2_match_1_text) or PATTERN_SNOWAGER_7.search(soup2_match_1_text):
                logger.info('Received nothing')
            elif PATTERN_SNOWAGER_8.search(soup2_match_1_text):
                logger.info('The Snowager attacked!')
            else:
                logger.warning('Unknown event!')
        else:
            logger.info('The Snowager is awake')

    def doAnchor(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Anchor')

        # Constants
        LINK_ANCHOR = '/pirates/anchormanagement.phtml'

        # Visit page
        result1 = self.account.get(LINK_ANCHOR)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('#form-fire-cannon input')

        # Grab form value and POST
        if soup1_match:
            soup1_value = soup1_match.get('value')
            result2 = self.account.post(
                LINK_ANCHOR,
                data={'action': soup1_value},
                referer=LINK_ANCHOR
            )
            self.save(result2, 'anchormanagement')

            # Find prize
            soup2 = bs(result2.content, 'lxml')
            soup2_match = soup2.select_one('.prize-item-name')
            if soup2_match:
                soup2_name = soup2_match.get_text()
                logger.info('Received: {}'.format(soup2_name))
            else:
                logger.info('Received nothing')
        else:
            logger.info('Already visited today!')

    def doAppleBobbing(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.AppleBobbing')

        # Constants
        LINK_APPLEBOB = '/halloween/applebobbing.phtml'
        PARAMS_APPLEBOB = {'bobbing': '1'}
        PATTERN_APPLEBOB_1 = re.compile(r'As you gaze into the water, about to bob your head in for a chance at appley-goodness')

        # Visit page
        result1 = self.account.get(LINK_APPLEBOB)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('#bob_content a')

        # Bob for apples
        if soup1_match:
            result2 = self.account.get(
                LINK_APPLEBOB,
                params=PARAMS_APPLEBOB,
                referer=LINK_APPLEBOB
            )
            self.save(result2, 'applebobbing')

            # Find prize
            soup2 = bs(result2.content, 'lxml')
            soup2_match1 = soup2.select_one('#bob_middle center b')
            soup2_match2 = soup2.select_one('#bob_middle')
            if soup2_match1:
                logger.info('Received: {}'.format(soup2_match1.get_text()))
            else:
                logger.info('Received nothing!')
        else:
            logger.info('Already visited today!')

    def doAdvent(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Advent')

        # Constants
        LINK_ADVENT_1 = '/winter/adventcalendar.phtml'
        LINK_ADVENT_2 = '/winter/adventClick.php'
        LINK_ADVENT_3 = '/winter/process_adventcalendar.phtml'
        TEXT_ADVENT = 'Collect My Prize!!!'
        PATTERN_ADVENT_1 = re.compile(r'day: "(?P<day>\d+?)"')
        PATTERN_ADVENT_2 = re.compile(r'ck: "(?P<ck>.+?)"')

        # Visit page
        result1 = self.account.get(LINK_ADVENT_1)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('.content div form input')

        # Check for receive rewards button!
        if soup1_match and soup1_match.get('value') == TEXT_ADVENT:
            match1 = PATTERN_ADVENT_1.search(result1.text)
            match2 = PATTERN_ADVENT_2.search(result1.text)

            # Click hidden object
            if match1 and match2:
                result2 = self.account.post(
                    LINK_ADVENT_2,
                    data={
                        'day': match1['day'],
                        'ck': match2['ck']
                    },
                    referer=LINK_ADVENT_1
                )
                self.save(result2, 'adventHidden')
                logger.info('Received: {}'.format(result2.json()['prize']['name']))

            # Get rewards
            result3 = self.account.post(
                LINK_ADVENT_3,
                referer=LINK_ADVENT_1
            )
            self.save(result3, 'adventRegular')
            soup3 = bs(result3.content, 'lxml')
            soup3_matches = soup3.select('.content div center b')
            if soup3_matches:
                for match in soup3_matches:
                    logger.info('Received {}'.format(match.get_text()))
            else:
                logger.info('Received nothing!')
        else:
            logger.info('Already visited today!')

    def doBankCollect(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.BankCollect')

        # Constants
        LINK_BANK_1 = '/bank.phtml'
        LINK_BANK_2 = '/process_bank.phtml'
        DATA_BANK = {'type': 'interest'}
        PATTERN_BANK = re.compile(r'Collect Interest \((?P<np>\d+) NP\)')

        # Visit page
        result1 = self.account.get(LINK_BANK_1)
        soup = bs(result1.content, 'lxml')
        soup_matches = soup.select('.contentModuleContent div form input')
        if soup_matches:
            soup_match = soup_matches[-1]  # Last match since there are other form inputs
            match = PATTERN_BANK.search(soup_match.get('value'))

            # Collect interest
            if match:
                result2 = self.account.post(
                    LINK_BANK_2,
                    data=DATA_BANK,
                    referer=LINK_BANK_1
                )
                self.save(result2, 'bankCollect')
                logger.info('Collected: {} NP'.format(match['np']))
            else:
                logger.warning('No collect button!')
        else:
            logger.info('Already collected or transacted today!')

        # TODO: Add auto bank account upgrade

    def doColtzan(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Coltzan')

        # Constants
        LINK_COLTZAN = '/desert/shrine.phtml'
        DATA_COLTZAN = {'type': 'approach'}
        TEXT_COLTZAN = 'Approach the Shrine'

        # Visit page
        result1 = self.account.get(LINK_COLTZAN)
        soup1 = bs(result1.content, 'lxml')
        soup1_matches = soup1.select('.content div form input')
        soup1_match = soup1_matches[1]  # First match is hidden input

        # Approach the shrine + also works for nothing happens
        if soup1_match and soup1_match.get('value') == TEXT_COLTZAN:
            result2 = self.account.post(
                LINK_COLTZAN,
                data=DATA_COLTZAN,
                referer=LINK_COLTZAN
            )
            self.save(result2, 'coltzan')
            soup2 = bs(result2.content, 'lxml')
            soup2_match = soup2.select_one('.content div div p')
            logger.info(soup2_match.get_text())
        else:
            logger.info('Already visited today!')

    def doDailyPuzzle(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.DailyPuzzle')

        # Constants
        LINK_PUZZLE_1 = '/community/index.phtml'
        LINK_PUZZLE_2 = 'http://www.jellyneo.net/?go=dailypuzzle'

        # Visit page
        result1 = self.account.get(LINK_PUZZLE_1)
        soup1 = bs(result1.content, 'lxml')
        # Question
        soup1_match1 = soup1.select_one('.question')
        # Date
        soup1_match2 = soup1.select_one('form[action="/community/index.phtml"] input')
        date = soup1_match2.get('value')

        # Visit Jellyneo solutions page
        result2 = self.account.get(LINK_PUZZLE_2)
        soup2 = bs(result2.content, 'lxml')
        soup2_matches = soup2.select('.panel p')
        # Uuestion
        soup2_match1 = soup2_matches[2]
        # Answer
        soup2_match2 = soup2_matches[3]

        # Check if question matches
        if soup1_match1.get_text() in soup2_match1.get_text():
            # Get options
            soup1_matches = soup1.select('select[name="trivia_response"] option')

            trivia_value = None
            for match in soup1_matches:
                if match.get_text() in soup2_match2.get_text():
                    trivia_value = match.get('value')

            if trivia_value:
                result3 = self.account.post(
                    LINK_PUZZLE_1,
                    data={
                        'trivia_date': date,
                        'trivia_response': trivia_value,
                        'submit': 'Submit'
                    },
                    referer=LINK_PUZZLE_1
                )
                self.save(result3, 'dailyPuzzle')
                soup3 = bs(result3.content, 'lxml')
                soup3_matches = soup3.select('.question b')
                # If NP and item
                if len(soup3_matches) > 1:
                    logger.info('Received: {} NP'.format(soup3_matches[0].get_text()))
                    logger.info('Received: {}'.format(soup3_matches[1].get_text()))
                # Else if only NP
                else:
                    logger.info('Received: {}'.format(soup3_matches[0].get_text()))
            else:
                logger.error('Matching trivia answer not found!')
        else:
            logger.error('Matching trivia question not found!')

    def doQuarry(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Quarry')

        # Constants
        LINK_QUARRY = '/magma/quarry.phtml'
        TEXT_QUARRY = "Hey!  What do you think you're doing?!"

        # Visit page
        result = self.account.get(LINK_QUARRY)
        self.save(result, 'quarry')
        soup = bs(result.content, 'lxml')
        soup_match = soup.select_one('.content div b')

        if soup_match and not soup_match.get_text() == TEXT_QUARRY:
            logger.info('Received: {}'.format(soup_match.get_text()))
        else:
            logger.info('Already visited today!')
