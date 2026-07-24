from dataclasses import dataclass
import numpy as np

@dataclass
class Room:
    id: int
    room_type: str          
    class_id: int           
    x1: int
    y1: int
    x2: int
    y2: int
    width: int
    height: int
    image: np.ndarray       