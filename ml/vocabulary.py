class Vocabulary:
    def __init__(self):
        self.tokens = []

    def build(self, values):
        # TODO: Implement vocabulary construction.
        self.tokens = list(values)
        return self
