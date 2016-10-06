from rgb_pwm import RGB_PWM
from config.config import Config
import RPi.GPIO as GPIO
import time
import threading
import random
import atexit

atexit.register(GPIO.cleanup)

class Light_controller:
	def __init__(self):

		class Status():
			def __init__(self, mode, params):
				self.mode = mode
				self.params = params

			def run(self):
				self.mode(*self.params)

		GPIO.setmode(GPIO.BOARD)
		self.leds = {
			'blue': RGB_PWM(Config.blue_pin, 0.7),
			'red': RGB_PWM(Config.red_pin, 1),
			'green': RGB_PWM(Config.green_pin, 0.09),
		}

		self.status = 'Normal'
		self.statuses = {
			'Normal': Status(self.blink_mode, [ 'blue', 0.2, 0.2 ]),
			'Test': Status(self.random_mode, []),
		}

		self.random_counter = 0
		self.led_keys = self.leds.keys()

		self.light_stop = threading.Event()
		light_thread = threading.Thread(target=self.run, args=(self.light_stop, ))
		light_thread.start()

	def run(self, stop_event):
		while not stop_event.is_set():
			self.statuses[self.status].run()

	def blink_mode(self, color, on_interval=0.5, off_interval=0.5):
		self.leds['blue'].turn_off()
		self.leds['red'].turn_off()
		self.leds['green'].turn_off()

		self.leds[color].turn_on()
		time.sleep(on_interval)
		self.leds[color].turn_off()
		time.sleep(off_interval)

	def random_mode(self):
		if self.random_counter % 200 == 0:
			self.random_color = random.sample(self.led_keys, 2)
		color = random.sample(self.led_keys + self.random_color*6, 1)[0]
		self.leds[color].change_brightness(random.random()*3)
		self.random_counter += 1
		time.sleep(0.05)

	def stop(self):
		self.light_stop.set()

if __name__ == "__main__":
	led_controller = Light_controller()
	time.sleep(5)
	print "change status to \"Test\""
	led_controller.status = "Test"
	time.sleep(5)
	led_controller.stop()
