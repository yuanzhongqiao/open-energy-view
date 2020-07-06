"""Test the Flask GUI."""

import os

from pgesmd.database import EnergyHistory
from . import create_app

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fill_database():
    """Fill database using the test data."""
    create_app()
    # db = EnergyHistory(path="/test/data/energy_history_test.db")
    
    # db.insert_espi_xml(xml, 50916)
    # print(f"Filled database with data from 2 year xml.")

if __name__ == "__main__":
    fill_database()
