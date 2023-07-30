import bme680
import time
import requests
import drivers
from time import sleep
from gpiozero import Buzzer
from gpiozero import LED 
from beep import beep
from payload import send_to_ubidots
from AQIScoring import humidity_score
from AQIScoring import get_gas_reference
from AQIScoring import get_gas_score
from AQIStatus import calculate_IAQ
buzzer = Buzzer(17)

display = drivers.Lcd()
red = LED(26)
yellow = LED(19)
green = LED(13)

temperature = 0
humidity = 0
pressure = 0
gas_resistance = 0
AQI_score = 0

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)
        if isinstance(value, int):
            print('{}: {}'.format(name, value))

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)
    
    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)
# show gas status
def check_internet_connection():
                    try:
                        response = requests.get("https://www.google.com", timeout=5)
                        if response.status_code == 200:
                            return True
                    except:
                            pass
                    return False

print('\n\nPolling:')
try:
    while True:
        if sensor.get_sensor_data():
            temperature = sensor.data.temperature
            pressure = sensor.data.pressure
            humidity = sensor.data.humidity
            output = '\n temperature : {0:.2f} C \npressure : {1:.2f} hPa \n humidity: {2:.2f} %'.format(
                temperature,
                pressure,
                humidity)
            if sensor.data.heat_stable:
                gas_resistance = sensor.data.gas_resistance
                get_gas_reference(gas_resistance)
                hum_score = humidity_score(humidity)
                gas_score      = get_gas_score()
                air_quality_score = hum_score + gas_score
                IAQ_text = calculate_IAQ(air_quality_score)
                print('Humidity score :', hum_score)
                print('Gas score :', gas_score)
                print('Air quality score :', air_quality_score)
                print('Air quality in room is ' + IAQ_text)
                print('{0} \n gas resistance : {1} Ohms'.format(
                    output,
                    gas_resistance))
               
                display.lcd_display_string("temp: {} C".format(temperature), 1)  
                display.lcd_display_string("humidity: {} RH".format(humidity), 2)  
                sleep(2)                                           
                display.lcd_display_string("pressure: {} hPa".format(pressure), 1)
                display.lcd_display_string("gas : {} Ohms".format(gas_resistance), 2)   
                sleep(2) 
                display.lcd_display_string("AQI: {}".format(air_quality_score), 1)
                display.lcd_display_string("{}".format(IAQ_text), 2)   
                sleep(2)      
                
                payload = {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "gas": gas_resistance,
                "air_quality_score": air_quality_score
                }

                if check_internet_connection():
                     send_to_ubidots(payload)
                else:
                    pass
                  
            else:
                print(output)

        time.sleep(2)

except KeyboardInterrupt:
    buzzer.off()
    red.off()
    yellow.off()
    green.off()
    display.lcd_clear()
    pass