
import os
import sys
import pygame
import settings
from pipboy import PipBoy
import threading
from input_manager import InputManager




def main():
    """Main entry point for the Pip-Boy application."""
    # Set up environment for headless/server operation  
    if settings.RASPI:
        os.environ["SDL_VIDEODRIVER"] = "x11"
        os.environ["DISPLAY"] = ":0"
        os.environ["SDL_AUDIODRIVER"] = "alsa"
    else:
        # For Replit/headless environment, use dummy video driver if no display available
        if not os.environ.get('DISPLAY'):
            os.environ["SDL_VIDEODRIVER"] = "dummy"

        
    pygame.init()
    
    # Try to initialize audio, but continue if it fails (headless environment)
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        print("Audio initialized successfully")
    except pygame.error as e:
        print(f"Audio initialization failed: {e}")
        print("Continuing without audio support")
    
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN if settings.RASPI else 0)
    print(pygame.display.get_driver())
    pygame.mouse.set_visible(False)
    
    pygame.display.set_caption("Pip-Boy")
    clock = pygame.time.Clock()
    
    input_manager = InputManager()

    pipboy = PipBoy(screen, clock, input_manager)
    pipboy_thread = threading.Thread(target=pipboy.run)
    pipboy_thread.daemon = True
    pipboy_thread.start()
    pipboy_thread_lock = threading.Lock()
    
    

    running = True
    while running:
        
        input_manager.run()
        
        with pipboy_thread_lock:
            pipboy.render()
        clock.tick(settings.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()