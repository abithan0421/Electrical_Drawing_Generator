
from generator import image_loader, zone_reader,  room_detector

def main():
    
    # Load Image
    resize_dimension = 1024
    # image_loader.flush()
    # image_loader.load_images_from_folder("base_floorplans/test/images", resize_dimension)
    processed_room_labels = zone_reader.read_zone_labels("processed_floor_plans/test/labels")
    room_detector.room_mapping()


    # Detect Rooms
    # rooms = detect_rooms(image)

    # # Read Rules
    # rules = read_rules("rules.json")

if __name__ == "__main__":
    main();
# Load Image

# ↓

# Detect Rooms

# ↓

# Read Rules

# ↓

# Load Symbols

# ↓

# Place Symbols

# ↓

# Write Labels

# ↓

# Save Image