from Models.ProjectG.Weapon.Bomb import Bomb
from Models.ProjectG.Weapon.FallingStar import FallingStar
from Models.ProjectG.Weapon.Laser import Laser
from Models.ProjectG.Weapon.Lightning import Lightning
from Models.ProjectG.Weapon.Saw import Saw
from Models.ProjectG.Weapon.Scythe import Scythe
from Models.ProjectG.Weapon.Star import Star
from Models.ProjectG.Weapon.magic_staff import magic_staff


class Options:
    def __init__(self, weapons):
        self.option_available = [Bomb(), FallingStar(),magic_staff(), Saw()]

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
                break

    def set_next_upgrade(self,option_to_change):
        for option in self.option_available:
            if option.name == option_to_change:
                option.set_next_upgrade()
                option.current_level += 1

