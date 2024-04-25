import configparser
config = configparser.ConfigParser()
config.sections()
config.read('setting.ini')
config.sections()

region_point = config['region_points']
region_point['position']
print(region_point['position'])
print(type(region_point['position']))
print(type(eval(region_point['position'])))