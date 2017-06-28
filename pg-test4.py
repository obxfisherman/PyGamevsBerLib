import pygame
import pygame.locals as pg
from timeit import default_timer as timer

K_ESC=27
K_UP=273
K_DOWN=274
K_RIGHT=275
K_LEFT=276
K_SPACE=32

map=['##############################',
'############.......###########',
'#####..#####.#####.#s.......##',
'####....##.....###.#.....a..##',
'###......#.....#.....#......##',
'###............#.........##.##',
'###......#.....#......#####.##',
'####.###########.....g#####.##',
'#.....###########.#####...#.##',
'#.....###.m..........##.#...##',
'#.....###............##...####',
'##.######........#...##...####',
'##d######........#...##...####',
'#...######o###...#...##...####',
'#...##......##...#...##.#.####',
'#.g.##......##.......##...####',
'######......##.......###.#####',
'######p.....############.#####',
'###########..............#####',
'##############################']

map_translate={'#':(1,1), '.':(4,2), 'g':(5,3), 'p':(6,2), 's':(7,2), 'a':(0,2), 'm':(1,2), 'd':(5,2), 'o':(4,3)}

map_width=len(map[0])
map_height=len(map)
map_Xscale=32
map_Yscale=32

tile_floor=20
tile_wall=8

characterbits = [(3,1), (2,1), (4,1), (6,1), (5,1)]
player_x=12
player_y=1


tiles=[]
X=0
Y=1

f = open('pg-timing.txt', 'w')

#-----------------------------------------------------------------------------------------------
def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

#-----------------------------------------------------------------------------------------------
def render():
    screen = pygame.display.get_surface()

    for y,row in enumerate(map):
        for x,cell in enumerate(row):
            l=map_translate[cell]
            screen.blit(tiles[l[X]][l[Y]], (x * map_Xscale, y * map_Yscale))

    for cell in characterbits:
        screen.blit(tiles[cell[X]][cell[Y]], (player_x * map_Xscale, player_y * map_Yscale))

    pygame.display.update()    

#-----------------------------------------------------------------------------------------------
def move(dx=0,dy=0):
    start_time=timer()
    global player_x, player_y
    destination=map[player_y + dy][player_x + dx]
    if destination in ['p','s','g']:
        t=map[player_y + dy][:player_x + dx] + '.' + map[player_y + dy][player_x + dx+1:]
        map[player_y + dy]=t
        print('you pick up an object')
        destination='.'
    if destination in ['.', 'o']:   #bump into empty floor or open door
        player_x+=dx    #move player to location
        player_y+=dy
    if destination=='d':     #bump into an open door
        #change the map from a closed door 'd' to an open door 'o'
        t=map[player_y + dy][:player_x + dx] + 'o' + map[player_y + dy][player_x + dx+1:]
        map[player_y + dy]=t
        print('the door opens')
    if destination in ['a', 'm']:
        print('you bump in a creature')
        print('player ({},{})'.format(player_x+dx, player_y+dy))
    render()
    end_time=timer()
    print('   time {}'.format(end_time - start_time))
    f.write('{}\n'.format(end_time - start_time))


#-----------------------------------------------------------------------------------------------
def main():
    print('player ({},{})'.format(player_x, player_y))
    running=True
    render()
    while running:
        # Process pygame events
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                pressed_key = event.key
                if event.key == K_ESC:
                    running=False
                if event.key == K_UP:
                    move(0,-1)
                if event.key == K_DOWN:
                    move(0,1)
                if event.key == K_LEFT:
                    move(-1,0)
                if event.key == K_RIGHT:
                    move(1,0)
                if event.key == K_SPACE:
                    move(0,0)
    
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('Map dimensions ({},{})'.format(map_width, map_height))
    pygame.init()
    pygame.display.set_mode((map_width*map_Xscale, map_height*map_Yscale))
    
    tiles=load_tile_table('Tiles.png', 32, 32)
    
    main()
    f.close()
