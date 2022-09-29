class Dispatcher:
    def __init__(self):
        self.dispatch_functions = []

    def register(self, *args):
        for function in args:
            self.dispatch_functions.append(function)

    def dispatch(self, tokens):
        """
        Dispatches the tokens to the registered functions, stopping after one function handles
        the request.
        """
        for function in self.dispatch_functions:
            match function(tokens):
                case ["respond", response]:
                    return response

        return "I don't know how to answer that."
