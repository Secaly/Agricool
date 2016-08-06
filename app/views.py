from app import app
from flask import Flask, Markup, render_template
from datetime import datetime
import csv

@app.route('/')
def index():

	"""
	Humidity Data
	"""

	# Open the data and set it into list
	fd_humidity = open('ressources/humidity.csv', 'r')
	reader_humidity = csv.reader(fd_humidity)
	data_humidity = list(reader_humidity)

	# Remove the first useless line of the csv
	data_humidity.remove(data_humidity[0])

	# Set variales
	date_humidity = []
	humidity = []

	# For each key : value in data list
	# set each key into date_humidity and each value into humidity
	for value in data_humidity:
		date_humidity.append(value[0])
		humidity.append(float(value[1]))


	"""
	Temperature Data
	"""

	# Open the data and set it into list
	fd_temperature = open('ressources/temperature.csv', 'r')
	reader_temperature = csv.reader(fd_temperature)
	data_temperature = list(reader_temperature)

	# Remove the first useless line of the csv
	data_temperature.remove(data_temperature[0])

	# Set variales
	date_temperature = []
	temperature = []

	# For each key : value in data list
	# set each key into date_temperature and each value into temperature
	for value in data_temperature:
		date_temperature.append(value[0])
		temperature.append(float(value[1]))


	"""
	Sporulation Oidium Data
	"""

	# Set variables
	i = 0
	sporulation_oidium = []
	last_time = datetime.strptime(date_humidity[0], '%d/%m/%Y %H:%M:%S')

	# For each data
	for date in date_humidity:

		# Set the actual time of the data
		new_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')

		# Set the last time that the conditions were filled
		if humidity[i] < 90:
			last_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')

		# Calculate the difference beetween now and the last time that the
		# conditions were filled
		time_difference = new_time - last_time
		time_difference_in_minutes = time_difference.total_seconds() / 60

		# if the time difference is superior than 60, set the value to 1
		if time_difference_in_minutes > 60:
			sporulation_oidium_is = True
			sporulation_oidium.append(1)

		# else if the conditions are met nevertheless, set the value to 0.5
		elif humidity[i] > 90:
			sporulation_oidium.append(0.5)

		# else the conditions aren't met, set the value to 0
		else:
			sporulation_oidium.append(0)

		# increment
		i = i + 1


	"""
	Botrytis
	"""

	# Set variables
	i = 0
	botrytis = []
	last_time = datetime.strptime(date_humidity[0], '%d/%m/%Y %H:%M:%S')

	# For each data
	for date in date_humidity:

		# Set the actual time of the data
		new_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')

		# Set the last time that the conditions were filled
		if humidity[i] < 90 or \
			temperature[i] <= 15 or \
			temperature[i] >= 20:
			last_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')

		# Calculate the difference beetween now and the last time that the
		# conditions were filled
		time_difference = new_time - last_time
		time_difference_in_minutes = time_difference.total_seconds() / 60

		# if the time difference is superior than 360, set the value to 1
		if time_difference_in_minutes > 360:
			botrytis.append(1)

		# else if the conditions are met nevertheless, set the value to 0.5
		elif humidity[i] > 90 and temperature[i] > 15 and temperature[i] < 20:
			botrytis.append(0.5)

		# else the conditions aren't met, set the value to 0
		else:
			botrytis.append(0)

		# increment
		i = i + 1


	"""
	Developpment Oidium Data
	"""

	# Set variables
	i = 0
	developpment_oidium = []
	sporulation_oidium_is = False
	last_time = datetime.strptime(date_humidity[0], '%d/%m/%Y %H:%M:%S')

	# For each data
	for date in date_humidity:

		# Check if the sporulation has happened
		if sporulation_oidium[i] == 1:
			sporulation_oidium_is = True

		# Set the actual time of the data
		new_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')

		# Set the last time that the conditions were filled
		if sporulation_oidium_is == False or \
			temperature[i] <= 20 or \
			humidity[i] >= 70:
			last_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')

		# Calculate the difference beetween now and the last time that the
		# conditions were filled
		time_difference = new_time - last_time
		time_difference_in_minutes = time_difference.total_seconds() / 60

		# if the time difference is superior than 600, set the value to 1
		if time_difference_in_minutes > 600:
			developpment_oidium.append(1)

		# else if the conditions are met nevertheless, set the value to 0.5
		elif sporulation_oidium_is == True and \
			temperature[i] > 20 and \
			humidity[i] < 70:
			developpment_oidium.append(0.5)

		# else the conditions aren't met, set the value to 0
		else:
			developpment_oidium.append(0)

		# increment
		i = i + 1


	return render_template('index.html',
		values_sporulation_oidium	=	sporulation_oidium,
		values_developpment_oidium	=	developpment_oidium,
		values_botrytis				=	botrytis,
		values_humidity				=	humidity,
		values_temperature			=	temperature,
		labels_humidity				=	date_humidity,
		labels_temperature			=	date_temperature)
