from PIL import Image
import os
import glob
import re


class Layer:
    def __init__(self, group='16', part='head', genders=['']):
        self.group = group
        self.part = part
        self.dna_codes = list()
        self.is_gender_specific = True if len(genders) > 1 else False
        for gender in genders:
            self.dna_codes.extend(Layer.allDnaCodes(self.group, self.part, gender))

        self.images = dict()
        for dna_code in self.dna_codes:
            picfile = 'faces/images/{}/{}-{}.png'.format(group, part, dna_code)
            self.images[dna_code] = Image.open(picfile)

    def draw(self, canvas, dna_code, location=(0,0)):
        canvas.paste(self.images[dna_code], location, mask=self.images[dna_code])

    @classmethod
    def allTypes(cls, group, part, gender=''):
        result = list()

        for f in glob.glob('faces/images/{}/{}-{}*.png'.format(group, part, gender)):
            #print(f)
            result.append(cls(picfile=f))

        return result

    @classmethod
    def allDnaCodes(cls, group, part, gender=''):
        result = list()

        for f in glob.glob('faces/images/{}/{}-{}*.png'.format(group, part, gender)):
            #print('faces/images/{}/{}-({}.+)\.png'.format(group, part, gender))
            m = re.search('faces/images/{}/{}-({}.+)\.png'.format(group, part, gender), f)
            #if m:
            #print(m.group(1))
            result.append(m.group(1))

        return result
