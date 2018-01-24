from PIL import Image
import os
import glob
import re


class BodyPart:
    def __init__(self, group='16', part='head', dna_code='01', picfile=None):
        if picfile is None:
            self.picfile = 'images/{}/{}-{}.png'.format(group, part, dna_code)
        else:
            self.picfile = picfile
        self.position = (0, 0)

    @property
    def picfile(self):
        return self._picfile

    @picfile.setter
    def picfile(self, value):
        if os.path.isfile(value):
            self._picfile = value
        else:
            raise ValueError('Image file {} does not exist.'.format(value))

    def draw(self, canvas, location=(0,0)):
        image = Image.open(self.picfile)
        canvas.paste(image, location, mask=image)

    @classmethod
    def allTypes(cls, group, part, gender=''):
        result = list()

        for f in glob.glob('images/{}/{}-{}*.png'.format(group, part, gender)):
            #print(f)
            result.append(cls(picfile=f))

        return result

    @classmethod
    def allDnaCodes(cls, group, part, gender=''):
        result = list()

        for f in glob.glob('images/{}/{}-{}*.png'.format(group, part, gender)):
            #print('images/{}/{}-({}.+)\.png'.format(group, part, gender))
            m = re.search('images/{}/{}-({}.+)\.png'.format(group, part, gender), f)
            #if m:
            #print(m.group(1))
            result.append(m.group(1))

        return result
