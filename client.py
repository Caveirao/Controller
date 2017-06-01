# -*- coding: utf-8 -*-
import pygame

pygame.joystick.init()

if(pygame.joystick.Joystick(0)):
	j = pygame.joystick.Joystick(0)
	j.init()
	name = j.get_name()
	print 'Joystick ' + name + 'detectado.'
else:
	print 'Joystick não detectado, verifique a conexão.'

