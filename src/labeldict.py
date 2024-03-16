class LabelDict:

    def __init__(self, labels):
        self.codes2labels_dct = []
        self.labels2codes_dct = {}
        i = 0
        for l in labels:
            if l not in self.labels2codes_dct:
                self.labels2codes_dct[l] = i
                i += 1
                self.codes2labels_dct.append(l)

    def codes2labels(self, cds):
        return [self.codes2labels_dct[c] for c in cds]
    
    def labels2codes(self, lbls):
        return [self.labels2codes_dct[l] for l in lbls]
    