import pygame, os
from pygame import Rect, Surface, event, image, sprite, font, draw, Color, math
from random import randint

#consts
ALL_LADDERS_ARE_SNAKES = True
NUM_PLAYERS = 20
AUTOADVANCE = False         # if this is False you have to press spacebar to advance
AUTODELAY_MS = 5          # unexpected behaviour if delay is too low
MOVE_SPEED_FRAMES_PER_TILE = 100
FPS=120



pygame.init()
pygame.font.init()
PLAYER_COLORS = [(255,255,255), (0,255,255), (255,0,255), (255,255,0), (255,0,0), (0,0,255), (0,255,0), (0,0,0)]

class Tile(sprite.Sprite):
    font = font.SysFont("Arial", size=16)
    player_colors = ((255,0,0), (0,255,0), (0,0,255))
    def __init__(self, rect:pygame.Rect, index, jmp_to:int, *groups:sprite.Group) -> None:
        self.rect = rect
        self.image = pygame.surface.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        self.ind = index
        draw.rect(self.image, (255,0,0), (0,0,self.rect.w-1, self.rect.h-1), 2)
        txt = self.font.render(str(index), 1, (0,0,0))
        self.image.blit(txt, (rect.w-txt.get_width(),rect.h-txt.get_height()))
        self.center = math.Vector2(rect.center)
        self.jump_to = jmp_to
        super().__init__(*groups)


            

class Player(sprite.Sprite):
    font = font.SysFont("Arial", size=16)
    def __init__(self, tileSize:tuple[float,float], ind:int, *groups) -> None:
        self.index = ind
        self.rect = Rect(0,0,tileSize[0],tileSize[1])
        self.center = pygame.Vector2(self.rect.center)
        self.image = Surface((tileSize[0],tileSize[1]), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(self.image, PLAYER_COLORS[ind%len(PLAYER_COLORS)], self.rect.center, self.rect.width//3)
        txt = self.font.render(str(ind), 1, (0,0,0))
        self.image.blit(txt, (self.rect.w/2-txt.get_width()/2,self.rect.h/2-txt.get_height()/2))
        self.target_tile = self.current_tile = 1
        self.speed = tileSize[0] * MOVE_SPEED_FRAMES_PER_TILE/100
        self.turn = 0
        super().__init__(*groups)

    def update(self, tiles:list[Tile], *args, **kwargs) -> None:
        
        if self.center !=  tiles[self.target_tile].center:
            ct = tiles[self.current_tile]
            if self.center == ct.center and self.current_tile <= self.target_tile:
                self.current_tile +=1
                ct = tiles[self.current_tile]
            new_pos = self.center.move_towards(ct.center, self.speed)
            
            if new_pos.distance_to(ct.center)<self.speed and self.current_tile == self.target_tile:
                if ALL_LADDERS_ARE_SNAKES:
                    jumpto_this = [tile.ind for tile in tiles if tile.jump_to == self.target_tile and tile.ind < tile.jump_to ]
                    if jumpto_this:
                        ct = tiles[jumpto_this[0]]
                    else:
                        ct = tiles[min(ct.jump_to, ct.ind)]
                else:
                    ct= tiles[ct.jump_to]

                # new_pos = ct.center
                
                
                self.current_tile = self.target_tile = ct.ind
            self.update_pos(new_pos)
            
        return super().update(*args, **kwargs)
    
    def update_pos(self, pos:math.Vector2):
        self.center = pos
        self.rect.center = int(self.center.x), int(self.center.y)

def init_tiles(resolution, *groups):
    tiles_jmp_to={2:38, 7:14, 8:31, 15:26, 16:6, 21:42, 28:84, 36:44, 46:25, 49:11, 51:67, 62:19, 64:60, 71:91, 74:53, 78:98, 87:94, 92:88, 95:75, 99:80 }
    num_tiles = 10
    borderwidth = 3
    w, h = (resolution[0]- (2*borderwidth)) / num_tiles, (resolution[1]- (2*borderwidth)) / num_tiles
    num = 1
    Tile(pygame.Rect(0,0,0,0), 0, 0, *groups) # dummy tile so that indexes are same as tile number
    for j in range(num_tiles):
        row = 9-j
        for i in range(num_tiles):
            
            col = i if row%2==1 else 9-i
            rect = pygame.Rect((w*col)+borderwidth, (h*row)+borderwidth, w, h)
            Tile(rect, num, tiles_jmp_to.get(num, num), *groups)
            num +=1

    return w+borderwidth, h+borderwidth



    
def update_player(turn, players:list[Player], tiles:list[Tile]):
    roll = 6
    while roll == 6:
        player = players[turn%NUM_PLAYERS]
        if player.target_tile<len(tiles)-1:
            roll = randint(1, 6)
            print(f"player {player.index} rolled {roll}")
            player.target_tile = min(player.target_tile+ roll, len(tiles)-1)
            player.turn +=1
            # print(f"rolled a {roll}; Player {player.index} to {player.target_tile}")

            if player.target_tile == len(tiles)-1:
                return True
        
def handle_events(players_list, tiles_list, current_players):
    global turn
    playing = True
    for e in event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            playing = False

        elif (e.type == NEXT_TURN and AUTOADVANCE) or (e.type==pygame.KEYDOWN and e.key == pygame.K_SPACE):
            turn += 1
            won = update_player(turn, players_list, tiles_list)
            
            if won:
                print(f"Player {turn%NUM_PLAYERS} won in {(turn//NUM_PLAYERS) + 1} turns")
                current_players -=1
                print(f"{current_players} Players remaining")
                if current_players <= 0:
                    pygame.quit()
                    playing = False
            
    return current_players, playing

NEXT_TURN = pygame.USEREVENT + 1

def main():
    global turn
    
    playing = True
    board_image = image.load("assets/S&N_Board.jpg")
    resolution = width, height = board_image.get_rect().size
    clock = pygame.time.Clock()
    tiles = sprite.Group()
    players = sprite.Group()
    all_sprites = sprite.Group()
    current_players = NUM_PLAYERS
    
    background = pygame.display.set_mode(resolution) 
    tileSize = init_tiles(resolution, tiles, all_sprites)
    win_times = []
    players_list = [Player(tileSize, i, players, all_sprites) for i in range(NUM_PLAYERS)]
    
    tiles_list = tiles.sprites()

    for player in players:
        player.update_pos(tiles_list[1].center)

    turn = 0
    if AUTOADVANCE:
        pygame.time.set_timer(NEXT_TURN, millis=AUTODELAY_MS)


    while playing:

        current_players, playing = handle_events(players_list, tiles_list, current_players)
        if not playing:
            continue
        background.blit(board_image, (0,0))

        
        # tiles.update(background)
        # tiles.draw(background)
        
        players.update(tiles_list)
        players.draw(background)


        pygame.display.flip()
        clock.tick(FPS)
        
        

def test1(r:int):
    roll = 6
    while roll == 6:
        roll = r+1%6

def test2(r: int):
    roll = randint(1, 6)
    
    None if roll!=6 else test2(r+1%6)

def test3(r: int):
    roll = r

    test2(r+1%6) if roll == 6 else None

if __name__ == '__main__':
    # main()
    import timeit

    t1 = [timeit.Timer(lambda: test1(i)).timeit() for i in range(1,6)]
    print("while:",round(sum(t1)/6,3))
    print(t1)

    t2 = [timeit.Timer(lambda: test2(i)).timeit() for i in range(1, 6)]
    print("if not 6:",round(sum(t2)/6, 3))
    print(t2)

    t3 = [timeit.Timer(lambda: test3(i)).timeit() for i in range(1, 6)]
    print("if 6:", round(sum(t3)/6, 3))
    print(t3)