import csv
import xlrd


class Reader:

	def __init__(self, reader, file_type):
		if file_type == "csv": self.reader = list(csv.reader(reader))
		else: self.reader = reader
		self.file_type = file_type
		self.idx = 0

	def readline(self):
		# get the next line content based on the file type
		if self.file_type == "csv":
			result = self.reader[self.idx]
			self.idx += 1
			return result
		elif self.file_type == "txt":
			result = self.reader.readline().strip()
			result = result.replace("\"", "")
			result = result.split('|')
			return result
		elif self.file_type == "xls":
			result = self.reader.row_values(self.idx)
			self.idx += 1
			return [str(r) for r in result]


def date_to_int(date, basedate = None, pattern = "&Y-&M-&D &h:&m:&s"):
	# if there basedate is not None, get the time by basedate time and addition second.
	if basedate is not None:
		return (int(basedate[0]) * 372 + int(basedate[1]) * 31 + (int(date) + int(basedate[2]))) * 86400
	
	# get the date divider by the pattern
	date_pattern_split = pattern.split(" ")[0].split("&")
	divider = date_pattern_split[1][1]
	
	# divide the date into year, month and day
	date_split = date.split(divider)
	year, month, day = 0, 0, 0
	for idx in range(len(date_split)):
		# get the date value
		d = date_pattern_split[idx + 1] if idx == 2 else date_pattern_split[idx + 1][0]
		value = float(date_split[idx].split(" ")[0]) if idx == 2 else float(date_split[idx])
		
		# assign the value to the variable
		if d == "Y": year = int(value)
		elif d == "M": month = int(value)
		elif d == "D": day = int(value)
	return (year * 372 + month * 31 + day) * 86400


def timestamp_to_int(timestamp, pattern = "&Y-&M-&D &h:&m:&s"):
	# get the timestamp divider by the pattern
	timestamp_pattern = pattern.split(" ")[1:]
	timestamp_pattern_split = timestamp_pattern[0].split("&")
	divider = timestamp_pattern_split[1][1]

	# adhoc for special situation
	if not isinstance(timestamp, list): timestamp = timestamp.split(" ")
	
	# divide the date into hour, minute, second
	timestamp_split = timestamp[0].split(divider)
	hour, minute, second = 0, 0, 0

	# adhoc for PM meridiem
	if len(timestamp_pattern) > 1 and len(timestamp) > 1 and timestamp_pattern[1] == "meridiem" and timestamp[1] == "PM":
		hour += 12
	for idx in range(len(timestamp_split)):
		# get the timestamp value
		d = timestamp_pattern_split[idx + 1] if idx == 2 else timestamp_pattern_split[idx + 1][0]
		value = float(timestamp_split[idx].split(" ")[0]) if idx == 2 else float(timestamp_split[idx])
		
		# assign the value to the variable
		if d == "h": hour += int(value)
		elif d == "m": minute = int(value)
		elif d == "s": second = int(value)
	return int(hour) * 3600 + int(minute) * 60 + int(second)


def datetime_to_int(datetime, basedate = None, pattern = "&Y-&M-&D &h:&m:&s"):
	# get the datetime by date and timestamp
	datetime_split = datetime.split(" ")
	date, timestamp = datetime_split[0], datetime_split[1:]
	return date_to_int(date, basedate, pattern) + timestamp_to_int(timestamp, pattern)


def int_to_datetime(value):
	# transform int to datetime
	second, value = value % 60, value // 60
	minute, value = value % 60, value // 60
	hour, value = value % 24, value // 24
	day, value = value % 31, value // 31
	month, year = value % 12, value // 12
	return "{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}".format(year, month, day, hour, minute, second)


def int_to_timestamp(value, hour_digit = 2):
	# transform int to datetime, hour digit to ensure the output can be sort correctly
	second, value = value % 60, value // 60
	minute, hour = value % 60, value // 60
	if hour_digit == 1: return "{:0>1d}:{:0>2d}:{:0>2d}".format(hour, minute, second)
	if hour_digit == 2: return "{:0>2d}:{:0>2d}:{:0>2d}".format(hour, minute, second)
	if hour_digit == 3: return "{:0>3d}:{:0>2d}:{:0>2d}".format(hour, minute, second)
	if hour_digit == 4: return "{:0>4d}:{:0>2d}:{:0>2d}".format(hour, minute, second)


def line_count_xls(file_name):
	bok = xlrd.open_workbook(file_name)
	sht = bok.sheets()[0]
	return sht.nrows


def line_count(file_name):
	count = 0
	with open(file_name) as f:
		for count, _ in enumerate(f, 1):
			pass
	return count
