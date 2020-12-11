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
        self.LINK_TRUDY_1 = '/trudys_surprise.phtml'
        self.LINK_TRUDY_2 = '/trudydaily/slotgame.phtml'
        self.LINK_TRUDY_3 = '/trudydaily/js/slotsgame.js'
        self.LINK_TRUDY_4 = '/trudydaily/ajax/claimprize.php'
        self.LINK_EVENTS = '/allevents.phtml'

        # Params
        self.PARAMS_TRUDY = {'delevent': 'yes'}

        # POST Data
        self.DATA_TRUDY_1 = {'action': 'beginroll'}
        self.DATA_TRUDY_2 = {'action': 'prizeclaimed'}

        # Search texts
        self.TEXT_TRUDY = "Trudy's Surprise"

        # Regexes
        self.PATTERN_TRUDY_1 = re.compile(r'(?P<link>/trudydaily/slotgame\.phtml\?id=(?P<id>.*?)&slt=(?P<slt>\d+))')
        self.PATTERN_TRUDY_2 = re.compile(r'(?P<link>/trudydaily/js/slotsgame\.js\?v=(?P<v>\d+))')

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
        # Links
        linkSnowager1 = '/winter/snowager.phtml'
        linkSnowager2 = '/winter/snowager2.phtml'
        linkSnowager3 = '/winter/icecaves.phtml'

        # Regexes
        patternSnowager1 = re.compile('The Snowager is currently sleeping\.\.\.')
        patternSnowager2 = re.compile('Come back later\.')
        patternSnowager3 = re.compile('You have already collected your prize today')
        patternSnowager4 = re.compile('NEW BATTLEDOME CHALLENGER')
        patternSnowager5 = re.compile('The snowager rears up and fires a')
        patternSnowager6 = re.compile('The Snowager is awake')
        patternSnowager7 = re.compile('The Snowager moves slightly in its sleep')
        patternSnowager8 = re.compile('The Snowager is awake')

        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Snowager')

        # Visit snowager page
        result1 = self.account.get(linkSnowager1)
        matchSnowager1 = patternSnowager1.search(result1.text)

        # Probe snowager
        if matchSnowager1:
            result2 = self.account.get(linkSnowager2, referer=linkSnowager1)
            self.save(result2, 'snowager')

            # Check for rewards, battledome challenger, and getting attacked
            matchSnowager2 = patternSnowager2.search(result2.text)
            matchSnowager3 = patternSnowager3.search(result2.text)
            matchSnowager4 = patternSnowager4.search(result2.text)
            matchSnowager5 = patternSnowager5.search(result2.text)
            matchSnowager6 = patternSnowager6.search(result2.text)
            matchSnowager7 = patternSnowager7.search(result2.text)
            matchSnowager8 = patternSnowager8.search(result2.text)
            if matchSnowager2 or matchSnowager3:
                logger.info('The Snowager has been visited')
            elif matchSnowager4:
                logger.info('The Snowager battledome challenger has been unlocked!')
            elif matchSnowager5:
                logger.info('The Snowager attacks!')
            elif matchSnowager7 or matchSnowager8:
                logger.info('Nothing happens')
            else:
                logger.warning('Unknown event!')
        else:
            logger.info('The Snowager is awake')

    def doAnchor(self):
        # Links
        linkAnchor1 = '/pirates/anchormanagement.phtml'
        linkAnchor2 = '/pirates/index.phtml'

        # Regexes
        patternAnchor1 = re.compile(
            'id="form-fire-cannon"><input name="action" type="hidden" value="(?P<value>.+?)">')
        patternAnchor2 = re.compile('<span class="prize-item-name">(?P<prize>.+?)</span>')

        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Anchor')

        # Visit page
        result1 = self.account.get(linkAnchor1)

        # Grab form value and POST
        matchAnchor1 = patternAnchor1.search(result1.text)

        if matchAnchor1:
            result2 = self.account.post(
                linkAnchor1,
                data={
                    'action': matchAnchor1['value']
                },
                referer=linkAnchor1
            )
            self.save(result2, 'anchormanagement')

            # Find prize
            matchAnchor2 = patternAnchor2.search(result2.text)
            if matchAnchor2:
                logger.info('Acquired ' + matchAnchor2['prize'])
            else:
                logger.info('Got nothing')
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
