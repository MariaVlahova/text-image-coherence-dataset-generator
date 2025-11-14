"""
Environment Check Script
Run this to verify your setup is correct before generating datasets.
"""

import sys
import os

def check_python_version():
    """Check if Python version is adequate."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} - Too old!")
        print("  → Please install Python 3.7 or higher")
        return False

def check_pillow():
    """Check if Pillow is installed."""
    print("\nChecking Pillow (PIL)...")
    try:
        import PIL
        from PIL import Image, ImageDraw, ImageFont
        print(f"  ✓ Pillow {PIL.__version__} - OK")
        return True
    except ImportError:
        print("  ✗ Pillow not found!")
        print("  → Install with: pip install Pillow")
        return False

def check_files():
    """Check if required files exist."""
    print("\nChecking required files...")
    required_files = [
        "main.py",
        "datasetGenaratorPStyle.py",
        "requirements.txt"
    ]
    
    all_found = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file} - Found")
        else:
            print(f"  ✗ {file} - Missing!")
            all_found = False
    
    return all_found

def check_write_permissions():
    """Check if we can write to the current directory."""
    print("\nChecking write permissions...")
    test_file = "test_write_permission.tmp"
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("  ✓ Write permissions - OK")
        return True
    except Exception as e:
        print(f"  ✗ Cannot write to directory!")
        print(f"  → Error: {e}")
        return False

def check_fonts():
    """Check if any fonts can be loaded."""
    print("\nChecking font availability...")
    
    font_paths = [
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\times.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    
    found_fonts = []
    for font_path in font_paths:
        if os.path.exists(font_path):
            found_fonts.append(font_path)
    
    if found_fonts:
        print(f"  ✓ Found {len(found_fonts)} fonts")
        for font in found_fonts[:3]:  # Show first 3
            print(f"    - {font}")
        return True
    else:
        print("  ⚠ No standard fonts found")
        print("  → You may need to update font paths in main.py")
        return True  # Not critical, just a warning

def check_import_modules():
    """Check if we can import our modules."""
    print("\nChecking project modules...")
    try:
        from datasetGenaratorPStyle import create_balanced_dataset, generate_table_data
        print("  ✓ datasetGenaratorPStyle - OK")
        print("  ✓ create_balanced_dataset function - OK")
        print("  ✓ generate_table_data function - OK")
        return True
    except ImportError as e:
        print(f"  ✗ Cannot import modules!")
        print(f"  → Error: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error importing modules!")
        print(f"  → Error: {e}")
        return False

def main():
    """Run all checks."""
    print("=" * 60)
    print("ENVIRONMENT CHECK")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Pillow Library", check_pillow),
        ("Required Files", check_files),
        ("Write Permissions", check_write_permissions),
        ("Font Availability", check_fonts),
        ("Project Modules", check_import_modules),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n  ✗ Unexpected error in {name}!")
            print(f"  → {e}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} checks passed")
    print()
    
    if passed == total:
        print("🎉 All checks passed! You're ready to generate datasets.")
        print("   Run: python main.py")
        print("   Or double-click: run_main.bat")
    elif passed >= total - 1:
        print("⚠ Almost ready! Fix the issues above and try again.")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        print("   Try running: setup.bat")
        print("   Or manually: pip install -r requirements.txt")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

