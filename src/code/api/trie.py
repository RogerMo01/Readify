class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False
        self.books = set()

class Trie:
    def __init__(self, books_by_word):
        self.root = TrieNode()
        self.books_by_word = books_by_word
        self.build_trie()

    def build_trie(self):
        for word in self.books_by_word.keys():
            self.insert(word)

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end = True
        node.books = self.books_by_word[word]

    def search(self, word):
        node = self.root
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return (False, set())

        return (node.end, node.books)

