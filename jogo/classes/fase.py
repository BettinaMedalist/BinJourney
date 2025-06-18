from classes.inimigo import*

class Fase(GameObject):
    def __init__(self, screen, image_path, player, delta_time):
        super().__init__(screen, image_path)
        self.enemies = []
        self.objects = []
        self.delta_time = delta_time
        self.player = player

    def add_enemy(self, enemy_type, x, y):
        self.enemies.append(Inimigo(self.screen, "jogo\sprites\sair.png", x, y))

    def add_object(self, object_type, x, y):
        pass

    def movement(self, player):
        self.rect.x += (player.left - player.right) * self.delta_time * player.running
        self.rect.y += (player.up - player.down) * self.delta_time * player.running
        for inimigo in self.enemies:
            inimigo.rect.x += (player.left - player.right) * self.delta_time * player.running
            inimigo.rect.y += (player.up - player.down) * self.delta_time * player.running
        for bala in player.shots:
            bala.rect.x += (player.left - player.right) * self.delta_time * player.running
            bala.rect.y += (player.up - player.down) * self.delta_time * player.running
    
    def update(self):
        for inimigo in self.enemies:
            for bala in self.player.shots:
                if inimigo.rect.colliderect(bala):
                    inimigo.vidas -= 1
                    self.player.shots.remove(bala)
                if self.enemies and inimigo.vidas <= 0:
                    self.enemies.remove(inimigo)

    def render(self):
        self.draw()
        for inimigo in self.enemies:
            inimigo.draw()