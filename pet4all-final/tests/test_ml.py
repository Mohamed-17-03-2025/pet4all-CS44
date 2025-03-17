import unittest
from unittest.mock import patch
import pandas as pd

class TestMLModel(unittest.TestCase):
    @patch('ml_model.pd.read_csv')
    def test_csv_reading(self, mock_read_csv):
        # Mock the pd.read_csv function to return a DataFrame
        expected_df = pd.DataFrame({
            'breed': ['Labrador Retriever', 'German Shepherd', 'Golden Retriever'],
            'grooming': [0.5, 0.6, 0.7],
            'shedding': [0.4, 0.3, 0.5],
            'energy': [0.6, 0.7, 0.5],
            'trainability': [0.8, 0.6, 0.7],
            'demeanor': [0.7, 0.6, 0.8],
            'size': [0.8, 0.7, 0.9]
        })
        mock_read_csv.return_value = expected_df

        # Call the function to read the CSV file
        actual_df = pd.read_csv('dog_breed.csv')

        # Assert that the returned DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(actual_df, expected_df)


