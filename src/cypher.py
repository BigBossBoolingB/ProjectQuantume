import base64

class CyrillicCypher:
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
