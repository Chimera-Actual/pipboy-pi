# PipBoy Pygame Project

## Overview
A Python-based Pip-Boy interface application inspired by the Fallout series, built with Pygame-ce. This interactive application simulates various aspects of the Pip-Boy interface including inventory management, character stats, world map, and radio functionality.

## Recent Changes (September 22, 2025)
- ✅ **Environment Setup**: Configured for Replit environment with proper Python dependencies
- ✅ **Path Configuration**: Fixed all asset paths to work from project root
- ✅ **Audio Handling**: Added graceful fallback for headless/server environments
- ✅ **Display Settings**: Updated for non-fullscreen operation with larger resolution (1024x768)
- ✅ **Dependencies**: Installed pygame-ce, numpy, Pillow, requests, tinytag, keyboard
- ✅ **Missing Files**: Created required configuration files (settings_secrets.py, user_config.py)

## Project Architecture

### Core Structure
- **modules/main.py**: Main application entry point with SDL environment setup
- **modules/pipboy.py**: Core PipBoy class managing the interface
- **modules/settings.py**: Configuration management and game data
- **modules/tab_manager.py**: Tab system coordination (STAT, INV, DATA, MAP, RADIO)

### Key Modules
- **tabs/**: Individual tab implementations (inventory, stats, data, map, radio)
- **data_models.py**: Data structures for items, characters, and UI elements
- **items.py**: Item loading and inventory management system
- **input_manager.py**: Keyboard/controller input handling

### Assets
- **fonts/**: Roboto and TechMono font families
- **images/**: UI overlays, character sprites, item icons, world map
- **sounds/**: Audio effects and ambient sounds (gracefully handled when unavailable)

## User Preferences
- **Display**: Windowed mode preferred for Replit environment
- **Resolution**: 1024x768 for better visibility in web preview
- **Audio**: Optional (gracefully handles absence in headless environments)
- **Configuration**: Uses configure.py for user-friendly setup

## Technical Notes

### Replit-Specific Adaptations
- Audio initialization with fallback for headless environment
- Path corrections from relative to project root
- SDL video driver configuration for server environments
- Graceful handling of missing audio devices

### Known Limitations
- Map functionality requires API keys for full operation
- Audio features limited in headless environments
- Some threading for background tasks (map loading, audio) may show errors but don't affect core functionality

## Running the Application
The application runs via the configured workflow:
```bash
python modules/main.py
```

## Development Notes
- Use `configure.py` to customize player settings, colors, and system preferences
- Items are loaded from `modules/items.ini` configuration file
- Settings can be overridden via `user_config.py`
- Core game loop runs at 24 FPS with threading for UI responsiveness