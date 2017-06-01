# -*- coding: utf-8 -*-
import pygame, time

axis_x = 0
axis_y = 1
x_inverted = False
y_inverted = False
move_forward = False
move_backward = False
move_right = False
move_left = False
event_flag = True
quit = False
refresh = 0.05

def event_handler(events):

	for event in events:
		print event
		if event.type == pygame.QUIT:
			# Se botão "sair" pressionado
			event_flag = True
			quit = True
		elif event.type == pygame.KEYDOWN:
			# Tecla pressionada
			print 'tecla'
			event_flag = True
			if event.key == 27:
				quit = True
				print quit
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				quit = False
		elif event.type == pygame.JOYAXISMOTION:
			# Os eixos do joystick foram acionados
			event_flag = True
			x = j.get_axis(axis_x)
			y = j.get_axis(axis_y)
			# Inverter eixos incorretos
			if x_inverted:
				x = -x
			if y_inverted:
				y = -y
			# Determinar valores up, down, left, right
			if x < -0.1:
				move_left = True
				move_right = False
			elif x > 0.1:
				move_left = False
				move_right = True
			else:
				move_left = False
				move_right = False

			if y < -0.1:
				move_forward = True
				move_backward = False
			elif y > 0.1:
				move_forward = False
				move_backward = True

pygame.joystick.init()
if(pygame.joystick.Joystick(0)):
	j = pygame.joystick.Joystick(0)
	j.init()
	name = j.get_name()
	print 'Joystick ' + name + 'detectado.'
else:
	print 'Joystick não detectado, verifique a conexão.'
screen = pygame.display.set_mode([300, 300])
pygame.display.set_caption('Caveirão')
pygame.font.init()
myfont = pygame.font.SysFont('', 20)
text = myfont.render('Teste', True, (0, 0, 0))

#try:
print "Pressione [ESC] para sair"

while True:
	event_handler(pygame.event.get())
	if event_flag:
		event_flag = False
		print quit
		if quit:
			print 'sair'
			break
		elif move_forward:
			print "frente"
		elif move_backward:
			print "trás"
		elif move_left:
			print "esquerda"
		elif move_right:
			print "direita"
	time.sleep(refresh)
#except KeyboardInterrupt:
#	print "OFF"