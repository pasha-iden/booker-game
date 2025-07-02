import pygame
from moviepy.editor import VideoFileClip


class Intro:
    def __init__(self):
        # self.images = [None]
        # saturations = (None,
        #                0, 0, 0, 0, 0, 0, 0, 255, 0, 0,
        #                255, 0, 0, 255, 0, 0, 0, 0, 0, 0,
        #                0, 0, 0, 0, 255)
        # for i in range(1, 26):
        #     image = pygame.image.load(f'Files/Images/Intro/{i}.jpg')
        #     size = (image.get_size()[0] // 4.5, image.get_size()[1] // 4.5)
        #     image = pygame.transform.smoothscale(image, (size[0], size[1]))
        #     self.images.append(pygame.Surface((size), pygame.SRCALPHA))
        #     self.images[i].blit(image, (0, 0))
        #     self.images[i].set_alpha(saturations[i])


        self.video = VideoFileClip("Files/Images/Intro/видео.mp4")
        self.video_start = 1405
        self.video_finish = self.video_start + 660


        self.frases = [pygame.Surface((200, 100), pygame.SRCALPHA), pygame.Surface((400, 200), pygame.SRCALPHA), pygame.Surface((500, 200), pygame.SRCALPHA)]
        self.font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=60)
        message = self.font.render('BOOKER', False, 'Red')
        self.frases[0].blit(message, (0, 0))
        self.font = pygame.font.Font('Files/Fonts/PressStart2P-Regular.ttf', size=50)
        message = self.font.render('BOOKER', False, 'Red')
        self.frases[1].blit(message, (0, 0))
        self.font = pygame.font.Font('Files/Fonts/PressStart2P-Regular.ttf', size=15)
        message = self.font.render('8-битное приключение', False, 'White')
        self.frases[2].blit(message, (0, 0))

        saturations = (None, None, None,
                       0, 0, 0, 255, 255, 255)
        frases = (None, None, None,
            'в одном солнечном городе...',
            'есть замечательное место...',
            'в котором готовят',
            'ЧЕРТОВСКИ',
            'ХОРОШИЙ',
            'КОФЕ')
        self.font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=30)
        for i in range(3, len(frases)):
            self.frases.append(pygame.Surface((len(frases[i]) * 30, 30), pygame.SRCALPHA))
            message = self.font.render(frases[i], False, 'White')
            self.frases[i].blit(message, (0, 0))
            self.frases[i].set_alpha(saturations[i])

        self.plot = {# в одном солнечном городе
                     20: (('текст', True, 3, (330, 400)),),
                     320: (('текст', False, 3),),
                     # есть замечательное место
                     470: (('текст', True, 4, (330, 400)),),
                     770: (('текст', False, 4),),
                     # в котором готовят
                     870: (('текст', True, 5, (330, 400)),),
                     # чертовски хороший кофе
                     1070: (('текст', True, 6, (410, 430)),),
                     1150: (('текст', True, 7, (432, 460)),),
                     1235: (('текст', True, 8, (490, 490)),),
                     # Booker
                     1380: (('текст', True, 0, (364, 346)),),
                     # 4 фото
                     # 1410: (('фото', True, 8, (570, 267)),),
                     # 1450: (('фото', None, 8), ('фото', True, 11, (570, 283))),
                     # 1490: (('фото', None, 11), ('фото', True, 25, (570, 236))),
                     # 1535: (('фото', None, 25), ('фото', True, 14, (570, 268))),
                     # 1570: (('фото', None, 14),),
                     self.video_finish : (('текст', None, 0), ('текст', None, 5), ('текст', None, 6), ('текст', None, 7), ('текст', None, 8), ('текст', True, 1, (364, 346)), ('текст', True, 2, (364, 400))),
                     }
        self.iin = [[], []]
        self.fin = [[], []]
        self.iou = [[], []]
        self.fou = [[], []]
        # 2 минуты - это 7200 fps
        self.timer = 0
        self.out = False


    def intro_cut(self, scene_surface):
        if self.timer == 0:
            pygame.mixer.music.load('Files/Sounds/Music/WELC0MEИ0.mp3')
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        if self.timer == 1065:
            pygame.mixer.music.load('Files/Sounds/Music/Skilsel.mp3')
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)

        scene_surface.fill('Black')
        if self.timer in self.plot:
            for el in self.plot[self.timer]:
                if el[1] == True:
                    if el[0] == 'фото':
                        self.iin[0].append(el[2])
                        self.iin[1].append(el[3])
                    else:
                        self.fin[0].append(el[2])
                        self.fin[1].append(el[3])
                elif el[1] == False:
                    if el[0] == 'фото':
                        self.iou[1].append( self.iin[1].pop(self.iin[0].index( el[2])))
                        self.iou[0].append( self.iin[0].pop(self.iin[0].index( el[2])))
                    else:
                        self.fou[1].append(self.fin[1].pop(self.fin[0].index(el[2])))
                        self.fou[0].append(self.fin[0].pop(self.fin[0].index(el[2])))
                elif el[1] == None:
                    if el[0] == 'фото':
                        self.iin[1].pop(self.iin[0].index(el[2]))
                        self.iin[0].pop(self.iin[0].index(el[2]))
                    else:
                        self.fin[1].pop(self.fin[0].index(el[2]))
                        self.fin[0].pop(self.fin[0].index(el[2]))


        # for el in self.iin[0]:
        #     if self.images[el].get_alpha() < 255:
        #         self.images[el].set_alpha( self.images[el].get_alpha() + 5)
        for el in self.fin[0]:
            if self.frases[el].get_alpha() < 255:
                self.frases[el].set_alpha( self.frases[el].get_alpha() + 5)

        # for el in self.iou[0]:
        #     if self.images[el].get_alpha() > 0:
        #         self.images[el].set_alpha( self.images[el].get_alpha() - 5)
        for el in self.fou[0]:
            if self.frases[el].get_alpha() > 0:
                self.frases[el].set_alpha( self.frases[el].get_alpha() - 5)

        # i = 0
        # while i < len(self.iou[0]):
        #     if self.images[self.iou[0][i]].get_alpha() == 0:
        #         self.iou[0].pop(i)
        #         self.iou[1].pop(i)
        #     else:
        #         i += 1
        i = 0
        while i < len(self.fou[0]):
            if self.frases[self.fou[0][i]].get_alpha() == 0:
                self.fou[0].pop(i)
                self.fou[1].pop(i)
            else:
                i += 1

        # for i in range(len(self.iin[0])):
        #     scene_surface.blit(self.images[self.iin[0][i]], self.iin[1][i])
        for i in range(len(self.fin[0])):
            scene_surface.blit(self.frases[self.fin[0][i]], self.fin[1][i])

        # for i in range(len(self.iou[0])):
        #     scene_surface.blit(self.images[self.iou[0][i]], self.iou[1][i])
        for i in range(len(self.fou[0])):
            scene_surface.blit(self.frases[self.fou[0][i]], self.fou[1][i])


        if self.timer > self.video_start and self.timer < self.video_finish:
            frame = self.video.get_frame((self.timer - self.video_start) / 60)  # получение кадра
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], 'RGB')  # преобразование кадра в Surface
            scene_surface.blit(frame_surface, (570, 199))


        if self.timer == self.video_finish + 5:
            area_to_shift = pygame.Rect(0, 364, 1024, 100)
            shifted_surface = scene_surface.subsurface(area_to_shift).copy()
            shifted_position = area_to_shift.move(4, 0)
            scene_surface.fill((0, 0, 0), area_to_shift)
            scene_surface.blit(shifted_surface, shifted_position)

        # print (self.timer)
        self.timer += 1

        if self.timer == 2560:
            self.out = True


if __name__ == '__main__':
    pass