from motor import Motor
from testing import Testing, bcolors


def main(args):
	return 0


if __name__ == '__main__':
	import sys

	print(bcolors.UNDERLINE+"Que vols executar?"+bcolors.ENDC)
	print(bcolors.HEADER+ "	1. Traca" +bcolors.ENDC)
	print(bcolors.WARNING + "	2. Tests" + bcolors.ENDC)
	print(bcolors.FAIL+"	3. Exit" + bcolors.ENDC)
	mode = int(input(bcolors.BOLD+'Mode(1, 2 o 3): '+bcolors.ENDC))
	while mode != 3:
		if mode == 1:
			motor = Motor(8,100,20)
			motor.run()
			print(motor.esdevenimentsProcessats)

		elif mode == 2:
			Testing()
		print(bcolors.UNDERLINE + "Que vols executar?" + bcolors.ENDC)
		print(bcolors.HEADER + "	1. Traca" + bcolors.ENDC)
		print(bcolors.WARNING + "	2. Tests" + bcolors.ENDC)
		print(bcolors.FAIL + "	3. Exit" + bcolors.ENDC)
		mode = int(input(bcolors.BOLD + 'Mode(1, 2 o 3): ' + bcolors.ENDC))
