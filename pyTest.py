#! /usr/bin/env python
import os
'''
Example
'''


def Debug( msg ):
    print( msg)

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

MEGAMAN_SPRITE_COLOR1 = (200,248,192)
MEGAMAN_SPRITE_COLOR = (0,0,0)

D_WIDTH = 800
D_HEIGHT = 600

NUM_ROWS = 3
NUM_COLS = 6

DEBUGGING = 0

class Event:
    """this is a superclass for any events that might be generated by an
    object and sent to the EventManager"""
    def __init__(self):
        self.name = "Generic Event"

class TickEvent(Event):
    def __init__(self):
        self.name = "CPU Tick Event"

class QuitEvent(Event):
    def __init__(self):
        self.name = "Program Quit Event"

class MapBuiltEvent(Event):
    def __init__(self, gameMap):
        self.name = "Map Finished Building Event"
        self.map = gameMap

class GameStartedEvent(Event):
    def __init__(self, game):
        self.name = "Game Started Event"
        self.game = game

class CharactorMoveRequest(Event):
    def __init__(self, direction, idNum):
        self.name = "Charactor Move Request"
        self.direction = direction
        self.idNum = idNum

class CharactorPlaceEvent(Event):
    """this event occurs when a Charactor is *placed* in a sector,
    ie it doesn't move there from an adjacent sector."""
    def __init__(self, charactor):
        self.name = "Charactor Placement Event"
        self.charactor = charactor

class CharactorMoveEvent(Event):
    def __init__(self, charactor):
        self.name = "Charactor Move Event"
        self.charactor = charactor
        

class CharactorAttackRequest(Event):
    def __init__(self, attack):
        self.name = "Charactor Attack Request"
        self.attack = attack

#this is more for GUI, tells the view when to animate the attack
class CharactorAttackEvent(Event):
    def __init__(self, attack, charactor):
        self.name = "Charactor Attack Event"
        self.attack = attack
        self.charactor = charactor

class AttackEvent(Event):
    def __init__(self, attack):
        self.name = "Charactor Attack Event"
        self.attack = attack
        


class HitEvent(Event):
    def __init__(self, attack, charactor):
        self.name = "Hit Event"
        self.charactor = charactor
        self.attack = attack

class ChargingEvent(Event):
    def __init__(self, charactorID):
        self.name = "Charging Event"
        self.charactorID = charactorID

class ChargingReleaseEvent(Event):
    def __init__(self, charactorID):
        self.name = "Charging Event"
        self.charactorID = charactorID

class ActivateChipEvent(Event):
    def __init__(self, charactorID):
        self.name = "Activate Chip Event"
        self.charactorID = charactorID

#------------------------------------------------------------------------------
class EventManager:
    """this object is responsible for coordinating most communication
    between the Model, View, and Controller."""
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
        self.eventQueue= []

    #----------------------------------------------------------------------
    def RegisterListener( self, listener ):
        self.listeners[ listener ] = 1

    #----------------------------------------------------------------------
    def UnregisterListener( self, listener ):
        if listener in self.listeners:
            del self.listeners[ listener ]
        
    #----------------------------------------------------------------------
    def Post( self, event ):
        if not isinstance(event, TickEvent):
            if DEBUGGING:
                Debug( "     Message: " + event.name )
        for listener in self.listeners:
            #NOTE: If the weakref has died, it will be 
            #automatically removed, so we don't have 
            #to worry about it.
            listener.Notify( event )

#------------------------------------------------------------------------------
class KeyboardController:
    """KeyboardController takes Pygame events generated by the
    keyboard and uses them to control the model, by sending Requests
    or to control the Pygame display directly, as with the QuitEvent
    """
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            #Handle Input Events
            for event in pygame.event.get():
                ev = None
                if event.type == QUIT:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                     and event.key == K_ESCAPE:
                    ev = QuitEvent()
                elif event.type == KEYDOWN \
                     and event.key == K_UP:
                    direction = DIRECTION_UP
                    ev = CharactorMoveRequest(direction, 1)
                elif event.type == KEYDOWN \
                     and event.key == K_DOWN:
                    direction = DIRECTION_DOWN
                    ev = CharactorMoveRequest(direction, 1)
                elif event.type == KEYDOWN \
                     and event.key == K_LEFT:
                    direction = DIRECTION_LEFT
                    ev = CharactorMoveRequest(direction, 1)
                elif event.type == KEYDOWN \
                     and event.key == K_RIGHT:
                    direction = DIRECTION_RIGHT
                    ev = CharactorMoveRequest(direction, 1)


                elif event.type == KEYDOWN \
                     and event.key == K_w:
                    direction = DIRECTION_UP
                    ev = CharactorMoveRequest(direction, 2)
                elif event.type == KEYDOWN \
                     and event.key == K_s:
                    direction = DIRECTION_DOWN
                    ev = CharactorMoveRequest(direction, 2)
                elif event.type == KEYDOWN \
                     and event.key == K_a:
                    direction = DIRECTION_LEFT
                    ev = CharactorMoveRequest(direction, 2)
                elif event.type == KEYDOWN \
                     and event.key == K_d:
                    direction = DIRECTION_RIGHT
                    ev = CharactorMoveRequest(direction, 2)

                #basic attack test for player 1
                elif event.type == KEYDOWN \
                     and event.key == K_q:
                    attack = BasicAttack(self.evManager, 1)
                    ev = CharactorAttackRequest(attack)

                elif event.type == KEYDOWN \
                     and event.key == K_e:
                    attack = SwordAttack(self.evManager, 1)
                    ev = CharactorAttackRequest(attack)

                elif event.type == KEYDOWN \
                     and event.key == K_u:
                    ev = ActivateChipEvent(1)

                elif event.type == KEYDOWN \
                     and event.key == K_i:
                    ev = SwapChipEvent(1)

                elif event.type == KEYDOWN \
                     and event.key == K_r:
                    ev = ChargingEvent(1)

                elif event.type == KEYUP \
                     and event.key == K_r:
                    ev = ChargingReleaseEvent(1)
                


                if ev:
                    self.evManager.Post( ev )


#------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.keepGoing = 1

    #----------------------------------------------------------------------
    def Run(self):
        clock = pygame.time.Clock()
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post( event )
            clock.tick(50)

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, QuitEvent ):
            #this will stop the while loop from running
            self.keepGoing = False


import pygame, sys
import random
from pygame.locals import *
import pygame.transform as trans
import spritesheet
from spriteanimation import SpriteStripAnim


#------------------------------------------------------------------------------
class HPSprite(pygame.sprite.Sprite):
    def __init__(self, charactor, group = None):
        pygame.sprite.Sprite.__init__(self, group)

        self.color = None
        self.rect = None
        self.image = None
        self.charactor = charactor
        self.basicfont = pygame.font.SysFont(None, 48)
        if self.charactor.idNum == 1:
            self.color = (255,0,0)
        else:
            self.color = (0,0,255)  
        self.update()
        


    def update(self):
        self.image = self.basicfont.render(str(self.charactor.health), True, self.color)
        self.rect = self.image.get_rect()
        if self.charactor.idNum == 1:
            self.rect.left = 0 
            self.rect.top = 0
        else: 
            self.rect.left = 300 
            self.rect.top = 0

class ChargeSprite(pygame.sprite.Sprite):
    def __init__(self, charactor, group = None):
        pygame.sprite.Sprite.__init__(self, group)
        self.color = None
        self.rect = None
        self.image = None
        self.charactor = charactor
    
        if self.charactor.idNum == 1:
            self.color = (255,0,0)
        else:
            self.color = (0,0,255)  
        self.update()
        


    def update(self):
        self.image = pygame.Surface( (128,20) )
        self.image.fill( (0,255,128) )

        statusBar = pygame.Surface(((128*((self.charactor.charge*1.0)/100)),20))
        statusBar.fill(self.color)
        self.image.blit(statusBar, (0,0))

        self.rect = self.image.get_rect()
        if self.charactor.idNum == 1:
            self.rect.left = 0 
            self.rect.top = 100
        else: 
            self.rect.left = 300 
            self.rect.top = 100



#------------------------------------------------------------------------------
class SectorSprite(pygame.sprite.Sprite):
    def __init__(self, sector, row, col, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        print("Path at terminal when executing this file")
        print(os.getcwd())
        fullname = os.path.join("C:",os.getcwd(),"sprites/panels.png")

        ss = spritesheet.spritesheet(fullname)
        # Sprite is 16x16 pixels at location 0,0 in the file...
        w,h = ss.get_dimensions()
        panel_w = w / NUM_COLS
        panel_h = h / NUM_ROWS
        self.image = ss.image_at((col*panel_w, row*panel_h, panel_w, panel_h))
        #self.image = ss.image_at((col * panel_w, row * panel_h , (col + 1) * panel_w, (row + 1) * panel_h))
        #self.image = pygame.image.load("ball.png")
        # self.image = pygame.Surface( (128,88) )
        # self.image.fill( (0,255,128) )

        self.sector = sector

#------------------------------------------------------------------------------
class CharactorSprite(pygame.sprite.Sprite):
    def __init__(self, charactor, group=None):
        pygame.sprite.Sprite.__init__(self, group)

        self.charactor = charactor
        self.idNum = self.charactor.idNum
        
        #--------------------------------- BLai's spritesheet
        ss = spritesheet.spritesheet('sprites/move.png')
        w,h = ss.get_dimensions()

        """charactorSurf = ss.image_at((0,0,w/4,h), MEGAMAN_SPRITE_COLOR)
        self.moveStrip = SpriteStripAnim('sprites/move.png', (0,0,w/4,h), 4, MEGAMAN_SPRITE_COLOR, True, 2)
        """
        
        atkSS = spritesheet.spritesheet('sprites/basic_attack.png')
        atkW, atkH = atkSS.get_dimensions()
        self.basicAttackStrip = SpriteStripAnim('sprites/basic_attack.png', (0,0,atkW/5,atkH), 5, MEGAMAN_SPRITE_COLOR, True, 2)


        #--------------------------------- CKwong's spritesheet
        
        ### sprite sheets have been rescaled to twice bigger
        
        baseSS = spritesheet.spritesheet('sprites/base_layer.png')
        baseW, baseH = baseSS.get_dimensions()
        
        charactorSurf = baseSS.image_at((0,0,108,108),MEGAMAN_SPRITE_COLOR)
        self.moveStrip = SpriteStripAnim('sprites/base_layer.png',(0,485,372/4,120),4, MEGAMAN_SPRITE_COLOR, True,2)
        
        #self.swordAttackStrip = SpriteStripAnim('sprites/base_layer.png',(0,610,389/4,120),4,MEGAMAN_SPRITE_COLOR,True,2)
        

        # charactorSurf = pygame.Surface( (64,64) )
        # charactorSurf = charactorSurf.convert_alpha()
        # charactorSurf.fill((0,0,0,0)) #make transparent
        # pygame.draw.circle( charactorSurf, (255,0,0), (32,32), 32 )
        self.defImage = charactorSurf #keep track of default image to reset after movement
        self.image = charactorSurf
        self.rect  = self.image.get_rect()


        self.actionFramesLeft = 0
        self.moveTo = None
        self.attack = None

        #---------------------------charging animations

        chargeSS = spritesheet.spritesheet("sprites/AreaGrab.png")

        chargeW, chargeH = chargeSS.get_dimensions()

        chargeRects = []
        chargeWidthSum = 0
        for w in range(4):
            newRect = (chargeWidthSum, 0, 38, 40)
            chargeRects.append(newRect)
            chargeWidthSum += w

        self.chargeImages = chargeSS.images_at(chargeRects, MEGAMAN_SPRITE_COLOR)
        self.chargeIndex = 0


    def updateAttackStrip(self, path, numFrames, width):
        tempSS = spritesheet.spritesheet(path)
        tempW, tempH = tempSS.get_dimensions()
        self.attackStrip = SpriteStripAnim(path,(0, 0,width,tempH),numFrames,MEGAMAN_SPRITE_COLOR,True,2)

    #----------------------------------------------------------------------
    def update(self):
        #movement updates
        changed = False
        if self.moveTo and (self.actionFramesLeft == 0):
            self.image = self.defImage.copy()
            
            self.rect = self.image.get_rect()
            self.rect.center = self.moveTo
            print (self.moveStrip.i)
            self.moveTo = None
            changed = True

        elif self.moveTo:
            self.image = self.moveStrip.next().copy()
            self.actionFramesLeft -= 1
            changed = True


        #attack updates
        elif self.attack and (self.actionFramesLeft == 0):
            self.image = self.defImage.copy()
            print (self.attackStrip.i)
            self.attack = None
            changed = True
        
        elif self.attack:
            #self.image = self.basicAttackStrip.next()
            self.image = self.attackStrip.next().copy()
            self.actionFramesLeft -= 1
            changed = True

        if self.charactor.charging:
            chargingImage = self.chargeImages[self.chargeIndex]
            self.image.blit(chargingImage, self.image.get_rect().center)
            self.chargeIndex = (self.chargeIndex + 1) % len(self.chargeImages)


        #mirror character on right side
        if self.idNum == 2 and changed:
            self.image = trans.flip(self.image, True, False)
                        

#------------------------------------------------------------------------------
class EffectSprite(pygame.sprite.Sprite):
    def __init__(self, pathToSprite, spriteWidths, top, height, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        #ss = spritesheet.spritesheet('sprites/Swords_blade.png')
        ss = spritesheet.spritesheet(pathToSprite)


        w,h = ss.get_dimensions()
        effectSurf = ss.image_at((0,0,59,120),MEGAMAN_SPRITE_COLOR)

        #self.swordEffectStrip = SpriteStripAnim('sprites/Swords_blade.png',(0,0,500/6,120),6,MEGAMAN_SPRITE_COLOR,True,2)
        self.effectStrip = SpriteStripAnim(pathToSprite,(0,0,500/len(spriteWidths),120), len(spriteWidths),MEGAMAN_SPRITE_COLOR,True,2)
        # w1 = 58
        # w2 = 78
        # w3 = 134
        # w4 = 103
        # w5 = 81
        # w6 = 49
        # rects = [(0,0,w1,90),(w1,0,w2,90), (w1+w2,0,w3,90),
        #          (w1+w2+w3,0,w4,90),(w1+w2+w3+w4,0,w5,90),
        #          (w1+w2+w3+w4+w5,0,w6,90)]

        rects = []
        widthSum = 0
        for w in spriteWidths:
            newRect = (widthSum, top, w, height)
            rects.append(newRect)
            widthSum += w

        self.effectStrip.images = ss.images_at(rects, MEGAMAN_SPRITE_COLOR)
        #--------------------------------- CKqqwong's spritesheet
                
        # charactorSurf = pygame.Surface( (64,64) )
        # charactorSurf = charactorSurf.convert_alpha()
        # charactorSurf.fill((0,0,0,0)) #make transparent
        # pygame.draw.circle( charactorSurf, (255,0,0), (32,32), 32 )

        self.defImage = effectSurf #keep track of default image to reset after movement
        self.image = effectSurf
        self.rect  = effectSurf.get_rect()


        self.actionFramesLeft = 0
        self.extras = None #for overlaying sprites on top

    def update(self):
        #attack updates
        if self.extras and (self.actionFramesLeft == 0):
            self.extras = None
            #self.image = self.defImage
            self.kill()
            print "attack update"
            print (self.effectStrip.i)
        elif self.extras:
            self.image = self.effectStrip.next()
            self.actionFramesLeft -= 1


#------------------------------------------------------------------------------
class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        pygame.init()
        self.window = pygame.display.set_mode( (D_WIDTH,D_HEIGHT) )
        pygame.display.set_caption( 'Example Game' )
        self.background = pygame.Surface( self.window.get_size() )
        self.background.fill( (0,0,0) )
        font = pygame.font.Font(None, 30)
        text = """Press SPACE BAR to start"""
        textImg = font.render( text, 1, (255,0,0))
        self.background.blit( textImg, (0,0) )
        self.window.blit( self.background, (0,0) )
        pygame.display.flip()

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()
        self.extraSprites = pygame.sprite.RenderUpdates()

    #----------------------------------------------------------------------
    def ShowMap(self, gameMap):
        # clear the screen first
        self.background.fill( (0,0,0) )
        self.window.blit( self.background, (0,0) )
        pygame.display.flip()

        # use this squareRect as a cursor and go through the
        # columns and rows and assign the rect 
        # positions of the SectorSprites
        squareRect = pygame.Rect( (-128,D_HEIGHT/2, 128,128 ) )

        column = 0
        row = 0
        for sector in gameMap.sectors:
            if column < NUM_COLS:
                squareRect = squareRect.move( 128,0 )
            else:
                column = 0
                row += 1
                squareRect = squareRect.move( -(128*(NUM_COLS-1)), 100)
            newSprite = SectorSprite( sector, row, column,self.backSprites)
            newSprite.rect = squareRect
            column += 1
            newSprite = None


    def ShowCharactorHP(self, charactor):
        hpSprite = HPSprite(charactor, self.frontSprites)
        chargeSprite = ChargeSprite(charactor, self.frontSprites)
    #----------------------------------------------------------------------
    def ShowCharactor(self, charactor):
        sector = charactor.sector
        charactorSprite = CharactorSprite( charactor, self.frontSprites )
        sectorSprite = self.GetSectorSprite( sector )
        charactorSprite.rect.center = sectorSprite.rect.center

    #----------------------------------------------------------------------
    def MoveCharactor(self, charactor):
        charactorSprite = self.GetCharactorSprite( charactor )

        sector = charactor.sector
        sectorSprite = self.GetSectorSprite( sector )

        charactorSprite.actionFramesLeft = 8
        charactorSprite.moveTo = sectorSprite.rect.midtop


    #----------------------
    def PerformAttackCharactor(self, charactor, attack):
        sector = charactor.sector
        
        
        charactorSprite = self.GetCharactorSprite(charactor)

        charactorSprite.attack = attack
        charactorSprite.updateAttackStrip(attack.pathToChSprite, attack.chSpriteFrames, attack.chSpriteWidth)

        charactorSprite.actionFramesLeft = attack.chSpriteFrames*2
        if attack.pathToSprite:
            extraSprite = EffectSprite( attack.pathToSprite, attack.spriteWidths, attack.spriteTop, attack.spriteHeight, self.extraSprites )
            sectorSprite = self.GetSectorSprite( sector )
            extraSprite.rect.center = sectorSprite.rect.midtop
            movingExtra = self.GetExtraSprite( extraSprite )
            movingExtra.extras = 1
            movingExtra.actionFramesLeft = 12

    #----------------------------------------------------------------------
    def GetCharactorSprite(self, charactor):
        for s in self.frontSprites:
            if hasattr(s, "idNum") and s.idNum  == charactor.idNum:
                return s
        return None

    def GetExtraSprite(self, extra):
        print self.extraSprites.sprites()
        for e in self.extraSprites:
            return e
        return None

    #----------------------------------------------------------------------
    def GetSectorSprite(self, sector):
        for s in self.backSprites:
            if hasattr(s, "sector") and s.sector == sector:
                return s


    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            #Draw Everything
            self.backSprites.clear( self.window, self.background )
            self.frontSprites.clear( self.window, self.background )
            self.extraSprites.clear( self.window, self.background )

            self.backSprites.update()
            self.frontSprites.update()
            self.extraSprites.update()

            dirtyRects1 = self.backSprites.draw( self.window )
            dirtyRects2 = self.frontSprites.draw( self.window )
            dirtyRects3 = self.extraSprites.draw(self.window)
            
            dirtyRects = dirtyRects1 + dirtyRects2 + dirtyRects3
            pygame.display.update( dirtyRects )


        elif isinstance( event, MapBuiltEvent ):
            gameMap = event.map
            self.ShowMap( gameMap )

 
        elif isinstance( event, CharactorPlaceEvent ):
            self.ShowCharactor( event.charactor )
            self.ShowCharactorHP(event.charactor)

        elif isinstance( event, CharactorMoveEvent ):
            self.MoveCharactor( event.charactor )

        elif isinstance( event, CharactorAttackEvent ):
            print "hello"
            self.PerformAttackCharactor( event.charactor, event.attack )

#------------------------------------------------------------------------------
class Game:
    """..."""

    STATE_PREPARING = 'preparing'
    STATE_RUNNING = 'running'
    STATE_PAUSED = 'paused'

    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.state = Game.STATE_PREPARING
        
        self.players = [ Player(evManager ,1), Player(evManager, 2) ] 
        self.map = Map( evManager )
        self.activeAttacks = []
    #----------------------------------------------------------------------
    def Start(self):
        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent( self )
        self.evManager.Post( ev )

    def ApplyAttacks(self):
        for att in self.activeAttacks:
            att.tillImpact = att.tillImpact - 1
            if att.tillImpact == 0:
                att.activate()
                
        #after all attacks are activated, remove the activated ones from the list. 
        self.activeAttacks = [att for att in self.activeAttacks if (att.tillImpact > 0)]

    def HandleAttackEvent(self, attack):
        t = attack.type
        sector = attack.sector

        #game determines the hit boxes of each attack, since it also has access to all of the other sectors
        if t == Attack.ROW:
            attack.area = self.map.getRow(sector)
        elif t == Attack.COL:
            attack.area = self.map.getCol(sector)
        
        #otherwise, no hitbox, and the attack wont hit anything (should not happen)

        #keep track of the new attack
        self.activeAttacks.append(attack)

    #----------------------------------------------------------------------qq
    def Notify(self, event):
        if isinstance( event, TickEvent ):
            #start the game if not started
            if self.state == Game.STATE_PREPARING:
                self.Start()
            #if there are active attacks, then their counter should decrememnt each tick until they activate
            self.ApplyAttacks()

        #add any new attacks that were invoked    
        elif isinstance(event, AttackEvent):
            self.HandleAttackEvent(event.attack)
            




#------------------------------------------------------------------------------
class Player(object):
    """..."""
    def __init__(self, evManager, idNum):
        self.evManager = evManager
        self.idNum = idNum
        self.game = None
        self.name = ""
        self.evManager.RegisterListener( self )

        self.charactors = [ Charactor(evManager, idNum) ]

    #----------------------------------------------------------------------
    def __str__(self):
        return '<Player %s %s>' % (self.name, id(self))


    #----------------------------------------------------------------------
    def Notify(self, event):
        pass

#------------------------------------------------------------------------------
class Charactor:
    """..."""

    STATE_INACTIVE = 0
    STATE_ACTIVE = 1

    def __init__(self, evManager, idNum):
        self.idNum = idNum
        self.evManager = evManager
        self.evManager.RegisterListener( self )

        self.sector = None
        self.attack = None
        self.state = Charactor.STATE_INACTIVE
        self.health = 100

        #attributes for charging a normal attack
        self.charging = False
        self.charge = 0

        #TODO: separate move delay and attack delay MAYBE
        self.delay = 0 #this variable accounts for any delay when taking actions = attacking and moving

        self.chips = []
        self.chipFactory = ChipFactory()


    #----------------------------------------------------------------------
    def __str__(self):
        return '<Charactor %s>' % id(self)

    #----------------------------------------------------------------------
    def Move(self, direction):
        if self.state == Charactor.STATE_INACTIVE or self.delay != 0:
            return

        if self.sector.MovePossible( direction ):
            self.delay = 10
            self.sector.ch = None #no longer standing on current sector
            newSector = self.sector.neighbors[direction]
            self.sector = newSector
            self.sector.ch = self
            ev = CharactorMoveEvent( self )
            self.evManager.Post( ev )

    #----------------------------------------------------------------------
    def Place(self, sector):
        self.sector = sector #set new sector
        self.sector.ch = self #set character on the sector
        self.state = Charactor.STATE_ACTIVE

        ev = CharactorPlaceEvent( self )
        self.evManager.Post( ev )

    def PerformAttack(self,attack):
        # make sure character is active and that it isnt performing any action
        if (self.state == Charactor.STATE_INACTIVE) or self.delay != 0:
            return
        self.delay = 20
        self.attack = attack
        attack.invoke(self.sector)
        ev = CharactorAttackEvent(attack, self)
        self.evManager.Post(ev)

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance( event, GameStartedEvent ):
            gameMap = event.game.map
            if self.idNum == 1:
                self.Place( gameMap.sectors[gameMap.startSectorIndex] )
            elif self.idNum == 2:
                self.Place(gameMap.sectors[gameMap.startSectorIndex2])

        elif isinstance( event, CharactorMoveRequest ) and event.idNum == self.idNum:
            self.Move( event.direction )

        elif isinstance( event, CharactorAttackRequest ):
            if event.attack.invokerID == self.idNum:
                self.PerformAttack( event.attack )
        
        #for a normal tick, delay of character actions should decrement        
        elif isinstance(event, TickEvent):
            if (self.delay > 0):
                self.delay -= 1
            if self.charging:
                self.charge += 1
            if len(self.chips) < 3:
                self.chips.append(self.chipFactory.getRandomChip(self.evManager, self.idNum))

        elif isinstance(event, HitEvent):
            if event.charactor.idNum == self.idNum:
                self.health -= event.attack.damage
            #TODO: should cause hit stun if performing an attack

        elif isinstance(event, ChargingEvent):
            if event.charactorID == self.idNum:
                self.charging = True
        
        elif isinstance(event, ChargingReleaseEvent):
            #if matching id, perform corresponding attack
            if event.charactorID == self.idNum and self.charge >= 100:
                self.PerformAttack(ChargedAttack(self.evManager, 1))
            elif event.charactorID == self.idNum:
                self.PerformAttack(BasicAttack(self.evManager, 1))
            #regardless of outcome, charging should be set back to default for charactor
            if event.charactorID == self.idNum:
                self.charge = 0
                self.charging = False

        elif isinstance(event, ActivateChipEvent) and event.charactorID == self.idNum:
            chipToActivate = self.chips.pop(0)
            ev = CharactorAttackRequest(chipToActivate.attack)
            self.evManager.Post(ev)
        


#------------------------------------------------------------------------------
class Map:
    """..."""

    STATE_PREPARING = 0
    STATE_BUILT = 1


    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager
        #self.evManager.RegisterListener( self )

        self.state = Map.STATE_PREPARING

        self.sectors = []
        self.startSectorIndex = 7
        self.startSectorIndex2 = 10

    #----------------------------------------------------------------------
    def Build(self):
        for i in range(18):
            self.sectors.append( Sector(self.evManager, i) )

        #all cells except top row can go up
        for i in xrange(NUM_COLS, 3*NUM_COLS, 1):
            self.sectors[i].neighbors[DIRECTION_UP] = self.sectors[i-NUM_COLS]

        #all cells except bottom row can go down
        for i in xrange(0, 2*NUM_COLS, 1):
            self.sectors[i].neighbors[DIRECTION_DOWN] = self.sectors[i+NUM_COLS]


        # all can go left except leftmost column
        for i in xrange(1, NUM_COLS, 1):
            for j in xrange(0,NUM_ROWS,1):
                k = i + NUM_COLS*j
                self.sectors[k].neighbors[DIRECTION_LEFT] = self.sectors[k-1]    

        for i in xrange(0, NUM_COLS - 1, 1):
            for j in xrange(0,NUM_ROWS,1):
                k = i + NUM_COLS*j
                self.sectors[k].neighbors[DIRECTION_RIGHT] = self.sectors[k+1]   


        self.state = Map.STATE_BUILT

        ev = MapBuiltEvent( self )
        self.evManager.Post( ev )


    def getRow(self,sector):
        row = sector.idNum / NUM_COLS
        rowStart = row * NUM_COLS
        return self.sectors[rowStart : rowStart + NUM_COLS]

    def getCol(self ,sector, offset):
        col = (sector.idNum % NUM_COLS)  + offset
        res = []
        for i in range(col, len(self.sectors), NUM_COLS):
            res.append(self.sectors)
        return res


    def getSectors(self,sectorIDs):
        res = []
        for s in self.sectors:
            if s.idNum in sectorIDs:
                res.append(s)
        return res

#------------------------------------------------------------------------------
class Sector:
    """..."""
    def __init__(self, evManager, idNum):
        self.evManager = evManager
        #self.evManager.RegisterListener( self )
        self.idNum = idNum
        self.ch = None

        self.neighbors = range(4)

        self.neighbors[DIRECTION_UP] = None
        self.neighbors[DIRECTION_DOWN] = None
        self.neighbors[DIRECTION_LEFT] = None
        self.neighbors[DIRECTION_RIGHT] = None

    #----------------------------------------------------------------------
    def MovePossible(self, direction):
        if self.neighbors[direction]:
            return 1


class Chip:
    def __init__(self, attack, thumbnail):
        self.attack = attack
        self.thumbnail = thumbnail #Should be path to thumbnail

class SwordChip(Chip):
    def __init__(self, evManager, invokerID):
        Chip.__init__(self, SwordAttack(evManager, invokerID), None)    



#This is for generating random chips to refill a character's chips. 
# if there is a new type of chip, just add it to the dictionary. 
class ChipFactory:
    def __init__(self):
        return

    def getRandomChip(self,evManager, invokerID):
        constructors = {1 : SwordChip} 
        i = random.randint(1,len(constructors))
        return constructors[i](evManager, invokerID)

#-----------------------------------------------------------------------------
class Attack:

    #Attack type enumeration
    ROW = 1
    COL = 2 
    CELL = 3

    def __init__(   self, 
                    evManager, 
                    invokerID, 
                    damage, 
                    length, 
                    t, 
                    rowOffset, 
                    colOffset,
                    pathToSprite,
                    spriteWidths,
                    spriteTop,
                    spriteHeight,
                    pathToChSprite,
                    chSpriteFrames,
                    chSpriteWidth):
        self.charactor = None # owner of the attack
        self.evManager = evManager
        self.invokerID = invokerID
        self.damage = damage
        self.sector = None

        #sprite information
        self.pathToSprite = pathToSprite
        self.spriteWidths = spriteWidths
        self.spriteTop = spriteTop
        self.spriteHeight = spriteHeight

        self.pathToChSprite = pathToChSprite
        self.chSpriteFrames = chSpriteFrames
        self.chSpriteWidth  = chSpriteWidth

        #offset from current sector where attack should take place
        #e.g. if it applies to column in front of character, column offset should be 1
        self.rowOffset = rowOffset
        self.colOffset = colOffset

        self.tillImpact = length # number of cycles until the 
        self.type = t #row, col, cell
        self.area = [] #hitzzones specified by nunmber, eg if tyoe = row, then 1 hits the first row, will be set when 
        self.active = False
    
    
    def invoke(self,sector):
        self.sector = sector

        self.active = True
        ev = AttackEvent(self)
        self.evManager.Post(ev)

    def activate(self):
        for s in self.area:
            if (s.ch and (s.ch.idNum != self.invokerID)) :
                ev = HitEvent(self, s.ch)
                self.evManager.Post(ev)


#------------------------------------------------------------------------------
#implement other types of attacks here
class BasicAttack(Attack):
    def __init__(self,evManager, invokerID):
        Attack.__init__(self, evManager, invokerID, 1, 10, Attack.ROW, 0, 0, None, 
            [], 0, 0, "sprites/basic_attack_copy.png", 5, 204)

class ChargedAttack(Attack):
    def __init__(self,evManager, invokerID):
        Attack.__init__(self, evManager, invokerID, 10, 10, Attack.ROW, 0, 0, None, 
            [], 0, 0, "sprites/basic_attack.png", 5, 204)


class SwordAttack(Attack):
    def __init__(self,evManager, invokerID):
        Attack.__init__(self, evManager, invokerID, 1, 10, Attack.ROW, 0, 0, None, 
            [], 0, 0, "sprites/sword_sized.png", 7, 100)
        # Attack.__init__(self, evManager, invokerID, 10, 10, Attack.COL, 0, 1, "sprites/Swords_blade.png", 
        #     [58,78,134,103,81,49], 90)   
 




#------------------------------------------------------------------------------
def main():
    """..."""
    evManager = EventManager()

    keybd = KeyboardController( evManager )
    spinner = CPUSpinnerController( evManager )
    pygameView = PygameView( evManager )
    pygameView2 = PygameView( evManager )
    game = Game( evManager )
    
    spinner.Run()

if __name__ == "__main__":
    main()
