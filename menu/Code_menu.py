
#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
#Ouverture de la fenêtre Pygame
fenetre = pygame.display.set_mode((1280, 720))

#Chargement et collage du fond
fond = pygame.image.load("imagefond.png")
fenetre.blit(fond, (0,0))




# Création d'un rect pour le bouton jouer (position, couleur, taille)
rect = pygame.draw.rect(fenetre,(((((1, 121, 111))))),pygame.Rect(560, 470, 220, 57))#(posistion largeur, hauteur fentre, taille longueur largeur)
rect = pygame.draw.rect(fenetre,(((1, 121, 111))),pygame.Rect(560, 335, 220, 57))
rect = pygame.draw.rect(fenetre,((1, 121, 111)),pygame.Rect(560, 190, 220, 57))

# Création des polices d'écriture avec différentes tailles
myfont = pygame.font.Font('Games.ttf', 50)
myfont2 =  pygame.font.Font('Games.ttf', 35)
myfont3 = pygame.font.Font('Games.ttf',70)


# Création du texte pour le bouton jouer avec une police présente plus haut
text = myfont.render("Credits", False, (0, 0, 0))
text2=myfont2.render("Level Editor",False, (0, 0, 0))
text3=myfont3.render("Jouer!",False, (0, 0, 0))


#Parametres echelle de droite
echelle2 = pygame.image.load("echelle.png").convert_alpha()
echelle2petit = pygame.transform.scale(echelle2,(300,300))#Changement de taille echelle2
fenetre.blit(echelle2petit, (800,270))

#Parametre Helico1
perso2 = pygame.image.load("Helico.png").convert_alpha()
fenetre.blit(perso2, (765,100))

#Parametre Helico retourné
perso2 = pygame.image.load("Helico RETOURNER.png").convert_alpha()
fenetre.blit(perso2, (75,100))

#Parametres perso de droite
perso2 = pygame.image.load("player2.png").convert_alpha()
perso2grand = pygame.transform.scale(perso2,(150,150)) #Changement de taille perso2
fenetre.blit(perso2grand, (930,420))

#Parametres de l'echelle2 de gauche
echelle = pygame.image.load("echelle.png").convert_alpha()
echellepetit = pygame.transform.scale(echelle,(300,300))#changement taille echelle
fenetre.blit(echellepetit, (150,270))

#Parametres perso de gauche
perso = pygame.image.load("player 1.png").convert_alpha()
persopetit= pygame.transform.scale(perso,(150,150))#changement taille perso1
fenetre.blit(persopetit, (300,420))




#Pour afficher les mots dans les boutons
fenetre.blit(text,(560, 470, 197, 57))
fenetre.blit(text2,(560, 335, 197, 57))
fenetre.blit(text3,(560, 190, 197, 57))
#Rafraîchissement de l'écran
pygame.display.flip()
continuer = 1


#Boucle infinie
while continuer:
	for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
		if event.type == QUIT:     #Si un de ces événements est de type QUIT
			continuer = 0      #On arrête la boucle



