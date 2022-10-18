from dataclasses import dataclass, asdict, field


class Builder:

    @staticmethod
    def auth(email=None, password=None):
        @dataclass
        class Auth:
            email: str
            password: str
            failure: str = "https://account.my.com/login/"

        return asdict(Auth(email=email, password=password))

    @staticmethod
    def campaign(name=None):
        @dataclass
        class Campaign:
            name: str = "test"
            objective: str = "traffic"
            package_id: int = 961
            banners: list = field(default_factory=lambda:
            [
                {
                    "urls": {
                        "primary": {
                            "id": 0
                        }
                    },
                    "textblocks": {},
                    "content": {
                        "image_240x400": {
                            "id": 0
                        }
                    },
                    "name": ""
                }
            ])
        return asdict(Campaign(name=name))

    @staticmethod
    def segment(name=None):
        @dataclass
        class Segment:
            name: str = "test"
            pass_condition: int = 1
            relations: list = field(default_factory=lambda:
            [
                {
                    "object_type": "remarketing_player",
                    "params": {}
                }
            ])
            logic_type: str = "or"
        return asdict(Segment(name=name))

    @staticmethod
    def params_default():
        @dataclass
        class Params:
            type: str = 'positive'
            left: int = 365
            right: int = 0
        return asdict(Params())

    @staticmethod
    def params_source_group(group_object_id: int):
        @dataclass
        class Params:
            source_id: int = group_object_id
            type: str = 'positive'

        return asdict(Params())
