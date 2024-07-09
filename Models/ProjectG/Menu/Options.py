from Models.ProjectG.Loots.RegenHealth import RegenHealth
from Models.ProjectG.Weapon.MainWeapon.Bomb import Bomb
from Models.ProjectG.Weapon.MainWeapon.FallingStar import FallingStar
from Models.ProjectG.Weapon.MainWeapon.Laser import Laser
from Models.ProjectG.Weapon.MainWeapon.Lightning import Lightning
from Models.ProjectG.Weapon.MainWeapon.Saw import Saw
from Models.ProjectG.Weapon.MainWeapon.Scythe import Scythe
from Models.ProjectG.Weapon.MainWeapon.Star import Star
from Models.ProjectG.Weapon.MainWeapon.magic_staff import magic_staff


class Options:
    def __init__(self, weapons):
        # Bomb(), FallingStar(),magic_staff(), Saw(), Lightning(),Laser(), Star(),Scythe()
        self.option_available = [Bomb(), FallingStar(),magic_staff(), Saw(), Lightning(),Laser(), Star(),Scythe()]

        # Construire un dictionnaire des options disponibles
        options_dict = {option.name: option for option in self.option_available}

        # Parcourir les armes et mettre à jour les options correspondantes (en cas de présence de l'arme sur le joueur)
        for weapon in weapons:
            if weapon.name in options_dict:
                self.set_next_upgrade(weapon.name)

    def remove_option(self, option_to_delete):
        for option in self.option_available:
            if option.name == option_to_delete:
                self.option_available.remove(option)
                if len(self.option_available) == 0:
                    self.option_available.append(RegenHealth(1, 1))
                break

    def set_next_upgrade(self, option_to_change):
        for option in self.option_available:
            if option.name == option_to_change:
                option.set_next_upgrade()
                option.current_level += 1
