import sql_func
import vk_crawler
import pandas as pd


def main():

    # запускаем бд

    sql_func.sql_start()

    # парсим признавашки

    owner_id = -59518047
    vk_crawler.get_public_posts(owner_id)

    # собираем информацию по лайкам, комментариям

    df = pd.read_sql_query("SELECT * from users_main", sql_func.base)
    vk_crawler.get_likes(df, owner_id)
    vk_crawler.get_comments(df, owner_id)

    # собираем все комментарии и их статистику

    vk_crawler.get_comments_stat(df, owner_id)
