"""
Module: apikeymanager.py
Author: GlenKusuma

This module provides a ApiKeyManager class for managing API keys stored in a .env file.
"""
from dotenv import dotenv_values

class ApiKeyManager:
    """
    A class for managing API keys stored in a .env file.
    """

    def __init__(self, file_path='.env'):
        """
        Initializes the ApiKeyManager instance.

        Args:
            file_path (str, optional): The path to the .env file. Defaults to '.env'.
        """
        self.file_path = file_path

    def get_api_keys(self):
        """
        Retrieves API keys from the .env file.

        Returns:
            tuple: A tuple containing the API key and secret key bytes.
        """
        # Load variables from .env file
        env_vars = dotenv_values(self.file_path)

        env_api_key = env_vars.get('API_KEY')
        env_secret_key = env_vars.get('SECRET_KEY')

        return env_api_key, env_secret_key.encode('utf-8')

# Example usage
if __name__ == "__main__":
    manager = ApiKeyManager()
    api_key, secret_key_bytes = manager.get_api_keys()
    print("API Key:", api_key)
    print("Secret Key (bytes):", secret_key_bytes)
