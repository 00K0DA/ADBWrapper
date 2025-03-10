from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    start_x: int
    start_y: int
    end_x: int
    end_y: int
