from dataclasses import dataclass, field, asdict


@dataclass
class Blog:
    title: str
    underline: str = field(init=False)

    # Part of the persistence, not essential to the class.
    _id: str = field(default="", init=False, compare=False)

    def __post_init__(self) -> None:
        self.underline = "=" * len(self.title)
