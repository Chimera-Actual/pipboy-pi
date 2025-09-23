"""
Pip-Boy Framework Visual Effects

Authentic Pip-Boy visual effects including CRT simulation, glitch effects,
blur effects, and screen distortions for that classic retro feel.
"""

import pygame
import random
import math
from threading import Thread
from typing import Optional, Tuple


class CRTEffect:
    """
    CRT monitor simulation with scanlines, noise, and screen curvature effects.
    """
    
    def __init__(self, screen_size: Tuple[int, int], theme):
        """
        Initialize CRT effect.
        
        Args:
            screen_size: Screen dimensions (width, height)
            theme: PipBoyTheme instance for colors
        """
        self.screen_size = screen_size
        self.theme = theme
        self.width, self.height = screen_size
        
        # Create overlay surface for CRT effects
        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.scanlines = pygame.Surface(screen_size, pygame.SRCALPHA)
        
        self._create_scanlines()
        
    def _create_scanlines(self):
        """Create the scanline overlay"""
        self.scanlines.fill((0, 0, 0, 0))
        
        # Draw horizontal scanlines
        for y in range(0, self.height, 2):
            pygame.draw.line(
                self.scanlines, 
                (0, 0, 0, 30), 
                (0, y), 
                (self.width, y)
            )
    
    def apply_noise(self, surface: pygame.Surface, intensity: float = 0.1):
        """
        Apply random noise to the surface.
        
        Args:
            surface: Target surface to modify
            intensity: Noise intensity (0.0 to 1.0)
        """
        if random.random() < intensity:
            noise_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)
            
            # Add random pixels
            for _ in range(random.randint(10, 50)):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                color = (*self.theme.light, random.randint(20, 100))
                pygame.draw.circle(noise_surface, color, (x, y), 1)
            
            surface.blit(noise_surface, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def apply_scanlines(self, surface: pygame.Surface):
        """Apply scanline effect to surface"""
        surface.blit(self.scanlines, (0, 0), special_flags=pygame.BLEND_PREMULTIPLIED)
    
    def render(self, surface: pygame.Surface, enable_noise: bool = True):
        """
        Apply CRT effects to the surface.
        
        Args:
            surface: Target surface
            enable_noise: Whether to apply noise effect
        """
        if enable_noise:
            self.apply_noise(surface)
        self.apply_scanlines(surface)


class GlitchEffect:
    """
    Various glitch effects including horizontal slice distortion and random artifacts.
    """
    
    def __init__(self, screen_size: Tuple[int, int], theme):
        """
        Initialize glitch effect.
        
        Args:
            screen_size: Screen dimensions
            theme: PipBoyTheme instance for colors
        """
        self.screen_size = screen_size
        self.theme = theme
        self.width, self.height = screen_size
    
    def horizontal_glitch(self, surface: pygame.Surface, intensity: int = 5):
        """
        Apply horizontal slice glitch effect.
        
        Args:
            surface: Target surface to modify
            intensity: Number of glitch slices
        """
        glitch_surface = surface.copy()
        
        for _ in range(random.randint(1, intensity * 3)):
            slice_height = random.randint(2, 15)
            y = random.randint(0, self.height - slice_height)
            x_offset = random.randint(-15, 15)
            
            slice_rect = pygame.Rect(0, y, self.width, slice_height)
            surface.blit(glitch_surface, (x_offset, y), slice_rect)
    
    def random_artifacts(self, surface: pygame.Surface, count: int = 3):
        """
        Add random visual artifacts.
        
        Args:
            surface: Target surface
            count: Number of artifacts to add
        """
        for _ in range(random.randint(1, count)):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            # Random line artifact
            end_x = x + random.randint(-5, 5)
            end_y = y + random.randint(-5, 5)
            
            pygame.draw.line(
                surface, 
                self.theme.light,
                (x, y),
                (end_x, end_y),
                random.randint(1, 2)
            )
    
    def tab_switch_glitch(self, surface: pygame.Surface, frame: int, total_frames: int = 20):
        """
        Special glitch effect for tab switching.
        
        Args:
            surface: Target surface
            frame: Current frame number
            total_frames: Total frames in effect
        """
        if frame < total_frames:
            time_factor = frame * 100  # Simulate time progression
            jump_offset = int(20 * math.sin(time_factor))
            
            # Create a temporary surface for the effect
            temp_surface = surface.copy()
            surface.blit(temp_surface, (0, -jump_offset))
    
    def apply_random_glitch(self, surface: pygame.Surface, chance: float = 0.5):
        """
        Randomly apply glitch effects based on chance.
        
        Args:
            surface: Target surface
            chance: Probability of applying effect (0.0 to 100.0)
        """
        if random.random() < chance / 100:
            effect_type = random.choice(['horizontal', 'artifacts', 'both'])
            
            if effect_type in ['horizontal', 'both']:
                self.horizontal_glitch(surface, random.randint(3, 8))
            
            if effect_type in ['artifacts', 'both']:
                self.random_artifacts(surface, random.randint(2, 5))


class BlurEffect:
    """
    Blur and bloom effects for smooth transitions and ambient lighting.
    """
    
    def __init__(self, theme):
        """
        Initialize blur effect.
        
        Args:
            theme: PipBoyTheme instance for colors and settings
        """
        self.theme = theme
    
    def box_blur(self, surface: pygame.Surface, intensity: int = 3) -> pygame.Surface:
        """
        Apply box blur to surface.
        
        Args:
            surface: Source surface
            intensity: Blur intensity
            
        Returns:
            Blurred surface
        """
        try:
            return pygame.transform.box_blur(surface, intensity)
        except AttributeError:
            # Fallback for older pygame versions
            return surface
    
    def apply_blur_transition(self, surface: pygame.Surface):
        """
        Apply blur effect for smooth transitions.
        
        Args:
            surface: Target surface to modify
        """
        screen_copy = surface.copy()
        
        for blur_radius in self.theme.BLUR_ITERATIONS:
            blur = self.box_blur(screen_copy, blur_radius)
            blur.set_alpha(self.theme.BLUR_ALPHA)
            surface.blit(blur, (0, 0), special_flags=pygame.BLEND_ADD)
    
    def apply_bloom(self, surface: pygame.Surface, intensity: int = 10):
        """
        Apply bloom effect with colored tint.
        
        Args:
            surface: Target surface
            intensity: Bloom intensity (alpha value)
        """
        if self.theme.BLOOM_EFFECT:
            screen_size = surface.get_size()
            bloom_surface = pygame.Surface(screen_size)
            bloom_surface.fill(self.theme.light)
            bloom_surface.set_alpha(intensity)
            surface.blit(bloom_surface, (0, 0))


class EffectManager:
    """
    Central manager for coordinating visual effects.
    """
    
    def __init__(self, screen_size: Tuple[int, int], theme):
        """
        Initialize effect manager.
        
        Args:
            screen_size: Screen dimensions
            theme: PipBoyTheme instance
        """
        self.screen_size = screen_size
        self.theme = theme
        
        # Initialize effect systems
        self.crt = CRTEffect(screen_size, theme) if theme.SHOW_CRT else None
        self.glitch = GlitchEffect(screen_size, theme)
        self.blur = BlurEffect(theme)
        
        # State tracking
        self.blur_pending = False
        self.glitch_thread: Optional[Thread] = None
    
    def trigger_blur(self):
        """Queue a blur effect for the next render"""
        self.blur_pending = True
    
    def trigger_glitch(self, tab_switch: bool = False):
        """
        Trigger a glitch effect.
        
        Args:
            tab_switch: Whether this is a tab switch glitch
        """
        if tab_switch and random.randint(0, 100) < self.theme.GLITCH_MOVE_CHANCE:
            if self.glitch_thread is None or not self.glitch_thread.is_alive():
                self.glitch_thread = Thread(
                    target=self._tab_switch_glitch_sequence, 
                    daemon=True
                )
                self.glitch_thread.start()
        else:
            self.trigger_blur()
    
    def _tab_switch_glitch_sequence(self):
        """Execute tab switch glitch sequence in thread"""
        # This would be called from the main render loop
        # Implementation depends on how the main loop handles threading
        pass
    
    def render_effects(self, surface: pygame.Surface):
        """
        Apply all enabled effects to the surface.
        
        Args:
            surface: Target surface
        """
        # Apply blur if pending
        if self.blur_pending:
            self.blur.apply_blur_transition(surface)
            self.blur_pending = False
        
        # Apply bloom effect
        self.blur.apply_bloom(surface)
        
        # Apply random glitches
        if self.theme.RANDOM_GLITCHES:
            self.glitch.apply_random_glitch(surface, self.theme.RANDOM_GLITCH_CHANCE)
        
        # Apply CRT effects
        if self.crt:
            self.crt.render(surface)


# Convenience functions
def create_effect_manager(screen_size: Tuple[int, int], theme) -> EffectManager:
    """Create a new effect manager with specified settings"""
    return EffectManager(screen_size, theme)