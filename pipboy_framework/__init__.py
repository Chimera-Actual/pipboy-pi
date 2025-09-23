"""
Pip-Boy Framework

A clean, reusable framework for creating authentic Pip-Boy style interfaces
with tab/sub-tab navigation and retro styling.
"""

from .core.framework import PipBoyFramework, create_framework
from .core.theme import PipBoyTheme, create_theme
from .core.tab_system import BaseTab, TabRegistry, TabSystem, create_tab_system
from .ui.components import BaseList, DataGrid, create_list, create_grid
from .ui.effects import EffectManager, create_effect_manager

__version__ = "1.0.0"
__author__ = "Pip-Boy Framework"

__all__ = [
    # Core framework
    'PipBoyFramework', 'create_framework',
    
    # Theme system
    'PipBoyTheme', 'create_theme',
    
    # Tab system
    'BaseTab', 'TabRegistry', 'TabSystem', 'create_tab_system',
    
    # UI components
    'BaseList', 'DataGrid', 'create_list', 'create_grid',
    
    # Effects
    'EffectManager', 'create_effect_manager'
]