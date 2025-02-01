import pygame
import os
import settings

class Overlays:
    def __init__(self, screen):
        self.overlays = []
        self.current_crt_image = 0
        self.overlay_image = pygame.image.load(settings.CRT_OVERLAY).convert_alpha()
        self.overlay_image.set_alpha(80)
        self.scanline_image = pygame.image.load(settings.SCANLINE_OVERLAY).convert_alpha()
        self.scanline_image.set_alpha(5)

        self.scanline_y = -self.scanline_image.get_height()
        self.scanline_height = self.scanline_image.get_height()
        self.screen = screen
        self.crt_static = [
            pygame.image.load(os.path.join(settings.CRT_STATIC, filename)).convert_alpha()
            for filename in os.listdir(settings.CRT_STATIC) if filename.endswith(".png")
        ]
        
        self.bloom_overlay = pygame.image.load(settings.BLOOM_OVERLAY).convert_alpha()
        self.bloom_overlay.set_alpha(20)
        

    def run(self):
        """CRT effect thread."""
        while True:
            self.scanline_y = (self.scanline_y + 2) % (settings.SCREEN_HEIGHT + self.scanline_height)
            self.current_crt_image = (self.current_crt_image + 1) % len(self.crt_static)
            pygame.time.wait(30)


    def render(self):
        
        self.screen.blit(self.crt_static[self.current_crt_image], (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.screen.blit(self.scanline_image, (0, (self.scanline_y - self.scanline_height)))
        self.screen.blit(self.overlay_image, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.screen.blit(self.bloom_overlay, (0, 0))
        
