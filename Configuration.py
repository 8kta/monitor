import configparser


class Configuration:
    _instance = None

    def __init__(self):
        self._source = None
        self._target = None
        self._owner = None
        self._group = None
        self._separator = None
        self._not_required = None
        self._loaded = False

    def load(self):
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read('config.ini')

        self._source = config['directories']['source']
        self._target = config['directories']['target']
        self._owner = config['permissions']['owner']
        self._group = config['permissions']['group']
        self._not_required = config['filters']['not_required'].split(",")

        if config['OS']['os'] == 'unix':
            self._separator = "/"
        else:
            self._separator = "\\"

        self._loaded = True

    def singleton(self):
        if self._loaded is False:
            self.load()
        else:
            return self

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def get_source(self):
        self.singleton()
        return self._source

    def get_target(self):
        self.singleton()
        return self._target

    def get_owner(self):
        self.singleton()
        return self._owner

    def get_group(self):
        self.singleton()
        return self._group

    def get_separator(self):
        self.singleton()
        return self._separator

    def get_not_required(self):
        self.singleton()
        return self._not_required


