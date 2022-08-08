import pandas as pd

DF = pd.read_csv("tests/data/titanic.csv", usecols=["Title", "CabinArea"])
COLUMN = "Title"
GROUPBY_COL = "CabinArea"
