"""
Example Tab Implementation

Demonstrates how to create custom tabs using the Pip-Boy framework.
Shows basic functionality including lists, data display, and interaction.
"""

import pygame
from typing import List
from pipboy_framework.core.tab_system import BaseTab
from pipboy_framework.ui.components import create_list, create_grid


class ExampleTab(BaseTab):
    """
    Example tab showing basic framework functionality.
    Displays a simple list and some sample data.
    """
    
    def __init__(self, screen: pygame.Surface, theme, draw_space: pygame.Rect):
        super().__init__(screen, theme, draw_space)
        
        # Example data
        self.items = [
            "First Item",
            "Second Item", 
            "Third Item",
            "Fourth Item",
            "Fifth Item"
        ]
        
        self.stats = [10, 25, 5, 50, 100]
        
        # Create UI components
        list_rect = pygame.Rect(
            draw_space.x + 20, 
            draw_space.y + 20, 
            draw_space.width // 2 - 40, 
            draw_space.height - 40
        )
        
        self.item_list = create_list(
            list_rect, 
            theme, 
            self.items, 
            enable_dot=True, 
            stats=self.stats
        )
        
        # Grid for info display
        grid_rect = pygame.Rect(
            draw_space.x + draw_space.width // 2 + 20,
            draw_space.y + 20,
            draw_space.width // 2 - 40,
            draw_space.height - 40
        )
        
        self.info_grid = create_grid(grid_rect, theme)
        
        # Initialize footer
        self._init_footer()
        
        # State
        self.selected_item_index = 0
        
    def _init_footer(self):
        """Initialize the footer for this tab"""
        footer_text = self.footer_font.render(
            "Example Tab - Navigate with arrows, select with Enter", 
            True, 
            self.theme.light
        )
        self.init_footer("main", text_surface=footer_text)
    
    def _update_info_grid(self):
        """Update the information grid with current selection"""
        selected_item = self.items[self.item_list.selected_index] if self.items else "None"
        selected_stat = self.stats[self.item_list.selected_index] if self.stats else 0
        
        entries = [
            {
                "label": "Selected Item",
                "value": selected_item,
                "highlight": True
            },
            {
                "label": "Item Value",
                "value": str(selected_stat)
            },
            {
                "label": "Total Items",
                "value": str(len(self.items))
            },
            {
                "label": "Framework Demo",
                "value": "Active",
                "highlight": False
            }
        ]
        
        self.info_grid.update(entries)
    
    def activate(self):
        """Called when this tab becomes active"""
        super().activate()
        self._update_info_grid()
    
    def deactivate(self):
        """Called when this tab becomes inactive"""
        super().deactivate()
    
    def scroll(self, direction: bool):
        """Handle scrolling through the list"""
        if self.item_list:
            self.item_list.change_selection(direction)
            self._update_info_grid()
    
    def select_item(self):
        """Handle item selection"""
        selected = self.item_list.get_selected_item()
        if selected:
            # Update footer with selection info
            footer_text = self.footer_font.render(
                f"Selected: {selected}", 
                True, 
                self.theme.light
            )
            self.update_footer("main", footer_text, (10, 5))
    
    def render(self):
        """Render the tab content"""
        # Clear the draw area
        pygame.draw.rect(self.screen, self.theme.background, self.draw_space)
        
        # Render components
        if self.item_list:
            self.item_list.render(self.screen, was_selected=True)
        
        if self.info_grid:
            self.info_grid.render(self.screen)
        
        # Render footer
        self.render_footer("main")


class DemoTab(BaseTab):
    """
    Another example tab demonstrating different content.
    Shows how to create multiple tabs with different functionality.
    """
    
    def __init__(self, screen: pygame.Surface, theme, draw_space: pygame.Rect):
        super().__init__(screen, theme, draw_space)
        
        # Demo content
        self.demo_text = [
            "This is a demo tab",
            "It shows different content",
            "Than the example tab",
            "Use tab navigation to switch",
            "Between different sections"
        ]
        
        # Initialize footer
        footer_text = self.footer_font.render(
            "Demo Tab - Switch tabs to see different content", 
            True, 
            self.theme.light
        )
        self.init_footer("main", text_surface=footer_text)
    
    def activate(self):
        """Called when this tab becomes active"""
        super().activate()
    
    def deactivate(self):
        """Called when this tab becomes inactive"""
        super().deactivate()
    
    def render(self):
        """Render the demo content"""
        # Clear the draw area
        pygame.draw.rect(self.screen, self.theme.background, self.draw_space)
        
        # Render demo text
        font = self.theme.get_main_font(16)
        y_offset = self.draw_space.y + 50
        
        for i, line in enumerate(self.demo_text):
            text_surface = font.render(line, True, self.theme.light)
            x_center = self.draw_space.x + (self.draw_space.width // 2) - (text_surface.get_width() // 2)
            self.screen.blit(text_surface, (x_center, y_offset + i * 30))
        
        # Add a simple animated element
        time = pygame.time.get_ticks()
        pulse_alpha = int(128 + 127 * (0.5 + 0.5 * pygame.math.cos(time * 0.003)))
        
        # Create a pulsing rectangle
        pulse_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
        pulse_color = (*self.theme.darker, pulse_alpha)
        pygame.draw.rect(pulse_surface, pulse_color, (0, 0, 200, 50), 2)
        
        pulse_x = self.draw_space.x + (self.draw_space.width // 2) - 100
        pulse_y = self.draw_space.y + self.draw_space.height - 100
        self.screen.blit(pulse_surface, (pulse_x, pulse_y))
        
        # Render footer
        self.render_footer("main")