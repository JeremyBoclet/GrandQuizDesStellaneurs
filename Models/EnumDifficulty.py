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
