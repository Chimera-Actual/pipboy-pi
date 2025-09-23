"""
Pip-Boy Framework Main Orchestrator

The main PipBoyFramework class that coordinates all components and provides
the primary interface for creating Pip-Boy style applications.
"""

import pygame
from typing import Tuple, Optional, Dict, Any
from pipboy_framework.core.theme import PipBoyTheme, create_theme
from pipboy_framework.core.tab_system import TabSystem, TabRegistry, create_tab_system
from pipboy_framework.ui.effects import create_effect_manager, EffectManager


class InputHandler:
    """
    Simple input handler for framework navigation.
    Can be extended or replaced with custom input handling.
    """
    
    def __init__(self):
        self.key_handlers: Dict[int, callable] = {}
    
    def register_key_handler(self, key: int, handler: callable):
        """Register a key handler function"""
        self.key_handlers[key] = handler
    
    def handle_events(self, events):
        """Process pygame events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_handlers:
                    self.key_handlers[event.key]()


class PipBoyFramework:
    """
    Main framework class that orchestrates the complete Pip-Boy interface.
    
    Usage:
        framework = PipBoyFramework(screen_size=(1024, 768))
        framework.register_tab("DEMO", DemoTab)
        framework.run()
    """
    
    def __init__(self, screen_size: Tuple[int, int] = (1024, 768), 
                 color_scheme: str = "classic_green",
                 assets_path: str = "pipboy_framework/assets",
                 fullscreen: bool = False,
                 fps: int = 24):
        """
        Initialize the Pip-Boy framework.
        
        Args:
            screen_size: Display resolution (width, height)
            color_scheme: Color scheme name from available themes
            assets_path: Path to framework assets
            fullscreen: Whether to run in fullscreen mode
            fps: Target frames per second
        """
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create display
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode(screen_size, flags)
        pygame.display.set_caption("Pip-Boy Framework")
        
        # Create clock for FPS control
        self.clock = pygame.time.Clock()
        self.fps = fps
        
        # Initialize core systems
        self.theme = create_theme(color_scheme, assets_path)
        self.registry = TabRegistry()
        self.tab_system: Optional[TabSystem] = None
        self.effect_manager = create_effect_manager(screen_size, self.theme)
        
        # Input handling
        self.input_handler = InputHandler()
        self._setup_default_input()
        
        # Framework state
        self.running = False
        self.initialized = False
    
    def _setup_default_input(self):
        """Setup default keyboard controls"""
        # Tab navigation
        self.input_handler.register_key_handler(pygame.K_LEFT, lambda: self._switch_tab(False))
        self.input_handler.register_key_handler(pygame.K_RIGHT, lambda: self._switch_tab(True))
        
        # Sub-tab navigation
        self.input_handler.register_key_handler(pygame.K_UP, lambda: self._switch_sub_tab(True))
        self.input_handler.register_key_handler(pygame.K_DOWN, lambda: self._switch_sub_tab(False))
        
        # Content navigation
        self.input_handler.register_key_handler(pygame.K_w, lambda: self._scroll(True))
        self.input_handler.register_key_handler(pygame.K_s, lambda: self._scroll(False))
        
        # Selection
        self.input_handler.register_key_handler(pygame.K_RETURN, self._select_item)
        self.input_handler.register_key_handler(pygame.K_SPACE, self._select_item)
        
        # Exit
        self.input_handler.register_key_handler(pygame.K_ESCAPE, self.stop)
    
    def register_tab(self, name: str, tab_class: type, sub_tabs: list = None):
        """
        Register a new tab with the framework.
        
        Args:
            name: Tab name (e.g., "DEMO", "TEST")
            tab_class: Class extending BaseTab
            sub_tabs: Optional list of sub-tab names
        """
        self.registry.register_tab(name, tab_class, sub_tabs or [])
    
    def set_theme(self, color_scheme: str):
        """Change the active color scheme"""
        self.theme.set_color_scheme(color_scheme)
    
    def get_available_themes(self) -> list:
        """Get list of available color schemes"""
        return list(self.theme.COLOR_SCHEMES.keys())
    
    def _ensure_initialized(self):
        """Ensure the framework is properly initialized"""
        if not self.initialized:
            if not self.registry.get_tab_names():
                raise RuntimeError("No tabs registered. Use register_tab() to add tabs before running.")
            
            # Create tab system
            self.tab_system = create_tab_system(self.screen, self.theme, self.registry)
            self.initialized = True
    
    def _switch_tab(self, direction: bool):
        """Switch to next/previous tab"""
        if self.tab_system:
            self.tab_system.switch_tab(direction)
    
    def _switch_sub_tab(self, direction: bool):
        """Switch to next/previous sub-tab"""
        if self.tab_system:
            self.tab_system.switch_sub_tab(direction)
    
    def _scroll(self, direction: bool):
        """Scroll within current tab"""
        if self.tab_system:
            self.tab_system.scroll(direction)
    
    def _select_item(self):
        """Select current item"""
        if self.tab_system:
            self.tab_system.select_item()
    
    def stop(self):
        """Stop the framework main loop"""
        self.running = False
    
    def render(self):
        """Render one frame"""
        # Clear screen
        self.screen.fill(self.theme.background)
        
        # Render tab system
        if self.tab_system:
            self.tab_system.render()
        
        # Apply visual effects
        self.effect_manager.render_effects(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """
        Run the main framework loop.
        Call this after registering all tabs.
        """
        self._ensure_initialized()
        self.running = True
        
        print(f"Pip-Boy Framework starting...")
        print(f"Registered tabs: {', '.join(self.registry.get_tab_names())}")
        print(f"Color scheme: {self.theme.background}")
        print("Controls: Arrow keys for navigation, Enter/Space to select, Esc to exit")
        
        try:
            while self.running:
                # Handle events
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                
                self.input_handler.handle_events(events)
                
                # Render frame
                self.render()
                
                # Control framerate
                self.clock.tick(self.fps)
                
        except KeyboardInterrupt:
            print("\nFramework interrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Shutting down Pip-Boy Framework...")
        pygame.quit()
    
    def get_current_tab_name(self) -> Optional[str]:
        """Get the name of the currently active tab"""
        if self.tab_system and self.tab_system.tab_names:
            return self.tab_system.tab_names[self.tab_system.current_tab_index]
        return None
    
    def get_fps_info(self) -> Dict[str, Any]:
        """Get current FPS information"""
        return {
            "target_fps": self.fps,
            "actual_fps": self.clock.get_fps(),
            "frame_time": self.clock.get_time()
        }


def create_framework(**kwargs) -> PipBoyFramework:
    """
    Convenience function to create a new framework instance.
    
    Args:
        **kwargs: Arguments passed to PipBoyFramework constructor
        
    Returns:
        New PipBoyFramework instance
    """
    return PipBoyFramework(**kwargs)