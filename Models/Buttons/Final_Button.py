import pygame


class Final_Button(pygame.sprite.Sprite):
    def __init__(self, name, category_id, x, y, question_num, real_category_id):
        super().__init__()
        self.name = name
        self.category_id = category_id
        self.read_category_id = real_category_id
        self.image = pygame.image.load("Assets/Finale/{}.png".format(name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (125, 125)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.SysFont("Verdana", 50)
        self.question_number = self.font.render(str(question_num)
                                                , True,
                                                (0, 0, 0))
        self.num = question_num
        self.had_been_chosen = False

    def get_rect(self):
        return self.rect

    def get_question_num(self):
        return self.question_number

    def get_num(self):
        return self.num
