import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


def test_ads1115_connection():
    i2c = busio.I2C(board.SCL, board.SDA)

    ads = ADS.ADS1115(i2c)
    channel = AnalogIn(ads, ADS.P0)

    print(f"Raw ADC value: {channel.value}")
    print(f"Voltage: {channel.voltage:.3f} V")

    assert channel.value >= 0