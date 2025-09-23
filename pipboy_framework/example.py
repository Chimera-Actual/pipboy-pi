"""
Pip-Boy Framework Example

Demonstrates how to use the framework to create a simple Pip-Boy style interface
with multiple tabs and authentic retro styling.
"""

import sys
import os

# Add the framework to the path
sys.path.insert(0, os.path.dirname(__file__))

from core.framework import create_framework
from tabs.example_tab import ExampleTab, DemoTab


def main():
    """Main function demonstrating framework usage"""
    print("Starting Pip-Boy Framework Example...")
    
    # Create framework instance
    framework = create_framework(
        screen_size=(1024, 768),
        color_scheme="classic_green",
        fullscreen=False,
        fps=24
    )
    
    # Register tabs
    framework.register_tab("EXAMPLE", ExampleTab)
    framework.register_tab("DEMO", DemoTab)
    
    # Optional: Add sub-tabs for demonstration
    # framework.register_tab("MULTI", ExampleTab, ["SUB1", "SUB2", "SUB3"])
    
    print("Framework configured with tabs:")
    for tab_name in framework.registry.get_tab_names():
        sub_tabs = framework.registry.get_sub_tabs(tab_name)
        if sub_tabs:
            print(f"  {tab_name}: {', '.join(sub_tabs)}")
        else:
            print(f"  {tab_name}")
    
    print("\nControls:")
    print("  Left/Right Arrow: Switch tabs")
    print("  Up/Down Arrow: Switch sub-tabs")
    print("  W/S: Scroll within tab")
    print("  Enter/Space: Select item")
    print("  Escape: Exit")
    
    try:
        # Run the framework
        framework.run()
    except Exception as e:
        print(f"Error running framework: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)