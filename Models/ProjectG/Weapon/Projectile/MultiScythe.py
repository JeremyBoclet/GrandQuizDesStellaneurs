from Models.ProjectG.Weapon.Projectile.Projectile_Scythe import Projectile_Scythe


class MultiScythe:
    def __init__(self, weapon, player, num_projectiles):
        self.player = player
        self.num_projectiles = num_projectiles
        self.weapon = weapon

        angle_gap = 360 / num_projectiles
        for i in range(num_projectiles):
            initial_angle = i * angle_gap
            projectile = Projectile_Scythe(self.weapon, player,initial_angle)
            self.weapon.projectile.add(projectile)
