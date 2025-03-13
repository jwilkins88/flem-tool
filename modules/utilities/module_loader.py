# pylint: disable=import-error
import modules as loaded_modules

# pylint: enable=import-error

from models import ModuleConfig


def load_module(module_config: ModuleConfig):
    """
    Loads and initializes a module based on the provided configuration.

    Args:
        module_config (ModuleConfig): The configuration object for the module to be loaded.

    Returns:
        object: An instance of the loaded module if found, otherwise None.

    Raises:
        KeyError: If the module type specified in the configuration is not found in loaded_modules.
    """
    print(loaded_modules)
    if module_config.module_type in loaded_modules.__dict__:
        return loaded_modules.__dict__[module_config.module_type](module_config)

    print(f"Module {module_config.module_type} not found")
    return None
