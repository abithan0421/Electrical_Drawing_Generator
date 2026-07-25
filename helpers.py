import json
from importlib import resources
from dataclasses import dataclass
import numpy as np

class ImageFileNotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg 
        super().__init__(msg)

try:
    raise ImageFileNotFoundError("System cannot find the file.")
except ImageFileNotFoundError as e:
    print("Instance message attribute:", e.msg) 


class CropRoomNotPossibleError(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)
try:
    raise CropRoomNotPossibleError("Cropping not posssible.")
except CropRoomNotPossibleError as e:
    print("Error found:", e.msg)

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

def room_mapping()->dict:
    raw_data = resources.files('config').joinpath('room_mapping.json').read_text()
    return json.loads(raw_data)