import re
import json
import time
import logging
from datetime import date
from pathlib import Path


class Freebies:

    def __init__(self, account):
        self.account = account
        # self.baseReferer = self.account.domain + '/'
        self.username = account.username
        self.pathString = '.debug'

        # Create debug directory
        self.debugOutput = Path(self.pathString)
        self.debugOutput.mkdir(exist_ok=True)

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
        # Links
        linkTrudy = '/trudys_surprise.phtml'

        # Regexes
        patternTrudy1 = re.compile("Trudy's Surprise has reset and is waiting for you!")
        patternTrudy2 = re.compile('(?P<link>/trudydaily/slotgame\.phtml\?id=(?P<id>.*?)&slt=(?P<slt>\d+))')
        patternTrudy3 = re.compile('(?P<link>/trudydaily/js/slotsgame\.js\?v=(?P<v>\d+))')

        # Setup logger
        logger = logging.getLogger('neobots.Freebies.Trudy')

        # Get inbox
        result1 = self.account.get('/allevents.phtml', referer='/index.html')

        # Check inbox for Trudy's daily
        if patternTrudy1.search(result1.text):
            result2 = self.account.get(linkTrudy, referer='/allevents.phtml')
            matchTrudy2 = patternTrudy2.search(result2.text)

            # Double check for Trudy availability
            if matchTrudy2:
                result3 = self.account.get(matchTrudy2['link'], referer=linkTrudy)
                matchTrudy3 = patternTrudy3.search(result3.text)

                # Check for slotsgame link
                if matchTrudy3:
                    result4 = self.account.get(matchTrudy3['link'], referer=matchTrudy2['link'])

                    # Start POSTing
                    result5 = self.account.xhr(
                        '/trudydaily/ajax/claimprize.php',
                        data={
                            'action': 'getslotstate',
                            'key': matchTrudy2['id']
                        },
                        referer=linkTrudy
                    )
                    self.save(result5, 'trudy_getslotstate', JSON=True)
                    json5 = json.loads(result5.text)
                    if not json5['error']:
                        time.sleep(5)
                        result6 = self.account.xhr(
                            '/trudydaily/ajax/claimprize.php',
                            data={
                                'action': 'beginroll'
                            },
                            referer=linkTrudy
                        )
                        self.save(result6, 'trudy_beginroll', JSON=True)
                        json6 = json.loads(result6.text)
                        if not json6['error']:
                            # Prize has been won
                            # Display before clicking the modal
                            logger.info(json6['prizes'])
                            result7 = self.account.xhr(
                                '/trudydaily/ajax/claimprize.php',
                                data={
                                    'action': 'prizeclaimed'
                                },
                                referer=linkTrudy
                            )
                            json7 = json.loads(result7.text)
                            if not json7['error']:
                                result8 = self.account.get(linkTrudy, referer=linkTrudy)
                            else:
                                logger.error(json7['error'])
                        else:
                            logger.error(json6['error'])
                    else:
                        logger.error(json5['error'])
                else:
                    logger.error('No slotsgame.js version string')
            else:
                logger.error('No slotgame id')
        else:
            logger.info("Trudy's Surprise has already been played today!")

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
