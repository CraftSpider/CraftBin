"""
    Holds various state and config for the rest of the package
"""

import pathlib


_DEFAULT_RESOURCE_PATH = pathlib.Path("./assets")


class Config:

    def __init__(self, settings=None):
        self.resource_path = _DEFAULT_RESOURCE_PATH
        self.block_size = 16
        self.models = {}
        self.blockstates = {}

        self.schematic = None

        if settings is not None:
            self.__dict__.update(settings)

    @property
    def ef_size(self):
        return self.block_size + 1


DEFAULT_CONFIG = Config()
_CUR_CONFIG = DEFAULT_CONFIG


def get_config():
    return _CUR_CONFIG


def set_config(config):
    global _CUR_CONFIG
    _CUR_CONFIG = config
