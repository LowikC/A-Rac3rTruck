from context import atruck
from atruck.CommandFactory import CommandFactory


if __name__ == "__main__":
    cmd_desc = {"name": "DummyCommand",
                "kwargs": {
                    "dummy_args": 1
                }}
    cmd = CommandFactory.from_dict(cmd_desc)
    cmd.run(None)
