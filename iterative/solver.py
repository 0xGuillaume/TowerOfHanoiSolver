import argparse
import curses
from curses import COLOR_BLACK, wrapper
from time import sleep


MIN_VAL = 3
MAX_VAL = 8
YCOL = 0
MS = 0.5


header = """
 _____                               __   _   _                   _ 
|_   _|                             / _| | | | |                 (_)
  | | _____      _____ _ __    ___ | |_  | |_| | __ _ _ __   ___  _ 
  | |/ _ \ \ /\ / / _ \ '__|  / _ \|  _| |  _  |/ _` | '_ \ / _ \| |
  | | (_) \ V  V /  __/ |    | (_) | |   | | | | (_| | | | | (_) | |
  \_/\___/ \_/\_/ \___|_|     \___/|_|   \_| |_/\__,_|_| |_|\___/|_|

"""


def ascii_drawing(disk_size:int, choice:int) -> str:
    """Draw a disk with ascii chars - ####"""

    disks = args.disks

    # Width du disque impaire
    max_width = disks * 2 - 1 
    disk = disk_size * 2 - 1 

    # Nombre d'espace à rajouter pour centrer le disque
    nb_blanks = max_width - disk
    blanks = ' ' *  int((nb_blanks / 2))

    # Concaténation du disque et des espaces
    if choice == 0:
        if disk_size % 2 == 0:
            draw = f"{blanks}{'#' * disk}{blanks}"
            #draw = CRED + f"{blanks}{'#' * disk}{blanks}" + CEND

        elif disk_size % 2 != 0:
            draw = f"{blanks}{'#' * disk}{blanks}"

    # Concaténation de la tour et des espaces
    elif choice == 1:
        draw = f"{blanks}{'|' * disk}{blanks}"
        #draw = f"{blanks}{CYELLOW + '|' * disk + CEND}{blanks}"

    return draw


def disk_index(tower:int, i:int, towers:int) -> str:
    """Test index out of orange - return ' ' or index"""

    try:
        width = towers[tower][i]
        disk = ascii_drawing(width, 0)
        return disk

    except IndexError:
        width = 1
        stick = ascii_drawing(width, 1)
        return stick


def render_game(stdscr:object, towers:list, move:int) -> str:
    """Print the game in cli"""

    disks = args.disks
    output = header + "\n"
    sleep(MS)

    # Draw the puzzle disks
    for i in reversed(range(disks)):
        line = "\t%s\t%s\t%s" % (
            disk_index(0, i, towers),
            disk_index(1, i, towers),
            disk_index(2, i, towers),
        )
        output += f"\n{line}"

    blanks = disks * 2 - 1

    # Draw towers bottom line
    stick = ' ' * int((blanks - len("|")) / 2)
    platform = ' ' * int((blanks - len("___")) / 2)
    base2 = f"\t{platform}‾‾‾{platform}\t{platform}‾‾‾{platform}\t{platform}‾‾‾{platform}\n"
    moves = f"\n[+] Move played : {move}/{min_movements()}" 
    output += f"\n{base2}\n{moves}"

    # Draw message to exit the game
    nlines = len(output.split("\n"))
    stdscr.addstr(nlines + 2, 0, "[!] Press any key to exit...", curses.color_pair(1))
    stdscr.refresh()

    return output


def range_int_type(arg:str) -> int:
    """Type function for argparse - int within some predefindes bounds"""

    try:
        value = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a integer digit.")

    if value < MIN_VAL or value > MAX_VAL:
        raise argparse.ArgumentTypeError(f"Argument must be < {MAX_VAL} and > {MIN_VAL}")

    return value


def args_parser() -> object:
    """Arguments parser for the Tower of Hanoi setup"""

    parser = argparse.ArgumentParser(description="Tower of Hanoi CLI")

    parser.add_argument("--disks", 
        "-d", 
        help="Setup Tower of Hanoi number of disks.",
        required=True,
        type=range_int_type
    )

    return parser


def min_movements() -> int:
    """Return the minimal movement to end the game"""

    n = args.disks
    minmov = 2 ** n - 1

    return minmov


# ====================================================================


def select_disk(towers:list, disk_moved:int, excludes:list) -> tuple:
    """Choisir un disque"""

    for count, tower in enumerate(towers):

        # Check if tower is not empty
        if not tower:
            continue

        else:
            disk = tower[-1]        

            # Check if disk has been tested
            if disk in excludes:
                continue

            else:
                # Check if picked disk has moved
                if disk != disk_moved:
                    return (count, disk)


def moving_disk(stdscr:object, towers:list, tower:list, disk:tuple, move:int) -> None:
    """Move a disk from a tower to another"""

    tower.append(disk[1])
    towers[disk[0]].pop()
    stdscr.addstr(YCOL, 1, render_game(stdscr, towers, move))
    stdscr.refresh()
    sleep(MS)


def init_game() -> list:
    """Initialiser le jeu"""

    nb_disks = args.disks
    game = [[disk + 1 for disk in reversed(range(nb_disks))], [], []]

    return game


def first_move(towers:list, x:int) -> int:
    """Bouge le premier disque"""

    towers[-x].append(towers[0].pop())
    disk_moved = towers[-x][0]

    return disk_moved


def main(stdscr) -> None:
    """Main job"""

    # Init curses window
    curses.init_pair(1, curses.COLOR_YELLOW, COLOR_BLACK)
    stdscr.clear()

    # Initializing puzzle
    towers = init_game()
    excludes = []
    goal = towers[0] 

    # Move 0 - Is not even
    if len(goal) % 2 != 0:
        disk_moved = first_move(towers, 1)
        x = 0

    # Move 0 - Is even
    elif len(goal) % 2 == 0:
        disk_moved = first_move(towers, 2)
        x = 1

    # First move
    move = 1
    stdscr.addstr(YCOL, 1, render_game(stdscr, towers, move))
    stdscr.refresh()
    sleep(MS)

    # Resolving the puzzle..
    while towers[-1] != goal:

        disk = select_disk(towers, disk_moved, excludes)

        if disk is None:
            break

        # Placer le disque
        for count, tower in enumerate(towers):

            # Pass if tower is the same where the disk was picked
            if count == disk[0]:
                continue

            # If tower is empty - Check if the disk can be placed here
            if not tower:
                if towers.index(tower) + x % 2 != disk[1] % 2:
                    disk_moved = disk[1]
                    excludes.clear()
                    move += 1
                    moving_disk(stdscr, towers, tower, disk, move)

                    break
            
            # If tower is not empty - Check if the tower and disk are not both even
            # & Check if the top disk is smaller than the picked one
            else:
                if disk[1] < tower[-1] and disk[1] % 2 != tower[-1] % 2:
                    disk_moved = disk[1]
                    excludes.clear()
                    move += 1
                    moving_disk(stdscr, towers, tower, disk, move)

                    break

                else:
                    continue

        # If disk cant be placed - Add into excludes disk
        excludes.append(disk[1])
    
    # Exit the game
    stdscr.getch()
    
    
# >>> Main Job
parser = args_parser()
args = parser.parse_args()
wrapper(main)