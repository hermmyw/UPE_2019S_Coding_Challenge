import requests, time

url = 'http://ec2-34-212-54-152.us-west-2.compute.amazonaws.com'
token = requests.post(url + '/session', data = {'uid': '704978214'}).json()['token']
oppodir = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}
coord = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}


class Maze():
    def __init__(self, representation):
        self.path = []
        self.representation = representation


def solve_challenge():
    maze_info = get_maze_info()
    print(maze_info['status'])

    if maze_info['status'] == 'FINISHED':
        return True

    elif maze_info['status'] == 'PLAYING':
        print('Level {} of {}'.format(maze_info['levels_completed'] + 1,
                                      maze_info['total_levels']))
        print('Maze size: {}'.format(maze_info['size']))

        rep = create_maze(maze_info['size'])
        The_maze = Maze(rep)

        sizeX, sizeY = maze_info['size']
        dirX, dirY = maze_info['cur_loc']

        if solve_maze(None, The_maze, sizeX, sizeY, dirX, dirY) == True: # solves challenge
            solve_challenge()


# returns whether you can get to the end of the maze from current location
def solve_maze(prev_dir, maze, sizeX, sizeY, x, y):
    location = x, y
    maze.path.append(location)
    maze.representation[y][x] = '0' # o for on the path

    for direction in ['right', 'down', 'up', 'left']:
        dx, dy = coord[direction]
        if (x + dx < 0 or x + dx > sizeX - 1
            or y + dy < 0 or y + dy > sizeY - 1 ):
            continue
        if (maze.representation[y+dy][x+dx] != '1'):
            continue

        r = try_move(direction).json()['result']
        if r == 1: # reach the end
            print('Congratulations! You have reached the end of the maze!')
            return True
        elif r == 0: # successful move
            if solve_maze(direction, maze, sizeX, sizeY, x+dx, y+dy) == True:
                return True
        else: # hit a wall
            maze.representation[y+dy][x+dx] = '0'
            continue


    # none of the directions worked: you can't reach the end from here
    maze.path.remove(location)
    maze.representation[y][x] = '0'
    # backtrack
    try_move(oppodir[prev_dir])
    return False



def create_maze(dimensions):
    cols, rows = dimensions
    return [['1' for x in range(cols)] for y in range(rows)]

def try_move(direction):
    return requests.post(url + '/game?token=' + token, {'action': direction})

def get_maze_info():
    return requests.get(url + '/game?token=' + token).json()

def main():
    solve_challenge()

if __name__ == '__main__':
    main()