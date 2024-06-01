class Trie:

    def __init__(self):
        self.head = {}

    def add(self, word):
        cur = self.head
        for ch in word:
            if ch not in cur:
                cur[ch] = {}
            cur = cur[ch]
        # '*' indicates the end of the word
        cur['*'] = word

    def searchIn(self, word):
        cur = self.head
        for ch in word:
            if ch not in cur:
                return False
            cur = cur[ch]

        if '*' in cur:
            #print(cur['*'],"-- spotted", end =" ")
            return True
        else:
            return False