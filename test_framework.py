#!/usr/bin/env python3
"""
Simple test to verify the Pip-Boy framework works correctly.
"""

import sys
import os

# Add framework to path
sys.path.insert(0, '.')

try:
    from pipboy_framework.core.framework import create_framework
    from pipboy_framework.tabs.example_tab import ExampleTab, DemoTab
    print("✓ Framework imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

def test_framework():
    """Test basic framework functionality"""
    print("Testing Pip-Boy Framework...")
    
    try:
        # Create framework
        framework = create_framework(
            screen_size=(800, 600),
            color_scheme="classic_green",
            fullscreen=False,
            fps=24
        )
        print("✓ Framework created successfully")
        
        # Register tabs
        framework.register_tab("TEST", ExampleTab)
        framework.register_tab("DEMO", DemoTab)
        print("✓ Tabs registered successfully")
        
        # Check theme colors
        print(f"✓ Theme loaded: {framework.theme.light}")
        
        # Test tab registry
        tabs = framework.registry.get_tab_names()
        print(f"✓ Registered tabs: {tabs}")
        
        print("✓ Framework test passed - ready for use!")
        return True
        
    except Exception as e:
        print(f"✗ Framework test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_framework()
    sys.exit(0 if success else 1)