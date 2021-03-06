# -*- coding: utf-8 -*-
"""
DreamPlex Plugin by DonDavici, 2012

https://github.com/DonDavici/DreamPlex

Some of the code is from other plugins:
all credits to the coders :-)

DreamPlex Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

DreamPlex Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
"""
#===============================================================================
# IMPORT
#===============================================================================
from Components.config import config
from enigma import eSize, getDesktop

from Components.VideoWindow import VideoWindow
from Components.Label import Label
from Components.Label import MultiColorLabel

from skin import parseColor

from __common__ import printl2 as printl

#===============================================================================
#
#===============================================================================
class DPH_ScreenHelper(object):

	#===============================================================================
	#
	#===============================================================================
	def __init__(self, forceMiniTv=False):
		printl("", self, "S")

		self.stopLiveTvOnStartup = config.plugins.dreamplex.stopLiveTvOnStartup.value

		# we use this e.g in DP_View to use miniTv for backdrops via libiframe
		self.forceMiniTv = forceMiniTv

		if not self.stopLiveTvOnStartup or self.forceMiniTv:
			self["miniTv"] = VideoWindow(decoder=0)
		else:
			self["miniTv"] = Label()

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def initMiniTv(self):
		printl("", self, "S")

		if not self.stopLiveTvOnStartup or self.forceMiniTv:
			# TODO make this dynamik via skin params file
			w = 400
			h = 225
			desk = getDesktop(0)
			self["miniTv"].instance.setFBSize(desk.size())
			self["miniTv"].instance.resize(eSize(w, h))
		else:
			self["miniTv"].hide()

		printl("", self, "C")

#===============================================================================
#
#===============================================================================
class DPH_MultiColorFunctions(object):

	#===============================================================================
	#
	#===============================================================================
	def __init__(self):
		printl("", self, "S")

		self.colorFunctionContainer = {}
		self.colorFunctionContainer["red"] = {}
		self.colorFunctionContainer["green"] = {}
		self.colorFunctionContainer["yellow"] = {}
		self.colorFunctionContainer["blue"] = {}

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def setColorFunction(self, color, level, functionList):
		printl("", self, "S")

		self.colorFunctionContainer[color][level] = functionList

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def getColorFunction(self, color, level):
		printl("", self, "S")

		printl("", self, "C")
		return self.colorFunctionContainer[color][level]

	#===============================================================================
	#
	#===============================================================================
	def executeColorFunction(self, color, level):
		printl("", self, "S")

		eval(self.colorFunctionContainer[color][level][1])

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def alterColorFunctionNames(self, level):
		printl("", self, "S")
		colorList = ["red", "green", "yellow", "blue"]

		for color in colorList:
			functionList = self.colorFunctionContainer[color][level]

			if functionList is not None:
				# if it is not already visible we change this now
				if self["btn_"+ color + "Text"].getVisible() == 0:
					self["btn_"+ color + "Text"].show()
					self["btn_"+ color].show()

				self["btn_"+ color + "Text"].setText(self.colorFunctionContainer[color][level][0])
			else:
				if self["btn_"+ color + "Text"].getVisible() == 1:
					self["btn_"+ color + "Text"].hide()
					self["btn_"+ color].hide()

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def setMultiLevelElements(self, levels):
		printl("", self, "S")
		self.levels = levels

		highlighted = parseColor("#e69405")
		normal = parseColor("#ffffff")

		for i in range(1,int(levels)+1):
			self["L"+str(i)] = MultiColorLabel()
			self["L"+str(i)].foreColors = [highlighted, normal]
			self["L"+str(i)].setText(str(i))

		printl("", self, "C")

	#===============================================================================
	#
	#===============================================================================
	def setLevelActive(self, currentLevel):
		printl("", self, "S")

		self.currentFunctionLevel = currentLevel
		printl("currentFunctionLevel: " + str(self.currentFunctionLevel), self, "D")

		for i in range(1,int(self.levels)+1):
			if int(self.currentFunctionLevel) == int(i):
				self["L" + str(i)].setForegroundColorNum(0)
			else:
				print "hide" + str(i)
				self["L" + str(i)].setForegroundColorNum(1)

		printl("", self, "C")
