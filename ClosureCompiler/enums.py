from enum import IntFlag


class TypeInferMode(IntFlag):
	none = 0b00
	check = 0b01
	infer = 0b10
