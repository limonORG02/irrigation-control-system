import sys
import os

# Ensure `src` is on sys.path so the project can be run from repository root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from init_demo_data import init_demo_data
from main import main

if __name__ == '__main__':
    init_demo_data()
    main()
