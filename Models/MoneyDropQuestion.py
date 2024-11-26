from Models.Questions import Questions


class MoneyDropQuestion(Questions):
    def __init__(self, question, answer, guess_A, guess_B, guess_C, guess_D,external_path,type_question):
        super().__init__(question, answer, "", "", "")
        self.guess_A = guess_A
        self.guess_B = guess_B
        self.guess_C = guess_C
        self.guess_D = guess_D
        self.external_path = external_path
        self.type_question = type_question
