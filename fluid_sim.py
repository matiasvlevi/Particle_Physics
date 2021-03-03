import pygame, sys
from pygame.locals import *
import time
import random

pygame.init()

clock = pygame.time.Clock()

fps = 120

wnx = 800
wny = 600

black = (0,0,0)
grey = (80,80,80)
white = (255,255,255)
black_transparent = (255,255,255,128)
red = (255,0,0)
BACKGROUNDCOLOR = (40,40,40)

#__ Elements __

sand = (255,160,50)
rock = (125,125,125)
bsand = (255,180,150)
brock = (180,180,180)
dirt = (110, 45, 0)
bdirt = (200, 90, 0)
water = (0, 150, 255)
bwater = (25, 200, 255)
wall = (100,100,100)
bwall = (140,140,140)

erase = False

Onbutton = False
color = sand
cubec = sand

wn = pygame.display.set_mode((wnx, wny))
wn.fill(white)

def cursor(cux,cuy,cuw):
	boxc = pygame.draw.rect(wn, black, [cux, cuy, cuw, cuw], 1)


def message(Font,Size,colort,xt,yt,text):
	font = pygame.font.SysFont('freepixelregular', Size, True)
	text = font.render(text, True, colort)
	wn.blit(text, (xt, yt))



def cube(cx,cy,cw,ch,cubec):
	pygame.draw.rect(wn, cubec, [cx, cy, cw, ch])


def floor(fx,fy,fw,fh):
	pygame.draw.rect(wn, grey, [fx, fy, fw, fh])
	pygame.draw.line(wn, black, (150,504), (800, 504), 10)

def sidebar(sx,sy,sw,sh):
	pygame.draw.rect(wn, grey, [0, 0, 150, 600])
	pygame.draw.line(wn, black, (154,0), (154, 500), 10)


def button(bx, by, bw, bh, text, abcol, bcol, colorchange):

	global color

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()


	if bx+bw > mouse[0] > bx and by+bh > mouse[1] > by:
		Onbutton = True
		pygame.draw.rect(wn, abcol, [bx, by, bw, bh])
		if click[0] == 1 and colorchange != None:
			color = colorchange

	else:
		pygame.draw.rect(wn, bcol, [bx, by, bw, bh])
		Onbutton = False





	font = pygame.font.SysFont('freepixelregular', 25,True)
	text = font.render(text, True, black)
	wn.blit(text, (bx + (bw/14), by + (bh/4)))


def main():


	number = 0

	toggle_fast = True
	erase = False


	cubex = [0] * number
	cubey = [0] * number
	cubec = [0] * number
	cubew = 10  #cube size
	cubeh = cubew


	floory = 500

	gravity = (cubew*-1)


	clickt = False

	exit = False



	while not exit:



		#________________ QUIT ________________________________________

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				exit = True

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_SPACE:
					toggle_fast = not toggle_fast
				if event.key == pygame.K_v:
					erase = not erase


		#_____________________ Click / spawn cube / erase cube _____________________________

			mouse = pygame.mouse.get_pos()
			click = pygame.mouse.get_pressed()

			if toggle_fast == False:

				if event.type == pygame.MOUSEBUTTONDOWN:
					if mouse[1] < floory and mouse[0] >= 154:



						cubex.append(round((mouse[0]/cubew),0)*cubew)
						cubey.append(round((mouse[1]/cubew),0)*cubew)
						cubec.append(color)





			if click[0] == 1 and toggle_fast == True:
				print(erase)
				if mouse[1] < floory and mouse[0] >= 154:



					cubex.append(round((mouse[0]/cubew),0)*cubew)
					cubey.append(round((mouse[1]/cubew),0)*cubew)
					cubec.append(color)




		#_____________________ GRAVITY _____________________________

		for i in range(len(cubex)):
			cubeR = pygame.Rect(cubex[i], cubey[i] + cubew, cubew, cubeh)
			cisect = [j for j in range(len(cubey)) if j-1 != i and cubeR.colliderect(pygame.Rect(cubex[j], cubey[j], cubew, cubeh))]
			watercheck = [j for j in range(len(cubey)) if j-1 != i and cubec[i] != (0, 150, 255) and cubec[j] == (0, 150, 255) and cubeR.colliderect(pygame.Rect(cubex[j], cubey[j], cubew, cubeh))]

			if not any(cisect) and not (cubey[i] + cubew) >= floory:
				if not cubec[i] == (100,100,100):
					cubey[i] -= gravity



		#________water physics___________

			cubeRxr = pygame.Rect(cubex[i] - cubew, cubey[i], cubew, cubeh)
			cubeRxl = pygame.Rect(cubex[i] + cubew, cubey[i], cubew, cubeh)
			cubeRdiagr = pygame.Rect(cubex[i] + 10, cubey[i] + 10, cubew, cubeh)
			cubeRdiagl = pygame.Rect(cubex[i] - 10, cubey[i] + 10, cubew, cubeh)
			cisectx = [j for j in range(len(cubex)) if j != i and cubeRxr.colliderect(pygame.Rect(cubex[j], cubey[j], cubew, cubeh))]
			cisectxl = [j for j in range(len(cubex)) if j != i and cubeRxl.colliderect(pygame.Rect(cubex[j], cubey[j], cubew, cubeh))]
			cisectdr = [j for j in range(len(cubex)) if j != i and cubeRdiagr.colliderect(pygame.Rect(cubex[j], cubey[j], cubew, cubeh))]
			cisectdl = [j for j in range(len(cubex)) if j != i and cubeRdiagl.colliderect(pygame.Rect(cubex[j], cubey[j], cubew, cubeh))]



			if cubec[i] == (0, 150, 255):

				if (cubey[i] + cubew) >= floory or any(cisect):  # on ground


					if not (cubex[i] + cubew) >= 800 and not cubex[i] <= 164:


						if any(cisectx) and not any(cisectxl):												#going right because of right wall
							cubex[i] += 10
						elif any(cisectxl) and not any(cisectx):												#going left because of left wall
							cubex[i] -= 10

						elif any(cisectx) and any(cisectxl):
							cubex[i] += 0

						elif any(cisect) or (cubey[i] + cubew) >= floory:

							negative = [-10, 10]
							cubex[i] += random.choice(negative)

						elif any(cisect) and not any(cisectdl) and not any(cisectdr):
							negative = [-10, 10]
							cubex[i] += random.choice(negative)





		#_____________________ DRAW _____________________________

		wn.fill(BACKGROUNDCOLOR)

		floor(0,floory,800,100)
		sidebar(0, 0, 150, 600)

		for i in range(len(cubex)):
			cube(cubex[i], cubey[i], cubew, cubeh, cubec[i])

		cursor(round((mouse[0]/cubew),0)*cubew, round((mouse[1]/cubew),0)*cubew, cubew,)

		button(20, 40, 50, 40, 'RCK', brock, rock, (125,125,125))
		button(20, 85, 50, 40, 'SND', bsand, sand, (255,160,50))
		button(20, 130, 50, 40, 'DRT', bdirt, dirt, (110, 45, 2))
		button(20, 175, 50, 40, 'WTR', bwater, water, (0, 150, 255))
		button(20, 220, 50, 40, 'WLL', bwall, wall, (100,100,100))

		#(Font,Size,colort,xt,yt,message):
		message(None, 20, black, 10,400,('ERASE:'+str(erase)))

		pygame.display.update()
		clock.tick(fps)

main()

pygame.quit()
quit()
