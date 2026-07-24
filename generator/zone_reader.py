
import os
import Room
import cv2

def read_zone_rules(label_folder, dimension):
    
    all_image_room_labels = {}
    for label_file in os.listdir(label_folder):
        if label_file.endswith(".txt"):
            label_path = os.path.join(label_folder, label_file)
            with open(label_path, 'r') as f:
                Rooms = []
                room_id = 1
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        class_id, x_center, y_center, width, height = map(float, parts)
                        if(class_id == 2):  
                            Rooms.append(get_room(x_center, y_center, width, height, dimension, label_folder, label_file, class_id, room_id))
                            room_id = room_id + 1
    all_image_room_labels[label_file] = Rooms
    return all_image_room_labels


def get_room(x_center, y_center,width, height, dimension, label_folder, label_file, class_id, room_id):
    px_center_x = x_center * dimension
    px_center_y = y_center * dimension
    px_width = width * dimension
    px_height = height * dimension
    
    x1 = px_center_x - (px_width // 2)
    y1 = px_center_y - (px_height // 2)
    
    x2 = px_center_x + (px_width // 2)
    y2 = px_center_y + (px_height // 2)
    
    image_name = os.path.splitext(label_file)[0] + ".png"   # or .jpg

    image_folder = os.path.join(
        os.path.dirname(label_folder), 
        "images"
    )

    image_path = os.path.join(
        image_folder,
        image_name
    )
    image = cv2.imread(image_path)
    room = Room(
                                    id = room_id,
                                    class_id = class_id,
                                    room_type = "unknown",
                                    x1 = int(x1),
                                    y1 = int(y1), 
                                    x2 = int(x2),
                                    y2 = int(y2),
                                    width = px_width,
                                    height = px_height,
                                    image = image[y1:y2, x1:x2]
                                )
    return room