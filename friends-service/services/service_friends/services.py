import httpx
from django.conf import settings


class MicroserviceClient:
    """
    Клиент для запросов в микросервисы.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get_data_from_microservice(
            self,
            endpoint,
            headers=None,
            params=None,
            *args,
            **kwargs
    ):

        url = settings.PROFILE_MICROSERVICE_URL

        try:
            with httpx.Client() as client:
                response = client.get(
                    f'{url}{endpoint}',
                    headers=headers,
                    params=params,
                    timeout=5.0)
            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}
        except httpx.TimeoutException as timeout_err:
            return {"error": "Timeout occurred", "details": str(timeout_err)}
        except httpx.RequestError as req_err:
            return {"error": "Request error", "details": str(req_err)}


class ProfileMicroserviceClient(MicroserviceClient):
    """
    Клиент для соединения с микросервисом Profile.
    """

    def __init__(self):
        default_base_url = settings.PROFILE_MICROSERVICE_URL
        super().__init__(default_base_url)
