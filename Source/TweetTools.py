import re

class TweetTools:
	"""Tools for tweets"""

	@staticmethod
	def getHashtags(tweetText):
		"""Extract and return the hashtags in the given tweet text as a list"""

		hashtags = re.findall("\#\w+", tweetText)

		# Remove "#"s and return
		return [hashtag[1:] for hashtag in hashtags]