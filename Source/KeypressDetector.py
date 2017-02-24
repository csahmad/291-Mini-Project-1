# Modified from this code:
# https://code.activestate.com/recipes/134892/
# (ActiveState user Danny Yoo)
# Accessed Feb 20, 2017

# Really reads characters instead of detecting keypresses

import os

_ON_WINDOWS = os.name == "nt"

if _ON_WINDOWS:
    import msvcrt

else:
    import tty, sys, termios

class KeypressDetector:
    """Detect a keypress and return the result"""

    @staticmethod
    def getKey(specialKeys = None):
        """
        Detect a keypress and return the result

        Arguments:
        specialKeys -- keys that are represented by more than one character
            that you would like this method to handle
        """

        if specialKeys is None: specialKeys = ()

        pressed = KeypressDetector._getCharacter()

        # While any special key starts with pressed, but does not equal
        # pressed, read a character
        while KeypressDetector._anyStrictlyStartsWith(specialKeys, pressed):
            pressed += KeypressDetector._getCharacter()

        return pressed

    @staticmethod
    def _anyStrictlyStartsWith(strings, string):
        """
        Return whether any of a collection of strings starts with string, but
        does not equal string
        """

        for s in strings:
            if s.startswith(string) and s != string: return True

        return False

    @staticmethod
    def _getCharacter():
        """Detect an inputted character and return the result"""

        if _ON_WINDOWS: return KeypressDetector._getKeyWindows()
        return KeypressDetector._getKeyUnix()

    @staticmethod
    def _getKeyWindows():
        """Detect a keypress and return the result on Windows"""

        return msvcrt.getch()

    @staticmethod
    def _getKeyUnix():
        """Detect a keypress and return the result on Unix"""

        standardInputDescriptor = sys.stdin.fileno()
        old_attributes = termios.tcgetattr(standardInputDescriptor)

        try:
            tty.setraw(standardInputDescriptor)
            pressed = sys.stdin.read(1)

        finally:
            termios.tcsetattr(standardInputDescriptor, termios.TCSADRAIN,
                old_attributes)

        return pressed

# Interactive test
if __name__ == "__main__":

    specialKeys = ("\x1b[A", "\x1b[B", "\x1b[D", "\x1b[C",
        "\027[A", "\027[B", "\027[D", "\027[C",
        "\x1b\x1b", "\027\027")

    specialKeyNames = {

        "\x1b[A": "[Up]", "\x1b[B": "[Down]",
        "\x1b[D": "[Left]", "\x1b[C": "[Right]",
        "\x1b\x1b": "[Double Escape]",

        "\027[A": "[Up]", "\027[B": "[Down]",
        "\027[D": "[Left]", "\027[C": "[Right]",
        "\027\027": "[Double Escape]"
    }

    print('Press "q" to quit')

    while True:

        pressed = KeypressDetector.getKey(specialKeys)

        if pressed == "q": break

        if pressed in ("\r", "\n"):
            print("You pressed: [Enter]")

        elif pressed in specialKeys:
            print("You pressed:" + specialKeyNames[pressed])

        else:
            print("You pressed:" + pressed)