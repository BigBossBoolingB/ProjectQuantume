import base64
import json
import os
from typing import Dict, Any

class Cypher:
    """
    Implements the 'Cyrillic Cypher' logic for state encryption.
    Currently uses Base64 encoding as a foundational obfuscation layer,
    simulating the encryption protocol for the Sovereign entity.
    """

    def encrypt(self, data: str) -> str:
        """Encrypts the data using the cypher."""
        # Encode to bytes, then base64, then decode back to string
        encoded_bytes = base64.b64encode(data.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def decrypt(self, data: str) -> str:
        """Decrypts the data using the cypher."""
        # Encode to bytes, then base64 decode, then decode back to string
        decoded_bytes = base64.b64decode(data.encode('utf-8'))
        return decoded_bytes.decode('utf-8')

    def load_state(self, filepath: str) -> Dict[str, Any]:
        """Loads and decrypts the state from the given filepath."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"State file not found: {filepath}")

        with open(filepath, 'r') as f:
            content = f.read()

        if not content:
             return {}

        try:
            decrypted_json = self.decrypt(content)
            return json.loads(decrypted_json)
        except Exception as e:
            # If decryption fails or json is invalid, raise
            raise ValueError(f"Failed to decrypt/parse state: {e}")

    def save_state(self, state: Dict[str, Any], filepath: str) -> None:
        """Encrypts and saves the state to the given filepath."""
        json_str = json.dumps(state, indent=4)
        encrypted_content = self.encrypt(json_str)
        with open(filepath, 'w') as f:
            f.write(encrypted_content)
