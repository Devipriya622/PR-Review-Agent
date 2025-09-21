# main.py
import sys, os
# add the "src" folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.cli import main

if __name__ == "__main__":
    main()
