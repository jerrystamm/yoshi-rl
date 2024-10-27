import numpy as np
import cv2
from src.PyGBA import PyGBA
from mgba.vfs import open_path
import pygame
from src.Timer import Timer

class YoshiWrapper():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((240, 160)) 
        pygame.display.set_caption('YoshiEnv')

        self.timer = Timer()

        self.gba = PyGBA('yoshi.gba')
        self.gba.core.reset()

        self.reset_state_data = open_path("save_state.mgba")
        self.gba.core.load_state(self.reset_state_data)

    def resetState(self):
        self.gba.core.reset()
        self.gba.core.load_state(self.reset_state_data)
        self.gba.core.run_frame()

    def doAction(self, action):
        match action:
            case 0:
                self.gba.press_key("down")
            case 1:
                self.gba.press_key("left")
            case 2:
                self.gba.press_key("right")
            case 3:
                self.gba.press_key("A")
            case 4:
                self.gba.press_key("B")
            case 5:
                self.gba.press_key("L")
            case 6:
                self.gba.press_key("R")
            case 7:
                self.gba.release_key("down")
            case 8:
                self.gba.release_key("left")
            case 9:
                self.gba.release_key("right")
            case 10:
                self.gba.release_key("A")
            case 11:
                self.gba.release_key("B")
            case 12:
                self.gba.release_key("L")
            case 13:
                self.gba.release_key("R")
            case default:
                # error
                pass

    def getMarioSafety(self):
        return self.gba.read_u32(0x30024c4)

    def getCurrentStep(self):
        return self.gba.read_u32(0x03006D90)
    
    def runFrame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        self.gba.core.run_frame()

        pygame_surface = pygame.surfarray.make_surface(self.getScreen())
        self.screen.blit(pygame_surface, (0, 0))
        pygame.display.flip()

    def getScreen(self):
        buffer = np.array(self.gba.video_buffer.to_pil())
        rgb_screen = cv2.cvtColor(buffer, cv2.COLOR_RGBA2RGB)
        return cv2.transpose(rgb_screen, (1, 0))
    