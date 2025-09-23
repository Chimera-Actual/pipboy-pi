"""
Pip-Boy Framework Tab System

Core tab management system providing main tab and sub-tab navigation,
pre-rendered surfaces, and thread lifecycle management for optimal performance.
"""

import pygame
import random
import math
from threading import Thread, Lock
from typing import Dict, List, Optional, Callable, Any
from abc import ABC, abstractmethod


class BaseTab(ABC):
    """
    Abstract base class for all tabs in the Pip-Boy framework.
    Provides standard interface for tab lifecycle and rendering.
    """
    
    def __init__(self, screen: pygame.Surface, theme, draw_space: pygame.Rect):
        """
        Initialize the base tab.
        
        Args:
            screen: Main screen surface
            theme: PipBoyTheme instance
            draw_space: Available drawing area for this tab
        """
        self.screen = screen
        self.theme = theme
        self.draw_space = draw_space
        self.footer_font = theme.get_footer_font()
        
        # Tab state
        self.is_active = False
        self.sub_tabs = []
        self.current_sub_tab_index = 0
        
        # Footer management
        self.tab_footers: Dict[str, pygame.Surface] = {}
    
    def init_footer(self, key: str, margins: Optional[List[int]] = None, 
                   text_surface: Optional[pygame.Surface] = None):
        """Initialize a footer surface for this tab"""
        footer_surface = pygame.Surface((self.screen.get_width(), self.theme.BOTTOM_BAR_HEIGHT))
        footer_surface.fill(self.theme.dark)
        
        if margins:
            line = 0
            for margin in margins:
                line += margin - self.theme.BOTTOM_BAR_VERTICAL_MARGINS // 2
                pygame.draw.line(
                    footer_surface,
                    self.theme.background,
                    (line, 0),
                    (line, self.theme.BOTTOM_BAR_HEIGHT),
                    self.theme.BOTTOM_BAR_VERTICAL_MARGINS
                )
        
        if text_surface:
            footer_surface.blit(text_surface, (0, 0))
        
        self.tab_footers[key] = footer_surface
    
    def update_footer(self, key: str, text_surface: pygame.Surface, destination: tuple = (0, 0)):
        """Update part of a footer surface"""
        if key in self.tab_footers:
            self.tab_footers[key].fill(
                self.theme.dark, 
                (destination[0], destination[1], text_surface.get_width(), text_surface.get_height())
            )
            self.tab_footers[key].blit(text_surface, destination)
    
    def render_footer(self, key: str):
        """Render a footer to the screen"""
        if key in self.tab_footers:
            self.screen.blit(
                self.tab_footers[key],
                (0, self.screen.get_height() - self.theme.BOTTOM_BAR_HEIGHT)
            )
    
    @abstractmethod
    def activate(self):
        """Called when this tab becomes active"""
        self.is_active = True
    
    @abstractmethod
    def deactivate(self):
        """Called when this tab becomes inactive"""
        self.is_active = False
    
    @abstractmethod
    def render(self):
        """Render the tab content"""
        pass
    
    def handle_threads(self, start: bool):
        """Handle background threads for this tab"""
        # Default implementation - override in subclasses that need threading
        pass
    
    def change_sub_tab(self, new_index: int):
        """Change the active sub-tab"""
        if 0 <= new_index < len(self.sub_tabs):
            self.current_sub_tab_index = new_index
    
    def scroll(self, direction: bool):
        """Handle scrolling within the tab"""
        # Default implementation - override in subclasses
        pass
    
    def select_item(self):
        """Handle item selection"""
        # Default implementation - override in subclasses
        pass
    
    def navigate(self, direction: int):
        """Handle directional navigation"""
        # Default implementation - override in subclasses
        pass


class TabRegistry:
    """
    Registry for managing available tabs and their configurations.
    """
    
    def __init__(self):
        self.tabs: Dict[str, type] = {}
        self.sub_tabs: Dict[str, List[str]] = {}
        self.tab_order: List[str] = []
    
    def register_tab(self, name: str, tab_class: type, sub_tabs: List[str] = None):
        """
        Register a new tab type.
        
        Args:
            name: Tab name (e.g., "STAT", "INV")
            tab_class: Tab class extending BaseTab
            sub_tabs: List of sub-tab names for this tab
        """
        self.tabs[name] = tab_class
        self.sub_tabs[name] = sub_tabs or []
        if name not in self.tab_order:
            self.tab_order.append(name)
    
    def get_tab_names(self) -> List[str]:
        """Get ordered list of tab names"""
        return self.tab_order.copy()
    
    def get_sub_tabs(self, tab_name: str) -> List[str]:
        """Get sub-tabs for a specific tab"""
        return self.sub_tabs.get(tab_name, [])
    
    def create_tab(self, name: str, screen: pygame.Surface, theme, draw_space: pygame.Rect) -> BaseTab:
        """Create a tab instance"""
        if name not in self.tabs:
            raise ValueError(f"Unknown tab: {name}")
        return self.tabs[name](screen, theme, draw_space)


class ThreadHandler:
    """
    Manages background threads for tabs, ensuring only active tabs run threads.
    """
    
    def __init__(self, tab_instances: Dict[int, BaseTab], initial_tab_index: int = 0):
        self.tab_instances = tab_instances
        self.current_tab_index = initial_tab_index
        self.previous_tab_index = None
        
        self.handle_current_tab()
    
    def update_tab_index(self, new_index: int):
        """Update active tab and manage thread lifecycle"""
        self.previous_tab_index = self.current_tab_index
        self.current_tab_index = new_index
        
        if self.current_tab_index != self.previous_tab_index:
            self.handle_current_tab()
            self.handle_previous_tab()
    
    def _start_thread(self, tab_index: int, flag: bool):
        """Start thread for tab thread management"""
        tab = self.tab_instances.get(tab_index)
        if tab and hasattr(tab, 'handle_threads'):
            thread = Thread(target=tab.handle_threads, args=(flag,), daemon=True)
            thread.start()
    
    def handle_current_tab(self):
        """Start threads for current tab"""
        if self.current_tab_index is not None:
            self._start_thread(self.current_tab_index, True)
    
    def handle_previous_tab(self):
        """Stop threads for previous tab"""
        if self.previous_tab_index is not None:
            self._start_thread(self.previous_tab_index, False)


class TabSystem:
    """
    Main tab system managing navigation, rendering, and effects.
    """
    
    def __init__(self, screen: pygame.Surface, theme, registry: TabRegistry):
        """
        Initialize the tab system.
        
        Args:
            screen: Main screen surface
            theme: PipBoyTheme instance
            registry: TabRegistry with registered tabs
        """
        self.screen = screen
        self.theme = theme
        self.registry = registry
        
        # Tab configuration
        self.tab_names = registry.get_tab_names()
        self.current_tab_index = 0
        self.previous_tab_index = None
        
        # Sub-tab state
        self.current_sub_tab_index = [0] * len(self.tab_names)
        self.previous_sub_tab_index = [0] * len(self.tab_names)
        
        # Font and layout
        self.main_tab_font = theme.get_main_font()
        self.tab_font_height = self.main_tab_font.get_height()
        
        # Pre-rendered surfaces
        self.subtab_bar_surfaces: Dict[str, List[pygame.Surface]] = {}
        self.subtab_offsets: Dict[str, List[float]] = {}
        self.header_background: Optional[pygame.Surface] = None
        self.tab_highlight_surfaces: List[pygame.Surface] = []
        self.tab_x_offset: List[float] = []
        
        # Effects and threading
        self.glitch_thread: Optional[Thread] = None
        self.render_blur = False
        self.switch_lock = Lock()
        
        # Calculate draw spaces
        self.draw_space = theme.calculate_draw_space(
            screen.get_width(), screen.get_height(), True
        )
        
        # Initialize tab instances
        self.tab_instances: Dict[int, BaseTab] = {}
        self._create_tab_instances()
        
        # Thread handler
        self.thread_handler = ThreadHandler(self.tab_instances, self.current_tab_index)
        
        # Pre-render all UI elements
        self._init_header_surfaces()
        self._init_subtab_data()
    
    def _create_tab_instances(self):
        """Create instances of all registered tabs"""
        for i, tab_name in enumerate(self.tab_names):
            self.tab_instances[i] = self.registry.create_tab(
                tab_name, self.screen, self.theme, self.draw_space
            )
    
    def _init_header_surfaces(self):
        """Pre-render static header elements and tab highlights"""
        # Calculate tab positioning
        tab_text_surface = pygame.Surface((self.screen.get_width(), self.tab_font_height))
        total_tab_width = sum(self.main_tab_font.size(tab)[0] for tab in self.tab_names)
        tab_spacing = (self.screen.get_width() - total_tab_width - 2 * self.theme.TAB_MARGIN) // (len(self.tab_names) + 1)
        
        self.tab_x_offset = [self.theme.TAB_MARGIN + tab_spacing]
        
        # Render tab text
        for i, tab in enumerate(self.tab_names):
            text_surface = self.main_tab_font.render(tab, True, self.theme.light)
            tab_text_surface.blit(text_surface, (self.tab_x_offset[i], self.theme.TAB_VERTICAL_OFFSET))
            self.tab_x_offset.append(
                (self.main_tab_font.size(tab)[0] + tab_spacing) + self.tab_x_offset[i]
            )
        
        # Create header background
        self.header_background = pygame.Surface((
            self.screen.get_width(), 
            self.tab_font_height + self.theme.TAB_SCREEN_EDGE_LENGTH + 1
        ))
        self.header_background.fill(self.theme.background)
        self.header_background.blit(tab_text_surface, (0, 0))
        
        # Add header lines
        pygame.draw.line(
            self.header_background, self.theme.light,
            (0, self.tab_font_height), 
            (self.screen.get_width(), self.tab_font_height), 1
        )
        pygame.draw.line(
            self.header_background, self.theme.light,
            (0, self.theme.TAB_SCREEN_EDGE_LENGTH + self.tab_font_height), 
            (0, self.tab_font_height), 1
        )
        pygame.draw.line(
            self.header_background, self.theme.light,
            (self.screen.get_width()-1, self.tab_font_height + self.theme.TAB_SCREEN_EDGE_LENGTH),
            (self.screen.get_width()-1, self.tab_font_height), 1
        )
        
        # Create tab highlight surfaces
        for i, tab in enumerate(self.tab_names):
            surface = pygame.Surface((self.screen.get_width(), self.tab_font_height + 1), pygame.SRCALPHA)
            tab_width = self.main_tab_font.size(tab)[0]
            x_start = self.tab_x_offset[i] - self.theme.TAB_HORIZONTAL_LINE_OFFSET
            x_end = self.tab_x_offset[i] + tab_width + self.theme.TAB_HORIZONTAL_LENGTH
            
            # Draw highlight elements
            pygame.draw.line(surface, self.theme.background, 
                            (x_start, self.tab_font_height), (x_end, self.tab_font_height), 1)
            pygame.draw.line(surface, self.theme.light,
                            (x_start, self.tab_font_height), 
                            (x_start, self.tab_font_height - self.theme.TAB_VERTICAL_LINE_OFFSET), 1)
            pygame.draw.line(surface, self.theme.light,
                            (x_end, self.tab_font_height), 
                            (x_end, self.tab_font_height - self.theme.TAB_VERTICAL_LINE_OFFSET), 1)
            pygame.draw.line(surface, self.theme.light,
                            (x_start, self.tab_font_height - self.theme.TAB_VERTICAL_LINE_OFFSET),
                            (x_start + self.theme.TAB_SCREEN_EDGE_LENGTH, 
                             self.tab_font_height - self.theme.TAB_VERTICAL_LINE_OFFSET), 1)
            pygame.draw.line(surface, self.theme.light,
                            (x_end, self.tab_font_height - self.theme.TAB_VERTICAL_LINE_OFFSET),
                            (x_end - self.theme.TAB_SCREEN_EDGE_LENGTH, 
                             self.tab_font_height - self.theme.TAB_VERTICAL_LINE_OFFSET), 1)
            
            self.tab_highlight_surfaces.append(surface)
    
    def _init_subtab_data(self):
        """Pre-render all possible subtab states"""
        for tab_name in self.tab_names:
            subtabs = self.registry.get_sub_tabs(tab_name)
            if not subtabs:
                continue
            
            active_surfaces = []
            inactive_surfaces = []
            total_widths = []
            self.subtab_offsets[tab_name] = []
            
            # Create individual text surfaces
            for subtab in subtabs:
                active = self.main_tab_font.render(subtab, True, self.theme.light)
                inactive = self.main_tab_font.render(subtab, True, self.theme.dark)
                active_surfaces.append(active)
                inactive_surfaces.append(inactive)
                total_widths.append(active.get_width())
            
            # Calculate offsets for centering
            cumulative_width = 0
            for i, width in enumerate(total_widths):
                main_tab_center = (self.tab_x_offset[self.tab_names.index(tab_name)] + 
                                 self.main_tab_font.size(tab_name)[0] / 2)
                subtab_center = cumulative_width + (width / 2)
                required_offset = main_tab_center - subtab_center
                self.subtab_offsets[tab_name].append(required_offset)
                cumulative_width += width + self.theme.SUBTAB_SPACING
            
            # Create complete subtab bar surfaces
            self.subtab_bar_surfaces[tab_name] = []
            for active_idx in range(len(subtabs)):
                surface = pygame.Surface((
                    self.screen.get_width(), 
                    self.tab_font_height + self.theme.TAB_SCREEN_EDGE_LENGTH
                ), pygame.SRCALPHA)
                current_x = self.subtab_offsets[tab_name][active_idx]
                
                for i in range(len(subtabs)):
                    text_surf = active_surfaces[i] if i == active_idx else inactive_surfaces[i]
                    surface.blit(text_surf, (current_x, self.theme.SUBTAB_VERTICAL_OFFSET))
                    current_x += text_surf.get_width() + self.theme.SUBTAB_SPACING
                
                self.subtab_bar_surfaces[tab_name].append(surface)
    
    def switch_tab(self, direction: bool):
        """
        Switch to next/previous tab.
        
        Args:
            direction: True for next tab, False for previous
        """
        with self.switch_lock:
            prev_tab_index = self.current_tab_index
            self.previous_tab_index = self.current_tab_index
            self.current_tab_index = max(0, min(
                (self.current_tab_index + (1 if direction else -1)) % len(self.tab_names), 
                len(self.tab_names) - 1
            ))
        
        # Handle tab activation/deactivation
        if prev_tab_index != self.current_tab_index:
            if prev_tab_index in self.tab_instances:
                self.tab_instances[prev_tab_index].deactivate()
            if self.current_tab_index in self.tab_instances:
                self.tab_instances[self.current_tab_index].activate()
        
        # Update thread handler
        self.thread_handler.update_tab_index(self.current_tab_index)
        
        # Apply visual effects
        if random.randrange(100) < self.theme.GLITCH_MOVE_CHANCE:
            if self.glitch_thread is None or not self.glitch_thread.is_alive():
                self.glitch_thread = Thread(target=self._tab_switch_glitch, daemon=True)
                self.glitch_thread.start()
        else:
            self.render_blur = True
    
    def switch_sub_tab(self, direction: bool):
        """
        Switch to next/previous sub-tab within current tab.
        
        Args:
            direction: True for next sub-tab, False for previous
        """
        current_main_index = self.current_tab_index
        current_sub_index = self.current_sub_tab_index[current_main_index]
        tab_name = self.tab_names[current_main_index]
        subtabs = self.registry.get_sub_tabs(tab_name)
        
        if not subtabs:
            return
        
        new_index = current_sub_index + (1 if direction else -1)
        new_index = max(0, min(new_index, len(subtabs) - 1))
        self.current_sub_tab_index[current_main_index] = new_index
        
        if new_index != current_sub_index:
            # Notify tab of sub-tab change
            if current_main_index in self.tab_instances:
                self.tab_instances[current_main_index].change_sub_tab(new_index)
    
    def _tab_switch_glitch(self):
        """Execute tab switch glitch effect"""
        for frame in range(self.theme.GLITCH_FRAME_COUNT):
            time = pygame.time.get_ticks()
            jump_offset = int(20 * math.sin(time))
            self.screen.blit(self.screen, (0, -jump_offset))
            pygame.time.wait(100)
    
    def scroll(self, direction: bool):
        """Forward scroll action to current tab"""
        if self.current_tab_index in self.tab_instances:
            self.tab_instances[self.current_tab_index].scroll(direction)
    
    def select_item(self):
        """Forward select action to current tab"""
        if self.current_tab_index in self.tab_instances:
            self.tab_instances[self.current_tab_index].select_item()
    
    def navigate(self, direction: int):
        """Forward navigation to current tab"""
        if self.current_tab_index in self.tab_instances:
            self.tab_instances[self.current_tab_index].navigate(direction)
    
    def render_header(self):
        """Render the pre-rendered header elements"""
        if self.header_background:
            self.screen.blit(self.header_background, (0, 0))
        if 0 <= self.current_tab_index < len(self.tab_highlight_surfaces):
            self.screen.blit(self.tab_highlight_surfaces[self.current_tab_index], (0, 0))
    
    def render_sub_tabs(self):
        """Render the pre-rendered subtab bar"""
        if not self.tab_names:
            return
        
        current_tab = self.tab_names[self.current_tab_index]
        if current_tab not in self.subtab_bar_surfaces:
            return
        
        subtab_index = self.current_sub_tab_index[self.current_tab_index]
        surfaces = self.subtab_bar_surfaces[current_tab]
        
        if 0 <= subtab_index < len(surfaces):
            surface = surfaces[subtab_index]
            y_pos = self.tab_font_height + self.theme.TAB_SCREEN_EDGE_LENGTH
            self.screen.blit(surface, (0, y_pos))
    
    def render_tab(self):
        """Render the current tab content"""
        if self.current_tab_index in self.tab_instances:
            self.tab_instances[self.current_tab_index].render()
    
    def apply_blur_effect(self):
        """Apply blur transition effect"""
        if self.render_blur:
            screen_copy = self.screen.copy()
            for blur_radius in self.theme.BLUR_ITERATIONS:
                try:
                    blur = pygame.transform.box_blur(screen_copy, blur_radius)
                    blur.set_alpha(self.theme.BLUR_ALPHA)
                    self.screen.blit(blur, (0, 0), special_flags=pygame.BLEND_ADD)
                except AttributeError:
                    # Fallback for older pygame versions
                    pass
            self.render_blur = False
    
    def render(self):
        """Render the complete tab system"""
        self.render_header()
        self.render_sub_tabs()
        self.render_tab()
        self.apply_blur_effect()


# Convenience functions
def create_tab_system(screen: pygame.Surface, theme, registry: TabRegistry) -> TabSystem:
    """Create a new tab system with specified components"""
    return TabSystem(screen, theme, registry)