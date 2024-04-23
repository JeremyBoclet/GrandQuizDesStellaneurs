from Models.Questions import Questions


class MoneyDropQuestion(Questions):
    def __init__(self, question, answer, guess_A, guess_B, guess_C, guess_D):
        super().__init__(question, answer, "", "", "")
        self.guess_A = guess_A
        self.guess_B = guess_B
        self.guess_C = guess_C
        self.guess_D = guess_D
