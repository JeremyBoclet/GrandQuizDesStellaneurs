from Models.ProjectG.Weapon.Laser import Laser
from Models.ProjectG.Weapon.Lightning import Lightning
from Models.ProjectG.Weapon.Saw import Saw
from Models.ProjectG.Weapon.Scythe import Scythe
from Models.ProjectG.Weapon.Star import Star
from Models.ProjectG.Weapon.magic_staff import magic_staff


class Options:
    def __init__(self):
        self.option_available = [magic_staff(), Star(), Scythe()]

    def remove_option(self, option_to_delete):
        for option in self.option_available:
            if option.name == option_to_delete:
                self.option_available.remove(option)
                break
