from bearlibterminal import terminal
from timeit import default_timer as timer

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

map_translate={'#':9, '.':20, 'g':29, 'p':22, 's':23, 'a':16, 'm':17, 'd':21, 'o':28}

map_width=len(map[0])
map_height=len(map)
map_Xscale=4
map_Yscale=2

tile_floor=20
tile_wall=8

characterbits = [11, 10, 14, 12, 13]
player_x=12
player_y=1

f = open('bl-timing.txt', 'w')


#-----------------------------------------------------------------------------------------------
def render():
    #terminal.clear()
    for y,row in enumerate(map):
        for x,cell in enumerate(row):
            terminal.put(x * map_Xscale, y * map_Yscale,0x1000 + map_translate[cell])

    for cell in characterbits:
        terminal.put(player_x * map_Xscale, player_y * map_Yscale,0x1000+ cell)

    terminal.refresh()    

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
        if terminal.has_input():
            key=terminal.read() 
            if key == terminal.TK_CLOSE or key == terminal.TK_ESCAPE:
                running=False
            if key == terminal.TK_UP:
                move(0,-1)
            if key == terminal.TK_DOWN:
                move(0,1)
            if key == terminal.TK_LEFT:
                move(-1,0)
            if key == terminal.TK_RIGHT:
                move(1,0)
            if key == terminal.TK_SPACE:
                move(0,0)
    
#-----------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('Map dimensions ({},{})'.format(map_width, map_height))
    terminal.open()
    terminal.set('window: title=''Tile Map'', size=120x40;')
    terminal.set('0x1000: Tiles.png, size=32x32, align=top-left, spacing=32x32')
    terminal.composition(terminal.TK_ON)

    main()

    terminal.close()
    f.close()