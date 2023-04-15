import sql_func
import pandas as pd


def test_wall():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from priznavashki", sql_func.base)
    assert len(df) == 40090


def test_comments():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from all_comments", sql_func.base)
    assert len(df) == 11


def test_likes_comments():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from likes_comments", sql_func.base)
    assert len(df) == 27505


def test_users_main():
    sql_func.sql_start()
    df = pd.read_sql_query("SELECT * from users_main", sql_func.base)
    assert len(df) == 461

