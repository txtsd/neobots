import re
import json
import time
import logging
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
        self.LINK_EVENTS = '/allevents.phtml'
        self.LINK_TRUDY_1 = '/trudys_surprise.phtml'
        self.LINK_TRUDY_2 = '/trudydaily/slotgame.phtml'
        self.LINK_TRUDY_3 = '/trudydaily/js/slotsgame.js'
        self.LINK_TRUDY_4 = '/trudydaily/ajax/claimprize.php'
        self.LINK_SNOWAGER_1 = '/winter/snowager.phtml'
        self.LINK_SNOWAGER_2 = '/winter/snowager2.phtml'
        self.LINK_ANCHOR = '/pirates/anchormanagement.phtml'

        # Params
        self.PARAMS_TRUDY = {'delevent': 'yes'}

        # POST Data
        self.DATA_TRUDY_1 = {'action': 'beginroll'}
        self.DATA_TRUDY_2 = {'action': 'prizeclaimed'}

        # Search texts
        self.TEXT_TRUDY = "Trudy's Surprise"
        self.TEXT_SNOWAGER = 'Attempt to steal a piece of treasure'

        # Regexes
        self.PATTERN_TRUDY_1 = re.compile(r'(?P<link>/trudydaily/slotgame\.phtml\?id=(?P<id>.*?)&slt=(?P<slt>\d+))')
        self.PATTERN_TRUDY_2 = re.compile(r'(?P<link>/trudydaily/js/slotsgame\.js\?v=(?P<v>\d+))')
        self.PATTERN_SNOWAGER_1 = re.compile(r'You carefully walk in and pick up a')
        self.PATTERN_SNOWAGER_2 = re.compile(r'You carefully walk in and hastily pick up an item')
        self.PATTERN_SNOWAGER_3 = re.compile(r'You have already collected your prize today.')
        self.PATTERN_SNOWAGER_4 = re.compile(r'Come back later.')
        self.PATTERN_SNOWAGER_5 = re.compile(r'The Snowager is awake')
        self.PATTERN_SNOWAGER_6 = re.compile(r'The Snowager moves slightly in its sleep')
        self.PATTERN_SNOWAGER_7 = re.compile(r'The Snowager awakes, looks straight at you')
        self.PATTERN_SNOWAGER_8 = re.compile(r'ROOOOAARRR')

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

        # Look for Trudy's Surprise event notfif at top of page
        result1 = self.account.get(self.LINK_INDEX)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('#neobdy.en div#main div#header table tr td.eventIcon.sf b')

        # If event exists
        if soup1_match and (soup1_match.get_text() == self.TEXT_TRUDY):
            result2 = self.account.get(
                self.LINK_TRUDY_1,
                params=self.PARAMS_TRUDY,
                referer=self.LINK_INDEX
            )
            soup2 = bs(result2.content, 'lxml')
            soup2_match = soup2.select_one('#frameTest')

            # Check for trudy game link
            if soup2_match:
                soup2_regexmatch = self.PATTERN_TRUDY_1.search(soup2_match.get('src'))
                result3 = self.account.get(
                    self.LINK_TRUDY_2,
                    params={
                        'id': soup2_regexmatch['id'],
                        'slt': soup2_regexmatch['slt']
                    },
                    referer=self.LINK_TRUDY_1
                )
                soup3 = bs(result3.content, 'lxml')
                soup3_matches = soup3.select('script')
                # Select the second script element which has the link we need
                soup3_match = soup3_matches[1]

                # Check for slotsgame link
                if soup3_match:
                    soup3_regexmatch = self.PATTERN_TRUDY_2.search(soup3_match.get('src'))
                    result4 = self.account.get(
                        self.LINK_TRUDY_3,
                        params={
                            'v': soup3_regexmatch['v'],
                        },
                        referer=soup2_regexmatch['link']
                    )

                    # Start POSTing
                    result5 = self.account.xhr(
                        self.LINK_TRUDY_4,
                        data={
                            'action': 'getslotstate',
                            'key': soup2_regexmatch['id']
                        },
                        referer=self.LINK_TRUDY_1
                    )
                    self.save(result5, 'trudy_getslotstate', JSON=True)
                    json5 = result5.json()
                    if not json5['error']:
                        time.sleep(5)
                        # Next POST
                        result6 = self.account.xhr(
                            self.LINK_TRUDY_4,
                            data=self.DATA_TRUDY_1,
                            referer=self.LINK_TRUDY_1
                        )
                        self.save(result6, 'trudy_beginroll', JSON=True)
                        json6 = result6.json()
                        if not json6['error']:
                            # Prize has been won
                            # Display before clicking the modal
                            logger.info(json6['prizes'])
                            result7 = self.account.xhr(
                                self.LINK_TRUDY_4,
                                data=self.DATA_TRUDY_2,
                                referer=self.LINK_TRUDY_1
                            )
                            json7 = result7.json()
                            if not json7['error']:
                                result8 = self.account.get(self.LINK_TRUDY_1, referer=self.LINK_TRUDY_1)
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

        # Visit snowager page
        result1 = self.account.get(self.LINK_SNOWAGER_1)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('.content center form input')

        # Probe snowager
        if soup1_match and soup1_match.get('value') == self.TEXT_SNOWAGER:
            result2 = self.account.get(self.LINK_SNOWAGER_2, referer=self.LINK_SNOWAGER_1)
            self.save(result2, 'snowager')
            soup2 = bs(result2.content, 'lxml')
            soup2_match_1 = soup2.select_one('td.content center p')
            soup2_match_1_text = soup2_match_1.get_text()
            if self.PATTERN_SNOWAGER_1.search(soup2_match_1_text):
                soup2_match_2 = soup2.select_one('td.content center p b')
                if soup2_match_2:
                    logger.info('Received: {}'.format(soup2_match_2.get_text()))
            elif self.PATTERN_SNOWAGER_1.search(soup2_match_1_text):
                soup2_match_2 = soup2.select_one('td.content center p b')
                if soup2_match_2:
                    logger.info('Received an exclusive prize: {}'.format(soup2_match_2.get_text()))
            elif self.PATTERN_SNOWAGER_3.search(soup2_match_1_text):
                logger.info('[Advent] The Snowager has been visited today')
            elif self.PATTERN_SNOWAGER_4.search(soup2_match_1_text):
                logger.info('The Snowager has been visited already')
            elif self.PATTERN_SNOWAGER_5.search(soup2_match_1_text):
                logger.info('The Snowager is awake!')
            elif self.PATTERN_SNOWAGER_6.search(soup2_match_1_text) or self.PATTERN_SNOWAGER_7.search(soup2_match_1_text):
                logger.info('Received nothing')
            elif self.PATTERN_SNOWAGER_8.search(soup2_match_1_text):
                logger.info('The Snowager attacked!')
            else:
                logger.warning('Unknown event!')
        else:
            logger.info('The Snowager is awake')

    def doAnchor(self):
        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Anchor')

        # Visit page
        result1 = self.account.get(self.LINK_ANCHOR)
        soup1 = bs(result1.content, 'lxml')
        soup1_match = soup1.select_one('#form-fire-cannon input')

        # Grab form value and POST
        if soup1_match:
            soup1_value = soup1_match.get('value')
            result2 = self.account.post(
                self.LINK_ANCHOR,
                data={'action': soup1_value},
                referer=self.LINK_ANCHOR
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
        # Links
        linkAppleBob1 = '/halloween/applebobbing.phtml'
        linkAppleBob2 = '/halloween/applebobbing.phtml?bobbing=1'

        # Regexes
        patternAppleBob1 = re.compile('<a href="/halloween/applebobbing.phtml?bobbing=1">')
        patternAppleBob2 = re.compile('<br><b>(?P<prize>.+?)</b></center><br>')

        # Setup logger
        logger = logging.getLogger('neobots.Freebies.AppleBobbing')

        # Visit page
        result1 = self.account.get(linkAppleBob1)
        matchAppleBob1 = patternAppleBob1.search(result1.text)

        if matchAppleBob1:
            # Bob for apples
            result2 = self.account.get(linkAppleBob2, referer=linkAppleBob1)
            self.save(result2, 'appleBobbing')

            # Find prize
            matchAppleBob2 = patternAppleBob2.search(result2.text)
            if matchAppleBob2:
                logger.info('Acquired ' + matchAppleBob2['prize'])
            else:
                logger.warning('Unknown event!')
        else:
            logger.info('Already visited today!')
