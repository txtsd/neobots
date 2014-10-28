# ---------------------------------------------------------------------
# neobots 1.0.5 -------------------------------------------------------
# Made by txtsd -------------------------------------------------------
# Based on raredaredevil's/DarkByte's HabiBot/NeoAuto -----------------
# Open Source Neopets Automation --------------------------------------
# ---------------------------------------------------------------------

# Import needed classes
import time  # Time module, used for sleeping
import datetime  # Time for ticks
import random  # Used to randomise numbers and summon one from between a range
import sys
import threading


# Begin Class
class habi:

    # Checked
    def __init__(self, acc, thegateway, build_housecount,
                 build_nestcount, build_storagecount, build_hospitalcount):
        self.lastexp = 0
        self.lastlevel = 0
        # A flag for to detect if this is the first run of the loop or not
        self.isfirstrun = 1
        # Buffer to store the last time we checked for gems on stage
        self.LAST_GEM_CHECK_TIME = 1
        # Buffer to store the last time we checked for eggs on stage
        self.LAST_EGG_CHECK_TIME = 1
        self.LAST_UPGRADE_CHECK_TIME = 1
        # Set amfs opener to our accounts (share the login/cookie)
        # self.theopener = acc.opener.open
        self.gateway = thegateway
        # Only load the services once when class inits, per tick just adds
        # more room for failure
        self.player_service = self.amfgetservice("PlayerService")
        self.event_service = self.amfgetservice("EventService")
        self.scene_service = self.amfgetservice("SceneService")
        self.Inventory_Service = self.amfgetservice("InventoryService")
        self.store_service = self.amfgetservice("StoreService")
        self.upgradeservice = self.amfgetservice("UpgradeService")
        print "-------init-------"
        self.mapdata = []
        self.themapid = '-1'
        self.amf_levelinfo = ""
        self.build_nestcount = build_nestcount
        self.build_housecount = build_housecount
        self.build_storagecount = build_storagecount
        self.build_hospitalcount = build_hospitalcount
        # Urgently buy this item id, because we need it to complete our map
        # (Set in build item function, if we dont have the item needed)
        self.urgentbuy = 0
        self.mapary = []
        self.dumpWorker = ""
        # with open("./storeItems.txt", "w") as f:
            # f.write(str(self.store_service.storeItems()))
        # self.itemcollection = self.scene_service.sceneItems()
        # for x in self.itemcollection:
            # if x['sceneItemType'] == "Structure":
                # print "Struc"
                # if x['x'] == "5" and x['y'] == "2":
                    # print "5,2"
                    # self.Inventory_Service.moveToItemBag(str(x["m_id"]))
                    # print "moved it to bag"

    # Checked
    def checkworkers(self):
        workerid = self.findnonbusyworker()
        doneone = 0
        if workerid > -1:
            lowestres = self.getlowestresource()
            if not (lowestres == "none"):
                print "[lowestRes:" + lowestres + "]"
                self.setworkercollect(workerid, lowestres)

    # Checked
    def checknonbuiltbuildings(self):
        doneone = 0
        pets = self.countpets()
        P3type = ""
        buildingdata = self.findnoncompletebuilding()
        if not buildingdata == -1:
            buildid = buildingdata["m_id"]
            badx = buildingdata["x"]
            bady = buildingdata["y"]
            if (pets[3] > 0):
                builderid = self.findnonbusysoldier()
                P3type = "soldier"
            else:
                builderid = self.findnonbusyworker()
                P3type = "worker"
            if builderid > -1:
                emptytile = self.findemptytilearound(badx, bady)
                if (emptytile):  # Empty tile found
                    doneone = 1
                    self.scene_service.moveItem(
                        str(builderid), str(emptytile[0]), str(emptytile[1]))
                    print "[" + P3type + "#" + str(builderid) + "] now building unbuilt structure at [" + str(emptytile[0]) + "," + str(emptytile[1]) + "]"
        return doneone

    # Temp
    def threadcollectgem(self, gemid):
        self.scene_service.collectGem(gemid)

    # Checked
    def checkgems(self):
        self.itemcollection = self.scene_service.sceneItems()
        print "Looking for gems on stage"
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Gem"):
                strid = str(x['m_id'])
                try:
                    threading.Thread(target=self.threadcollectgem, args=(strid,)).start()
                except:
                    # print "Gem thread Timeout Error"
                    threading.Thread(target=self.threadcollectgem, args=(strid,)).start()
                # if str((self.scene_service.collectGem(str(x['m_id']))) ==
                # "True"):
                print "[gem#" + str(x['m_id']) + "] collected!"

    # Checked
    def countmapitems(self):
        counter = [0, 0, 0, 0, 0]
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Structure"):
                counter[0] += 1
                if (x['type'] == "House"):
                    counter[1] += 1
                elif (x['type'] == "Storage"):
                    counter[2] += 1
                elif (x['type'] == "Nest"):
                    counter[3] += 1
                elif (x['type'] == "Hospital"):
                    counter[4] += 1
        return counter

    # Checked
    def readmapfile(self, thefolder):
        print str(thefolder)
        with open(thefolder) as f:
            lines = f.readlines()
        lines2 = []
        for x in lines:
            # Fix EOL
            lines2.append(x.replace("\n", ""))
        return lines2

    # Checked
    def loadmapdata(self, mapid):
        maps = self.readmapfile("./data/habimaps/" + mapid + ".txt")
        return maps

    # Checked
    def autoreshack(self):
        # Automatially perform reshack
        doneone = 1
        while doneone == 1:
            self.amf_playerinfo = self.player_service.playerinfo()
            resp = self.amf_playerinfo
            if int(resp['isSetup']) == 0:
                print "New habi detected, sending setup packet"
                self.player_service.skillSetup()  # Sets up a brand new habi
            print "Resetting player"
            self.player_service.reset()
            rand = random.randrange(0, 100)
            if (rand < 50):
                self.themapid = '0'
            else:
                self.themapid = '2'
            print "Choosing map " + self.themapid
            self.scene_service.setupHabitarium(self.themapid)
            print "Setting tutorial to complete"
            self.player_service.setTutorialProgress("-1")
            print "Sending Update"
            self.event_service.update('40', '40')
            self.event_service.simulate()
            self.scene_service.collectGem("16")
            self.event_service.update('40', '40')
            self.itembag = self.Inventory_Service.itemBag()
            doneone = 0
            print "[#houses:" + str(self.countinvitems("House")) + "]"
            if (self.countinvitems("House") < self.build_housecount):
                # Reshack is generating a house
                doneone = 1
                print "Resource Hack Generating a house"
                self.store_service.buyItem("15")  # 15h, 20s, 22n
                self.event_service.update('40', '40')
                self.event_service.simulate()
                print "Resource Hack Generated a house"
            print "[#storages:" + str(self.countinvitems("Storage")) + "]"
            if doneone == 0:
                if (self.countinvitems("Storage") < self.build_storagecount):
                    doneone = 1
                    print "Resource Hack Generating a Storage Center"
                    self.store_service.buyItem("20")  # 15h, 20s, 22n
                    self.event_service.update('40', '40')
                    self.event_service.simulate()
                    print "Resource Hack Generated a Storage Center"
            print "[#nests:" + str(self.countinvitems("Nest")) + "]"
            if doneone == 0:
                if (self.countinvitems("Nest") < 20):
                    doneone = 1
                    print "Resource Hack Generating a Nest"
                    self.store_service.buyItem("22")  # 15h, 20s, 22n
                    self.event_service.update('40', '40')
                    self.event_service.simulate()
                    print "Resource Hack Generated a Nest"
            if doneone == 0:
                # Nothing left to do break
                print "Done"
                break
                return 1

    # Checked
    def findinvitem(self, itemname):
        retid = 0
        for x in self.itembag:
            if (x[1]['sceneItemType'] == "Structure"):
                if (x[1]['type'] == itemname):
                    if (x[1]['isBuilt'] is False):
                        retid = x[1]['m_id']
                        return retid
        return retid

    # Checked
    def findinveggprof(self, profname):
        retid = 0
        for x in self.itembag:
            if (x[1]['sceneItemType'] == "Egg"):
                if profname in x[1]['name']:
                    retid = x[1]['m_id']
                    return retid
        return retid

    # Checked
    def countinvitems(self, itemname):
        retid = 0
        # print "entered countinvitems" + str(retid)
        for x in self.itembag:
            # print "loop #" + str(x[0])
            if (x[1]['sceneItemType'] == "Structure"):
                if (x[1]['type'] == str(itemname)):
                    # print "true"
                    retid += 1
                    # print "retid" + str(retid)
        return retid

    # Checked
    def countinveggs(self):
        counter = [0, 0, 0, 0]
        for x in self.itembag:
            if (x[1]['sceneItemType'] == "Egg"):
                counter[0] += 1
                if "Worker" in x[1]['name']:
                    counter[1] += 1
                elif "Nester" in x[1]['name']:
                    counter[2] += 1
                elif "Soldier" in x[1]['name']:
                    counter[3] += 1
        return counter

    # Checked
    def setDumpWorker(self):
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                if (x['profession'] == "worker"):
                    self.dumpWorker = x['m_id']
                    break
        # print "[worker#" + str(self.dumpWorker) + "] has been set as nestdump
        # builder"
        return x

# ---------------------------------------------------------------------
# DoLoop()
# ---------------------------------------------------------------------
    def DoLoop(self):
        try:
            print "\n----Begin Loop----"
            # self.gateway.opener = self.theopener
            self.itemcollection = self.scene_service.sceneItems()
            self.amf_playerinfo = self.player_service.playerinfo()
            playerlevel = self.amf_playerinfo['habitariumLevel']
            self.itembag = self.Inventory_Service.itemBag()
            if (playerlevel < 2):
                if not ((self.countinvitems("House") >= self.build_housecount) and (self.countinvitems("Storage") >= self.build_storagecount) and (self.countinvitems("Nest") >= 20)):
                    self.autoreshack()
                    print "---End ResHack----"
                    return 0
            # Check if first run; if so, load some config
            if self.isfirstrun == 1:
                # Force check reshack
                # self.needResHack()
                print "First run of tick, loading files"
                # This is the first run of this code..
                # Players map id
                for x in self.itemcollection:
                    if (x['sceneItemType'] == 'Resource'):
                        if (x['x'] == 1) and (x['y'] == 1):
                            if (x['type'] == 'pollen'):
                                self.themapid = '0'
                                print 'found pollen at [1,1]'
                                break
                        if (x['x'] == 1) and (x['y'] == 2):
                            if (x['type'] == 'water'):
                                self.themapid = '1'
                                print 'found water at [1,2]'
                                break
                        if (x['x'] == 0) and (x['y'] == 4):
                            if (x['type'] == 'stone'):
                                self.themapid = '2'
                                print 'found stone at [0,4]'
                                break
                # load the map file
                self.mapary = self.loadmapdata(self.themapid)
                self.isfirstrun = 0
                print "-----End Loop-----"
                return 0
            # End firstRun check
            if (self.themapid == '-1'):
                print 'Map not loaded. Re-run client.'
                sys.exit()
            self.amf_levelinfo = self.event_service.simulate()  # Level info
            self.updateinfo = self.event_service.update('40', '40')
            maxxp = self.amf_levelinfo['player']['levelInfo']['nextXP']
            thisexp = self.amf_levelinfo['player']['xp'] - self.lastexp
            self.lastexp = self.amf_levelinfo['player']['xp']
            if (self.amf_playerinfo['habitariumLevel'] > self.lastlevel):
                self.player_service.nextLevelGains()
            self.lastlevel = self.amf_playerinfo['habitariumLevel']
            # Set counts for feed
            self.stonecount = int(self.updateinfo['resources']['stone'])
            self.mudcount = int(self.updateinfo['resources']['mud'])
            self.woodcount = int(self.updateinfo['resources']['wood'])
            self.pollencount = int(self.updateinfo['resources']['pollen'])
            self.grasscount = int(self.updateinfo['resources']['grass'])
            self.watercount = int(self.updateinfo['resources']['water'])
            if (playerlevel < 50):
                print "[" + str(datetime.datetime.now().time())[:-3] + "] [" + str(self.amf_playerinfo['neoUsername']) + "] [level:" + str(self.amf_playerinfo['habitariumLevel']) + "] [+exp:" + str(thisexp) + "] [totalExp:" + str(self.amf_levelinfo['player']['xp']) + "/" + str(maxxp) + "]"
            else:
                print "[" + str(datetime.datetime.now().time())[:-3] + "] [" + str(self.amf_playerinfo['neoUsername']) + "] [level:" + str(self.amf_playerinfo['habitariumLevel']) + "] [nextGem:" + str((self.amf_levelinfo['player']['cappedXP']) % 1000) + "/1000] [lvl50gemsCollected:" + str(self.amf_levelinfo['player']['cappedXPRewards']) + "]"
            print "[#stone:" + str(self.stonecount) + "] [#mud:" + str(self.mudcount) + "] [#wood:" + str(self.woodcount) + "] [#pollen:" + str(self.pollencount) + "] [#grass:" + str(self.grasscount) + "] [#water:" + str(self.watercount) + "]"
            # Counts and prints the amount of each type of P3
            # pets = self.countpets()
            # print "[#workers:" + str(pets[1]) + "] [#nesters:" + str(pets[2]) + "] [#soldiers:" + str(pets[3]) + "]"
            # Do timer dependent code
            self.tilecollection = self.amf_levelinfo['map']['tiles']
            if (time.time() - float(self.LAST_GEM_CHECK_TIME) > 120):  # 2min
                self.LAST_GEM_CHECK_TIME = time.time()  # Update time
                self.checkgems()  # Check for any gems and collect them
            if self.checknonbuiltbuildings() == 0:
                if self.findnonhealthybuildings() == 0:
                    self.checkworkers()
            self.buildmap(playerlevel)
            self.checkhungry()
            # Check for full houses with healed pets and move them out
            self.checkhouses()
            self.checkhospitals()
            self.checknesters()
            # Check for eggs, harvest a bunch, then hatch/discard
            self.checkeggs()
            # We dont urgently need to buy a item
            if self.urgentbuy == 0:
                # Check for upgrades based on current player level.
                self.checkupgrades(playerlevel)
                # print "Done checking"
                if (playerlevel >= 30):
                    if (self.stonecount > 20000) and (self.woodcount > 20000) and (self.mudcount > 20000):
                        print "Buying a dump nest"
                        self.store_service.buyItem("22")
                if (playerlevel >= 40):
                    if (self.stonecount > 8250) and (self.woodcount > 6900) and (self.mudcount > 4850):
                        self.dumpNest()
            else:
                # Urgentbuy
                self.urgentBuy()
                # print "Done spending"
            print "-----End Loop-----"
        except KeyboardInterrupt:
            print "\n------------------"
            print "neobots was interrupted via keyboard"
            print "------------------"
            sys.exit()
        except:
            print "------------------"
            print "-Something broke--"
            print "------------------"
            time.sleep(10)

# ---------------------------------------------------------------------
# End DoLoop()
# ---------------------------------------------------------------------

    # Checked - Made this myself
    def dumpNest(self):
        if not (self.itemexistat(0, 9)):
            if (self.countinvitems("Nest") > 3):
                getnest = self.findinvitem("Nest")
                # hardcoded location change later
                if (getnest != 0):
                    self.scene_service.moveItem(str(getnest), "0", "9")
                    print "[dumpNest#" + str(getnest) + "] placed at [0,9]"
        else:
            for x in self.itemcollection:
                if (x['sceneItemType'] == "Structure"):
                    if (x['x'] == "0") and (x['y'] == "9"):
                        if (x['isBuilt'] is False):
                            if (self.countpets()[3] > 0):
                                soldier = self.findnonbusysoldier()
                                if soldier > -1:
                                    # hardcoded location change later
                                    print "[soldier#" + str(soldier) + "] now building a dump nest"
                                    self.scene_service.moveItem(
                                        str(soldier), "1", "9")
                            else:
                                dudex = self.setDumpWorker()
                                if not (dudex['attachedTo'] == x['m_id']):
                                    print "[worker#" + str(dudex['m_id']) + "] now building a dump nest"
                                    self.scene_service.moveItem(
                                        str(dudex['m_id']), "1", "9")
                        else:
                            if (x['itemLevel'] == 1):
                                if (self.mudcount > 850):
                                    if (self.stonecount > 1050):
                                        if (self.woodcount > 800):
                                            print "[dumpNest#" + str(x['m_id']) + "] upgraded to lvl2"
                                            self.upgradeservice.buyUpgrade(
                                                "22", str(x['m_id']))
                            elif (x['itemLevel'] == 2):
                                if (self.mudcount > 950):
                                    if (self.stonecount > 1300):
                                        if (self.woodcount > 900):
                                            print "[dumpNest#" + str(x['m_id']) + "] upgraded to lvl3"
                                            self.upgradeservice.buyUpgrade(
                                                "23", str(x['m_id']))
                            elif (x['itemLevel'] == 3):
                                print "[dumpNest#" + str(x['m_id']) + "] has served its purpose"
                                self.Inventory_Service.moveToItemBag(
                                    str(x['m_id']))
                                print "Moved [dumpNest#" + str(x['m_id']) + "] to bag"
                                self.Inventory_Service.deleteItem(
                                    str(x['m_id']))
                                print "Deleted [dumpNest#" + str(x['m_id']) + "] from bag"

    def buildmap(self, playerlevel):
        structures = self.countmapitems()
        print "[tStrc,tHous,tStor,tNest,tHosp] " + str(structures)
        if (structures[1] < self.build_housecount):
            print "Trying to build a House"
            invitem = self.findinvitem("House")
            if (invitem == 0):
                self.urgentbuy = 15
                print "Do not have a needed item in iventory; item will be bought"
                return 0
            else:
                print "House found in inventory so building it"
                shuffledmap = self.mapary
                random.shuffle(shuffledmap)
                for currenttile in shuffledmap:
                    tempdata = currenttile.split(":")
                    tilecoords = tempdata[0]
                    tiletype = tempdata[1]
                    tilecoords = tilecoords.split(",")
                    tileX = tilecoords[0]
                    tileY = tilecoords[1]
                    if tiletype == "build":
                        if self.itemexistat(tileX, tileY) is False:
                            self.scene_service.moveItem(
                                str(invitem), str(tileX), str(tileY))
                            self.urgentbuy = 0
                            return 1
        if (structures[2] < self.build_storagecount):
            print "Trying to build a Storage"
            invitem = self.findinvitem("Storage")
            if (invitem == 0):
                self.urgentbuy = 20
                print "Do not have a needed item in iventory; item will be bought"
                return 0
            else:
                print "Storage found in inventory so building it"
                shuffledmap = self.mapary
                random.shuffle(shuffledmap)
                for currenttile in shuffledmap:
                    tempdata = currenttile.split(":")
                    tilecoords = tempdata[0]
                    tiletype = tempdata[1]
                    tilecoords = tilecoords.split(",")
                    tileX = tilecoords[0]
                    tileY = tilecoords[1]
                    if tiletype == "build":
                        if self.itemexistat(tileX, tileY) is False:
                            self.scene_service.moveItem(
                                str(invitem), str(tileX), str(tileY))
                            self.urgentbuy = 0
                            return 1
        if (structures[3] < self.build_nestcount):
            print "Trying to build a Nest"
            invitem = self.findinvitem("Nest")
            if (invitem == 0):
                self.urgentbuy = 22
                print "Do not have a needed item in iventory; item will be bought"
                return 0
            else:
                print "Nest found in inventory so building it"
                shuffledmap = self.mapary
                random.shuffle(shuffledmap)
                for currenttile in shuffledmap:
                    tempdata = currenttile.split(":")
                    tilecoords = tempdata[0]
                    tiletype = tempdata[1]
                    tilecoords = tilecoords.split(",")
                    tileX = tilecoords[0]
                    tileY = tilecoords[1]
                    if tiletype == "build":
                        if self.itemexistat(tileX, tileY) is False:
                            self.scene_service.moveItem(
                                str(invitem), str(tileX), str(tileY))
                            self.urgentbuy = 0
                            return 1
        if (playerlevel >= 15):
            if (structures[4] < self.build_hospitalcount):
                print "Trying to build a Hospital"
                invitem = self.findinvitem("Hospital")
                if (invitem == 0):
                    self.urgentbuy = 41
                    print "Do not have a needed item in iventory; item will be bought"
                    return 0
                else:
                    print "Hospital found in inventory so building it"
                    shuffledmap = self.mapary
                    random.shuffle(shuffledmap)
                    for currenttile in shuffledmap:
                        tempdata = currenttile.split(":")
                        tilecoords = tempdata[0]
                        tiletype = tempdata[1]
                        tilecoords = tilecoords.split(",")
                        tileX = tilecoords[0]
                        tileY = tilecoords[1]
                        if tiletype == "build":
                            if self.itemexistat(tileX, tileY) is False:
                                self.scene_service.moveItem(
                                    str(invitem), str(tileX), str(tileY))
                                self.urgentbuy = 0
                                return 1

    # Checked - AMF stuff makes no sense to me
    def amfgetservice(self, servicename):
        # self.gateway.opener = self.theopener
        theret = self.gateway.getService(servicename)  # Get The service

        return theret

    # Checked - Modified to flow better
    def checkupgrades(self, playerlevel):
        print "Searching for upgrades"
        ret = 0  # return 0 if none done
        # Get list of all upgrades player has
        # first give them a default
        got_nester_lvl_1_upgrade = 0
        got_worker_lvl_1_upgrade = 0
        got_nester_lvl_2_upgrade = 0
        got_worker_lvl_2_upgrade = 0
        got_soldier_lvl_1_upgrade = 0
        got_soldier_lvl_2_upgrade = 0
        playersupgrades = self.upgradeservice.playerUpgrades()
        # with open("./playerUpgrades.txt", "w") as f:
            # f.write(str(playersupgrades))
            # print "upgradeservice.playerUpgrades()"
        # availableupgrades = self.upgradeservice.availableUpgrades()
        # with open("./availableUpgrades.txt", "w") as g:
            # g.write(str(availableupgrades))
            # print "upgradeservice.availableUpgrades()"
        for x in playersupgrades:
            if x['m_id'] == 1:  # Level 1 worker upgrade
                got_worker_lvl_1_upgrade = 1
            if x['m_id'] == 2:  # Level 2 worker upgrade
                got_worker_lvl_2_upgrade = 1
            if x['m_id'] == 6:  # Level 1 nester upgrade
                got_nester_lvl_1_upgrade = 1
            if x['m_id'] == 7:  # Level 2 nester upgrade
                got_nester_lvl_2_upgrade = 1
            if x['m_id'] == 11:  # Level 1 soldier upgrade
                got_soldier_lvl_1_upgrade = 1
            if x['m_id'] == 12:  # Level 1 soldier upgrade
                got_soldier_lvl_2_upgrade = 1
        # dont even waste my cpu if no upgrades available for this level (11+
        # for upgrades)
        if playerlevel >= 11:
            # print "playerlevel > 10"
            for x in self.itemcollection:
                # level 1 workers
                if got_worker_lvl_1_upgrade == 0:  # only if we havent got all
                    if (x['sceneItemType'] == "Character"):
                        # if (x['unlockLevel']) == 1:
                        if x['profession'] == "worker":
                            if self.pollencount > 25:
                                if self.grasscount > 25:
                                    if self.watercount > 50:
                                        upgradeid = x['m_id']
                                        print "Upgraded workers from lvl1 to lvl2 [upgradeID#" + str(upgradeid) + "]"
                                        # print pollencount
                                        self.upgradeservice.buyUpgrade(
                                            "1", str(upgradeid))
                                        return 1
                # level 1 nesters
                if got_nester_lvl_1_upgrade == 0:  # only if we havent got all
                    if (x['sceneItemType'] == "Character"):
                        # if (x['unlockLevel']) == 1:
                        if x['profession'] == "nester":
                            if self.pollencount > 25:
                                if self.grasscount > 25:
                                    if self.watercount > 50:
                                        upgradeid = x['m_id']
                                        print "Upgraded nesters from lvl1 to lvl2 [upgradeID#" + str(upgradeid) + "]"
                                        # print pollencount
                                        self.upgradeservice.buyUpgrade(
                                            "6", str(upgradeid))
                                        return 1
                # level 1 soldiers - this only executes if the player has a soldier on
                # stage but if so its a nice little +200 exp tweak
                if got_soldier_lvl_1_upgrade == 0:  # only if we havent got all
                    if (x['sceneItemType'] == "Character"):
                        # if (x['unlockLevel']) == 1:
                        if x['profession'] == "soldier":
                            if self.pollencount > 25:
                                if self.grasscount > 25:
                                    if self.watercount > 50:
                                        upgradeid = x['m_id']
                                        print "Upgraded soldiers from lvl1 to lvl2 [upgradeID#" + str(upgradeid) + "]"
                                        self.upgradeservice.buyUpgrade(
                                            "11", str(upgradeid))
                                        return 1
                if playerlevel >= 13:
                    # print "playerlevel > 12"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'House'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 1):
                                if (self.mudcount > 600):
                                    if (self.stonecount > 1300):
                                        if (self.woodcount > 950):
                                            print "[house#" + str(upgradeid) + "] upgraded to lvl2"
                                            self.upgradeservice.buyUpgrade(
                                                "16", str(upgradeid))
                                            return 1
                if playerlevel >= 17:
                    # print "playerlevel > 16"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'Nest'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 1):
                                if (self.mudcount > 850):
                                    if (self.stonecount > 1050):
                                        if (self.woodcount > 800):
                                            print "[nest#" + str(upgradeid) + "] upgraded to lvl2"
                                            self.upgradeservice.buyUpgrade(
                                                "22", str(upgradeid))
                                            return 1
                if playerlevel >= 21:
                    # print "playerlevel > 20"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'Storage'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 1):
                                if (self.mudcount > 1250):
                                    if (self.stonecount > 1800):
                                        if (self.woodcount > 3400):
                                            print "[storage#" + str(upgradeid) + "] upgraded to lvl2"
                                            self.upgradeservice.buyUpgrade(
                                                "19", str(upgradeid))
                                            return 1
                if playerlevel >= 25:
                    # print "playerlevel > 24"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'Hospital'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 1):
                                if (self.mudcount > 2100):
                                    if (self.stonecount > 4800):
                                        if (self.woodcount > 3900):
                                            print "[hospital#" + str(upgradeid) + "] upgraded to lvl2"
                                            self.upgradeservice.buyUpgrade(
                                                "28", str(upgradeid))
                                            return 1
                if playerlevel >= 31:
                    # print "playerlevel > 30"
                    # level 2 workers
                    # only if we havent got all
                    if got_worker_lvl_2_upgrade == 0:
                        if (x['sceneItemType'] == "Character"):
                            # if (x['unlockLevel']) == 1:
                            if x['profession'] == "worker":
                                if self.pollencount > 30:
                                    if self.grasscount > 30:
                                        if self.watercount > 60:
                                            upgradeid = x['m_id']
                                            print "Upgraded workers from lvl2 to lvl3 [upgradeID#" + str(upgradeid) + "]"
                                            self.upgradeservice.buyUpgrade(
                                                "2", str(upgradeid))
                                            return 1
                    # level 2 nesters
                    # only if we havent got all
                    if got_nester_lvl_2_upgrade == 0:
                        if (x['sceneItemType'] == "Character"):
                            # if (x['unlockLevel']) == 1:
                            if x['profession'] == "nester":
                                if self.pollencount > 30:
                                    if self.grasscount > 30:
                                        if self.watercount > 60:
                                            upgradeid = x['m_id']
                                            print "Upgraded nesters from lvl2 to lvl3 [upgradeID#" + str(upgradeid) + "]"
                                            self.upgradeservice.buyUpgrade(
                                                "7", str(upgradeid))
                                            return 1
                    # level 2 soldiers
                    # only if we havent got all
                    if got_soldier_lvl_2_upgrade == 0:
                        if (x['sceneItemType'] == "Character"):
                            # if (x['unlockLevel']) == 1:
                            if x['profession'] == "soldier":
                                if self.pollencount > 30:
                                    if self.grasscount > 30:
                                        if self.watercount > 60:
                                            upgradeid = x['m_id']
                                            print "Upgraded soldiers from lvl2 to lvl3 [upgradeID#" + str(upgradeid) + "]"
                                            self.upgradeservice.buyUpgrade(
                                                "12", str(upgradeid))
                                            return 1
                if playerlevel >= 36:
                    # print "playerlevel > 35"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'House'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 2):
                                if (self.mudcount > 850):
                                    if (self.stonecount > 2200):
                                        if (self.woodcount > 1150):
                                            print "[house#" + str(upgradeid) + "] upgraded to lvl3"
                                            self.upgradeservice.buyUpgrade(
                                                "17", str(upgradeid))
                                            return 1
                if playerlevel >= 40:
                    # print "playerlevel > 39"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'Nest'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 2):
                                if (self.mudcount > 950):
                                    if (self.stonecount > 1300):
                                        if (self.woodcount > 900):
                                            print "[nest#" + str(upgradeid) + "] upgraded to lvl3"
                                            self.upgradeservice.buyUpgrade(
                                                "23", str(upgradeid))
                                            return 1
                if playerlevel >= 44:
                    # print "playerlevel > 43"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'Storage'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 2):
                                if (self.mudcount > 1300):
                                    if (self.stonecount > 1850):
                                        if (self.woodcount > 3800):
                                            print "[storage#" + str(upgradeid) + "] upgraded to lvl3"
                                            self.upgradeservice.buyUpgrade(
                                                "20", str(upgradeid))
                                            return 1
                if playerlevel >= 48:
                    # print "playerlevel > 43"
                    if (x['sceneItemType'] == 'Structure'):
                        if (x['type'] == 'Hospital'):
                            upgradeid = x['m_id']
                            if (x['itemLevel'] == 2):
                                if (self.mudcount > 2100):
                                    if (self.stonecount > 5250):
                                        if (self.woodcount > 4400):
                                            print "[hospital#" + str(upgradeid) + "] upgraded to lvl3"
                                            self.upgradeservice.buyUpgrade(
                                                "29", str(upgradeid))
                                            return 1

    # Checked
    def findnonhealthybuildings(self):
        doneone = 0
        pets = self.countpets()
        print "Checking for unhealthy buildings"
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Structure"):
                # Buildings have a heath and a decay level
                # Only use decay levels in this version, it's better this way
                if (x['decayLevel'] > 1):
                    buildid = x['m_id']
                    if (pets[3] > 0):
                        builderid = self.findnonbusysoldier()
                    else:
                        builderid = self.findnonbusyworker()
                    if not int(builderid) == -1:
                        badx = self.getbuildingx(buildid)
                        bady = self.getbuildingy(buildid)
                        emptytile = self.findemptytilearound(badx, bady)
                        if emptytile:  # tile found
                            doneone = 1
                            self.scene_service.moveItem(
                                str(builderid), str(badx), str(bady))
                            print "[P3#" + str(builderid) + "] now fixing unhealthy building at [" + str(badx) + "," + str(bady) + "]"
                            return doneone
        return doneone

    # Checked - Set about 5k for gpw
    def getlowestresource(self):
        print "Finding lowest resource"
        lowestres = "none"
        lowestrescount = 0
        lowestrescount = self.woodcount
        lowestres = "wood"
        if (self.mudcount < lowestrescount):
            lowestrescount = self.mudcount
            lowestres = "mud"
        if (self.stonecount < lowestrescount):
            lowestrescount = self.stonecount
            lowestres = "stone"
        # if (self.grasscount < lowestrescount):
        #    lowestrescount = self.grasscount
        #    lowestres = "grass"
        # if (self.pollencount < lowestrescount):
        #    lowestrescount = self.pollencount
        #    lowestres = "pollen"
        # if (self.watercount < lowestrescount):
        #    lowestrescount = self.watercount
        #    lowestres = "water"
        return lowestres

    # Checked
    def checkhouses(self):
        for y in self.itemcollection:
            if (y['sceneItemType'] == "Structure"):
                if (y['type'] == "House"):
                    for x in self.itemcollection:
                        if (x['sceneItemType'] == "Character"):
                            if((x['tenantOf']) == y['m_id']):
                                maxhunger = x['maxAttributes']['hunger']
                                maxrest = x['maxAttributes']['rest']
                                if (int(x['hunger']) == int(maxhunger)) and (int(x['rest']) == int(maxrest)):
                                    print "Moving fully healthy [" + str(x['profession']) + "#" + str(x['m_id']) + "] out of [house#" + str(y['m_id']) + "]"
                                    self.scene_service.moveItem(
                                        str(x['m_id']), str(6), str(6))

    # Checked
    def checkhospitals(self):
        for y in self.itemcollection:
            if (y['sceneItemType'] == "Structure"):
                if (y['type'] == "Hospital"):
                    for x in self.itemcollection:
                        if (x['sceneItemType'] == "Character"):
                            if((x['tenantOf']) == y['m_id']):
                                maxhunger = x['maxAttributes']['hunger']
                                maxrest = x['maxAttributes']['rest']
                                if (int(x['hunger']) == int(maxhunger)) and (int(x['rest']) == int(maxrest)):
                                    print "Moving fully healthy [" + str(x['profession']) + "#" + str(x['m_id']) + "] out of [hospital#" + str(y['m_id']) + "]"
                                    self.scene_service.moveItem(
                                        str(x['m_id']), str(6), str(6))

    # Checked
    def findemptyhouse(self):
        for y in self.itemcollection:
            if (y['sceneItemType'] == 'Structure'):
                if (y['type'] == 'House'):
                    maxchars = y['characterCapacity']
                    tencount = self.findtenantcount(y['m_id'])
                    if (int(tencount) < int(maxchars)):
                        return y

    # Checked
    def findemptyhospital(self):
        for y in self.itemcollection:
            if (y['sceneItemType'] == 'Structure'):
                if (y['type'] == 'Hospital'):
                    maxchars = y['characterCapacity']
                    tencount = self.findtenantcount(y['m_id'])
                    if (int(tencount) < int(maxchars)):
                        return y

    # Checked
    def findtenantcount(self, searchid):
        counter = 0
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                if((x['tenantOf']) == searchid):
                    counter += 1
        return counter

    # Checked
    def checkhungry(self):
        hosp = False
        print "Checking for tired or hungry P3s"
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Structure"):
                if (x['type'] == "Hospital"):
                    if (x['isBuilt'] is True):
                        hosp = True
                        break
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                if (int(x['tenantOf']) == -1):
                    if (int(x['hunger']) < 50) or (int(x['rest']) < 50):
                        if (int(x['m_id']) > 0):
                            if hosp:
                                currhosp = self.findemptyhospital()
                                if not (currhosp is None):
                                    result = self.scene_service.makeTenant(
                                        (str(x['m_id'])), str(currhosp['m_id']))
                                    if (result is True):
                                        print "Placed [" + str(x['profession']) + "#" + str(x['m_id']) + "] in [hospital#" + str(currhosp['m_id']) + "]"
                                    break
                            else:
                                currhouse = self.findemptyhouse()
                                if not (currhouse == None):
                                    result = self.scene_service.makeTenant(
                                        (str(x['m_id'])), str(currhouse['m_id']))
                                    if (result is True):
                                        print "Placed [" + str(x['profession']) + "#" + str(x['m_id']) + "] in [house#" + str(currhouse['m_id']) + "]"
                                    break

    # Checked
    def setworkercollect(self, cid, lowestres):
        if (self.themapid == '0'):
            if (lowestres == "wood"):
                print "[worker#" + str(cid) + "] is now collecting wood"
                self.scene_service.moveItem(str(cid), "2", "8")
            elif (lowestres == "stone"):
                print "[worker#" + str(cid) + "] is now collecting stone"
                self.scene_service.moveItem(str(cid), "0", "4")
            elif (lowestres == "mud"):
                print "[worker#" + str(cid) + "] is now collecting mud"
                self.scene_service.moveItem(str(cid), "9", "3")
            elif (lowestres == "grass"):
                print "[worker#" + str(cid) + "] is now collecting grass"
                self.scene_service.moveItem(str(cid), "4", "1")
            elif (lowestres == "pollen"):
                print "[worker#" + str(cid) + "] is now collecting pollen"
                self.scene_service.moveItem(str(cid), "2", "1")
            elif (lowestres == "water"):
                print "[worker#" + str(cid) + "] is now collecting water"
                self.scene_service.moveItem(str(cid), "3", "3")
        if (self.themapid == '1'):
            if (lowestres == "wood"):
                print "[worker#" + str(cid) + "] is now collecting wood"
                self.scene_service.moveItem(str(cid), "1", "8")
            elif (lowestres == "stone"):
                print "[worker#" + str(cid) + "] is now collecting stone"
                self.scene_service.moveItem(str(cid), "4", "9")
            elif (lowestres == "mud"):
                print "[worker#" + str(cid) + "] is now collecting mud"
                self.scene_service.moveItem(str(cid), "8", "9")
            elif (lowestres == "grass"):
                print "[worker#" + str(cid) + "] is now collecting grass"
                self.scene_service.moveItem(str(cid), "1", "9")
            elif (lowestres == "pollen"):
                print "[worker#" + str(cid) + "] is now collecting pollen"
                self.scene_service.moveItem(str(cid), "8", "6")
            elif (lowestres == "water"):
                print "[worker#" + str(cid) + "] is now collecting water"
                self.scene_service.moveItem(str(cid), "0", "3")
        if (self.themapid == '2'):
            if (lowestres == "wood"):
                print "[worker#" + str(cid) + "] is now collecting wood"
                self.scene_service.moveItem(str(cid), "5", "9")
            elif (lowestres == "stone"):
                print "[worker#" + str(cid) + "] is now collecting stone"
                self.scene_service.moveItem(str(cid), "0", "5")
            elif (lowestres == "mud"):
                print "[worker#" + str(cid) + "] is now collecting mud"
                self.scene_service.moveItem(str(cid), "9", "3")
            elif (lowestres == "grass"):
                print "[worker#" + str(cid) + "] is now collecting grass"
                self.scene_service.moveItem(str(cid), "3", "7")
            elif (lowestres == "pollen"):
                print "[worker#" + str(cid) + "] is now collecting pollen"
                self.scene_service.moveItem(str(cid), "1", "6")
            elif (lowestres == "water"):
                print "[worker#" + str(cid) + "] is now collecting water"
                self.scene_service.moveItem(str(cid), "3", "4")

    # Checked
    def itemexistat(self, thex, they):
        theret = False
        for x in self.itemcollection:
            if (x['x'] == str(thex)):
                if (x['y'] == str(they)):
                    theret = True
        return theret

    # Checked
    def findemptytilearound(self, thex, they):
        # Find a empty tile next to a certain tile, used for adjacent placement
        # Checks tile to left, to right, above and below could be improved with
        # diagonal but not really needed
        foundone = []
        for x in self.tilecollection:
            searchx = int(thex) - 1
            searchy = int(they)
            if (x['x'] == int(searchx)):
                if (x['y'] == int(searchy)):
                    if (x['walkable'] is True):
                        if self.itemexistat(searchx, searchy) is False:
                            foundone = [searchx, searchy]
                            return foundone
            searchx = int(thex) + 1
            searchy = int(they)
            if (x['x'] == int(searchx)):
                if (x['y'] == int(searchy)):
                    if (x['walkable'] is True):
                        if self.itemexistat(searchx, searchy) is False:
                            foundone = [searchx, searchy]
                            return foundone
            searchx = int(thex)
            searchy = int(they) - 1
            if (x['x'] == int(searchx)):
                if (x['y'] == int(searchy)):
                    if (x['walkable'] is True):
                        if self.itemexistat(searchx, searchy) is False:
                            foundone = [searchx, searchy]
                            return foundone
            searchx = int(thex)
            searchy = int(they) + 1
            if (x['x'] == int(searchx)):
                if (x['y'] == int(searchy)):
                    if (x['walkable'] is True):
                        if self.itemexistat(searchx, searchy) is False:
                            foundone = [searchx, searchy]
                            return foundone
        return foundone

    # Checked - Combine with below
    def getbuildingx(self, buildingid):
        # Get building X coord (should be updated to single function for both
        # coords)
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Structure"):
                if (x['m_id'] == buildingid):
                    return (x['x'])

    # Checked - Combine with above
    def getbuildingy(self, buildingid):
        # Get building Y coord (should be updated to single function for both
        # coords)
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Structure"):
                if (x['m_id'] == buildingid):
                    return (x['y'])

    # Checked - returns an array [#char, #work, #nest, #sold]
    def countpets(self):
        counter = [0, 0, 0, 0]
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                counter[0] += 1
                if (str(x['profession']) == "worker"):
                    counter[1] += 1
                elif (str(x['profession']) == "nester"):
                    counter[2] += 1
                elif (str(x['profession']) == "soldier"):
                    counter[3] += 1
        return counter

    # Checked - Rewritten for minimal CPU usage
    def checkeggs(self):
        self.itembag = self.Inventory_Service.itemBag()
        # self.itemcollection = self.scene_service.sceneItems()
        # print "entered checkeggs()"
        # with open("./itembag.txt", "w") as f:
            # f.write(str(self.itembag))
        # with open("./itemcollection.txt", "w") as g:
            # g.write(str(self.itemcollection))
        # print "done writing"
        eggcount = self.countinveggs()
        print "[tEggs,wEggs,nEggs,sEggs]       " + str(eggcount)
        pets = self.countpets()
        print "[tP3s, tWork,tNest,tSold]       " + str(pets)
        maxpetcount = self.amf_playerinfo['maxPopulation']
        # Discard extra stored eggs from bag
        if (eggcount[3] > 0):
            # Store in soldierID to show id in printmsg
            self.scene_service.moveItem(
                str(self.findinveggprof("Soldier")), "6", "6")
            print "Discarded Soldier Egg from inventory. Goddamn free eggs."
        if (eggcount[1] > 43):
            self.scene_service.moveItem(
                str(self.findinveggprof("Worker")), "6", "6")
            print "Discarded Worker Egg from inventory [MaxStoredWorkers]"
        if (eggcount[2] > 3):
            self.scene_service.moveItem(
                str(self.findinveggprof("Nester")), "6", "6")
            print "Discarded Nester Egg from inventory [MaxStoredNesters]"
        # Check eggs on stage
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Egg") and (not (x['species'] == None)):
                if (x['profession'] == "soldier"):
                    self.scene_service.discardEgg(str(x['m_id']))
                    print "[egg#" + str(x['m_id']) + "] discarded [soldier]"
                if (x['profession'] == "nester"):
                    if (pets[2] < 3) and (pets[0] < maxpetcount):
                        self.scene_service.hatchEgg(str(x['m_id']))
                        print "[egg#" + str(x['m_id']) + "] hatched [" + str(x['profession']) + "]"
                        return 0
                    elif (eggcount[2] >= 3):
                        self.scene_service.discardEgg(str(x['m_id']))
                        print "[egg#" + str(x['m_id']) + "] discarded [maxNesterEgg]"
                        return 0
                    else:
                        self.scene_service.harvestEgg(str(x['m_id']))
                        print "Harvested [egg#" + str(x['m_id']) + "] [nester]"
                        return 0
                if (x['profession'] == "worker"):
                    if (pets[2] >= 3) and (pets[0] < maxpetcount):
                        self.scene_service.hatchEgg(str(x['m_id']))
                        print "[egg#" + str(x['m_id']) + "] hatched [" + str(x['profession']) + "]"
                        return 0
                    elif (eggcount[1] >= 43):
                        self.scene_service.discardEgg(str(x['m_id']))
                        print "[egg#" + str(x['m_id']) + "] discarded [maxWorkerEgg]"
                        return 0
                    else:
                        self.scene_service.harvestEgg(str(x['m_id']))
                        print "Harvested [egg#" + str(x['m_id']) + "] [worker]"
                        return 0
        # Get egg from bag
        if (pets[0] < maxpetcount):
            if (eggcount[2] > 0):
                if (pets[2] < 3):
                    print "Moving nester egg from bag to hatch on next tick"
                    self.scene_service.moveItem(
                        str(self.findinveggprof("Nester")), "6", "6")
            if (eggcount[1] > 0):
                if (pets[2] >= 3):
                    print "Moving worker egg from bag to hatch on next tick"
                    self.scene_service.moveItem(
                        str(self.findinveggprof("Worker")), "6", "6")

    # Checked
    def checknesters(self):
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                if (str(x['profession']) == "nester"):
                    if (int(x['tenantOf'] == -1)):
                        if (int(x['hunger']) > 50) and (int(x['rest']) > 50):
                            nestid = self.findemptynest()
                            if not (nestid == -1):
                                result = self.scene_service.makeTenant(
                                    (str(x['m_id'])), str(nestid))
                                print "Placed inactive [nester#" + str(x['m_id']) + "] in [nest#" + str(nestid) + "]"
                                break

    # Checked - Add check for decay level in addition to health
    def findemptynest(self):
        ret = -1
        for x in self.itemcollection:
            if (x['sceneItemType'] == 'Structure'):
                if (x['type'] == 'Nest'):
                    if (str(x['isBuilt']) == 'True'):
                        if (int(x['health']) > 50):
                            tencount = self.findtenantcount(x['m_id'])
                            if (tencount == 0):
                                ret = x['m_id']
        return ret

    # Checked
    def findnoncompletebuilding(self):
        theret = -1
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Structure"):
                if (x['isBuilt'] is False):
                    theret = x
                    return theret
                    break
        return theret

    # Checked
    def urgentBuy(self):
        if (self.urgentbuy == 15):
            if (self.mudcount > 1200):
                if (self.stonecount > 950):
                    if (self.woodcount > 1200):
                        print "----urgentBuy----"
                        print "Buying Urgently needed house"
                        self.store_service.buyItem(str(self.urgentbuy))
                        print "Bought Urgently needed house"
                        self.urgentbuy = 0
                        return 1
        if (self.urgentbuy == 20):
            if (self.mudcount > 1550):
                if (self.stonecount > 1450):
                    if (self.woodcount > 1850):
                        print "----urgentBuy----"
                        print "Buying Urgently needed storage"
                        self.store_service.buyItem(str(self.urgentbuy))
                        print "Bought Urgently needed storage"
                        self.urgentbuy = 0
                        return 1
        if (self.urgentbuy == 22):
            if (self.mudcount > 950):
                if (self.stonecount > 650):
                    if (self.woodcount > 800):
                        print "----urgentBuy----"
                        print "Buying Urgently needed nest"
                        self.store_service.buyItem(str(self.urgentbuy))
                        print "Bought Urgently needed nest"
                        self.urgentbuy = 0
                        return 1
        if (self.urgentbuy == 41):
            if (self.mudcount > 1800):
                if (self.stonecount > 6750):
                    if (self.woodcount > 2450):
                        print "----urgentBuy----"
                        print "Buying Urgently needed hospital"
                        self.store_service.buyItem(str(self.urgentbuy))
                        print "Bought Urgently needed hospital"
                        self.urgentbuy = 0
                        return 1

    # Checked
    def findnonbusyworker(self):
        theid = -1
        viableworkers = []
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                if (x['profession'] == "worker"):
                    if (x['tenantOf'] == -1):
                        if (x['attachedTo'] == -1):
                            viableworkers.append(x['m_id'])
                            random.shuffle(viableworkers)
                            theid = viableworkers[0]
        return theid

    # Checked
    def findnonbusysoldier(self):
        theid = -1
        viablesoldiers = []
        for x in self.itemcollection:
            if (x['sceneItemType'] == "Character"):
                if (x['profession'] == "soldier"):
                    if (x['tenantOf'] == -1):
                        if (x['attachedTo'] == -1):
                            viablesoldiers.append(x['m_id'])
                            random.shuffle(viablesoldiers)
                            theid = viablesoldiers[0]
        return theid
