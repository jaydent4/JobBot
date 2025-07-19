import hashlib

def hash(data):
    return hashlib.sha256(data).hexdigest()

def compare(root1, root2):
    if not root1 and not root2:
        return True
    if not root1 or not root2:
        return False
    if hashlib.compare_digest(bytes.fromhex(root1.hash), bytes.fromhex(root2.hash)):
        return True
    left = compare(root1.left, root2.left)
    right = compare(root1.right, root2.right)
    return left or right

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
        
