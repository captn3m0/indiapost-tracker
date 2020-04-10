import math

class VectorCompare:
  def magnitude(self,concordance):
    total = 0
    for word,count in concordance.items():
      total += count ** 2
    return math.sqrt(total)

  def relation(self,concordance1, concordance2):
    relevance = 0
    topvalue = 0
    for word, count in concordance1.items():
      if word in concordance2:
        topvalue += count * concordance2[word]
    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
