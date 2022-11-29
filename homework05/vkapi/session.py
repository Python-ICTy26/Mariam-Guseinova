import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Session:
    """
    Сессия.
    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self._session = requests.Session()
        self._session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=max_retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
            ),
        )
        self._base_url = base_url
        self._timeout = timeout

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self._session.get(self._base_url + "/" + url, params=kwargs, timeout=self._timeout)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self._session.post(self._base_url + "/" + url, data=kwargs)
