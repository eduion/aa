import pandas as pd
import pymysql
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy import dot
from numpy.linalg import norm
import datetime

# 連線資料庫
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='what_should_i_eat')
cursor = db.cursor()


def get_pd(tabel_name, index, uID):
    # 取得資料
    if (uID != "NULL"):
        sql = f"SELECT * FROM {tabel_name} WHERE uID = {uID}"
    else:
        sql = f"SELECT * FROM {tabel_name}"
    cursor.execute(sql)
    result = cursor.fetchall()  # tuple
    # 查欄位名稱
    sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{tabel_name}'"
    cursor.execute(sql)
    columns = [row[0] for row in cursor.fetchall()]
    # tuple 轉 pd
    result = pd.DataFrame(result, columns=columns)
    if (index != 'NULL'):
        result.set_index(index, inplace=True)
    # print(result)
    return result


def selectCount(tabel_name):
    sql = f"SELECT COUNT(*) FROM {tabel_name}"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result[0][0]


def GoFilter(Restaurant, TimeFilter, MealFilter, LabelFilter, NewRLabel):
    # print(len(Restaurant))
    # 營業時間
    if (TimeFilter == True):
        # print(len(Restaurant), 'Time')
        Restaurant = checkTime(Restaurant)
    # 正餐
    if (MealFilter == 1):
        # print(len(Restaurant), 'Meal')
        Restaurant = Restaurant[Restaurant['meal_or_not'] == 1]
    if (MealFilter == 0):
        # print(len(Restaurant), 'NOT Meal')
        Restaurant = Restaurant[Restaurant['meal_or_not'] == 0]
    # 類別
    if (LabelFilter != '全部'):
        # print(len(Restaurant), '!=全部')
        for rID in Restaurant:
            if ((NewRLabel.loc[rID, LabelFilter] == 0) and (rID in Restaurant.index)):
                Restaurant = Restaurant.drop(rID)
    # print(len(Restaurant))
    return Restaurant


def checkTime(Restaurant):
    date = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    day_of_week = datetime.datetime.today().weekday()
    currentTime = datetime.datetime.now().time()
    for index, row in Restaurant.iterrows():
        rID = index
        # print(rID)
        RestaurantTime = row[date[day_of_week]].split(';')
        openCheck = [False] * len(RestaurantTime)
        # print(RestaurantTime)
        for index, eachTime in enumerate(RestaurantTime):
            eachTime = eachTime.strip().split('~')
            # print(eachTime)
            if (eachTime != ['']):
                start_time = datetime.time(int(eachTime[0].split(':')[0]), int(eachTime[0].split(':')[1][0]),
                                           int(eachTime[0].split(':')[1][1]))
                # print(eachTime[0].split(':')[0])
                # print(eachTime[0].split(':')[1][0])
                # print(eachTime[0].split(':')[1][1])
                end_time = datetime.time(int(eachTime[1].split(':')[0]), int(eachTime[1].split(':')[1][0]),
                                         int(eachTime[1].split(':')[1][1]))
                if (start_time <= currentTime <= end_time):
                    openCheck[index] = True
                else:
                    openCheck[index] = False
        # print(openCheck)
        if (True not in openCheck):
            Restaurant = Restaurant.drop(index=rID)
    return Restaurant


def RecommenderInit(uID, recommend_num, UserLike, NewRLabel):
    # 餘弦算相似度
    SimilarityMatrix = cosine_similarity(UserLike.values, NewRLabel.values)
    SimilarityMatrix = pd.DataFrame(SimilarityMatrix, index=UserLike.index, columns=NewRLabel.index)
    result = get_the_most_similar_res(uID, SimilarityMatrix, recommend_num)
    return result


def RecommenderContent(uID, recommend_num, NewRLabel, CostDetail):
    # user vector
    resRating = pd.merge(CostDetail[["uID", "rID"]], NewRLabel, on='rID')
    # print(resRating)
    resRating.drop(['rID'], axis=1, inplace=True)
    # print(resRating)
    user_vec = resRating.groupby("uID").mean()
    # 餘弦算相似度
    SimilarityMatrix = cosine_similarity(user_vec.values, NewRLabel.values)
    SimilarityMatrix = pd.DataFrame(SimilarityMatrix, index=user_vec.index, columns=NewRLabel.index)
    result = get_the_most_similar_res(uID, SimilarityMatrix, recommend_num)
    return result


def get_the_most_similar_res(uID, SimilarityMatrix, recommend_num):
    # Get the most similar restaurant
    # Find the top-n restaurant most similar to the user
    user_like = SimilarityMatrix.loc[uID].values
    SortedIndex = np.argsort(user_like)[::-1][:recommend_num]
    result = (list(SimilarityMatrix.columns[SortedIndex]))
    return result


def RecommenderUserBasedCollaborativeFiltering(uID, SimilarUsers_num, recommend_num, NewRLabel, CostDetail):
    resRating = pd.merge(CostDetail[["uID", "rID", "rating"]], NewRLabel, on='rID')
    # Calculate the similarity between the user and other users
    similarities = []
    user_ids = []
    for other_user in resRating.uID.unique():
        if other_user == uID:
            continue
        common_res = find_common_res(uID, other_user, resRating)
        if len(common_res) < 10:
            sim = 0
        else:
            # 尚未測試
            print('hello')
            sim = cal_similarity_for_res_ratings(uID, other_user, common_res, resRating)
        similarities.append(sim)
        user_ids.append(other_user)
    # Find top n similar users
    similarities, user_ids = np.array(similarities), np.array(user_ids)
    sorted_index = (np.argsort(similarities)[::-1][:SimilarUsers_num]).tolist()
    most_similar_users = user_ids[sorted_index].tolist()
    result = recommend(uID, most_similar_users, recommend_num, resRating)
    return result


def find_common_res(user1, user2, df):
    # Find restaurant that both users have watched
    s1 = set((df.loc[df["uID"] == user1, "rID"].values))
    s2 = set((df.loc[df["uID"] == user2, "rID"].values))
    # return 交集的元素
    return s1.intersection(s2)


def cal_similarity_for_res_ratings(user1, user2, res_id, df, method="cosine"):
    # Calculate the similarity for res ratings between user1 and user2
    u1 = df[df["uID"] == user1]
    u2 = df[df["uID"] == user2]
    vec1 = u1[u1.rID.isin(res_id)].sort_values(by="rID")["rating"].values
    vec2 = u2[u2.rID.isin(res_id)].sort_values(by="rID")["rating"].values
    # cosine
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def recommend(uID, similar_users, recommend_num, df):
    # Find the restaurant the user hasn't seen and the similar users have seen.
    seen_res = np.unique(df.loc[df["uID"] == uID, "rID"].values)
    not_seen_res = df["rID"].isin(seen_res) == False
    similar_res = df["uID"].isin(similar_users)
    # 沒吃過且相似
    not_seen_res_ratings = df[not_seen_res & similar_res][["rID", "rating"]]
    # Find average ratings by the most similar users
    average_ratings = not_seen_res_ratings.groupby("rID").mean()
    top_ratings = average_ratings.sort_values(by="rating", ascending=False).iloc[:recommend_num]
    return top_ratings.index.tolist()


def GoMerge(init, content, filtering):
    score = [0 for x in range(max(init))]
    tempResult = {}
    result = []
    # print(len(score))
    recommend = [init, content, filtering]
    for aList in recommend:
        # print(aList)
        for point, restaurant in enumerate(aList):
            score[restaurant - 1] += point
    afterSorted = sorted(score)
    for restaurant, point in enumerate(afterSorted):
        if (point != 0):
            # rID rScore
            tempResult[score.index(point) + 1] = point
    for key, value in tempResult.items():
        result.append(key)
    return result


def GoSorted(DistanceSort, RatingSort, Restaurant):
    # 距離
    # 評分
    if (RatingSort):
        result = Restaurant.sort_values(by="rMap_Score", ascending=False)
        result = result.index.tolist()
    else:
        return ['distance sorted coding...']
    return result

def main(uID, TimeFilter, MealFilter, LabelFilter, DistanceSort, RatingSort):
    print(uID, TimeFilter, MealFilter, LabelFilter, DistanceSort, RatingSort)
    Restaurant = get_pd('1_restaurant', "rID", "NULL")
    NewRLabel = get_pd('1_new_rlabel', 'rID', "NULL")
    UserLike = get_pd('1_user_like', 'uID', uID)
    CostDetail = get_pd('1_cost_detail', 'cID', "NULL")
    uNum = selectCount('1_user_info')

    # 過濾 -> 推薦 or 排序 -> output
    FilterResult = GoFilter(Restaurant, TimeFilter, MealFilter, LabelFilter, NewRLabel)
    # print(FilterResult)

    if (DistanceSort or RatingSort):
        RecommenderResult = GoSorted(DistanceSort, RatingSort, FilterResult)
        return RecommenderResult
    else:
        # 如果這個人沒有記帳紀錄
        if (True not in list(CostDetail['uID'] != uID)):
            # print('no cost')
            # uID, recommend_num, UserLike, NewRLabel
            RecommenderResult = RecommenderInit(uID, len(FilterResult), UserLike, NewRLabel)
            return RecommenderResult
        else:
            init = RecommenderInit(uID, len(FilterResult), UserLike, NewRLabel)
            content = RecommenderContent(uID, len(FilterResult), NewRLabel, CostDetail)
            filtering = RecommenderUserBasedCollaborativeFiltering(uID, uNum, len(FilterResult), NewRLabel, CostDetail)
            # (init)
            # print(content)
            # print(filtering)
            RecommenderResult = GoMerge(init, content, filtering)
            return RecommenderResult
    # print(FinalResult)
    db.close

#
# if __name__ == '__main__':
#     main()