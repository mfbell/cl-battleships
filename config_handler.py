"""Configuration file handler.

Writen by Max Bell
This copy is for CLI Battleships (defaults).
"""

__author__ = "Max Bell"
__copyright__ = "Copyright 2017, Max Bell"
__credits__ = ["Max Bell"]
__license__ = "license.txt"
__version__ = "1.2.1"
__maintainer__ = "Max Bell"
__email__ = "you@need.not.known"
__status__ = "Finished"

# File configuration file module, works like ini files.
from configparser import ConfigParser
# String rep of value to value type
from ast import literal_eval


class ConfigHandler():
        """A configuration file handler with defaults.
        
        This copy is for CLI Battleships (defaults).
        """
        
        def __init__(self):
            """All functions must be called when needed."""
            self.set = {}
    
        def __str__(self):
            """Change the class's docstring to change the discription."""
            return self.__doc__ 
            
        def setup(self, path="battleships.ini"):
            """Do setup for battleships.py.
            
            path: Path/name of the file.
                  - Defaults to battleships.ini
                  - If it has not .ini, it will be added.
                  
            Writing the file to self.set is done this long way around because
            If key do not exist they are kept as defaults. 
            Intergated check if they are unknown
            I have not go around to simplifing it after the others.
            The top to probably can be done anyway but have not looked/tested it.
            """
            
            if not path.endswith(".ini"):
                path += ".ini"
            self.defaults_("set")
            # Import the ini as a dict
            imported = self.import_(path)
            for section in imported:
                # sections
                for sub in imported[section]:
                    # keys
                    # Trys to set.
                    try:
                        self.set[section][sub] = imported[section][sub]
                    # If that section is not in defaults:
                    except KeyError:
                        # Setup and set.
                        self.set[section] = {}
                        self.set[section][sub] = imported[section][sub]
                        # Print warning.
                        print("Unknown section, '{0}', in '{1}' was imported.".format(section, path))
                    # See if the key is in defaults.
                    try:
                        if not sub in self.defaults[section]:
                            # Gets to here if section was in defaults but not key.
                            print("Unknown key, '{0}', in '{1}:{2}' was imported.".format(sub, path, section))
                    # Thrown if section is not in defaults, so their must also be no key in it.
                    except KeyError:
                        print("Unknown key, '{0}', in '{1}:{2}' was imported.".format(sub, path, section))
            return self.set
            
            
            
        def import_(self, path="battleships.ini"):
            """Import setting files to be read and returned as a dict.
            
            path: Path/name of the file.
                  - Defaults to battleships.ini
                  - If it has not .ini, it will be added.
            """
            
            # .ini
            if not path.endswith(".ini"):
                path += ".ini"
            # Setup and read.
            config = ConfigParser()
            config.read(path)
            var = {}
            for section in config.sections():
                # sections
                var[section] = {}
                for item in config[section]:
                    # key
                    try:
                        # Change string version of value to its type.
                        var[section][item] = literal_eval(config[section][item])
                    except (ValueError, SyntaxError):
                        # These are the errors I got while handing settings I had.
                        # ValueError covers trying to make a str a str.
                        # SyntaxError covers strings which look like things like operands. 
                        # e.g. ">>>"
                        var[section][item] = config[section][item]
            return var
            
            
        def export(self, path, exports=["settings"], var=None):
            """Export the a dict to a ini file.
            
            path: Path/name of the file.
                  - If it has not .ini, it will be added.
            exports: The keys to export in the dict.
                     - Defaults to "settings".
                     - Use ["*"] for all.
            """
            
            if not var:
                var = self.set
            # Setup write to.
            config = ConfigParser()
            # All sections
            if exports == ["*"]:
                exports = []
                for key in var:
                    exports.append(key)
            for section in exports:
                # sections
                config[section] = var[section]
            # .ini
            if not path.endswith(".ini"):
                path += ".ini"
            # Write to file
            with open(path, "w") as configfile:
                config.write(configfile)
            return None
                
        def defaults_(self, do=None):
            """Default settings
            
            do: Do an action.
                - "set": Sets self.set to self.defaults
                - "return" Returns the dict self.defaults
                
            Any passed through valiables must be passed to the class.
            e.g:
            from config_handler import ConfigHandler
            ConfigHandler.<var> = xyz
            or (not tested)
            import config_handler
            config_handler.ConfigHandler.<var> = xyz
            """
            
            
            self.defaults = {}
            # Menus
            self.defaults["menus"] = {}
            self.defaults["menus"]["default"] = ["No menu set :\\", "Sorry..."]
            self.defaults["menus"]["main"] = ["Battleships v{0}", "<menu placeholder>\n"]
            self.defaults["menus"]["winner"] = [" Player {0} Won!", " Well done", " You get some really bad ascii art :)"]
            self.defaults["menus"]["password"] = ["Player {0}'s password:"]
            self.defaults["menus"]["attack"] = ["Player {0}.", "Enter XY coordinates to attack."]
            self.defaults["menus"]["get-xy"] = ["Place {0}", "Start XY coordinates:", "Change ship: {1}"]
            self.defaults["menus"]["direction"] = ["Direction of ship:", "e.g. n for north", "Change XY: {0}"]
            self.defaults["menus"]["false-clear"] = ["Your system is not giving all the modules I need to me. :(", "Like this I can not function fully. :'("]
            self.defaults["menus"]["set-password"] = ["Set player {0}'s password"]
            self.defaults["menus"]["ship"] = ["Player {0} ship placement", "Select Ship:"]
            self.defaults["menus"]["help"] = ["Help Centre...", "Not much here. In menus type in what you want.", "You got to here fine so...?", "I should probably do this propably at some point and get spelling right too. :\\"]
            self.defaults["menus"]["settings"] = ["Settings menu", "Enter settings to change value of:", "{0} to escape"]
            self.defaults["menus"]["settings-change"] = ["Enter new value:", "{0} to escape"]
            self.defaults["menus"]["settings-list-index"] = ["List index to change", "0 to {0}"]
            # Errors
            self.defaults["errors"] = {}
            self.defaults["errors"]["unknown_cmd"] = "Unknown command... :\\"
            self.defaults["errors"]["xy"] = "Invalid coordinates, try formating as XY."
            self.defaults["errors"]["ship"] = "Ship placed or unavailable :\\"
            self.defaults["errors"]["coords-taken"] = "Coordinate already taken..."
            self.defaults["errors"]["blocked"] = "Blocked by another ship..."
            self.defaults["errors"]["out-of-bounds"] = "Ship goes out of bounds..."
            self.defaults["errors"]["password"] = "Incorrect password. :\\"
            self.defaults["errors"]["auth-off"] = "Auth protection is disabled in settings."
            self.defaults["errors"]["settings"] = "Unknown settings... :\\"
            self.defaults["errors"]["direction"] = "Invalid direction..."
            self.defaults["errors"]["settings-value"] = "Invalid value, try using same value type."
            self.defaults["errors"]["invalid-index"] = "Invalid index."
            # Settings
            self.defaults["settings"] = {}
            self.defaults["settings"]["auth"] = True
            self.defaults["settings"]["escape-key"] = "x"
            self.defaults["settings"]["cmd-limited"] = not self.setup_errors["import-os"] # Passed through by importing module
            self.defaults["settings"]["catch-repeat-shots"] = False
            self.defaults["settings"]["cli_prompt"] = ">>>"
            self.defaults["settings"]["dev"] = False # Dev shortcuts
            self.defaults["settings"]["ships"] = {"carrier": 5,
                                      "battleship": 4,
                                      "cruiser": 3,
                                      "submarine":3,
                                      "destroyer":2}
            self.defaults["settings"]["chars"] = {"open": "O",
                                      "ship": "#",
                                      "hit": "X",
                                      "miss": "Ø"}
            # Some other stuff
            self.defaults["ascii"] = {}
            self.defaults["ascii"]["wd"] = ["               _ _       _", "              | | |     | |", " __      _____| | |   __| | ___  _ __   ___", " \ \ /\ / / _ \ | |  / _` |/ _ \| '_ \ / _ \ ", "  \ V  V /  __/ | | | (_| | (_) | | | |  __/", "   \_/\_/ \___|_|_|  \__,_|\___/|_| |_|\___|"]
            
            # Sets self.set to self.defaults
            if do == "set":
                self.set = self.defaults
                return None
            # Returns self.defaults
            elif do == "return":
                return self.defaults
            else:
                return None
        
        def _test(self, dict=None):
            """Test if all keys and their values in dict are defaults.
            
            dict: A dictionary.
                  - Defaults to self.set
            """
            c = {1: 0, 2: 0}
            valid = []
            self.defaults_()
            if not dict:
                dict = self.set
            for a in dict:
                # sections
                for b in dict[a]:
                    # keys
                    c[1] += 1
                    if self.defaults[a][b] == dict[a][b]:
                        # Yes
                        valid.append(True)
                        c[2] += 1
                    else:
                        # No
                        valid.append(False)
            # Overall
            if c[1] == c[2]:
                x = True
            else:
                x = False
            return x, valid
            
            

            
if __name__ == "__main__":
    print("SettingsHandler, import to use.")