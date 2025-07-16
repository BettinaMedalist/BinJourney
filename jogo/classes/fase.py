from classes.inimigo import*
from classes.parede import*

class Fase:# não herda mais o (GameObject):
    def __init__(self, screen, player, delta_time):
        # não precisa super().__init__(screen, image_path)
        self.screen = screen
        self.delta_time = delta_time
        self.player = player

        self.all_sprites = pygame.sprite.Group()

        #trocar as lista de inimigos e objetos por groups de sprite
        
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        


    # Adiciona aos grupos em vez de listas
    def add_enemy(self, enemy_type, angle, x, y):
        new_enemy = Inimigo_Pistola(self.screen, angle, x, y)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def add_object(self, object_type, angle, x, y):
        if object_type == "parede":
            new_wall = Parede(x, y)
            self.walls.add(new_wall)
            self.all_sprites.add(new_wall)



    def movement(self):
        # Normaliza o vetor de direção
        if self.player.direction.length() > 0:
            self.player.direction.normalize_ip()

        # --- Movimento e Colisão Horizontal ---
        mov_x = self.player.direction.x * self.player.speed * self.delta_time
        
        player_rect_copy = self.player.rect.copy()
        player_rect_copy.x += mov_x
        
        # Criamos a lista de retângulos das paredes
        wall_rects = [wall.rect for wall in self.walls]
        
        # <<< A CORREÇÃO ESTÁ AQUI >>>
        # Usamos collidelist para comparar um Rect com uma lista de Rects
        colliding_wall_index = player_rect_copy.collidelist(wall_rects)

        # Se o resultado for -1, significa que NÃO HOUVE colisão
        if colliding_wall_index == -1:
            # Move o mundo inteiro se não houver colisão
            for tile in self.background_group:
                tile.rect.x -= mov_x
            for sprite in self.all_sprites:
                if sprite != self.player:
                    sprite.rect.x -= mov_x

        # --- Movimento e Colisão Vertical ---
        mov_y = self.player.direction.y * self.player.speed * self.delta_time
        
        player_rect_copy = self.player.rect.copy()
        player_rect_copy.y += mov_y

        # <<< E A CORREÇÃO ESTÁ AQUI TAMBÉM >>>
        colliding_wall_index = player_rect_copy.collidelist(wall_rects)
        
        if colliding_wall_index == -1:
            # Move o mundo inteiro se não houver colisão
            for tile in self.background_group:
                tile.rect.y -= mov_y
            for sprite in self.all_sprites:
                if sprite != self.player:
                    sprite.rect.y -= mov_y

    def update(self):
        #usando groups da pra mudar a logica de colisão dos tiros para apenas essa linha que ja verifica tudo
        pygame.sprite.groupcollide(self.player.shots, self.enemies, True, True)
        pygame.sprite.groupcollide(self.player.shots, self.walls, True, False)

    def render(self):
        # aq muda tbm
        self.background_group.draw(self.screen)
        self.enemies.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.player.shots.draw(self.screen)
    


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, groups):
        super().__init__(groups) # Adiciona a tile aos grupos informados
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))