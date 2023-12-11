import pygame
import numpy as np

# Toggle
clicked = "off"
active = None
activelist = []
endgame = False

# Window setup
MINX, MAXX = 300, 1100
MINY, MAXY = 40, 840
WIDTH, HEIGHT = 1440, 900
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Chess Game")

# Background--------------------------------------------------------
BACKGROUND = pygame.image.load('Assets/elegantBG.jpg')
BGSz = WIDTH, HEIGHT
BG = pygame.transform.scale(BACKGROUND, BGSz)
   
# Board pygame.image.load-------------------------------------------------------
BOARD = pygame.image.load('Assets/board.jpg')
BDSz = (800, 800)
BD = pygame.transform.scale(BOARD, BDSz)
    
# Cursor pygame.image.load------------------------------------------------------
CURSOR = pygame.image.load('Assets/cursor.png')

# Random Variables
turn = 0

# Piece setup
PCWIDTH, PCHEIGHT = 80, 90
xcordslist = [330, 430, 530, 630, 730, 830, 930, 1030]
ycordslist = [45, 145, 245, 345, 445, 545, 645, 745]
deathx = [60, 160, 1200, 1300]
deathy = [150, 225, 300, 375, 450, 525, 600, 675]
blackpiece_locations = []
whitepiece_locations = []

# Dots Setup
DOT_size = 25
DOT_color = (133, 25, 25)
dots_list = []
new_dots_list = []
dotxcords = [370, 470, 570, 670, 770, 870, 970, 1070]
dotycords = [85, 185, 285, 385, 485, 585, 685, 785]

# Piece Class
class pieces():

    def __init__(self, num, cordx, cordy, moves, imag):
        self.normx, self.normy = PCWIDTH, PCHEIGHT
        self.norm = self.normx, self.normy
        self.smallx, self.smally = PCWIDTH * 0.7, PCHEIGHT * 0.7
        self.small = self.smallx, self.smally
        self.posx = xcordslist[cordx]
        self.posy = ycordslist[cordy]
        self.imageload = pygame.image.load(imag)
        self.image = self.imageload
        self.num = num
        self.mouse = pygame.mouse.get_pos()
        self.moves = moves
        self.posxarray = xcordslist.index(self.posx)
        self.posyarray = ycordslist.index(self.posy)
        self.leftmouse = pygame.mouse.get_pressed()[0]
        self.rightmouse = pygame.mouse.get_pressed()[1]
        self.kingcheck = False
        if num < 17:
            self.color = "black"
        elif num > 16:
            self.color = "white"
        self.active = None
        self.clickable = True
        

    def pcblit(self):
        self.mouse = pygame.mouse.get_pos()
        self.leftmouse = pygame.mouse.get_pressed()[0]
        self.rightmouse = pygame.mouse.get_pressed()[1]
        if self.posx + self.normx > self.mouse[0] > self.posx and self.posy + self.normy > self.mouse[1] > self.posy and self.clickable:
            self.sizeUP = self.small
            self.posxUP, self.posyUP = (self.posx + 12.5),(self.posy + 12.5)
        else:
            self.sizeUP = self.norm
            self.posxUP, self.posyUP = self.posx, self.posy
        self.transcale = pygame.transform.scale(self.image, self.sizeUP)
        WIN.blit(self.transcale, (self.posxUP, self.posyUP))
        if turn == 0 or turn == 2:
            self.active = None
    
    def piece_select(self):
        if self.posx + self.normx > self.mouse[0] > self.posx and self.posy + self.normy > self.mouse[1] > self.posy and self.color == "white" and turn == 0:    
            dots_list_result = self.valid_moves()
            self.ACTIVE()
            return dots_list_result
        elif self.posx + self.normx > self.mouse[0] > self.posx and self.posy + self.normy > self.mouse[1] > self.posy and self.color == "black" and turn == 2:    
            dots_list_result = self.valid_moves()
            self.ACTIVE()
            return dots_list_result

    def kingmoves(self):
        stoplist = []
        if self.color == "black":
            stoplist = black_pieces
            # if self.CHECK() == "Check":
                # self.kingcheck = True
            # else:
            #     self.kingcheck = False
        elif self.color == "white":
            stoplist = white_pieces
            # if self.CHECK() == "Check":
                # self.kingcheck = True
            # else:
                # self.kingcheck = False
        new_array = []
        king_array = np.ones((8, 8))
        if -1< self.posyarray-1< 8 and -1< self.posxarray-1 < 8 and (self.posyarray-1, self.posxarray-1) not in stoplist:
            king_array[self.posyarray-1, self.posxarray-1] = 7
        if -1< self.posyarray-1 < 8 and -1< self.posxarray+1 < 8 and (self.posyarray-1, self.posxarray+1) not in stoplist:
            king_array[self.posyarray-1, self.posxarray+1] = 7
        if -1< self.posyarray+1 < 8 and -1< self.posxarray-1 < 8 and (self.posyarray+1, self.posxarray-1) not in stoplist:
            king_array[self.posyarray+1, self.posxarray-1] = 7
        if -1< self.posyarray+1 < 8 and -1< self.posxarray+1 < 8 and (self.posyarray+1, self.posxarray+1) not in stoplist:
            king_array[self.posyarray+1, self.posxarray+1] = 7
        if -1< self.posyarray-1 < 8 and (self.posyarray-1, self.posxarray) not in stoplist:
            king_array[self.posyarray-1,self.posxarray] = 7
        if -1<self.posxarray+1 < 8 and (self.posyarray, self.posxarray+1) not in stoplist:
            king_array[self.posyarray,self.posxarray+1] = 7
        if -1<self.posxarray-1 < 8 and (self.posyarray, self.posxarray-1) not in stoplist:
            king_array[self.posyarray,self.posxarray-1] = 7
        if -1< self.posyarray+1 < 8 and (self.posyarray+1, self.posxarray):
            king_array[self.posyarray+1,self.posxarray] = 7
        king_array[self.posyarray, self.posxarray] = 10
        new_array = np.where(king_array == 7)
        return new_array
    
    def queenmoves(self):
        stoplist = []
        if self.color == "black":
            stoplist = black_pieces
            semilist = white_pieces
        elif self.color == "white":
            stoplist = white_pieces
            semilist = black_pieces
        new_array = []
        queen_array = np.ones((8, 8))
        for i in range(8):
            if -1< self.posyarray-i < 8 and -1< self.posxarray-i < 8 and ((self.posyarray-i,self.posxarray-i)) not in stoplist:
                queen_array[self.posyarray-i, self.posxarray-i] = 7
            if ((self.posyarray-i,self.posxarray-i)) in stoplist and i != 0:
                break
            if ((self.posyarray-i,self.posxarray-i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray-i < 8 and -1< self.posxarray+i < 8 and ((self.posyarray-i,self.posxarray+i)) not in stoplist:
                queen_array[self.posyarray-i, self.posxarray+i] = 7
            if ((self.posyarray-i,self.posxarray+i)) in stoplist and i != 0:
                break
            if ((self.posyarray-i,self.posxarray+i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray+i < 8 and -1< self.posxarray-i < 8 and ((self.posyarray+i,self.posxarray-i)) not in stoplist:
                queen_array[self.posyarray+i, self.posxarray-i] = 7
            if ((self.posyarray+i,self.posxarray-i)) in stoplist and i != 0:
                break
            if ((self.posyarray+i,self.posxarray-i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray+i < 8 and -1< self.posxarray+i < 8 and ((self.posyarray+i,self.posxarray+i)) not in stoplist:
                queen_array[self.posyarray+i, self.posxarray+i] = 7
            if ((self.posyarray+i,self.posxarray+i)) in stoplist and i != 0:
                break
            if ((self.posyarray+i,self.posxarray+i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray-i < 8 and ((self.posyarray-i, self.posxarray)) not in stoplist:
                    queen_array[self.posyarray-i,self.posxarray] = 7
            if ((self.posyarray-i,self.posxarray)) in stoplist and i != 0:
                break
            if ((self.posyarray-i,self.posxarray)) in semilist and i != 0:
                break
        for i in range(8):
            if -1<self.posxarray+i < 8 and ((self.posyarray, self.posxarray+i)) not in stoplist:
                    queen_array[self.posyarray,self.posxarray+i] = 7
            if ((self.posyarray,self.posxarray+i)) in stoplist and i != 0:
                break
            if ((self.posyarray,self.posxarray+i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1<self.posxarray-i < 8 and ((self.posyarray, self.posxarray-i)) not in stoplist:
                    queen_array[self.posyarray,self.posxarray-i] = 7
            if ((self.posyarray,self.posxarray-i)) in stoplist and i != 0:
                break
            if ((self.posyarray,self.posxarray-i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray+i < 8 and ((self.posyarray+i, self.posxarray)) not in stoplist :
                    queen_array[self.posyarray+i,self.posxarray] = 7
            if ((self.posyarray+i,self.posxarray)) in stoplist and i != 0:
                break
            if ((self.posyarray+i,self.posxarray)) in semilist and i != 0:
                break
            queen_array[self.posyarray, self.posxarray] = 8
        new_array = np.where(queen_array == 7)
        return new_array
    
    def bishopmoves(self):
        stoplist = []
        if self.color == "black":
            stoplist = black_pieces
            semilist = white_pieces
        elif self.color == "white":
            stoplist = white_pieces
            semilist = black_pieces
        new_array = []
        bishop_array = np.ones((8, 8))
        for i in range(8):
            if -1< self.posyarray-i < 8 and -1< self.posxarray-i < 8 and ((self.posyarray-i,self.posxarray-i)) not in stoplist:
                bishop_array[self.posyarray-i, self.posxarray-i] = 7
            if ((self.posyarray-i,self.posxarray-i)) in stoplist and i != 0:
                break
            if ((self.posyarray-i,self.posxarray-i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray-i < 8 and -1< self.posxarray+i < 8 and ((self.posyarray-i,self.posxarray+i)) not in stoplist:
                bishop_array[self.posyarray-i, self.posxarray+i] = 7
            if ((self.posyarray-i,self.posxarray+i)) in stoplist and i != 0:
                break
            if ((self.posyarray-i,self.posxarray+i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray+i < 8 and -1< self.posxarray-i < 8 and ((self.posyarray+i,self.posxarray-i)) not in stoplist:
                bishop_array[self.posyarray+i, self.posxarray-i] = 7
            if ((self.posyarray+i,self.posxarray-i)) in stoplist and i != 0:
                break
            if ((self.posyarray+i,self.posxarray-i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray+i < 8 and -1< self.posxarray+i < 8 and ((self.posyarray+i,self.posxarray+i)) not in stoplist:
                bishop_array[self.posyarray+i, self.posxarray+i] = 7
            if ((self.posyarray+i,self.posxarray+i)) in stoplist and i != 0:
                break
            if ((self.posyarray+i,self.posxarray+i)) in semilist and i != 0:
                break
            bishop_array[self.posyarray, self.posxarray] = 3
        new_array = np.where(bishop_array == 7)
        return new_array
    
    def knightmoves(self):
        stoplist = []
        if self.color == "black":
            stoplist = black_pieces
        elif self.color == "white":
            stoplist = white_pieces
        new_array = []
        knight_array = np.ones((8, 8))
        if -1< self.posyarray-2 < 8 and -1<self.posxarray-1 < 8 and ((self.posyarray-2,self.posxarray-1)) not in stoplist:
            knight_array[self.posyarray-2,self.posxarray-1] = 7
        if -1< self.posyarray-2 < 8 and -1<self.posxarray+1 < 8 and ((self.posyarray-2,self.posxarray+1)) not in stoplist:
            knight_array[self.posyarray-2,self.posxarray+1] = 7
        if -1< self.posyarray-1 < 8 and -1<self.posxarray+2 < 8 and ((self.posyarray-1,self.posxarray+2)) not in stoplist:
            knight_array[self.posyarray-1,self.posxarray+2] = 7
        if -1< self.posyarray+1 < 8 and -1<self.posxarray+2 < 8 and ((self.posyarray+1,self.posxarray+2)) not in stoplist:
            knight_array[self.posyarray+1,self.posxarray+2] = 7
        if -1< self.posyarray+2 < 8 and -1<self.posxarray-1 < 8 and ((self.posyarray+2,self.posxarray-1)) not in stoplist:
            knight_array[self.posyarray+2,self.posxarray-1] = 7
        if -1< self.posyarray+2 < 8 and -1<self.posxarray+1 < 8 and ((self.posyarray+2,self.posxarray+1)) not in stoplist:
            knight_array[self.posyarray+2,self.posxarray+1] = 7
        if -1< self.posyarray-1 < 8 and -1<self.posxarray-2 < 8 and ((self.posyarray-1,self.posxarray-2)) not in stoplist:
            knight_array[self.posyarray-1,self.posxarray-2] = 7
        if -1< self.posyarray+1 < 8 and -1<self.posxarray-2 < 8 and ((self.posyarray+1,self.posxarray-2)) not in stoplist:
            knight_array[self.posyarray+1,self.posxarray-2] = 7
        new_array = np.where(knight_array == 7)
        return new_array
    
    def rookmoves(self):
        stoplist = []
        if self.color == "black":
            stoplist = black_pieces
            semilist = white_pieces
        elif self.color == "white":
            stoplist = white_pieces
            semilist = black_pieces
        new_array = []
        rook_array = np.ones((8, 8))
        for i in range(8):
            if -1< self.posyarray-i < 8 and ((self.posyarray-i, self.posxarray)) not in stoplist:
                    rook_array[self.posyarray-i,self.posxarray] = 7
            if ((self.posyarray-i,self.posxarray)) in stoplist and i != 0:
                break
            if ((self.posyarray-i,self.posxarray)) in semilist and i != 0:
                break
        for i in range(8):
            if -1<self.posxarray+i < 8 and ((self.posyarray, self.posxarray+i)) not in stoplist:
                    rook_array[self.posyarray,self.posxarray+i] = 7
            if ((self.posyarray,self.posxarray+i)) in stoplist and i != 0:
                break
            if ((self.posyarray,self.posxarray+i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1<self.posxarray-i < 8 and ((self.posyarray, self.posxarray-i)) not in stoplist:
                    rook_array[self.posyarray,self.posxarray-i] = 7
            if ((self.posyarray,self.posxarray-i)) in stoplist and i != 0:
                break
            if ((self.posyarray,self.posxarray-i)) in semilist and i != 0:
                break
        for i in range(8):
            if -1< self.posyarray+i < 8 and ((self.posyarray+i, self.posxarray)) not in stoplist :
                    rook_array[self.posyarray+i,self.posxarray] = 7
            if ((self.posyarray+i,self.posxarray)) in stoplist and i != 0:
                break
            if ((self.posyarray+i,self.posxarray)) in semilist and i != 0:
                break
            rook_array[self.posyarray,self.posxarray] = 5
        new_array = np.where(rook_array == 7)
        return new_array
    
    def pawnblackmoves(self):
        stoplist = []
        stoplist = black_pieces
        semilist = white_pieces
        new_array = []
        pawnblack_array = np.ones((8, 8))
        if self.posyarray == 7:
            self.moves = "queenmoves"
            self.image = pygame.image.load('Assets/queenB.png')
        if self.moves == "queenmoves":
            return self.queenmoves()
        if ((self.posyarray+1, self.posxarray)) not in stoplist and ((self.posyarray+1, self.posxarray)) not in semilist:
            pawnblack_array[self.posyarray+1, self.posxarray] = 7
            if self.posyarray == 1 and ((self.posyarray+2, self.posxarray)) not in stoplist and ((self.posyarray+2, self.posxarray)) not in semilist:
                pawnblack_array[self.posyarray+2, self.posxarray] = 7
        if ((self.posyarray+1, self.posxarray+1)) not in stoplist and ((self.posyarray+1, self.posxarray+1)) in semilist:
            pawnblack_array[self.posyarray+1, self.posxarray+1] = 7
        if ((self.posyarray+1, self.posxarray-1)) not in stoplist and ((self.posyarray+1, self.posxarray-1)) in semilist:
            pawnblack_array[self.posyarray+1, self.posxarray-1] = 7
        new_array = np.where(pawnblack_array == 7)
        return new_array
        
    def pawnwhitemoves(self):
        stoplist = []
        stoplist = white_pieces
        semilist = black_pieces
        new_array = []
        pawnwhite_array = np.ones((8, 8))
        if self.posyarray == 0:
            self.moves = "queenmoves"
            self.image = pygame.image.load('Assets/queenB.png')
        if self.moves == "queenmoves":
            return self.queenmoves()
        if ((self.posyarray-1, self.posxarray)) not in stoplist and ((self.posyarray-1, self.posxarray)) not in semilist:
            pawnwhite_array[self.posyarray-1, self.posxarray] = 7
            if self.posyarray == 6 and ((self.posyarray-2, self.posxarray)) not in stoplist and ((self.posyarray-2, self.posxarray)) not in semilist:
                pawnwhite_array[self.posyarray-2, self.posxarray] = 7
        if ((self.posyarray-1, self.posxarray+1)) not in stoplist and ((self.posyarray-1, self.posxarray+1)) in semilist:
            pawnwhite_array[self.posyarray-1, self.posxarray+1] = 7
        if ((self.posyarray-1, self.posxarray-1)) not in stoplist and ((self.posyarray-1, self.posxarray-1)) in semilist:
            pawnwhite_array[self.posyarray-1, self.posxarray-1] = 7
        new_array = np.where(pawnwhite_array == 7)
        return new_array

    def location_check(self):
        if self.other_collision_rect() != None and self.clickable and self.color == "white" and (((ycordslist.index(self.other_collision_rect()[1])), (xcordslist.index(self.other_collision_rect()[0])))) not in whitepiece_locations:
            whitepiece_locations.append(((ycordslist.index(self.other_collision_rect()[1])), (xcordslist.index(self.other_collision_rect()[0]))))
        if self.other_collision_rect() != None and self.clickable and self.color == "black" and (((ycordslist.index(self.other_collision_rect()[1])), (xcordslist.index(self.other_collision_rect()[0])))) not in blackpiece_locations:
            blackpiece_locations.append(((ycordslist.index(self.other_collision_rect()[1])), (xcordslist.index(self.other_collision_rect()[0]))))    

    def valid_moves(self):
        if self.clickable:
            dots_list = []
            self.moveslist = []
            new_array = [0, 1]
            if self.moves == "kingmoves":
                new_array = self.kingmoves()
            if self.moves == "queenmoves":
                new_array = self.queenmoves()
            if self.moves == "bishopmoves":
                new_array = self.bishopmoves()
            if self.moves == "knightmoves":
                new_array = self.knightmoves()
            if self.moves == "rookmoves":
                new_array = self.rookmoves()
            if self.moves == "pawnblackmoves":
                new_array = self.pawnblackmoves()
            if self.moves == "pawnwhitemoves":
                new_array = self.pawnwhitemoves()
            if len(new_array) > 0:
                new_arrayx = new_array[1]
                new_arrayy= new_array[0]
            self.moveslistx = []
            self.moveslisty = []
            if type(new_arrayx) == np.ndarray:
                for i in new_arrayx:
                    self.moveslistx.append(dotxcords[i])
                for i in new_arrayy:
                    self.moveslisty.append(dotycords[i])
            for i in range(len(new_array[0])):
                if MINX <= self.moveslistx[i] <= MAXX and MINY <= self.moveslisty[i] <= MAXY:
                    dots_list.append((self.moveslistx[i], self.moveslisty[i]))
            return (dots_list)
    
    def DOTS_DRAW(x, y):
        mouse = pygame.mouse.get_pos()
        if x + DOT_size > mouse[0] > x - DOT_size and y + DOT_size > mouse[1] > y - DOT_size:
            sizeUP = DOT_size * 0.7
        else:
            sizeUP = DOT_size
        pygame.draw.circle(WIN, (DOT_color), (x, y), sizeUP)

    def DOTS_APPEND(x, y):
        dots_list.append((x, y))
    
    def DOTS_CLICK(self, x, y):
        mouse = pygame.mouse.get_pos()
        mouseL = pygame.mouse.get_pressed()[0]
        if x + DOT_size > mouse[0] > x - DOT_size and y + DOT_size > mouse[1] > y - DOT_size and mouseL and self.active == self.num:
            newx = dotxcords.index(x)
            newy = dotycords.index(y)
            self.posx = xcordslist[int(newx)]
            self.posy = ycordslist[int(newy)]
            self.posxarray = xcordslist.index(self.posx)
            self.posyarray = ycordslist.index(self.posy)
            return "Continue"
        
    def ACTIVE(self):
        self.active = self.num
        activelist.append(self.active)
        return activelist
        
    def ARRAYSET(self):
        boardarray = np.ones((8, 8))
        if self.color == "white":
            boardarray[self.posyarray, self.posxarray] = 0
        if self.color == "black":
            boardarray[self.posyarray, self.posxarray] = 2
        return boardarray
    
    def collision_rect(self):
        if self.active == self.num:
            return self.posx, self.posy

    def other_collision_rect(self):
        if self.active != self.num:
            return self.posx, self.posy

    def REMOVE(self):
        if self.moves == "kingmoves":
            return 42
        if self.color == "white":
            if self.num < 25:
                self.posx = deathx[2]
            else:
                self.posx = deathx[3]
            self.posy = deathy[(self.num-17)%8]
            self.posxarray = self.posx
            self.posyarray = self.posy
            self.clickable = False
        if self.color == "black":
            if self.num < 9:
                self.posx = deathx[0]
            else:
                self.posx = deathx[1]
            self.posy = deathy[(self.num-1)%8]
            self.posxarray = self.posx
            self.posyarray = self.posy
            self.clickable = False

    # def CHECKlist(self):
    #     check_check = []
    #     for piece in piece_list:
    #         if self.color == "white":
    #             if piece.moves != "kingmoves" and piece.color == "black":
    #                 if piece.valid_moves() != None and piece.valid_moves() not in check_check:
    #                     check_check.extend((piece.valid_moves()))
    #         if self.color == "black":
    #             if piece.moves != "kingmoves" and piece.color == "white":
    #                 if piece.valid_moves() != None and piece.valid_moves() not in check_check:
    #                     check_check.extend((piece.valid_moves()))
    #     return check_check
        
    # def CHECK(self):
    #     if ((self.posx + 40, self.posy + 40)) in self.CHECKlist():
    #         return "Check"
    #     else:
    #         return "Safe"
    
    # def writeCheck(self):
    #     if self.kingcheck:
    #         winner = pygame.image.load('Assets/check.png')
    #         transcale = pygame.transform.scale(winner, (200, 200))
    #         if self.color == "black":
    #             WIN.blit(transcale, (60, 650))
    #         if self.color == "white":
    #             WIN.blit(transcale, (1200, 650))


def ENDGAME():
    if endgame:
        winner = pygame.image.load('Assets/winner.png')
        transcale = pygame.transform.scale(winner, (600, 600))
        WIN.blit(transcale, (420, 120))
        return True



kb = pieces(1, 4, 0, "kingmoves", ('Assets/kingB.png'))
qb = pieces(2, 3, 0, "queenmoves", ('Assets/queenB.png'))
bbl = pieces(3, 2, 0, "bishopmoves", ('Assets/bishopB.png'))
bbr = pieces(4, 5, 0, "bishopmoves", ('Assets/bishopB.png'))
nbl = pieces(5, 1, 0, "knightmoves", ('Assets/knightB.png'))
nbr = pieces(6, 6, 0, "knightmoves", ('Assets/knightB.png'))
rbl = pieces(7, 0, 0, "rookmoves", ('Assets/rookB.png'))
rbr = pieces(8, 7, 0, "rookmoves", ('Assets/rookB.png'))
pb1 = pieces(9, 0, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb2 = pieces(10, 1, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb3 = pieces(11, 2, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb4 = pieces(12, 3, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb5 = pieces(13, 4, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb6 = pieces(14, 5, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb7 = pieces(15, 6, 1, "pawnblackmoves", ('Assets/pawnB.png'))
pb8 = pieces(16, 7, 1, "pawnblackmoves", ('Assets/pawnB.png'))

kw = pieces(17, 4, 7, "kingmoves", ('Assets/kingW.png'))
qw = pieces(18, 3, 7, "queenmoves", ('Assets/queenW.png'))
bwl = pieces(19, 2, 7, "bishopmoves", ('Assets/bishopW.png'))
bwr = pieces(20, 5, 7, "bishopmoves", ('Assets/bishopW.png'))
nwl = pieces(21, 1, 7, "knightmoves", ('Assets/knightW.png'))
nwr = pieces(22, 6, 7, "knightmoves", ('Assets/knightW.png'))
rwl = pieces(23, 0, 7, "rookmoves", ('Assets/rookW.png'))
rwr = pieces(24, 7, 7, "rookmoves", ('Assets/rookW.png'))
pw1 = pieces(25, 0, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw2 = pieces(26, 1, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw3 = pieces(27, 2, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw4 = pieces(28, 3, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw5 = pieces(29, 4, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw6 = pieces(30, 5, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw7 = pieces(31, 6, 6, "pawnwhitemoves", ('Assets/pawnW.png'))
pw8 = pieces(32, 7, 6, "pawnwhitemoves", ('Assets/pawnW.png'))

piece_list = [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]

def draw_window(mouse):
    WIN.blit(BG, (0, 0))
    WIN.blit(BD, (320, 40))
    
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
run = True
while run:
    turn = turn % 4
    mouse = pygame.mouse.get_pos()
    mouseLR = pygame.mouse.get_pressed()
    clock.tick(FPS)
    draw_window(mouse)

    if clicked == "off":
        dots_list = []
    
    for piece in [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]:
        piece.pcblit()
    
    whitepiece_locations = []
    blackpiece_locations = []
    for piece in [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]:
        piece.location_check()
    white_pieces = whitepiece_locations
    black_pieces = blackpiece_locations
    if clicked == "on" and (turn == 0 or turn == 2):
        for piece in [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]:
            new_dots_list = piece.piece_select()
            if new_dots_list != None:
                for i in range(len(new_dots_list)):
                    pieces.DOTS_APPEND(new_dots_list[i][0], new_dots_list[i][1])
                turn += 1
    if clicked == "on" and (turn == 1 or turn == 3):
        result = "Go"
        for i in range(len(dots_list)):
            pieces.DOTS_DRAW(dots_list[i][0], dots_list[i][1])
            for piece in [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]:
                piece.DOTS_CLICK(dots_list[i][0], dots_list[i][1])
                if piece.DOTS_CLICK(dots_list[i][0], dots_list[i][1]) == "Continue":
                    result = "break"
                    turn += 1
                    clicked = "off"
                    dots_list = []
                    for other_piece in [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]:
                        for piece in [kb, qb, bbl, bbr, nbl, nbr, rbl, rbr, pb1, pb2, pb3, pb4, pb5, pb6, pb7, pb8, kw, qw, bwl, bwr,  nwl, nwr, rwl, rwr, pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8]:
                            if (other_piece.collision_rect()) == (piece.other_collision_rect()) and (other_piece.collision_rect()) != None and (piece.other_collision_rect()) != None:
                                piece.REMOVE()
                                if piece.REMOVE() == 42:
                                    endgame = True
                    break
            if result == "break":
                break
    print(pygame.KEYDOWN)
    if ENDGAME():
        if pygame.K_SPACE == 1:
            run = False
    # kb.writeCheck()
    # kw.writeCheck()
    CSR = pygame.transform.scale(CURSOR, (30, 30))
    WIN.blit(CSR, mouse)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = "on"
            elif event.button == 3:
                clicked = "off"
                if turn == 1:
                    turn = 0
                if turn == 3:
                    turn = 2
    
    pygame.display.flip()
pygame.quit()