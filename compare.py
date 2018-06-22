import math


class VectorCompare:
    def __init__(self):
        pass

    @staticmethod
    def magnitude(concordance):
        total = 0
        for word, count in list(concordance.items()):
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in list(concordance1.items()):
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
