
import os
import cv2
from helpers import ImageFileNotFoundError, CropRoomNotPossibleError, Room

def read_zone_labels(label_folder):
    all_image_room_labels = {}
    for label_file in os.listdir(label_folder):
        if label_file.endswith(".txt"):
            label_path = os.path.join(label_folder, label_file)
            image_id = os.path.splitext(label_file)[0]
            with open(label_path, 'r') as f:
                rooms = []
                room_id = 1
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id, x_center, y_center, width, height = label_mapping(parts)
                        if(class_id == 2):
                            image = load_image(label_file, label_folder)
                            if(image is None):
                                raise ImageFileNotFoundError("Image file not exist") 
                            rooms.append(get_room(x_center, y_center, width, height, class_id, room_id, image))
                            room_id += 1
                if(len(rooms)>0):
                    all_image_room_labels[image_id] = rooms
    return all_image_room_labels


def label_mapping(parts):
    class_id = int(parts[0])
    x_center = float(parts[1])
    y_center = float(parts[2])
    width = float(parts[3])
    height = float(parts[4])
    return class_id, x_center, y_center, width , height

def load_image(label_file , label_folder):
    image_name = os.path.splitext(label_file)[0] + ".jpg"   # or .jpg
        
    image_folder = os.path.join(
                os.path.dirname(label_folder), 
                "images"
            )

    image_path = os.path.join(
                image_folder,
                image_name
            )
    
    image_path_normalized = os.path.normpath(image_path)
    image = cv2.imread(image_path_normalized)
    return image

def yolo_to_pixels(x_center, y_center, width, height, image):
    img_height, img_width = image.shape[:2]
    
    px_center_x = x_center * img_width
    px_center_y = y_center * img_height
    px_width = width * img_width
    px_height = height * img_height
        
    x1 = px_center_x - (px_width / 2)
    y1 = px_center_y - (px_height / 2)
    x2 = px_center_x + (px_width / 2)
    y2 = px_center_y + (px_height / 2)
    
        
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(img_width, int(x2))
    y2 = min(img_height, int(y2))

    return x1, y1, x2, y2

def crop_room(x1, y1, x2, y2, image):
    crop = None
    if(x2 > x1 and y2 > y1): 
        crop = image[y1:y2, x1:x2]
    return crop

def create_room(room_id, class_id, x1, y1, x2, y2, crop):
    room = Room(
                id = room_id,
                class_id = class_id,
                room_type = "unknown",
                x1 = x1,
                y1 = y1,
                x2 = x2,
                y2 = y2,
                width = x2 - x1,
                height = y2 - y1,
                image = crop
            )
    return room

def get_room(x_center, y_center,width, height, class_id, room_id, image):

    x1, y1, x2, y2 = yolo_to_pixels(x_center, y_center, width, height, image)

    crop =  crop_room(x1, y1, x2, y2, image)
    if(crop is None):
            raise CropRoomNotPossibleError("Room cropping is not possible")

    room = create_room(room_id, class_id, x1, y1, x2, y2, crop)
    
    return room