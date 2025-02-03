from dataclasses import dataclass

@dataclass(init=False)
class CallbackDataBuilder:
    prefix: str
    args: list[str]
    named_args: dict

    def __init__(self, prefix, *args: str, **kwargs):
        self.prefix = prefix
        self.args = list(args)
        self.named_args = {}

        for key in kwargs.keys():
            self.named_args[key] = kwargs[key]

    @staticmethod
    def parse(data):
        if ":" in data:
            prefix, args = data.split(":", 1)
            anonymous_args = []
            named_args = {}
            for arg in args.split("|"):
                if "=" in arg:
                    key, value = arg.split("=")
                    named_args[key] = value
                else:
                    anonymous_args.append(arg)

            return CallbackDataBuilder(prefix, *anonymous_args, **named_args)
        else:
            return CallbackDataBuilder(data)

    def build(self):
        if not (self.args + list(self.named_args.keys())):
            return self.prefix
        string = f"{self.prefix}:"
        string += "|".join(self.args)
        string += "|" if self.args and self.named_args else ""
        string += "|".join([f"{key}={self.named_args[key]}" for key in self.named_args.keys()])
        return string

    def __getitem__(self, item):
        if item in self.named_args.keys():
            return self.named_args[item]
        else:
            return None

def callback_data(prefix, *args, **kwargs):
    return CallbackDataBuilder(prefix, *args, **kwargs).build()

def parse_callback_data(data):
    return CallbackDataBuilder.parse(data)

