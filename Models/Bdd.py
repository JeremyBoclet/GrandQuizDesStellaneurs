from collections import OrderedDict
from pyexcel_ods import save_data
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


class Bdd:
    def __init__(self):
        self.connect = "oui"
       # self.connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};Server=WEP-LP-JBL;Database=Snake;Trusted_Connection=yes;")
       # connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": "DRIVER={ODBC Driver 17 for SQL Server};Server=WEP-LP-JBL;Database=Snake;Trusted_Connection=yes;"})
       #  self.engine = create_engine(connection_url)

    def execute_query(self, query):
        self.connection.cursor().execute(query)
        self.connection.commit()

    def get_question(self, category_id):
        query = "SELECT Question, Answer, Questions.Category_ID, Category_Question.Category_Name, TypeQuestion, PathExternalQuestion, ExternalName FROM GrandQuiz.dbo.Questions INNER JOIN GrandQuiz.dbo.Category_Question on Category_Question.Category_ID = Questions.Category_ID WHERE Questions.Category_ID = {} AND Question_ID < 1000 ORDER BY NEWID()".format(category_id)
        print(query)
        df = pd.read_sql(query, self.engine)
        return df

    def get_question_round3(self, category_id):
        query = "SELECT Question, Answer, Questions.Category_ID, Category_Question.Category_Name, TypeQuestion, " \
                "PathExternalQuestion, ExternalName FROM GrandQuiz.dbo.Questions INNER JOIN GrandQuiz.dbo.Category_Question on " \
                "Category_Question.Category_ID = Questions.Category_ID WHERE Questions.Category_ID = {} AND " \
                "Question_ID > 2000 ORDER BY NEWID()".format(
            category_id)
        df = pd.read_sql(query, self.engine)
        return df

    def get_final_question(self, question_id):
        query = "SELECT Question, Answer, Questions.Category_ID, Category_Question.Category_Name, TypeQuestion, " \
                "PathExternalQuestion, ExternalName FROM GrandQuiz.dbo.Questions INNER JOIN GrandQuiz.dbo.Category_Question on " \
                "Category_Question.Category_ID = Questions.Category_ID WHERE Question_ID = {}".format(question_id)
        df = pd.read_sql(query, self.engine)
        return df

    def request_query(self, query):
        df = pd.read_sql(query, self.engine)
        return df

    def read_excel(self, sheet_name):
        df = pd.read_excel(r"C:\Developpement\GrandQuizDesStellaneurs\GrandQUizDesStellaneurs\Questions.ods", sheet_name)
        df = df.sample(frac=1)
        return df

    def get_players(self):
        df = pd.read_excel(r"C:\Developpement\GrandQuizDesStellaneurs\GrandQUizDesStellaneurs\Players.ods",
                           "Players")
        return df

    def write_points(self,point,player):
        # First read into dataframe
        df = pd.read_excel(r"C:\Developpement\GrandQuizDesStellaneurs\GrandQUizDesStellaneurs\Players.ods",
                           "Players")

        # Change everything to string since we're just writing
        df = df.astype(str)
        # Initiliaze data to be written as an empty list, as pyods needs a list to write
        whole_data_list = []
        # Initiliaze the empty dict() for the data
        d = OrderedDict()
        whole_data_list.append(["PlayerName", "Main_Category", "Player_Points"])
        # loop through data frame and update the data list
        for index, row in df.iterrows():
            if row["PlayerName"] == player:
                row["Player_Points"] = point

            whole_data_list.append(list(row.values))

        # Populate dict() with updated data list
        d.update({"Players": whole_data_list})
        # Finally call save_data() from pyods to store the ods file
        save_data(r"C:\Developpement\GrandQuizDesStellaneurs\GrandQUizDesStellaneurs\Players.ods", d)
        # save_ods_from_excel('/Users/gkm/Downloads/Financial Sample.xlsx', '/tmp/sample-financial.ods')