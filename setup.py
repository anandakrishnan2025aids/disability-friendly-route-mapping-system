"""
Initialization Script for Disability Friendly Route Mapping System
Run this script to set up the database and verify the installation
"""

import sys
import os

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    required = ['flask']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ✗ {package} missing")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed\n")
    return True

def initialize_database():
    """Initialize the SQLite database"""
    print("Initializing database...")
    try:
        from models import init_db
        init_db()
        print("✓ Database initialized successfully\n")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}\n")
        return False

def verify_files():
    """Verify all required files exist"""
    print("Verifying project files...")
    
    required_files = [
        'app.py',
        'models.py',
        'route_calculator.py',
        'templates/navigation.html',
        'static/js/navigation.js',
        'static/css/navigation.css'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} missing")
            missing.append(file)
    
    if missing:
        print(f"\n⚠ Missing files: {', '.join(missing)}")
        return False
    
    print("✓ All required files present\n")
    return True

def print_next_steps():
    """Print instructions for running the application"""
    print("=" * 60)
    print("Setup Complete! 🎉")
    print("=" * 60)
    print("\nNext steps:")
    print("\n1. Start the application:")
    print("   python app.py")
    print("\n2. Open your browser:")
    print("   http://localhost:5000")
    print("\n3. Navigate to Smart Navigation:")
    print("   http://localhost:5000/navigation")
    print("\n4. Test the system:")
    print("   python example_usage.py")
    print("\n5. Read the documentation:")
    print("   - README.md (complete documentation)")
    print("   - QUICKSTART.md (user guide)")
    print("   - ALGORITHM.md (algorithm details)")
    print("\n" + "=" * 60)
    print("Happy navigating! 🗺️♿")
    print("=" * 60)

def main():
    """Main initialization function"""
    print("\n" + "=" * 60)
    print("Disability Friendly Route Mapping System")
    print("Initialization Script")
    print("=" * 60 + "\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Verify files
    if not verify_files():
        print("\n⚠ Some files are missing. Please ensure all files are present.")
        sys.exit(1)
    
    # Step 3: Initialize database
    if not initialize_database():
        print("\n⚠ Database initialization failed. Check error messages above.")
        sys.exit(1)
    
    # Step 4: Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
