import base64
import json
from typing import Union, Dict, Any

class CyrillicCypher:
    """
    Implements the 'Cyrillic Cypher' logic for state encryption.
    Currently uses Base64 encoding as a foundational obfuscation layer,
    simulating the encryption protocol for the Sovereign entity.
    """

    def encrypt(self, data: Union[str, Dict[str, Any]]) -> str:
        """Encrypts the data using the cypher. Handles dicts by dumping to JSON."""
        if isinstance(data, dict):
            data = json.dumps(data)

        # Encode to bytes, then base64, then decode back to string
        encoded_bytes = base64.b64encode(data.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def decrypt(self, data: str) -> Union[str, Dict[str, Any]]:
        """Decrypts the data using the cypher. Attempts to parse JSON."""
        # Encode to bytes, then base64 decode, then decode back to string
        decoded_bytes = base64.b64decode(data.encode('utf-8'))
        decrypted_str = decoded_bytes.decode('utf-8')

        try:
            return json.loads(decrypted_str)
        except json.JSONDecodeError:
            return decrypted_str
