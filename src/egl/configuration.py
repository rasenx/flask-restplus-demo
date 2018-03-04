import os
import collections
import yaml


class ConfigurationEnvironmentError(ValueError):
    pass


class ConfigurationError(ValueError):

    def __init__(self, arg_var, env_var):
        self.message = "Argument '{}' or environment variable '{}' are required.".format(arg_var, env_var)

    def __str__(self):
        return self.message


def load_config_file(file):
    with open(file, 'r') as stream:
        for data in yaml.load_all(stream):
            yield data


def load_config_files(directory, files):
    for name in files:
        file = os.path.join(directory, name)
        if os.path.isfile(file):
            yield from load_config_file(file)
        else:
            pass


def merge(a: dict, b: dict) -> dict:
    if b:
        for k, v in b.items():
            if isinstance(v, collections.Mapping):
                key = a.get(k, {})
                result = merge(key, v)
                a[k] = result
            else:
                a[k] = b[k]
    return a


class Configuration:

    def __init__(self, directory=None, files=None, environment=None, environments=None):

        # the directory we will load from
        self.directory = directory or os.environ.get('CONFIG_DIR')
        if not self.directory:
            raise ConfigurationError('directory', 'CONFIG_DIR')

        # the files we will load
        self.files = files or os.environ.get('CONFIG_FILES') or ['config.yml', 'localhost.yml', 'secrets.yml']
        if not self.files:
            raise ConfigurationError('files', 'CONFIG_FILES')

        # the environments we will support
        self.environments = environments or os.environ.get('CONFIG_ENVS') or ['production', 'staging', 'development', 'testing']
        if not self.environments:
            raise ConfigurationError('environments', 'CONFIG_ENVS')

        # the current environment
        self.environment = environment or os.environ.get('CONFIG_ENV') or 'development'
        if not self.environment:
            raise ConfigurationError('environment', 'CONFIG_ENV')

        # make sure environment is one of the items in environments
        if self.environment not in self.environments:
            raise ConfigurationEnvironmentError("The environment '{}' is not in environments list: {}".format(self.environment, self.environments))

        self.config_files = []
        self.configs = {}
        self.reload()

    def reload(self):
        self.config_files = list(load_config_files(self.directory, self.files))
        self.configs = {}
        baseline = {}

        # load configs for each environment, each environment is the baseline for the next
        for environment in self.environments:
            # build a config for that environment, inheriting from the last baseline config, this becomes the new baseline
            baseline = self._build_config(environment, baseline)

            # save that environment's config
            self.configs[environment] = baseline

    def get(self, path=None, default=None, environment='development', exceptions=False):

        config = self.configs[environment]

        if path:
            keys = path.split('.')
            for key in keys:
                try:
                    # walk down the key path into the config until the last key is found
                    config = config[int(key)] if key.isdigit() else config[key]
                except KeyError:
                    if exceptions:
                        raise
                    config = None
                    break

        return config if config is not None else default

    def _build_config(self, environment='development', baseline=None):

        # clone baseline
        config = merge({}, baseline)

        # merge in the environment keys from all discovered config files
        for config_file in self.config_files:
            if environment in config_file:
                merge(config, config_file[environment])

        return config

