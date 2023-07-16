from Models.Bdd import Bdd


class Players:
    def __init__(self, name, main_category_id):
        self.name = name
        self.bdd = Bdd()
        self.total_point = 0
        self.get_players_point()
        self.main_category_id = main_category_id

    def add_point(self, point):
        self.total_point += point

    def get_players_point(self):
        df = self.bdd.request_query("SELECT PlayerPoint FROM GrandQuiz.dbo.Players WHERE PlayerName = '{}'".
                                    format(self.name))
        df.reset_index()

        for index, row in df.iterrows():
            self.total_point = row["PlayerPoint"]
