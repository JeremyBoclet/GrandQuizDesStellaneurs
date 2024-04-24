def convert_difficulty_to_number_password(difficulty):
    match difficulty:
        case "Easy":
            return 7
        case "Medium":
            return 6
        case "Hard":
            return 5


def convert_difficulty_to_number_wordle(difficulty):
    match difficulty:
        case "Easy":
            return 5
        case "Medium":
            return 6
        case "Hard":
            return 7


def get_error_message(code_err):
    match code_err:
        case -1:
            "Aucune bonne réponse ne correspond au choix possible, vérifiez le fichier excel"
        case 1:
            return "Maximum 3 choix"
        case 2:
            return "Montant supérieur au montant restant"
        case 3:
            return "Il reste de l'argent à miser"
        case 4:
            return "Un seul choix au maximum"
        case _:
            return ""


def int_try_parse(value):
    try:
        return int(value)
    except ValueError:
        return None
