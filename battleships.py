"""CLI Battleships. PvP Local.
Writen by mtech0

Automatically runs on open as main.
If imported:
<var> = (Battleships.)b()
<var>.run()
Will start the game.
"""

__author__ = "mtech0"
__copyright__ = "Copyright 2017, mtech0"
__credits__ = ["mtech0"]
__license__ = "license.txt"
__version__ = "0.7.3"
__maintainer__ = "mtech0"
__email__ = "you@need.not.known"
__status__ = "Development"
_setup_errors = {}

from getpass import getpass                 # Non-echoed inputs
from platform import system as os_name      # OS Name
from ast import literal_eval                # String rep of value to value type
from config_handler import ConfigHandler    # Configuration File Handler

# Try to get command-line access
try:
    from os import system
    _setup_errors["import-os"] = True
except:
    _setup_errors["import-os"] = False
    """I need to get a system to work with the school system.
    I really don't like the method \n as it puts it at the bottom 
    of the screen :'(
    """

    
class Battleships():
    """Contains the CLI version of the game."""
    
    def __init__(self):
        """Setup... thats about it."""
        
        self.auth_ = {}
        # Settings/Menus/Errors
        global _setup_errors
        self.configObj = ConfigHandler()
        self.configObj.setup_errors = _setup_errors
        self.config = self.configObj.setup()
        return None
        
    def __str__(self):
        """Change the class's docstring to change the discription."""
        return self.__doc__
        
    def run(self):
        """The menu loop of the game."""
        
        while True:
            # Main menu handling
            cmd = self.menu(["play", "help", "settings", "exit"], [a.format(__version__) for a in self.config["menus"]["main"]], None, None, None, None)
            if cmd == "play":
                self.play()
            elif cmd == "help":
                self.help()
            elif cmd == "settings":
                print("Entering experimental zone: prone to crash. WIP")
                self.settings_menu()
            elif cmd == "exit":
                exit()
        return None
    
    def play(self):
        """Central control of the game."""
        
        self.stats = {0: {"hits": 0,
                          "misses": 0,
                          "passes": 0,
                          "repeats": 0},
                      1: {"hits": 0,
                          "misses": 0,
                          "passes": 0,
                          "repeats": 0}}
        # Generate the grids
        # grids works like this:
        # Nest inside is 0 and 1, they are respectively player 0 and 
        #  player 1.
        # Inside of both of them is the their x axis which inside of
        #  them have the their y axis.
        # Inside of each [x][y] is "p" which is their personal grid 
        #  and "a" which is is their attack grid.
        self.grids = {}
        self.grids[0] = {}
        self.grids[1] = {}
        for x in range(10):
            self.grids[0][x] = {}
            self.grids[1][x] = {}
            for y in range(10):
                self.grids[0][x][y] = {"p":"O", "a":"O"}
                self.grids[1][x][y] = {"p":"O", "a":"O"}
                
        if not self.config["settings"]["dev"]:
            # If setting: auth is true -> Sets up password.
            self.auth("fs")
        
            # Ship placement
            for p in range(2):
                if self.config["settings"]["auth"]:
                    self.auth("c", [a.format(p) for a in self.config["menus"]["password"]], self.auth_[p])
                ships_left = {}
                for ship in self.config["settings"]["ships"]:
                    ships_left[ship] = self.config["settings"]["ships"][ship]
                while ships_left:
                    called = self.get_ship(p, ships_left)
                    del ships_left[called[2]]
        else:
            self._dev()
            
        # Attack loop
        p = 0
        grid_acceptables = self.grid_accepts()
        change = True
        ship_points_total = 0
        for ship in self.config["settings"]["ships"]:
            ship_points_total += self.config["settings"]["ships"][ship]
        while True:
            # Auth
            if change:
                self.auth("c", [a.format(p) for a in self.config["menus"]["password"]], self.auth_[p])
            change = True
            # Get attack XY
            self.gp(p, ["p","a"])
            xy = self.menu(grid_acceptables, [a.format(p) for a in self.config["menus"]["attack"]], 
                           self.config["errors"]["xy"], False)
            # Skip turn - WHY??? :\
            if xy == "x":
                print("Skipping turn...\n")
                self.stats[p]["passes"] += 1
            # catch-repeat-shots True
            elif ((self.grids[p][int(xy[0])][int(xy[1])]["a"] == self.config["settings"]["chars"]["miss"] or 
                   self.grids[p][int(xy[0])][int(xy[1])]["a"] == self.config["settings"]["chars"]["hit"]) and 
                  self.config["settings"]["catch-repeat-shots"]):
                change = False
                self.stats[p]["repeats"] += 1
                print("Your have already fired here.\nYou have catch-repeat-shots on. Retake.\n")
            # catch-repeat-shots False
            elif (self.grids[p][int(xy[0])][int(xy[1])]["a"] == self.config["settings"]["chars"]["miss"] or 
                   self.grids[p][int(xy[0])][int(xy[1])]["a"] == self.config["settings"]["chars"]["hit"]):
                self.stats[p]["repeats"] += 1
                print("Your have already fired here?? WHY\n")
            # Hit or miss? And apply
            elif self.grids[int(not p)][int(xy[0])][int(xy[1])]["p"] == self.config["settings"]["chars"]["ship"]:
                self.grids[p][int(xy[0])][int(xy[1])]["a"] = self.config["settings"]["chars"]["hit"]
                self.grids[int(not p)][int(xy[0])][int(xy[1])]["p"] = self.config["settings"]["chars"]["hit"]
                self.stats[p]["hits"] += 1
                print("HIT at", xy, "\n")
            elif self.grids[int(not p)][int(xy[0])][int(xy[1])]["p"] == self.config["settings"]["chars"]["open"]:
                self.grids[p][int(xy[0])][int(xy[1])]["a"] = self.config["settings"]["chars"]["miss"]
                self.grids[int(not p)][int(xy[0])][int(xy[1])]["p"] = self.config["settings"]["chars"]["miss"]
                self.stats[p]["misses"] += 1
                print("MISS at", xy, "\n")
                
            # Dev thing
            if self.config["settings"]["dev"]:
                self.stats[p]["hits"] = int(self.menu([str(a) for a in range(20)],["Dev hit menu","player {0} hits change to".format(p)]))
            
            # Won?
            if self.stats[p]["hits"] == ship_points_total:
                break
            # Player change
            elif p and change:
                p = 0
            elif not p and change:
                p = 1
                
        # Winning end for p
        for line in self.config["ascii"]["wd"]:
            print(line)
        self.menu(["*"], [a.format(p) for a in self.config["menus"]["winner"]], preclear=False)
        return None

        
    # Ship placement loop functions
    def get_ship(self, p, ships_left, call=True):
        """Asks the user which ships to configure.
        Also with call true calls the next function in "ship placement loop".
        
        p: Player
        ships_left: A list of ships to chose from.
        call: Calls the next function in the "ship placement loop" if true (defaut).
              - If false it return the ship chosen by the user. 
                Used for when recalling to change value.
        """
        # Select ship
        ships_ = []
        temp_ship_menu = [a.format(p) for a in self.config["menus"]["ship"]]
        for s in ships_left:
            ships_.append(s)
            temp_ship_menu.append(s)
        ship = self.menu(ships_, temp_ship_menu, self.config["errors"]["ship"])
        # Ship placement loop call or not.
        if call:
            called = self.get_xy(p, ships_left, ship)
            return called
        else:
            return ship
                
    def get_xy(self, p, ships_left, ship, call=True):
        """Asks the user for start XY.
        Also with call true calls the next function in "ship placement loop".
        
        p: Player
        ships_left: A list of ships to chose from. 
                    - Not need but for args consistancy and pass though to other calls.
        ship: A string of the name of the ship been configured.
        call: Calls the next function in the "ship placement loop" if true (defaut).
              - If false it return the ship chosen by the user. 
                Used for when recalling to change value.
        """
        grid_acceptables = self.grid_accepts()
        while True:
            self.gp(p,["p"])
            xy = self.menu(grid_acceptables, [a.format(ship, self.config["settings"]["escape-key"]) for a in self.config["menus"]["get-xy"]], 
                           self.config["errors"]["xy"], False)
            # Check for escape-key
            if xy == self.config["settings"]["escape-key"]:
                ship = self.get_ship(p, ships_left, False)
            # Check if free
            elif self.grids[p][int(xy[0])][int(xy[1])]["p"] == self.config["settings"]["chars"]["open"]:
                break
            else:
                print(self.config["errors"]["coords-taken"])
        # Ship placement loop call or not.
        if call:
            called = self.get_ship_direction(p, ships_left, ship, xy)
            return called
        else:
            return xy

    def get_ship_direction(self, p, ships_left, ship, xy, call=True):
        """Asks the user ship direction.
        Also with call true calls the next function in "ship placement loop".
        
        p: Player
        ships_left: A list of ships to chose from. 
                    - Not need but for args consistancy and pass though. Not API facing.
        ship: A string of the name of the ship been configured.
        xy: A string of XY value.
        call: Calls the next function in the "ship placement loop" if true (defaut).
              - If false it return the ship chosen by the user. 
                Used for when recalling to change value.
        """
        while True:
            self.gp(p,["p"])
            direction = self.menu(["x","n","e","s","w"], [a.format(self.config["settings"]["escape-key"]) for a in self.config["menus"]["direction"]],
                                  self.config["error"]["direction"], False)
            # Test to see if spaces are free.
            valid = []
            try:
                # Check for escape-key, Change XY?
                if direction == "x":
                    xy = self.get_xy(p, ships_left, ship, False)
                    valid.append("xy-change")
                # Spaces open?
                elif direction == "n":
                    for space in range(self.config["settings"]["ships"][ship]):
                        if self.grids[p][int(xy[0])][int(xy[1])+space]["p"] == self.config["settings"]["chars"]["open"]:
                            valid.append(True)
                        else:
                            valid.append(False)
                elif direction == "e":
                    for space in range(self.config["settings"]["ships"][ship]):
                        if self.grids[p][int(xy[0])+space][int(xy[1])]["p"] == self.config["settings"]["chars"]["open"]:
                            valid.append(True)
                        else:
                            valid.append(False)
                elif direction == "s":
                    for space in range(self.config["settings"]["ships"][ship]):
                        if self.grids[p][int(xy[0])][int(xy[1])-space]["p"] == self.config["settings"]["chars"]["open"]:
                            valid.append(True)
                        else:
                            valid.append(False)
                elif direction == "w":
                    for space in range(self.config["settings"]["ships"][ship]):
                        if self.grids[p][int(xy[0])-space][int(xy[1])]["p"] == self.config["settings"]["chars"]["open"]:
                            valid.append(True)
                        else:
                            valid.append(False)
                # break?
                if "xy-change" in valid:
                    pass
                elif not False in valid:
                    break
                else:
                    print(self.config["errors"]["blocked"])
            except KeyError:
                print(self.config["errors"]["out-of-bounds"])
        # Ship placement loop - nothing would need to recall this but keep it in for consistancy.
        if call:
            called = self.place_ship(p, ships_left, ship, xy, direction)
            return called
        else:
            return direction

                        
    def place_ship(self, p, ships_left, ship, xy, direction):
        """Place the ship on the player's map.
        This is the end of the ship placement loop and just return 
        the info used to place the ship.
        
        p: Player
        ships_left: A list of ships to chose from. 
                    - Not need but for args consistancy and pass though. Not API facing.
        ship: A string of the name of the ship been configured.
        xy: A string of XY value.
        direction: A string of the direction of the ship from XY.
        call: Calls the next function in the "ship placement loop" if true (defaut).
              - If false it return the ship chosen by the user. 
                Used for when recalling to change value.
        """
        # Place ship
        if direction == "n":
            for space in range(self.config["settings"]["ships"][ship]):
                self.grids[p][int(xy[0])][int(xy[1])+space]["p"] = self.config["settings"]["chars"]["ship"]
        elif direction == "e":
            for space in range(self.config["settings"]["ships"][ship]):
                self.grids[p][int(xy[0])+space][int(xy[1])]["p"] = self.config["settings"]["chars"]["ship"]
        elif direction == "s":
            for space in range(self.config["settings"]["ships"][ship]):
                self.grids[p][int(xy[0])][int(xy[1])-space]["p"] = self.config["settings"]["chars"]["ship"]
        elif direction == "w":
            for space in range(self.config["settings"]["ships"][ship]):
                self.grids[p][int(xy[0])-space][int(xy[1])]["p"] = self.config["settings"]["chars"]["ship"]   
        return p, ships_left, ship, xy, direction
    
    
    # Tools
    def clear(self, lines=100):
        """Clears the screen.
        
        Lines if used if system is not available.
        lines: The amound of lines to clear by.
            - Defaults to 100
        Needs to be rewriten to work on school computers.
        """
        try:
            if self.config["settings"]["cmd-limited"]:
                raise
            elif os_name() == "Windows":
                system("cls")
            elif os_name() == "Linux":
                system("clear")
            else:
                raise
        except:
            # Don't know what error it throughs as I have not been able to test.
            print("\n"*lines)
            for line in self.config["menus"]["false-clear"]:
                print(line)
        return None
    
    def auth(self, flag="c", text=None, var=None, prompt=None, incorrect=None):
        """Handles the collection of authentication tasks.
        
        flag: What to do.
              - Defaults to c.
              - c: compare an input to var.
              - s: return an input
              - fs: Full setup of passwords - preset
        text: A list of line to display when asking to input.
        var: for use with flag c, the value to compare the input too.
              - Defaults to None so if not needed to be given for other flags
        prompt: The prompt when asking for an input.
                - Defaults to self.config["settings"]["cli_prompt"].
        incorrect: The text to print when an invalid command is given.
                   - Defaults to "Incorrect password. :\\"
        """
        
        # Defaults
        if not incorrect:
            incorrect = self.config["errors"]["password"]
        if not prompt:
            prompt = self.config["settings"]["cli_prompt"]
        
        # Compare
        if flag == "c":
            print("\n".join(text) + "\n")
            while True:
                x = getpass(prompt)
                if x == var:
                    break
                else:
                    print(incorrect)
            self.clear()
            return None
        # Set
        elif flag == "s":
            t = "\n".join(text) + "\n" + prompt
            x = getpass(t)
            return x
        # Full setup
        elif flag == "fs":
            if self.config["settings"]["auth"]:
                for p in range(2):
                    self.auth_[p] = self.auth("s", [a.format(p) for a in self.config["menus"]["set-password"]])
                    self.clear()
            else:
                print(self.config["errors"]["auth-off"])
            return None
    
    
    def gp(self, player, grids_, lables=True):
        """Grip formator and printer.
        This prints grids formated correctly
        
        player: Player grid(s) to show - 0 or 1 int.
        grids_: The grid(s) to show - "p", "a" as a list
        lables: XY lables and headers
        """
        
        for grid in grids_:
            if lables:
                if grid == "a":
                    print("    Attacking:\n")
                elif grid == "p":
                    print("    Defending:\n")
            for y in range(9, -1, -1):
                if lables:
                    print(" " + str(y), end="  ")
                for x in range(0, 10):
                    print(self.grids[player][x][y][grid], end=" ")
                print()
            print("\n    0 1 2 3 4 5 6 7 8 9\n")
        return None
            
    def menu(self, acceptables, lines=None, unknown=None,
             preclear=True, prompt=None, postclear=True):
        """A menu CLI genorator.
        
        This function generates a menu with given lines and then only
        accepts inputs that are in acceptables, when it get ones of these it
        returns it.
        
        acceptables: A list of commands to accept must be provided.
                     - All inputs are made lowercase so it is best
                       if commands are too...
        lines: The list of lines to print before asking for an input.
               - Defaults to self.config["menus"]["default"].
        prompt: The prompt when asking for an input.
                - Defaults to self.config["settings"]["cli_prompt"].
        unknown: The text to print when an invalid command is given.
                 - Defaults to self.config["settings"]["_unknown_cmd"].
        preclear: Clear the screen before printing the menu.
                  - Defaults to true.
        postclear: Clear the screen after a succesful command is given.
                   - Defaults to true.
        """
        
        # Defaults
        if not lines:
            lines = self.config["menus"]["default"]
        if not prompt:
            prompt = self.config["settings"]["cli_prompt"]
        if not unknown:
            unknown = self.config["errors"]["unknown_cmd"]
        # Menu generator
        if preclear:
            self.clear()
        for line in lines:
            print(line)
        while True:
            cmd = input(prompt).lower()
            if cmd in acceptables or "*" in acceptables:
                break
            else:
                print(unknown)
        if postclear:
            self.clear()
        return cmd
        
    def grid_accepts(self, escape=True):
        """Returns a list of acceptable grid coords.
        
        escape: If true, self.escape-key will be included. If it is anothing other
                than true, except False, None, 0, that will be included.
        """
        
        grid_acceptables =[]
        if escape:
            grid_acceptables.append(self.config["settings"]["escape-key"])
        for x in range(10):
            for y in range(10):
                grid_acceptables.append(str(x) + str(y))
        return grid_acceptables
    
    # Dev stuffs
    def dev(self):
        """The non public front facing dev mode.
        Constantly changing
        """
        
        self.config["settings"]["dev"] = True
        self.play()
        
    def _dev(self):
        """The second dev function:
        Constantly changing
        """
        
        for p in range(2):
            xy = "00"
            self.auth_[p] = ""
            for ship in self.config["settings"]["ships"]:
                self.place_ship(p, ["DEVVY MODE", "NO NEED"], ship, xy, "n")
                xy = str(int(xy)+10)
                
    # Other menu stuffs
    def help(self):
        """A help menu/message of sorts... idk, need to complete."""
        self.menu(["*"], self.config["menus"]["help"], prompt="Return\n")
        
        
    # Dis failing...
    def settings_menu(self, dict_=None, recalled=False, base_dict="settings"):
        """The settings menu."""
        
        if not dict_:
            dict_ = self.config["settings"]
        keys_show= [a for a in dict_]
        keys = keys_show.append(self.config["settings"]["escape-key"])
        key = self.menu(keys_show, [a.format(self.config["settings"]["escape-key"]) for a in self.config["menus"]["settings"]], keys)
        accept = [None]
        value = ""
        if key == self.config["settings"]["escape-key"]:
            accept = [None]
            action = None
        elif isinstance(dict_[key], bool):
            accept = ["true", "false"]
        elif dict_[key] is None:
            accept = ["true", "false", "none"]
        elif isinstance(dict_[key], str):
            accept = ["*"]
        elif isinstance(dict_[key], int):
            accept = [a for a in range(1000)] # You would need to change this depending on the settings you have.
        elif isinstance(dict_[key], float):
            print("This setting has a float as a value? No setting should have a float...") # Could do it but don't need to.
        elif isinstance(dict_[key], list):
            accept = ["LIST"]
        elif isinstance(dict_[key], dict):
            accept = ["DICT"]
        elif isinstance(dict_[key], tuple):
            print("This setting can not be changed")
            # Yes it can but I am not going to alow it to be nor is there any settings as tuples anyway.
        
        if None in accept:
            pass
        elif accept == ["LIST"]:
            length = len(dict_[key])
            new_dict = {}
            for item in dict_[key]:
                new_dict[dict_[key].index(item)] = item
            value = self.settings_menu(new_dict, True)
            action = "list"
        elif accept == ["DICT"]:
            value = self.settings_menu(dict_[key])
            action = "dict"
        else:
            accept.append(self.config["settings"]["escape-key"])
            value = self.menu(accept, [a.format(self.config["settings"]["escape-key"]) for a in self.config["menus"]["settings-change"]], 
                         self.config["errors"]["settings-value"], False)
            action = "other"
        
        if value == "true":
            value = True
        elif value == "false":
            value = False
        elif value == "none":
            value = None
        
        if recalled:
            return value, key
        elif action == "other":
            try:
                self.config[base_dict][key] = literal_eval(value)
            except (ValueError, SyntaxError):
                self.config[base_dict][key] = value
            return None
        elif action == "list" or action == "dict":
            try:
                self.config[base_dict][key][value[1]] = literal_eval(value[0])
            except (ValueError, SyntaxError):
                self.config[base_dict][key][value[1]] = value[0]
            return None
        
def b():
    """Battleships shortcut :)"""
    return Battleships()

def run():
    """Run the game if you want to this way..."""
    z = Battleships()
    z.run()
    
if __name__ == "__main__":
    run()
