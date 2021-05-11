#!/usr/bin/env python3
from enum import Enum

class EmojiImage(Enum):
	BOMB = "Images/bomb.png"
	FLAG = "Images/flag.png"
	EMPTY = "Images/empty.png"
	PRESSED = "Images/pressed.png" 
	DISCOVER = "Images/find.png"
	ONE = "Images/1.png"
	TWO = "Images/2.png"
	THREE = "Images/3.png"
	FOUR = "Images/4.png"
	FIVE = "Images/5.png"
	SIX = "Images/6.png"
	SEVEN = "Images/7.png"
	EIGHT = "Images/8.png"
	
	def picture_from(string):
		if string =="ó":
			return EmojiImage.BOMB.value
		if string == "P":
			return EmojiImage.FLAG.value
		if string == "":
			return EmojiImage.EMPTY.value
		if string == "_":
			return EmojiImage.PRESSED.value
		if string == "1":
			return EmojiImage.ONE.value
		if string == "2":
			return EmojiImage.TWO.value
		if string == "3":
			return EmojiImage.THREE.value
		if string == "4":
			return EmojiImage.FOUR.value
		if string == "5":
			return EmojiImage.FIVE.value
		if string == "6":
			return EmojiImage.SIX.value
		if string == "7":
			return EmojiImage.SEVEN.value
		if string == "8":
			return EmojiImage.EIGHT.value