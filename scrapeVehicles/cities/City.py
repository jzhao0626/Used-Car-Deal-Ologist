class City:
    """A simple example class"""

    name = None
    state = None
    url = None

    def __init__(self, name, state, url):
        self.name = name
        self.state = state
        self.url = url

    def __str__(self):
        return f"{self.name}, {self.state}: {self.state}"
