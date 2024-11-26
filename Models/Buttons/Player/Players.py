from Models.Bdd import Bdd


class Players:
    def __init__(self, name, main_category_id):
        self.name = name
        self.bdd = Bdd()
        self.total_point = 0
        self.get_players_point()
        self.main_category_id = main_category_id
        self.maximum_md_point = 400
        self.remaining_md_point = self.maximum_md_point

    def add_point(self, point):
        self.total_point += point

    def set_md_point(self, point):
        self.maximum_md_point = point
        self.remaining_md_point = point

    def get_players_point(self):
        df = self.bdd.get_players()
        # df = self.bdd.request_query("SELECT PlayerPoint FROM GrandQuiz.dbo.Players WHERE PlayerName = '{}'".
        #                            format(self.name))
        df.reset_index()

        for index, row in df.iterrows():
            if row["PlayerName"] == self.name:
                self.total_point = row["Player_Points"]
                break
