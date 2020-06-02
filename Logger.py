from flask import session
import re

import config


class YDL_Logger():
	vidRegex = re.compile("\[ffmpeg\] Destination: " + config.save_dir + "(.*)$")
	downloadProgressRegex = re.compile('\[download\] (.*)$')

	def debug(self, msg):
		# print("DEBUG:")
		# print(msg)
		matches = YDL_Logger.downloadProgressRegex.findall(msg)
		if matches and len(matches) > 0:
			print('TODO: sending progress.....')
		else:
			matches = YDL_Logger.vidRegex.findall(msg)
			if matches and len(matches) > 0:
				session['vid'] = matches[0]

	def warning(self, msg):
		print("WARNING:")
		print(msg)

	def error(self, msg):
		print("ERROR:")
		print(msg)