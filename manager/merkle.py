import hashlib

def hash(data):
    return hashlib.sah256(data).hexdigest()

class MerkleTreeNode:
    def __init__(self, data):
        self.hash = hash
        self.left = None
        self.right = None

class MerkleTree:
    def __init__(self, data):
        self.root = self.construct_tree(data)

    def construct_tree(self, data) -> MerkleTreeNode:
        if len(data) % 2 != 0:
            data.append(data[-1])
        
        return None
        
