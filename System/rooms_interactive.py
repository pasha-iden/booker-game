from Objects.interactives import Interactive


def room_interactive (scene_room):
    objects = []

    if scene_room == 1:
        room_interactives = [(600, 600, 50, 50)]

    if scene_room == 2:
        room_interactives = [(500, 500, 50, 50)]

    if scene_room == 3:
        room_interactives = [(400, 400, 50, 50)]

    for object in room_interactives:
        Interactive(objects, object[0], object[1], object[2], object[3])

    return objects

if __name__ == '__main__':
    pass
