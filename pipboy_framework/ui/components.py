"""
Pip-Boy Framework UI Components

Reusable UI components for creating authentic Pip-Boy interfaces.
Includes lists, grids, and animated elements with the classic retro styling.
"""

import pygame
from threading import Thread, Event, Lock
from typing import List, Optional, Any, Tuple, Dict, Callable
from abc import ABC, abstractmethod


class BaseList:
    """
    Base scrollable list component with Pip-Boy styling.
    Supports item selection, highlighting, and optional stats display.
    """
    
    def __init__(self, draw_space: pygame.Rect, theme, items: Optional[List[str]] = None,
                 enable_dot: bool = False, stats: Optional[List[Any]] = None,
                 dot_size: int = 4, text_margin: int = 10, selection_dot_margin: int = 6):
        """
        Initialize the list component.
        
        Args:
            draw_space: Available drawing area
            theme: PipBoyTheme instance for styling
            items: List of item names to display
            enable_dot: Whether to show selection dots
            stats: Optional list of stats corresponding to items
            dot_size: Size of selection dots
            text_margin: Left margin for text
            selection_dot_margin: Margin for selection dots
        """
        self.draw_space = draw_space
        self.theme = theme
        self.font = theme.get_main_font()
        self.enable_dot = enable_dot
        self.font_height = self.font.get_height()
        self.selection_rect_width = draw_space.width
        
        # Colors
        self.selection_rect_color = theme.light
        self.text_color = theme.light
        self.selected_text_color = theme.dark
        self.text_margin = text_margin

        # Stats-related properties
        self.stats = stats
        if self.stats and items and len(self.stats) != len(items):
            raise ValueError("Length of stats must match the number of items")
        
        if self.stats:
            self.stats_color = theme.light
            self.selected_stats_color = theme.dark
            self.max_stat_width = max([self.font.size(str(stat))[0] for stat in self.stats]) if self.stats else 0

        # Dot-related properties
        self.dot = None
        self.dot_darker = None
        self.dot_size = dot_size
        self.selection_dot_margin = selection_dot_margin
        self.dot_color = theme.light
        self.dot_darker_color = theme.dark

        # Surfaces and state
        self.list_surface = None
        self.selected_text = None
        self.selected_stat = None
        self.view_surface = pygame.Surface((self.draw_space.width, self.draw_space.height), pygame.SRCALPHA)

        # Selection state
        self.selected_index = 0
        self.previously_selected_index = 0
        self.items = items or [""]
        
        # Initialize stats column position
        self.stats_column_center_x = 0
        
        # Initialize components
        self._init_selection_rect()
        self._prepare_list_surface()
        
        if self.enable_dot:
            self._create_dots()

    def _prepare_list_surface(self):
        """Pre-render the list items"""
        if not self.items:
            self.list_surface = pygame.Surface((self.draw_space.width, 0), pygame.SRCALPHA)
            return
            
        height = self.font_height * len(self.items)
        self.list_surface = pygame.Surface((self.draw_space.width, height), pygame.SRCALPHA)
        
        if self.stats:
            self.stats_column_center_x = self.selection_rect_width - self.max_stat_width
            
        for i, item in enumerate(self.items):
            # Render item label
            text_surface = self.font.render(item, True, self.text_color)
            self.list_surface.blit(text_surface, (self.text_margin, i * self.font_height))
            
            # Render stat if enabled
            if self.stats:
                stat = str(self.stats[i])
                stat_surface = self.font.render(stat, True, self.stats_color)
                stat_x = self.stats_column_center_x - (stat_surface.get_width() // 2)
                self.list_surface.blit(stat_surface, (stat_x, i * self.font_height))
                
        self.update_list()

    def _create_dots(self):
        """Initialize dot surfaces only if enabled"""
        self.dot = pygame.Surface((self.dot_size, self.dot_size), pygame.SRCALPHA)
        self.dot.fill(self.dot_color)
        self.dot_darker = pygame.Surface((self.dot_size, self.dot_size), pygame.SRCALPHA)
        self.dot_darker.fill(self.dot_darker_color)

    def _init_selection_rect(self):
        """Initialize the selection rectangle"""
        self.selection_rect = pygame.Rect(0, 0, self.selection_rect_width, self.font_height)

    def set_items(self, items: List[str], stats: Optional[List[Any]] = None):
        """Update the list items and optionally their stats"""
        self.items = items
        if stats is not None:
            if len(stats) != len(items):
                raise ValueError("Length of stats must match the number of items")
            self.stats = stats
        else:
            self.stats = None
            
        if self.selected_index >= len(self.items):
            self.selected_index = max(0, len(self.items) - 1)
        self._prepare_list_surface()

    def update_list(self):
        """Update the selection highlight and selected text"""
        if not self.items:
            self.selected_text = None
            return
            
        self.selection_rect.y = self.selected_index * self.font_height
        selected_item = self.items[self.selected_index]
        self.selected_text = self.font.render(selected_item, True, self.selected_text_color)
        
        if self.stats:
            stat = str(self.stats[self.selected_index])
            self.selected_stat = self.font.render(stat, True, self.selected_stats_color)

    def change_selection(self, direction: bool) -> int:
        """
        Change the selected item.
        
        Args:
            direction: True for up, False for down
            
        Returns:
            Previous selection index
        """
        new_index = self.selected_index + (-1 if direction else 1)
        prev_index = self.selected_index
        
        if 0 <= new_index < len(self.items):
            self.selected_index = new_index
            self.update_list()
            
        return prev_index

    def get_selected_item(self) -> Optional[str]:
        """Get the currently selected item"""
        if self.items and 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None

    def render(self, screen: pygame.Surface, active_index: Optional[int] = None, was_selected: bool = False):
        """Render the list to the screen"""
        if not self.list_surface or not self.selected_text:
            return

        self.view_surface.fill(self.theme.background)
        self.view_surface.blit(self.list_surface, (0, 0))

        # Draw selection rectangle
        pygame.draw.rect(self.view_surface, self.selection_rect_color, self.selection_rect)
        self.view_surface.blit(self.selected_text, (self.text_margin, self.selection_rect.y))
        
        if self.stats and self.selected_stat:
            stat_x = self.selection_rect_width - self.max_stat_width - (self.selected_stat.get_width() // 2)
            self.view_surface.blit(self.selected_stat, (stat_x, self.selection_rect.y))

        # Conditional dot rendering
        if self.enable_dot and active_index is not None and was_selected and self.dot and self.dot_darker:
            dot = self.dot_darker if (active_index == self.selected_index) else self.dot
            dot_y = (active_index * self.font_height + 
                    (self.font_height // 2) - 
                    (self.dot_size // 2))
            self.view_surface.blit(dot, (self.text_margin - self.selection_dot_margin, dot_y))

        screen.blit(self.view_surface, (self.draw_space.x, self.draw_space.y))


class DataGrid:
    """
    Grid component for displaying structured data with labels, values, and icons.
    Supports highlighting, dividers, and flexible layout.
    """
    
    def __init__(self, draw_space: pygame.Rect, theme, padding: int = 5, text_margin: float = 0.5):
        """
        Initialize the data grid.
        
        Args:
            draw_space: Available drawing area
            theme: PipBoyTheme instance for styling
            padding: Padding between entries
            text_margin: Margin multiplier for text positioning
        """
        self.draw_space = draw_space
        self.theme = theme
        self.font = theme.get_main_font()
        self.line_height = self.font.get_height()
        self.padding = padding
        self.top_margin = text_margin
        self.bottom_margin = text_margin * 2
        
        # Pre-computed rendering elements
        self.precomputed_bg = []
        self.precomputed_text = []
        self.precomputed_divider = None
        
        # Text surface cache for performance
        self.text_cache: Dict[Tuple[str, Tuple[int, int, int]], pygame.Surface] = {}

    def _get_rendered_text(self, text: str, color: Tuple[int, int, int]) -> pygame.Surface:
        """Get cached rendered text surface"""
        key = (text, color)
        if key not in self.text_cache:
            self.text_cache[key] = self.font.render(text, True, color)
        return self.text_cache[key]

    def update(self, entries: List[Dict[str, Any]]):
        """
        Update the grid with new entries.
        
        Expected entry format:
        {
            'label': str,
            'value': str (optional),
            'icon': pygame.Surface (optional),
            'icon_front': bool (optional),
            'highlight': bool (optional),
            'split': bool (optional),
            'lines': [{'value': str, 'icon': Surface}] (optional)
        }
        """
        self.precomputed_bg = []
        self.precomputed_text = []
        self.precomputed_divider = None
        
        current_y = self.draw_space.bottom - self.theme.GRID_BOTTOM_MARGIN

        # Calculate total height needed
        total_height = sum(
            (self.top_margin + self.line_height + 
             (max(0, len(entry.get("lines", [])) - 1) * self.line_height) + 
             self.bottom_margin) + self.padding
            for entry in entries
        )

        current_y -= total_height
        current_y = max(current_y, self.draw_space.top)

        label_x = self.draw_space.left + self.padding

        for entry in entries:
            if current_y >= self.draw_space.bottom:
                break

            bg_color = self.theme.darker if entry.get("highlight") else self.theme.dark
            entry_lines = []
            label_y = current_y + self.top_margin
            icon_x = label_x
            icon_front_x = label_x
            value_x = self.draw_space.right - self.padding
            
            # Handle front icon
            if entry.get("icon_front") and "icon" in entry:
                icon_surface = entry["icon"]
                entry_lines.append(("icon", icon_surface, (icon_x, label_y + 1)))
                icon_front_x += icon_surface.get_width() + self.padding

            # Label
            label_surface = self._get_rendered_text(entry["label"], self.theme.light)
            label_pos = (icon_front_x, label_y)
            entry_lines.append(("label", label_surface, label_pos))

            value_y = label_y

            # Multi-line values
            if "lines" in entry:
                for i, line in enumerate(entry["lines"]):
                    if i > 0:
                        value_y += self.line_height
                    components = []
                    line_width = 0

                    if "icon" in line:
                        components.append(line["icon"])
                        line_width += line["icon"].get_width() + self.padding

                    text_surface = self.font.render(str(line["value"]), True, self.theme.light)
                    components.append(text_surface)
                    line_width += text_surface.get_width()

                    # Right-align components
                    current_x = value_x - line_width
                    for component in components:
                        y_pos = value_y + (1 if component == line.get("icon") else 0)
                        entry_lines.append(("component", component, (current_x, y_pos)))
                        current_x += component.get_width() + self.padding

            # Single value
            text_width = 0
            if "value" in entry:
                text_surface = self._get_rendered_text(str(entry["value"]), self.theme.light)
                text_width = text_surface.get_width()
                entry_lines.append(("value", text_surface, (value_x - text_width, value_y)))
                
            # Rear icon
            if not entry.get("icon_front") and "icon" in entry:
                icon_surface = entry["icon"]
                icon_x = value_x - icon_surface.get_width() - text_width - (self.padding * 2)
                entry_lines.append(("icon", icon_surface, (icon_x, value_y + 1)))

            # Calculate entry height
            additional_lines = max(0, len(entry.get("lines", [])) - 1)
            entry_height = int(self.top_margin) + self.line_height + additional_lines * self.line_height + int(self.bottom_margin)

            # Store background rectangle
            self.precomputed_bg.append((
                pygame.Rect(self.draw_space.left, current_y, self.draw_space.width, entry_height),
                bg_color
            ))

            # Store text elements
            for element in entry_lines:
                self.precomputed_text.append((element[1], element[2]))

            # Add vertical divider if needed
            if self.precomputed_divider is None and entry.get("split") and icon_x is not None:
                self.precomputed_divider = pygame.Rect(
                    icon_x, current_y, self.padding, entry_height
                )

            current_y += entry_height
            if entry != entries[-1]:
                current_y += self.padding

    def render(self, surface: pygame.Surface):
        """Render the grid to the surface"""
        # Draw backgrounds first
        for rect, bg_color in self.precomputed_bg:
            pygame.draw.rect(surface, bg_color, rect)

        # Draw text and icons
        for text_surface, pos in self.precomputed_text:
            surface.blit(text_surface, pos)

        # Draw vertical divider if it exists
        if self.precomputed_divider is not None:
            pygame.draw.rect(surface, self.theme.background, self.precomputed_divider)


class AnimatedSprite:
    """
    Animated sprite component with threading support.
    Supports looping, sound effects, and frame control.
    """
    
    def __init__(self, screen: pygame.Surface, images: List[pygame.Surface], 
                 position: Tuple[int, int], frame_duration: int, 
                 frame_order: Optional[List[int]] = None, loop: bool = True, 
                 sound_callback: Optional[Callable] = None):
        """
        Initialize animated sprite.
        
        Args:
            screen: Target surface
            images: List of frame images
            position: Screen position
            frame_duration: Duration per frame in milliseconds
            frame_order: Custom frame order (defaults to sequential)
            loop: Whether to loop animation
            sound_callback: Function to call for sound effects
        """
        self.screen = screen
        self.images = images
        self.position = position
        self.frame_duration = frame_duration / 1000.0
        self.frame_order = frame_order or list(range(len(images)))
        self.loop = loop
        self.sound_callback = sound_callback

        self.current_frame_index = 0
        self.done = False
        self.running = False
        self.stop_event = Event()
        self.lock = Lock()
        self.thread = None

    def _update_loop(self):
        """Thread function for updating frames"""
        while not self.stop_event.is_set() and not self.done:
            with self.lock:
                if self.done:
                    break

                self.current_frame_index += 1
                if self.current_frame_index >= len(self.frame_order):
                    if self.loop:
                        self.current_frame_index = 0
                        if self.sound_callback:
                            self.sound_callback()
                    else:
                        self.done = True
                        break

            self.stop_event.wait(timeout=self.frame_duration)

    def start(self):
        """Start the animation"""
        if self.thread is None or not self.thread.is_alive():
            self.done = False
            self.stop_event.clear()
            self.thread = Thread(target=self._update_loop, daemon=True)
            if self.sound_callback:
                self.sound_callback()
            self.thread.start()

    def stop(self):
        """Stop the animation instantly"""
        self.stop_event.set()
        self.thread = None

    def render(self):
        """Render the current frame (thread-safe)"""
        with self.lock:
            if self.images and self.frame_order:
                frame_idx = self.frame_order[self.current_frame_index]
                if 0 <= frame_idx < len(self.images):
                    self.screen.blit(self.images[frame_idx], self.position)

    def reset(self):
        """Reset and restart the animation"""
        self.stop()
        self.current_frame_index = 0
        self.done = False
        self.start()


# Convenience factory functions
def create_list(draw_space: pygame.Rect, theme, items: Optional[List[str]] = None, 
               **kwargs) -> BaseList:
    """Create a new BaseList with theme defaults"""
    return BaseList(draw_space, theme, items, **kwargs)

def create_grid(draw_space: pygame.Rect, theme, **kwargs) -> DataGrid:
    """Create a new DataGrid with theme defaults"""
    return DataGrid(draw_space, theme, **kwargs)