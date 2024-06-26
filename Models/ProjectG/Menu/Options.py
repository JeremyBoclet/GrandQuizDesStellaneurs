from Models.ProjectG.Weapon.Laser import Laser
from Models.ProjectG.Weapon.Lightning import Lightning
from Models.ProjectG.Weapon.Saw import Saw
from Models.ProjectG.Weapon.Scythe import Scythe
from Models.ProjectG.Weapon.Star import Star
from Models.ProjectG.Weapon.magic_staff import magic_staff


def option_available():
    return [Laser(), Lightning(),Saw(),magic_staff(),Star(),Scythe()]


class Option:
    def __init__(self):
        self.test = 1
        option_available()

