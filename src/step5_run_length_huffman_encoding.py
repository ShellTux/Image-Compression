from collections import defaultdict
from heapq import heapify, heappush, heappop

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequency(image):
    """
    Calculate the frequency of each byte in the image.

    Args:
        image (ndarray): Quantized image.

    Returns:
        dict: Frequency dictionary.
    """
    frequency = defaultdict(int)

    for byte in image.flatten():
        frequency[byte] += 1

    return frequency

def build_huffman_tree(frequency):
    """
    Build the Huffman tree from the frequency dictionary.

    Args:
        frequency (dict): Frequency dictionary.

    Returns:
        Node: Root node of the Huffman tree.
    """
    priority_queue = []

    for char, freq in frequency.items():
        node = Node(char, freq)
        heapify(priority_queue)
        heappush(priority_queue, node)

    while len(priority_queue) > 1:
        node1 = heappop(priority_queue)
        node2 = heappop(priority_queue)

        merged_node = Node(None, node1.freq + node2.freq)
        merged_node.left = node1
        merged_node.right = node2

        heappush(priority_queue, merged_node)

    return priority_queue[0]

def build_codes(root):
    """
    Build the Huffman codes from the Huffman tree.

    Args:
        root (Node): Root node of the Huffman tree.

    Returns:
        dict: Huffman codes dictionary.
    """
    huffman_codes = {}

    def build_codes_recursive(node, code):
        if node.char:
            huffman_codes[node.char] = code

        if node.left:
            build_codes_recursive(node.left, code + "0")

        if node.right:
            build_codes_recursive(node.right, code + "1")

    build_codes_recursive(root, "")

    return huffman_codes

def rle_encoding(image):
    """
    Apply Run-Length Encoding to the image.

    Args:
        image (ndarray): Quantized image.

    Returns:
        str: RLE-encoded image.
    """
    rle_image = ""

    for byte in image.flatten():
        count = 1
        while byte == image.flatten()[image.flatten().index(byte) + 1]:
            count += 1
            image.flatten()[image.flatten().index(byte) + 1] = -1

        rle_image += f"{byte}-{count}"

    return rle_image

def main():
    pass

if __name__ == "__main__":
    main()
