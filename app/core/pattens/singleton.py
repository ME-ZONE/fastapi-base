class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs) -> "Singleton":
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
