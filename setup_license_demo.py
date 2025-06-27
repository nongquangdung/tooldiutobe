#!/usr/bin/env python3
"""
Voice Studio License System Setup & Demo
Script để setup và demo hệ thống license hoàn chỉnh
"""

import os
import sys
import time
import subprocess
import threading
import requests
import json
from datetime import datetime

def print_banner():
    """In banner cho demo"""
    print("=" * 80)
    print("🎤 VOICE STUDIO LICENSE SYSTEM - SETUP & DEMO")
    print("=" * 80)
    print("🔧 Setting up complete license management system...")
    print("   • License server with database")
    print("   • Hardware fingerprinting") 
    print("   • Trial mode with feature limits")
    print("   • Demo licenses for testing")
    print("   • Admin tools for management")
    print("")

def check_dependencies():
    """Kiểm tra dependencies cần thiết"""
    print("📦 Checking dependencies...")
    
    required_packages = ['flask', 'requests', 'PyQt5']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("🔧 Auto-installing missing dependencies...")
        try:
            for package in missing:
                print(f"   Installing {package}...")
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ {package} installed successfully")
                else:
                    print(f"   ❌ Failed to install {package}: {result.stderr}")
                    return False
            print("   ✅ All dependencies installed")
            return True
        except Exception as e:
            print(f"   ❌ Auto-install failed: {e}")
            print("   Please install manually: pip install " + " ".join(missing))
            return False
    
    print("   ✅ All dependencies found")
    return True

def start_license_server():
    """Start license server trong background"""
    print("\n🚀 Starting license server...")
    
    try:
        # Change to license_server directory
        os.chdir("license_server")
        
        # Start server process
        server_process = subprocess.Popen(
            [sys.executable, "start_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # Change back to root
        os.chdir("..")
        
        # Wait for server to start
        print("   Waiting for server to start...")
        for i in range(10):
            try:
                response = requests.get("http://localhost:5000/health", timeout=2)
                if response.status_code == 200:
                    print("   ✅ License server is running on http://localhost:5000")
                    return server_process
            except:
                pass
            
            time.sleep(1)
            print(f"   {'.' * (i + 1)}")
        
        print("   ❌ Failed to start license server")
        return None
        
    except Exception as e:
        print(f"   ❌ Error starting server: {e}")
        return None

def create_demo_licenses():
    """Tạo demo licenses"""
    print("\n📝 Creating demo licenses...")
    
    try:
        # Run admin tool to create demo licenses
        result = subprocess.run([
            sys.executable, "license_server/admin.py", "demo"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Demo licenses created successfully")
            return True
        else:
            print(f"   ❌ Failed to create demo licenses: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error creating demo licenses: {e}")
        return False

def test_license_integration():
    """Test license integration"""
    print("\n🧪 Testing license system integration...")
    
    try:
        result = subprocess.run([
            sys.executable, "simple_license_demo.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ License integration test passed")
            # Print key results
            lines = result.stdout.split('\n')
            for line in lines:
                if "Hardware ID:" in line or "Status:" in line or "SUMMARY" in line:
                    print(f"   {line.strip()}")
            return True
        else:
            print(f"   ❌ License integration test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing license integration: {e}")
        return False

def show_demo_instructions():
    """Hiển thị hướng dẫn sử dụng demo"""
    print("\n" + "=" * 80)
    print("🎯 DEMO INSTRUCTIONS - HOW TO USE")
    print("=" * 80)
    
    # Load demo licenses if available
    demo_keys = []
    try:
        if os.path.exists("license_server/demo_licenses.json"):
            with open("license_server/demo_licenses.json", "r") as f:
                data = json.load(f)
                demo_keys = data.get("licenses", [])
    except:
        pass
    
    print("\n1️⃣  DEMO LICENSE KEYS (copy these for testing):")
    if demo_keys:
        for lic in demo_keys:
            print(f"   📦 {lic['plan'].upper()}: {lic['key']}")
            print(f"      Expires: {lic['expires'][:10]}")
    else:
        print("   VS-DEMO1234-BASIC567-TEST8901 (Basic - 7 days)")
        print("   VS-PRO12345-PREMIUM6-TESTING7 (Pro - 30 days)") 
        print("   VS-ENTERPR8-BUSINESS-SOLUTION (Enterprise - 1 year)")
    
    print(f"\n2️⃣  START VOICE STUDIO:")
    print(f"   python main.py")
    print(f"   → Go to Advanced Window → License Tab")
    print(f"   → Enter a license key and click 'Activate'")
    
    print(f"\n3️⃣  ADMIN MANAGEMENT:")
    print(f"   cd license_server")
    print(f"   python admin.py health              # Check server")
    print(f"   python admin.py create --email test@example.com --plan pro")
    print(f"   python admin.py status --key VS-XXXXXXXX-XXXXXXXX-XXXXXXXX")
    print(f"   python admin.py verify --key VS-XXXXXXXX-XXXXXXXX-XXXXXXXX")
    
    print(f"\n4️⃣  FEATURE TESTING:")
    print(f"   • Trial mode: Basic TTS, 5 exports/day")
    print(f"   • Pro license: All features, unlimited exports") 
    print(f"   • Hardware binding: License tied to this PC")
    print(f"   • Offline support: Works 7 days without internet")
    
    print(f"\n5️⃣  BUSINESS DEPLOYMENT:")
    print(f"   • Deploy license_server/ to cloud (Heroku, AWS, etc.)")
    print(f"   • Update SERVER_URL in license_manager.py")
    print(f"   • Set up domain with SSL certificate")
    print(f"   • Use admin.py for customer license management")
    
    print("\n" + "=" * 80)
    print("🎉 VOICE STUDIO LICENSE SYSTEM READY FOR BUSINESS!")
    print("   Hardware fingerprinting ✅")
    print("   Trial mode with limits ✅") 
    print("   Feature access control ✅")
    print("   License server & admin tools ✅")
    print("   UI integration complete ✅")
    print("=" * 80)

def main():
    """Main setup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return
    
    # Start license server
    server_process = start_license_server()
    if not server_process:
        print("\n❌ Cannot start license server - demo aborted")
        return
    
    try:
        # Create demo licenses
        if create_demo_licenses():
            print("   📋 Demo licenses ready for testing")
        
        # Test license integration  
        if test_license_integration():
            print("   🔧 License system integration confirmed")
        
        # Show instructions
        show_demo_instructions()
        
        # Keep server running
        print(f"\n⏳ License server is running...")
        print(f"   Press Ctrl+C to stop the demo")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n👋 Stopping license server...")
            
    finally:
        # Clean up
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main() 