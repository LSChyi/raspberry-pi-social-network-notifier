import RPi.GPIO as GPIO

class RGB_PWM:
	def __init__(self, pin, discount_factor):
		self.pin = pin
		self.discount_factor = discount_factor
		self.brightness = 0
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, False)
		self.pwm =  GPIO.PWM(pin, 60)
		self.increasing = True

	def max_brightness(self):
		return 100 * self.discount_factor

	def change_brightness(self, step):
		if self.increasing:
			self + step
		else:
			self - step

		if self.brightness == self.max_brightness() or self.brightness == 0:
			self.increasing = not self.increasing
	
	def turn_on(self):
		self + 100
	
	def turn_off(self):
		self - 100

	def __add__(self, value):
		self.brightness += value * self.discount_factor
		self.brightness = self.max_brightness() if self.brightness > self.max_brightness() else self.brightness
		self.pwm.start(self.brightness) 
		return self

	def __sub__(self, value):
		self.brightness -= value * self.discount_factor
		self.brightness = 0 if self.brightness < 0 else self.brightness
		self.pwm.start(self.brightness) 
		return self

if __name__ == "__main__":
	import time
	import random
	from config.config import Config

	GPIO.setmode(GPIO.BOARD)

	pwms = {
		'blue': RGB_PWM(Config.blue_pin, 0.7),
		'red': RGB_PWM(Config.red_pin, 1),
		'green': RGB_PWM(Config.green_pin, 0.09),
	}

	pwms['blue'].turn_on()
	time.sleep(1)
	pwms['blue'].turn_off()

	pwms['red'].turn_on()
	time.sleep(1)
	pwms['red'].turn_off()

	pwms['green'].turn_on()
	time.sleep(1)
	pwms['green'].turn_off()

	keys = pwms.keys()
	counter = 0
	for _ in xrange(1000):
		if counter % 200 == 0:
			random_color = random.sample(keys, 2)
		color = random.sample(keys + random_color*6, 1)[0]
		pwms[color].change_brightness(random.random()*3)
		counter += 1
		time.sleep(0.05)
	
	GPIO.cleanup()
