#!/usr/bin/env python2

import os, sys, getopt, pygame
from pygame import mixer, image, font, transform

NTSC=(525, 480)
red=pygame.Color(255, 0, 0, 0)
blue=pygame.Color(0, 0, 255, 0)
black=pygame.Color(0, 0, 0, 0)

mySurf=pygame.Surface(NTSC)
font.init()
mixer.init()
myFont=font.SysFont(font.get_default_font(), 23)

films={}
clips=[]

counter=0

for line in sys.stdin.readlines():
	for token in line.strip().split():
		if(len(token)==0): next
		if not (token in films):
			mySurf.fill(black)
			centrePos=(len(token)/2)
			centre=token[centrePos]
			pre=token[:centrePos]
			post=token[centrePos+1:]
			print(pre+" "+centre+" "+post)
			preI=myFont.render(pre, True, blue)
			postI=myFont.render(post, True, blue)
			centreI=myFont.render(centre, True, red)
			clumpWidth=0 ; clumpHeight=0
			for i in [preI, centreI, postI]:
				clumpWidth+=i.get_width()
				clumpHeight+=i.get_height()
			clump=pygame.Surface((clumpWidth, clumpHeight))
			x=0
			for i in [preI, centreI, postI]:
				clump.blit(i, (x, 0))
				x+=i.get_width()
			scale=1
			if (NTSC[0]/(1.0*clumpWidth) > NTSC[1]/(1.0*clumpHeight)):
				scale=NTSC[0]/(1.0*clumpWidth)
			else:
				scale=NTSC[1]/(1.0*clumpHeight)
			if (scale>1):
				scale=1.0/scale
			resizedClump=transform.scale(clump, (int(clumpWidth*scale), int(clumpHeight*scale)))
			mySurf.blit(resizedClump, ((NTSC[0]/2)-(resizedClump.get_height()/2), (NTSC[1]/2)-(resizedClump.get_height()/2)))
			image.save(mySurf, "temp.png")
			os.system("rm -f temp.txt")
			f=open("temp.txt", "w")
			f.write(token)
			f.close()
			os.system("text2wave temp.txt -o temp.wav")
			s=mixer.Sound("temp.wav")
			seconds=int(s.get_length()+0.5)
			cmd="mencoder -oac copy -ovc lavc -o temp.avi -mf fps=1 "+("mf://temp.png"*seconds)
			os.system(cmd)
			os.system("mencoder -oac copy -ovc lavc -audiofile temp.wav -o "+str(counter)+".avi temp.avi")
			os.system("rm -f temp.{wav,txt,png,avi}")
			films[token]=str(counter)+".avi"
			counter+=1
		clips.append(films[token])
os.system("mencoder -oac copy -ovc copy -o temp.avi "+(" ".join(clips)))
os.system("mencoder -oac copy -ovc lavc -o blip.avi -speed 5 temp.avi")
os.system("rm temp.avi")
os.system("rm -f "+(" ".join(films.values())))


