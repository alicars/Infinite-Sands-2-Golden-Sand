import pygame
import SandTestHelper
import SandArrays
import math
import Buttons


#SandMain includes the main loop as well as the GUI control


def main():

    DefaultResolution = (240,180)
    ScaleFactor = 5
    UIAreaHeight = 40

    clock = pygame.time.Clock()
    FPS = 60


    screen = SetupWindow(DefaultResolution, ScaleFactor, UIAreaHeight)
    AllSand = SandArrays.AllSand(DefaultResolution[0], DefaultResolution[1] - UIAreaHeight, screen, ScaleFactor )
    AllButtons = Buttons.AllButtons(screen, AllSand, ScaleFactor, UIAreaHeight, DefaultResolution )

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        if ProcessEvents(screen, AllSand, AllButtons ) == 1:
            running = False
        NonEventUpdates(screen,AllSand)
        pygame.display.flip()
        clock.tick(FPS)




def ProcessEvents(screen, AllSand , AllButtons):
    # event handling, gets all event from the event queue
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            AllButtons.HandleClick(  pygame.mouse.get_pos() )


            # I'm not sure if checking on every mouse down is the most efficient way...
            # Should work for now


        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            return 1



    if ( pygame.mouse.get_pressed()[0]):
        pos = pygame.mouse.get_pos()

        newX = math.floor (pos[0] / AllSand.ScaleFactor)
        newY = math.floor (pos[1] / AllSand.ScaleFactor)
        #scale position here instead of in SandArray (the actual SandArrays don't keep track of scale factor) 

        NewPos = (newX, newY   )
        AllSand.CreateSand(NewPos)



    # only return 1 when its time to close the window
    return 0

def NonEventUpdates(screen, AllSand):
    AllSand.UpdateSand()






class Window:
    MainScreen = pygame.display.set_mode((240,180))
    SandScreen = pygame.Surface((240, 160))
    ScaledResolution = ()
    SandScreenResolution = ()
    ScaleFactor = 0



    def __init__(self, Resolution, ScaleFactor, UIAreaHeight):

        NewResolution = (Resolution[0] * ScaleFactor, Resolution[1] * ScaleFactor )
        SandScreenSize = (NewResolution[0], NewResolution[1] - (UIAreaHeight * ScaleFactor) )
        # we leave a small area at the bottom for ui

        self.ScaledResolution = NewResolution
        self.SandScreenResolution = SandScreenSize
        self.ScaleFactor = ScaleFactor

        self.MainScreen = pygame.display.set_mode( NewResolution  )
        self.SandScreen = pygame.Surface(SandScreenSize)




        bgColor = (0,0,255)
        self.MainScreen.fill( bgColor  ) # temp bg color

        # draw the sand screen onto the mainscreen
        #bgImage = pygame.image.load("smile.png")
        #MainScreen.blit (bgImage ,(10,10 ) ,area=None, special_flags=0)
        self.MainScreen.blit (self.SandScreen, (0,0))



        pygame.display.flip()



    def SetPixelColor(self, position, Color):
        # used by SandArrays to update screen
        # Set PixelColor automatically scales 1 pixel up to n^2 pixels, where n is scale factor
        # Crucially, SetPixelColor requires the already scaled value as input


        minX = math.floor ( position[0]/ self. ScaleFactor ) * self.ScaleFactor
        minY = math.floor (position[1] / self.ScaleFactor) * self.ScaleFactor


        for i in range (self.ScaleFactor):
            for j in range (self.ScaleFactor):
                newPosition = (minX + i, minY + j)
                self.SandScreen.set_at(newPosition, Color )



        self.MainScreen.blit (self.SandScreen, (0,0))

    def DrawRect(self, top, left, wid, height, color ):
        # used by Buttons.py to create
        # top, left are upper left position
        pygame.draw.rect(self.MainScreen,color ,(top,left,wid,height))





def SetupWindow(Resolution, ScaleFactor, UIAreaHeight):
    # initialize the pygame module
    # returns the screeen as Window object
    pygame.init()


    pygame.display.set_caption("Infinite Sands 2: Golden Sand")

    # create a surface on screen that has the size of 240 x 180
    screen = Window(Resolution, ScaleFactor, UIAreaHeight)

    return screen



def DividePos(oldPos, scaleFactor):
    #divides and returns by scale factor
    newX = math.floor ( oldPos[0] / scaleFactor )
    newY = math.floor ( oldPos[1] / scaleFactor )
    newPos = (newX, newY)
    return newPos

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
