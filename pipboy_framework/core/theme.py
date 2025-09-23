"""
Pip-Boy Framework Theme System

Provides authentic Pip-Boy color schemes, typography, and styling constants
for creating faithful reproductions of the classic interface.
"""

import pygame
import os
from typing import Dict, Tuple, Optional, NamedTuple

class ColorScheme(NamedTuple):
    """Pip-Boy color scheme definition"""
    background: Tuple[int, int, int]
    light: Tuple[int, int, int]
    middle: Tuple[int, int, int]
    darker: Tuple[int, int, int]
    dark: Tuple[int, int, int]

class PipBoyTheme:
    """
    Central theme management for Pip-Boy framework.
    Handles color schemes, fonts, spacing, and visual effects.
    """
    
    # Built-in color schemes
    COLOR_SCHEMES = {
        'classic_green': ColorScheme(
            background=(0, 0, 0),
            light=(0, 255, 0),
            middle=(0, 190, 0),
            darker=(0, 127, 0),
            dark=(0, 63, 0)
        ),
        'amber': ColorScheme(
            background=(0, 0, 0),
            light=(255, 176, 0),
            middle=(191, 132, 0),
            darker=(127, 88, 0),
            dark=(63, 44, 0)
        ),
        'blue': ColorScheme(
            background=(0, 0, 0),
            light=(0, 162, 255),
            middle=(0, 122, 191),
            darker=(0, 81, 127),
            dark=(0, 41, 63)
        ),
        'white': ColorScheme(
            background=(0, 0, 0),
            light=(255, 255, 255),
            middle=(191, 191, 191),
            darker=(127, 127, 127),
            dark=(63, 63, 63)
        )
    }
    
    def __init__(self, assets_path: str = "assets", color_scheme: str = "classic_green"):
        """
        Initialize theme with specified color scheme and assets path.
        
        Args:
            assets_path: Path to framework assets directory
            color_scheme: Name of color scheme to use
        """
        self.assets_path = assets_path
        self.fonts_path = os.path.join(assets_path, "fonts")
        self.sounds_path = os.path.join(assets_path, "sounds")
        
        # Set color scheme
        self.set_color_scheme(color_scheme)
        
        # Initialize fonts
        self._init_fonts()
        
        # Layout constants
        self._init_layout()
        
        # Visual effects settings
        self._init_effects()
    
    def set_color_scheme(self, scheme_name: str):
        """Set the active color scheme"""
        if scheme_name not in self.COLOR_SCHEMES:
            raise ValueError(f"Unknown color scheme: {scheme_name}. Available: {list(self.COLOR_SCHEMES.keys())}")
        
        scheme = self.COLOR_SCHEMES[scheme_name]
        self.background = scheme.background
        self.light = scheme.light
        self.middle = scheme.middle
        self.darker = scheme.darker
        self.dark = scheme.dark
        
        # Convenience aliases for backward compatibility
        self.PIP_BOY_LIGHT = self.light
        self.PIP_BOY_MIDDLE = self.middle
        self.PIP_BOY_DARKER = self.darker
        self.PIP_BOY_DARK = self.dark
        self.BACKGROUND = self.background
    
    def _init_fonts(self):
        """Initialize font paths and load commonly used fonts"""
        # Font paths
        self.ROBOTO_PATH = os.path.join(self.fonts_path, "Roboto")
        self.ROBOTO_CONDENSED_PATH = os.path.join(self.ROBOTO_PATH, "RobotoCondensed-Regular.ttf")
        self.ROBOTO_CONDENSED_BOLD_PATH = os.path.join(self.ROBOTO_PATH, "RobotoCondensed-Bold.ttf")
        self.ROBOTO_REGULAR_PATH = os.path.join(self.ROBOTO_PATH, "Roboto-Regular.ttf")
        self.ROBOTO_BOLD_PATH = os.path.join(self.ROBOTO_PATH, "Roboto-Bold.ttf")
        
        self.TECHMONO_PATH = os.path.join(self.fonts_path, "TechMono")
        self.TECHMONO_REGULAR_PATH = os.path.join(self.TECHMONO_PATH, "TechMono-Regular.ttf")
        
        # Default font selection
        self.MAIN_FONT_PATH = self.ROBOTO_CONDENSED_PATH
        
        # Cache for loaded fonts
        self._font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
    
    def _init_layout(self):
        """Initialize layout and spacing constants"""
        # Tab layout
        self.TAB_MARGIN = 20
        self.TAB_VERTICAL_OFFSET = 0
        self.TAB_VERTICAL_LINE_OFFSET = 10
        self.TAB_HORIZONTAL_LINE_OFFSET = 4
        self.TAB_SCREEN_EDGE_LENGTH = 2
        self.TAB_HORIZONTAL_LENGTH = self.TAB_HORIZONTAL_LINE_OFFSET // 1.1
        self.TAB_BOTTOM_MARGIN = 2
        self.TAB_SIDE_MARGIN = 0
        
        # Sub-tab layout
        self.SUBTAB_SPACING = 5
        self.SUBTAB_VERTICAL_OFFSET = 1
        
        # Bottom bar
        self.BOTTOM_BAR_VERTICAL_MARGINS = 2
        self.BOTTOM_BAR_HEIGHT = 18
        self.BOTTOM_BAR_MARGIN = 5
        
        # Lists and grids
        self.LIST_TOP_MARGIN = 10
        self.GRID_BOTTOM_MARGIN = 0
        self.GRID_RIGHT_MARGIN = 35
        self.GRID_LEFT_MARGIN = 5
        
        # Interactive elements
        self.SELECTION_DOT_SIZE = 4
        self.TEXT_MARGIN = 10
        self.SELECTION_MARGIN = 6
    
    def _init_effects(self):
        """Initialize visual effects settings"""
        self.SHOW_CRT = True
        self.BLOOM_EFFECT = True
        self.GLITCH_MOVE_CHANCE = 60
        self.RANDOM_GLITCHES = True
        self.RANDOM_GLITCH_CHANCE = 0.5
        
        # Animation settings
        self.DEFAULT_FPS = 24
        self.GLITCH_FRAME_COUNT = 20
        self.BLUR_ITERATIONS = range(1, 18, 6)
        self.BLUR_ALPHA = 180
    
    def get_font(self, path: str, size: int) -> pygame.font.Font:
        """
        Get a cached font or load it if not cached.
        
        Args:
            path: Path to font file
            size: Font size
            
        Returns:
            Loaded pygame Font object
        """
        key = (path, size)
        if key not in self._font_cache:
            try:
                self._font_cache[key] = pygame.font.Font(path, size)
            except (pygame.error, FileNotFoundError):
                # Try alternative paths for fonts
                try:
                    # Try fonts directory at project root
                    alt_path = path.replace("pipboy_framework/assets/fonts", "fonts")
                    self._font_cache[key] = pygame.font.Font(alt_path, size)
                except (pygame.error, FileNotFoundError):
                    # Fallback to system font if custom font fails
                    print(f"Font not found at {path} or {alt_path}, using system font")
                    self._font_cache[key] = pygame.font.Font(None, size)
        return self._font_cache[key]
    
    def get_main_font(self, size: int = 14) -> pygame.font.Font:
        """Get the main interface font with specified size"""
        return self.get_font(self.MAIN_FONT_PATH, size)
    
    def get_footer_font(self, size: int = 12) -> pygame.font.Font:
        """Get the footer font with specified size"""
        return self.get_font(self.ROBOTO_CONDENSED_BOLD_PATH, size)
    
    def calculate_draw_space(self, screen_width: int, screen_height: int, 
                           include_subtabs: bool = True) -> pygame.Rect:
        """
        Calculate the main content drawing area.
        
        Args:
            screen_width: Screen width
            screen_height: Screen height
            include_subtabs: Whether to account for subtab space
            
        Returns:
            Rect defining the usable content area
        """
        font_height = self.get_main_font().get_height()
        
        if include_subtabs:
            top_offset = (self.TAB_SCREEN_EDGE_LENGTH + font_height * 2 + 
                         self.TAB_BOTTOM_MARGIN)
        else:
            top_offset = (self.TAB_SCREEN_EDGE_LENGTH + font_height + 
                         self.TAB_BOTTOM_MARGIN)
        
        bottom_offset = self.BOTTOM_BAR_HEIGHT + self.BOTTOM_BAR_MARGIN
        
        return pygame.Rect(
            0, 
            top_offset, 
            screen_width, 
            screen_height - bottom_offset - top_offset
        )
    
    def get_sound_path(self, sound_name: str) -> str:
        """Get path to a sound file"""
        return os.path.join(self.sounds_path, sound_name)

# Convenience function for quick theme access
def create_theme(color_scheme: str = "classic_green", assets_path: str = "assets") -> PipBoyTheme:
    """Create a new theme instance with specified settings"""
    return PipBoyTheme(assets_path, color_scheme)