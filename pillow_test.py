# pillow_test.py
print("Testing Pillow/PIL...")

try:
    import PIL
    print("✓ PIL imported successfully")
    print(f"✓ PIL version: {PIL.__version__}")
except ImportError as e:
    print(f"✗ PIL import failed: {e}")

try:
    from PIL import Image
    print("✓ PIL.Image imported successfully")
except ImportError as e:
    print(f"✗ PIL.Image import failed: {e}")

try:
    import pillow
    print("✓ pillow imported successfully")
except ImportError as e:
    print(f"✗ pillow import failed (this is normal): {e}")

print("Pillow check complete.")