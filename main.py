from motor import Motor
from testing import Testing, bcolors


def main(args):
	return 0


if __name__ == '__main__':
	import sys

	print("Que vols executar?")
	print("	1. Traca")
	print("	2. Tests")
	mode = int(input('Mode( 1 o 2 ): '))
	if mode == 1:
		motor = Motor(8,100,20)
		motor.run()
		print(motor.esdevenimentsProcessats)

	elif mode == 2:
		Testing()


	# Probar que los estados sean correctos, BUSY, IDLE (main, parking,estibador) con los iniciservei
	# o cuando no tienen nada (unitario)
