class Inventory:
    def __init__(self, player, screen):
        self.player = player
        # [Laser(), Lightning(),Saw(),magic_staff(),Star(),Scythe(), Bomb()]
        self.weapons = []
        self.screen = screen
        self.enemy_targeted = None

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def set_enemy(self, enemy):
        self.enemy_targeted = enemy

    def update(self):
        for item in self.weapons:
            item.update(self.player, self.enemy_targeted)
            if item.show_image:
                item.projectile.draw(self.screen)

