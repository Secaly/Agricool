from app import app
from flask import Flask, Markup, render_template
from datetime import datetime
import csv

@app.route('/')
def index():

	"""
	Humidity Data
	"""
	fd_humidity = open('ressources/humidity.csv', 'r')
	reader_humidity = csv.reader(fd_humidity)
	data_humidity = list(reader_humidity)
	data_humidity.remove(data_humidity[0])
	date_humidity = []
	humidity = []
	for value in data_humidity:
		date_humidity.append(value[0])
		humidity.append(float(value[1]))

	"""
	Temperature Data
	"""
	fd_temperature = open('ressources/temperature.csv', 'r')
	reader_temperature = csv.reader(fd_temperature)
	data_temperature = list(reader_temperature)
	data_temperature.remove(data_temperature[0])
	date_temperature = []
	temperature = []
	for value in data_temperature:
		date_temperature.append(value[0])
		temperature.append(float(value[1]))

	"""
	Sporulation Oidium Data
	"""
	i = 0
	sporulation_oidium = []
	for date in date_humidity:
		new_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')
		if humidity[i] < 90:
			last_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')
		time_difference = new_time - last_time
		time_difference_in_minutes = time_difference.total_seconds() / 60
		if time_difference_in_minutes > 60:
			sporulation_oidium.append(1)
		elif humidity[i] > 90:
			sporulation_oidium.append(0.5)
		else:
			sporulation_oidium.append(0)
		i = i + 1

	"""
	Botrytis
	"""
	i = 0
	botrytis = []
	for date in date_humidity:
		new_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')
		if humidity[i] < 90 or temperature[i] <= 15 or temperature[i] >= 20:
			last_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')
		time_difference = new_time - last_time
		time_difference_in_minutes = time_difference.total_seconds() / 60
		print(time_difference_in_minutes)
		if time_difference_in_minutes > 360:
			botrytis.append(1)
		elif humidity[i] > 90 and temperature[i] > 15 or temperature[i] < 20:
			botrytis.append(0.5)
		else:
			botrytis.append(0)
		i = i + 1

	"""
	Developpment Oidium Data
	"""
	i = 0
	developpment_oidium = []
	for date in date_humidity:
		new_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')
		if sporulation_oidium[i] != 1 or temperature[i] <= 20:
			last_time = datetime.strptime(date_humidity[i], '%d/%m/%Y %H:%M:%S')
		time_difference = new_time - last_time
		time_difference_in_minutes = time_difference.total_seconds() / 60
		if time_difference_in_minutes > 600:
			developpment_oidium.append(1)
		elif sporulation_oidium[i] == 1 and temperature[i] > 20:
			developpment_oidium.append(0.5)
		else:
			developpment_oidium.append(0)
		i = i + 1


	return render_template('index.html',
		values_sporulation_oidium=sporulation_oidium,
		values_developpment_oidium=developpment_oidium,
		values_humidity=humidity, values_botrytis=botrytis,
		labels_humidity=date_humidity, values_temperature=temperature,
		labels_temperature=date_temperature)
