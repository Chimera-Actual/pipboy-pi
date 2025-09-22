try:
    from .wireframe import *
except ImportError:
    # Fallback implementation when wireframe module isn't available
    def draw_wireframe_sphere(*args, **kwargs):
        pass
    
    def draw_wireframe_cube(*args, **kwargs):
        pass