import configparser
import os


class Configuration:
    def __init__(self):
        self.settings, self.upgrades = self.load_config()

    def load_config(self):
        # Créer un objet ConfigParser
        config = configparser.ConfigParser()
        config_file = "../Models/ProjectG/ExternalFiles/config.ini"

        # Lire le fichier de configuration
        if not os.path.isfile(config_file):
            raise FileNotFoundError(f"The configuration file {config_file} does not exist.")

        config.read(config_file)

        # Extraire les valeurs de configuration
        settings = {
            'WIDTH': config.getint('settings', 'WIDTH'),
            'HEIGHT': config.getint('settings', 'HEIGHT'),
        }

        upgrades = {
            'ADD_PROJECTILE': "Augmente le nombre de projectile de {}",
            'REDUCE_COOLDOWN': "Réduction du cooldown",
            'PROJECTILE_SPEED_INCREASED': "Vitesse de projectile augmenté",
            'DAMAGE_INCREASED': "Dégats augmentés",
            'BOUNCE_INCREASED': "Nombre de rebond augmenté de {}"
        }

        return settings, upgrades

