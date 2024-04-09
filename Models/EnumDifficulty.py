def convert_difficulty_to_number(difficulty):
    match difficulty:
        case "Easy":
            return 7
        case "Medium":
            return 6
        case "Hard":
            return 5
