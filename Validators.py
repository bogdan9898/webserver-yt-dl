from flask_sieve import JsonRequest


class ShareableLink(JsonRequest):
	def rules(self):
		return {
			'url': ['required', 'url']
		}

	def messages(self):
		return {
			'url.required': '<url> is required',
			'url.url': "<url> is not a valid url"
		}