#!/usr/bin/env python3
"""
Demo runner for the Pip-Boy Framework.
This replaces modules/main.py to demonstrate the new framework.
"""

import sys
import os
import pygame

# Ensure we can import the framework
sys.path.insert(0, '.')

try:
    from pipboy_framework.core.framework import create_framework
    from pipboy_framework.tabs.example_tab import ExampleTab, DemoTab
    print("Pip-Boy Framework Demo Starting...")
except ImportError as e:
    print(f"Failed to import framework: {e}")
    sys.exit(1)

def main():
    """Main demo function"""
    try:
        # Create framework with suitable settings for Replit
        framework = create_framework(
            screen_size=(1024, 768),
            color_scheme="classic_green",
            fullscreen=False,
            fps=24
        )
        
        # Register example tabs
        framework.register_tab("EXAMPLE", ExampleTab)
        framework.register_tab("DEMO", DemoTab)
        
        print("Framework initialized successfully!")
        print("Controls: Arrow keys for navigation, Enter to select, Esc to exit")
        
        # Run the framework
        framework.run()
        
    except Exception as e:
        print(f"Error running framework: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)