# https://www.geeksforgeeks.org/python/define-custom-exceptions-in-python/
class PlatformError(Exception):
    """
    Exception raised for detecting an invalid platform.
    """
    def __init__(self):
        super().__init__("Invalid operating system!")

class StatsError(Exception):
    """
    Exception raised for reading stats unsuccessfully.
    """
    def __init__(self):
        super().__init__("All of the needed stats have not been read successfully!")

class ConstantError(Exception):
    """
    Exception raised for reading stats unsuccessfully.
    """
    def __init__(self, variable, value):
        super().__init__(f"The chosen {variable} value is unavailable: {value}")
