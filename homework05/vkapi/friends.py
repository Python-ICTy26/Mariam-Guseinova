import dataclasses
import math
import time
import typing as tp
from time import sleep

from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError
from vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    current_session = Session(base_url=VK_CONFIG["domain"])
    data = {
        "access_token": VK_CONFIG["access_token"],
        "user_id": str(user_id),
        "count": str(count),
        "offset": str(offset),
        "fields": fields,
        "v": VK_CONFIG["version"],
    }
    query = "friends.get"
    response = current_session.get(query, query=data)
    json = response.json()
    return FriendsResponse(json["response"]["count"], json["response"]["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[dict]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.
    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Список идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    current_session = Session(base_url=VK_CONFIG["domain"])
    data = {
        "access_token": VK_CONFIG["access_token"],
        "source_uid": source_uid,
        "target_uid": target_uid,
        "target_uids": target_uids,
        "order": order,
        "count": count,
        "offset": 0,
        "v": VK_CONFIG["version"],
    }
    answer = []
    query = "friends.getMutual"
    for i in range((len(target_uids) / 100).__ceil__() if target_uids else 1):
        data["offset"] = i * 100
        response = current_session.get(query, params=data)
        json = response.json()
        answer += json["response"]
        if i % 2 == 0:
            sleep(1)
    return answer
