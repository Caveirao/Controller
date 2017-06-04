# -*- coding: utf-8 -*-
import pygame, socket, struct

global event_flag
global quit
global left_motor
global right_motor
l_axis = 1
left_motor = False
right_motor = False
event_flag = True
quit = False

def event_handler(events):

    global event_flag
    global quit
    global move_forward
    global move_backward
    global move_left
    global move_right
    global left_motor
    global right_motor

    for event in events:
        if event.type == pygame.QUIT:
            # Se botão "sair" pressionado
            event_flag = True
            quit = True
        elif event.type == pygame.KEYDOWN:
            # Tecla pressionada
            event_flag = True
            if event.key == 27:
                quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                quit = False
        elif event.type == pygame.JOYAXISMOTION:
            # Os eixos do joystick foram acionados
            event_flag = True
            y = j.get_axis(l_axis)
            if y < 0:
                left_motor = 1
            elif y > 0:
                left_motor = -1
            else:
                left_motor = 0
        elif event.type == pygame.JOYBUTTONDOWN:
            event_flag = True
            if event.button == 0:
                right_motor = 1
            if event.button == 2:
                right_motor = -1
        elif event.type == pygame.JOYBUTTONUP:
            event_flag = True
            if event.button == 0:
                right_motor = 0
            if event.button == 2:
                right_motor = 0      
                
# Detecção e inicialização do joystick
pygame.joystick.init()
if(pygame.joystick.Joystick(0)):
	j = pygame.joystick.Joystick(0)
	j.init()
	name = j.get_name()
	print 'Joystick ' + name + 'detectado.'
else:
	print 'Joystick não detectado, verifique a conexão.'
# Configuração de vídeo, relógio
width = 640
height = 480
image = pygame.image.load('img/logo.png')
image = pygame.transform.scale(image, (300,300))
img_rect = image.get_rect(centerx=(width/2))
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Caveirão')
clock = pygame.time.Clock()
# Configuração do socket UDP
HOST = "127.0.0.1"
PORT = 5005
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    print "Pressione [ESC] para sair"
     
    while quit != True:
        screen.blit(image, img_rect)
        pygame.display.flip()
        event_handler(pygame.event.get())
        if event_flag:
            event_flag = False
            if left_motor == 1 and right_motor == 1:
                data = [1, 1]
            elif left_motor == 1 and right_motor == -1:
                data = [1, -1]
            elif left_motor == -1 and right_motor == 1:
                data = [-1, 1]
            elif left_motor == -1 and right_motor == -1:
                data = [-1, -1]
            else:
                data = [0, 0]
            package = struct.pack('>2h', data[0], data[1])
            udp.sendto(package, (HOST, PORT))
        
    clock.tick(30)
except KeyboardInterrupt:
	print "\nOFF"

udp.close()
pygame.quit()