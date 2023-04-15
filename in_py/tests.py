import sql_func
import pandas as pd


def test_wall():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from priznavashki", sql_func.base)
    assert len(df) == 40090