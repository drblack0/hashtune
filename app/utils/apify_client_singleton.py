from apify_client import ApifyClientAsync


class ApifyClientSingleton:
    _instance = None

    def __new__(cls, token: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = ApifyClientAsync(token=token)
        return cls._instance

    def get_client(self) -> ApifyClientAsync:
        return self.client
