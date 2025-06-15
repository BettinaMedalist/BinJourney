import pygame

#Apenas para facilitar o carregamento de imagens
def carregar_imagem(caminho):
    imagem = pygame.image.load(caminho).convert_alpha()
    return imagem

def meio(coord, game_object, tela):
    #Retorna a posição em central da tela para determinado game_object
    if coord == "x":
        return ((tela.get_width() - game_object.width) / 2)
    elif coord == "y":
        return ((tela.get_height() - game_object.height) / 2)