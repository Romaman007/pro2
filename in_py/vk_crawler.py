import vk_api
from datetime import datetime
import requests
import sql_func
import pandas as pd


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def get_public_posts(pub_id: int):
    login, password = '+79539152617', 'Ukulele12!'
    vk_session = vk_api.VkApi(login, password, auth_handler=auth_handler)
    sql_func.create_table()
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    wall = tools.get_all_iter('wall.get', 50, {'owner_id': pub_id})
    for i in range(1000000):
        post = next(wall)
        try:
            if post['signer_id'] != post['owner_id']:
                sql_func.add_post(post['id'], post['signer_id'],
                                  datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d'), post['likes']['count'],
                                  post['comments']['count'], post['reposts']['count'], post['text'])
        except:
            try:
                sql_func.add_post(post['id'], post['owner_id'],
                                  datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d'), post['likes']['count'],
                                  post['comments']['count'], post['reposts']['count'], post['text'])
            except:
                pass


def get_data(method: str, params_method: dict, offset=0, count=200):
    params = {
        'access_token': 'vk1.a.gLDlT2EB-hLrXmwtO3uUXSqzMAdkvKesRl_R0FtbhvZIYKi4MKDdE5XIOkGkNlJSEyIF4NfTJ5zFYRGpEZ0wB6JtD8CUUdbdct2lAluFjkMruWKtbZ2gzXXa7B_u1yKrB35wxpQKX8O5apNFNtvEynPxaB0u6yTFfUC222hrVMNGQzpX945Jeszr2FS8rauj4IDr89wPRuFHUSlte-YUxg',
        'v': 5.131,
        'count': count,
        'offset': offset,
    }
    for key, item in params_method.items():
        params[key] = item
    data = []
    response = requests.get(f'https://api.vk.com/method/{method}', params=params)
    try:
        response_data = response.json()['response']['items']
        data.extend(response_data)
    except KeyError:
        pass
        params['offset'] += params['count']
    if method == 'wall.get':
        print(f'Log: Get info from owner_id: {params["owner_id"]}. He has {len(data)} posts on a wall')
    return data


def collect_search(tags: list, params: dict):
    method = 'newsfeed.search'
    params_search = params

    for i in tags:
        params_search['q'] = i
        data = get_data(method, params_search)
        for i, post in enumerate(data):
            try:
                sql_func.add_post_search(post['id'], post['owner_id'],
                                         datetime.fromtimestamp(post['date']).strftime('%Y-%m-%d'),
                                         post['likes']['count'], post['comments']['count'], post['reposts']['count'],
                                         post['text'])
            except:
                pass


def get_likes(df: pd.DataFrame, owner_id: int):
    for id in df['post_id']:
        params_get_likes = {
            'type': 'post',
            'owner_id': owner_id,
            'item_id': id,
            'friends_only': 0
        }
        method = 'likes.getList'
        data = get_data(method, params_get_likes)
        for i in data:
            try:
                sql_func.add_user_likes(i, 1, 0)
            except:
                sqll = 'UPDATE likes_comments SET likes==imp.likes+1 FROM( SELECT likes  FROM likes_comments WHERE user_id== ?) AS imp WHERE user_id== ?'
                sql_func.cur.execute(sqll, (i, i))
                sql_func.base.commit()


def get_comments(df: pd.DataFrame, owner_id: int):
    for id in df['post_id']:
        params_get_comments = {
            'preview_length': 0,
            'owner_id': owner_id,
            'post_id': id,
            'need_likes': 1,
        }
        method = 'wall.getComments'
        data = get_data(method, params_get_comments)
        for i in data:
            try:
                sql_func.add_user_likes(i['from_id'], 0, 1)
            except:
                sqll = 'UPDATE likes_comments SET comments==imp.comments+1 FROM( SELECT comments  FROM likes_comments WHERE user_id== ?) AS imp WHERE user_id== ?'
                sql_func.cur.execute(sqll, (i['from_id'], i['from_id']))
                sql_func.base.commit()


def get_comments_stat(df: pd.DataFrame, owner_id: int):
    for id in df['post_id']:
        params_get_comments = {
            'preview_length': 0,
            'owner_id': owner_id,
            'post_id': id,
            'need_likes': 1,
            'thread_items_count': 10
        }
        method = 'wall.getComments'
        data = get_data(method, params_get_comments)
        for i in data:
            lk_array = []
            try:
                for j in i['thread']['items']:
                    lk_array = []
                    try:
                        params_get_likes = {
                            'type': 'comment',
                            'owner_id': owner_id,
                            'item_id': j['id'],
                            'friends_only': 0
                        }
                        method = 'likes.getList'
                        lk_array = get_data(method, params_get_likes)
                        sql_func.add_comment(j['id'], j['from_id'], j['post_id'], j['likes']['count'], j['text'],
                                             datetime.fromtimestamp(j['date']).strftime('%Y-%m-%d'), str(lk_array))
                    except:
                        try:
                            sql_func.add_comment(j['id'], j['from_id'], j['post_id'], j['likes']['count'], j['text'],
                                                 datetime.fromtimestamp(j['date']).strftime('%Y-%m-%d'), str(lk_array))
                        except:
                            pass
            except:
                pass
            lk_array = []
            try:
                params_get_likes = {
                    'type': 'comment',
                    'owner_id': owner_id,
                    'item_id': i['id'],
                    'friends_only': 0,
                    'filter': 'likes'
                }
                method = 'likes.getList'
                lk_array = get_data(method, params_get_likes)
                sql_func.add_comment(i['id'], i['from_id'], i['post_id'], i['likes']['count'], i['text'],
                                     datetime.fromtimestamp(i['date']).strftime('%Y-%m-%d'), str(lk_array))
            except:
                try:
                    sql_func.add_comment(i['id'], i['from_id'], i['post_id'], i['likes']['count'], i['text'],
                                         datetime.fromtimestamp(i['date']).strftime('%Y-%m-%d'), str(lk_array))
                except:
                    pass
