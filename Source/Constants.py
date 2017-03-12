class Constants:
	"""Constants used in this program"""

	COMMIT_CHANGES = True
	"""Whether to commit changes to the database (or rollback)"""

	USE_CLEAR = True
	"""Set to False to prevent program from clearing terminal"""

	CONNECTION_STRING = "gwynne.cs.ualberta.ca:1521/CRS"
	"""The connection string used to connect to Oracle"""

	SELECTED_STRING = "=> "
	"""
	The string to display to the left of a selected item in the terminal
	interface
	"""

	UNSELECTED_STRING = "   "
	"""
	The string to display to the left of an unselected item in the terminal
	interface
	"""

	ENTER_KEYS = ("\r", "\n", " ")
	"""Keys to interpret as 'enter' in the terminal interface"""

	# \x1b\x1b, \027\027: "Esc" key pressed twice
	EXIT_KEYS = ("\x1b\x1b", "\027\027", "q", "Q", "e", "E")
	"""Keys to interpret as 'exit' in the terminal interface"""

	UP_KEYS = ("\x1b[A", "\027[A", "w", "W")
	"""Keys to interpret as 'up' in the terminal interface"""

	DOWN_KEYS = ("\x1b[B", "\027[B", "s", "S")
	"""Keys to interpret as 'down' in the terminal interface"""

	LEFT_KEYS = ("\x1b[D", "\027[D", "a", "A")
	"""Keys to interpret as 'left' in the terminal interface"""

	RIGHT_KEYS = ("\x1b[C", "\027[C", "d", "D")
	"""Keys to interpret as 'right' in the terminal interface"""

	SPECIAL_KEYS = ENTER_KEYS + EXIT_KEYS + UP_KEYS + DOWN_KEYS + LEFT_KEYS + \
		RIGHT_KEYS
