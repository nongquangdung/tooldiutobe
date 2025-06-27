#!/usr/bin/env python3
"""
Script to update Voice Studio client with production license server URL
"""

import sys
import re

def update_license_manager_url(new_url):
    """Update license server URL in license_manager.py"""
    
    license_manager_path = "src/core/license_manager.py"
    
    try:
        # Read current file
        with open(license_manager_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find license_server_url
        pattern = r'self\.license_server_url\s*=\s*["\'][^"\']*["\']'
        new_line = f'self.license_server_url = "{new_url}"'
        
        # Replace the URL
        updated_content = re.sub(pattern, new_line, content)
        
        # Write back to file
        with open(license_manager_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated license server URL to: {new_url}")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {license_manager_path}")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        return False

def main():
    print("🔧 VOICE STUDIO CLIENT URL UPDATER")
    print("==================================")
    
    if len(sys.argv) > 1:
        new_url = sys.argv[1]
    else:
        print("Enter your production license server URL:")
        print("Examples:")
        print("  Heroku: https://my-voice-studio.herokuapp.com")
        print("  DigitalOcean: https://license.mydomain.com")
        print("  AWS: https://xxxxx.execute-api.region.amazonaws.com/dev")
        print("")
        new_url = input("URL: ").strip()
    
    # Validate URL
    if not new_url.startswith(('http://', 'https://')):
        print("❌ URL must start with http:// or https://")
        return
    
    # Ensure URL doesn't end with slash
    new_url = new_url.rstrip('/')
    
    # Update the file
    if update_license_manager_url(new_url):
        print("")
        print("🎉 CLIENT UPDATE SUCCESSFUL!")
        print("===========================")
        print(f"License Server URL: {new_url}")
        print("")
        print("📋 Next steps:")
        print("1. Test connection: python simple_license_demo.py")
        print("2. Run Voice Studio: python src/main.py")
        print("3. Go to Advanced Window → License Tab")
        print("4. Enter a license key and activate!")
        print("")
        print("🔑 Demo license keys:")
        print("   Basic: VS-FDJCRLSW-DJ0NY94X-CWAJQOSY")
        print("   Pro: VS-MKDERGNT-7QZ0P9LG-VLRUN2H9")
        print("   Enterprise: VS-58FE6CRJ-8GIK1NMF-KY7LZQAH")

if __name__ == "__main__":
    main() 