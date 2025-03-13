import hashlib

def calculate_file_hash(file_path, chunk_size=8192):
    """Calculate a hash for the given file"""
    hasher = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        
        return hasher.hexdigest()
        
    except IOError as e:
        raise ValueError(f"Failed to read file: {str(e)}")
