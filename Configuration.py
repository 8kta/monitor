import configparser


class Configuration:
    _instance = None

    def __init__(self):
        self._source = None
        self._target = None
        self._loaded = False

    def load(self):
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read('config.ini')

        self._source = config['directories']['source']
        self._target = config['directories']['target']

        self._loaded = True

    def singleton(self):
        if self._loaded is False:
            self.load()
        else:
            return self

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            # cls._instance.value = None
        return cls._instance

    # def set_value(self, value):
    #     self.value = value
    #
    # def get_value(self):
    #     return self.value

    def get_source(self):
        self.singleton()
        return self._source

    def get_target(self):
        self.singleton()
        return self._target


