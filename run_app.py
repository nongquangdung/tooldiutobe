#!/usr/bin/env python3
"""
Simple launcher script for the Voice Studio application
Handles Python path setup and runs the main application
"""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

# Change to src directory
os.chdir(src_path)

# Import and run main
from main import main

if __name__ == "__main__":
    main()