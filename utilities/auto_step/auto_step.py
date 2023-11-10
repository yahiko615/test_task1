import inspect

import allure


def autostep(cls):
    """
                The auto_step decorator is designed to automatically wrap class methods in Allure report steps.

                Parameters:
                - cls: The class whose methods will be automatically wrapped in Allure steps.

                Returns:
                - Returns the class with methods wrapped in Allure steps.

                Note:
                - Methods whose names start with an underscore (_) are not wrapped in Allure steps.

                """
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if not name.startswith('_'):
            setattr(cls, name, allure.step(method))
    return cls
