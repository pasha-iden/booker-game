from Objects.furniture import Furniture


def room_furniture (scene_room):
    objects = []

    if scene_room == 1:
        room_furnitures = ((0, 350, 200, 100),)

    if scene_room == 2:
        room_furnitures = ((0, 350, 200, 100),
                           (400, 250, 150, 130))

    if scene_room == 3:
        room_furnitures = ((0, 350, 200, 100),
                           (400, 250, 150, 130),
                           (0, 0, 250, 200),
                           (400, 0, 100, 150),
                           (550, 0, 100, 100),
                           (780, 230, 100, 100),
                           (720, 420, 150, 130))

    for object in room_furnitures:
        Furniture(objects, object[0], object[1], object[2], object[3])

    recreate_room = False
    return objects, recreate_room

if __name__ == '__main__':
    pass
