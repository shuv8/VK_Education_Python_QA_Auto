"""Module of static json builder"""

from dataclasses import dataclass, asdict


class Builder:
    """Builder class"""

    @staticmethod
    def capability(apk: str):
        """Capability static method"""

        @dataclass
        class Capability:
            """Capability data class"""

            platformName: str = "Android"
            platformVersion: str = "11.0"
            automationName: str = "Appium"
            appPackage: str = "ru.mail.search.electroscope"
            appActivity: str = ".ui.activity.AssistantActivity"
            app: str = apk
            orientation: str = "PORTRAIT"
            autoGrantPermissions: str = 'true'

        return asdict(Capability())
