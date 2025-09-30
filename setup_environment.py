"""
Sovereign OSINT Toolkit - Environment Setup Script
Automates virtual environment creation and dependency installation
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and handle errors"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def detect_python():
    """Detect available Python executable"""
    python_candidates = ['python3', 'python', 'py']
    
    for candidate in python_candidates:
        success, stdout, stderr = run_command(f"{candidate} --version", check=False)
        if success:
            return candidate
    
    print("❌ No Python installation found!")
    sys.exit(1)

def create_venv():
    """Create virtual environment"""
    python_cmd = detect_python()
    venv_name = "sovereign_env"
    
    print(f"🐍 Using Python: {python_cmd}")
    print(f"📁 Creating virtual environment: {venv_name}")
    
    # Create virtual environment
    success, stdout, stderr = run_command(f"{python_cmd} -m venv {venv_name}")
    
    if not success:
        print(f"❌ Failed to create virtual environment: {stderr}")
        sys.exit(1)
    
    print("✅ Virtual environment created successfully!")
    return venv_name

def get_activation_command(venv_name):
    """Get the activation command based on OS"""
    system = platform.system().lower()
    
    if system == "windows":
        return f"{venv_name}\\Scripts\\activate"
    else:  # linux, darwin (macOS)
        return f"source {venv_name}/bin/activate"

def install_dependencies(venv_name):
    """Install project dependencies in the virtual environment"""
    system = platform.system().lower()
    
    # Get pip path based on OS
    if system == "windows":
        pip_path = f"{venv_name}\\Scripts\\pip"
    else:
        pip_path = f"{venv_name}/bin/pip"
    
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    run_command(f"{pip_path} install --upgrade pip")
    
    # Install requirements
    success, stdout, stderr = run_command(f"{pip_path} install -r requirements.txt")
    
    if success:
        print("✅ All dependencies installed successfully!")
    else:
        print(f"❌ Dependency installation failed: {stderr}")
        sys.exit(1)

def main():
    """Main setup function"""
    print("🦁 Sovereign OSINT Toolkit - Environment Setup")
    print("=" * 50)
    
    # Check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Already in a virtual environment. Continuing anyway...")
    
    # Create virtual environment
    venv_name = create_venv()
    
    # Install dependencies
    install_dependencies(venv_name)
    
    # Display next steps
    activation_cmd = get_activation_command(venv_name)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print(f"1. Activate virtual environment: {activation_cmd}")
    print("2. Run the dashboard: streamlit run src/visualization/dashboard/app.py")
    print("3. Deactivate when done: deactivate")
    
    # Create a quick activation script for convenience
    create_activation_script(venv_name, activation_cmd)

def create_activation_script(venv_name, activation_cmd):
    """Create quick activation scripts for user convenience"""
    
    # Create activate.sh for Unix systems
    with open('activate_sovereign.sh', 'w') as f:
        f.write(f"""#!/bin/bash
echo "🦁 Activating Sovereign OSINT Environment"
{activation_cmd}
echo "✅ Virtual environment activated!"
echo "🚀 Run: streamlit run src/visualization/dashboard/app.py"
echo "🔴 Deactivate with: deactivate"
""")
    
    # Create activate.bat for Windows
    with open('activate_sovereign.bat', 'w') as f:
        f.write(f"""@echo off
echo 🦁 Activating Sovereign OSINT Environment
call {venv_name}\\Scripts\\activate
echo ✅ Virtual environment activated!
echo 🚀 Run: streamlit run src/visualization/dashboard/app.py
echo 🔴 Deactivate with: deactivate
""")
    
    # Make shell script executable
    if platform.system().lower() != "windows":
        os.chmod('activate_sovereign.sh', 0o755)
    
    print(f"\n📜 Quick activation scripts created:")
    print(f"   - activate_sovereign.sh (macOS/Linux)")
    print(f"   - activate_sovereign.bat (Windows)")

if __name__ == "__main__":
    main()