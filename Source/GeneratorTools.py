class GeneratorTools:
	"""Tools for working with generators"""

	@staticmethod
	def next(generator, amount):
		"""Get up to the next given amount of items from the given generator"""

		# Get next few items and pad with None if not enough items left
		items = [next(generator, None) for _ in range(amount)]

		# Remove None values and return
		return [item for item in items if item is not None]