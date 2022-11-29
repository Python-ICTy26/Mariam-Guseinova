import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, fields=["bdate"]).items
    ages = []
    for friend in friends:
        if "bdate" in friend:
            bdate = friend["bdate"].split(".")
            if len(bdate) == 3:
                age = dt.datetime.now().year - int(bdate[2])
                if dt.datetime.now().month < int(bdate[1]) and dt.datetime.now().day < int(
                    bdate[0]
                ):
                    age -= 1
                ages.append(age)

    if len(ages) == 0:
        return None
    return statistics.median(ages)
