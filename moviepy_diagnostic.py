# moviepy_diagnostic.py - Run this to diagnose MoviePy issues
import sys
import os

print("=== MoviePy Diagnostic Script ===")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print()

# Check if moviepy is in sys.modules
print("1. Checking if moviepy is importable...")
try:
    import moviepy
    print(f"✓ MoviePy imported successfully")
    print(f"✓ MoviePy version: {moviepy.__version__}")
    print(f"✓ MoviePy location: {moviepy.__file__}")
    print(f"✓ MoviePy directory: {os.path.dirname(moviepy.__file__)}")
except Exception as e:
    print(f"✗ Error importing moviepy: {e}")
    sys.exit(1)

print()

# Check moviepy directory structure
print("2. Checking MoviePy directory structure...")
moviepy_dir = os.path.dirname(moviepy.__file__)
print(f"Contents of {moviepy_dir}:")
try:
    for item in os.listdir(moviepy_dir):
        item_path = os.path.join(moviepy_dir, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")
except Exception as e:
    print(f"✗ Error listing directory: {e}")

print()

# Check if editor.py exists
print("3. Checking for editor module...")
editor_path = os.path.join(moviepy_dir, "editor.py")
if os.path.exists(editor_path):
    print(f"✓ editor.py found at: {editor_path}")
else:
    print(f"✗ editor.py NOT found at: {editor_path}")
    
    # Check for __init__.py in editor subdirectory
    editor_init_path = os.path.join(moviepy_dir, "editor", "__init__.py")
    if os.path.exists(editor_init_path):
        print(f"✓ editor/__init__.py found at: {editor_init_path}")
    else:
        print(f"✗ editor/__init__.py NOT found at: {editor_init_path}")

print()

# Try to import editor
print("4. Attempting to import moviepy.editor...")
try:
    import moviepy.editor as mp
    print("✓ moviepy.editor imported successfully!")
    print(f"✓ Available functions: {[attr for attr in dir(mp) if not attr.startswith('_')][:10]}...")
except Exception as e:
    print(f"✗ Error importing moviepy.editor: {e}")
    print(f"✗ Error type: {type(e).__name__}")
    
    # Try importing specific components
    print("\n5. Testing individual component imports...")
    components = [
        'moviepy.video.io.VideoFileClip',
        'moviepy.audio.io.AudioFileClip',
        'moviepy.video.fx',
        'moviepy.audio.fx'
    ]
    
    for component in components:
        try:
            module_parts = component.split('.')
            module_name = '.'.join(module_parts[:-1])
            class_name = module_parts[-1]
            
            __import__(module_name)
            print(f"  ✓ {module_name} imported successfully")
        except Exception as comp_e:
            print(f"  ✗ {module_name} failed: {comp_e}")

print()

# Check dependencies
print("6. Checking MoviePy dependencies...")
dependencies = ['decorator', 'imageio', 'imageio_ffmpeg', 'numpy', 'pillow', 'proglog']

for dep in dependencies:
    try:
        __import__(dep)
        print(f"  ✓ {dep} - OK")
    except ImportError as e:
        print(f"  ✗ {dep} - MISSING: {e}")
    except Exception as e:
        print(f"  ✗ {dep} - ERROR: {e}")

print()

# Check FFmpeg
print("7. Checking FFmpeg availability...")
try:
    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"✓ FFmpeg executable found: {ffmpeg_exe}")
    
    # Test if FFmpeg is actually executable
    import subprocess
    result = subprocess.run([ffmpeg_exe, '-version'], capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("✓ FFmpeg is working correctly")
    else:
        print(f"✗ FFmpeg execution failed: {result.stderr}")
        
except Exception as e:
    print(f"✗ FFmpeg check failed: {e}")

print()
print("=== Diagnostic Complete ===")