import hashlib

"""
Computes SHA256 hash
Args:
    data: list
Returns:
    str, computed hash
"""
def hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

"""
Computes checksum
Args:
    prev_hash: list, previously computed hash from previous scrape
Returns:
    bool
"""
def checksum(prev_hash, data):
    new_merkle = compute_merkle(data)
    return hashlib.compare_digest(bytes.fromhex(prev_hash), bytes.fromhex(new_merkle))

"""
Computes merkle root
Args:
    data: list
Returns:
    str, computed merkle root
"""
def compute_merkle(data):
    if not data:
        return None
    if len(data) == 1:
        return hash(data[0])
    next_level = []
    for i in range(0, len(data), 2):
        combined_hash = hash(data[i] + data[i + 1])
        next_level.append(combined_hash)
    return compute_merkle(next_level)

    
        
