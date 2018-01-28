from . import layer
#from bodypart import bodypart.BodyPart
#from colourpart import colourpart.ColourPart
from . import colourlayer
from PIL import Image
import random
import glob

class Composite:
    def __init__(self, genders):
#        self.group = group

        self.layers = list()
        self.all_dna = dict()
        self.genders = genders

    @staticmethod
    def makeDnaKey(dna):
        gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour = self.dna.split('-')
        return '-'.join([gender, head, eye, mouth, beard, hair, hair_colour, glasses])

    @staticmethod
    def makeDna(gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour):
        return '-'.join([gender, head, eye, eye_colour, mouth, beard, hair, hair_colour, glasses, glasses_colour])

    def draw(self, canvas, dna, location=(0,0)):
        # dna
        # gender
        # head number
        # eye type and colour
        # eye colour
        # mouth type
        # facial hair type
        # hair type
        # hair colour
        # glasses
        # glasses colour
        dna_codes = dna.split('-')

        for idx, dna_code in enumerate(dna_codes[1:]):
            self.layers[idx].draw(canvas, dna_code, location)

    def dnaStep(self, level):
        if level >= len(self.layers):
            return None

        result = dict()
        next_codes = self.dnaStep(level + 1)
        for gender in self.genders:
            result[gender] = list()
            for dna_code in [x for x in self.layers[level].dna_codes
                             if gender == '' or x[0] == gender or not self.layers[level].is_gender_specific]:
                if next_codes is None:
                    result[gender].append(dna_code)
                else:
                    for next_code in next_codes[gender]:
                        result[gender].append('-'.join([dna_code, next_code]))
                        #print('-'.join([dna_code, next_code]))
        return result

    def getAllDna(self):
        result = dict()
        next_codes = self.dnaStep(0)
        for gender in self.genders:
            result[gender] = list()
            for next_code in next_codes[gender]:
                result[gender].append('-'.join([gender, next_code]))
        return result

    @classmethod
    def allFaces(cls, group, genders=['m', 'f']):
        lip_colours = [(240, 50, 20),
                        (250, 30, 200)]
        hair_colours = [(0, 0, 0),
                        (120, 60, 0),
                        (200, 50, 0),
                        (220, 200, 0)]
        eye_colours = [(100, 50, 0),
                       (0, 100, 240),
                       (0, 180, 70)]
        glasses_colours = [(0, 0, 0),
                           (200, 0, 0),
                           (0, 0, 220)]
        result = cls(genders)
        result.layers.append(layer.Layer(group, 'head', genders))
        result.layers.append(colourlayer.ColourLayer(group, 'eye', colours=eye_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'mouth', genders, colours=lip_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'beard', genders, colours=hair_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'hair', genders, colours=hair_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'glasses', genders, colours=glasses_colours))

        result.all_dna = result.getAllDna()

        # Now lose the dna with different coloured facial hair to hair
        new_dna = list()
        for gender in genders:
            for dna in result.all_dna[gender]:
                c = dna.split('-')
                if '.' not in c[4] or c[4].split('.')[1] == c[5].split('.')[1]:
                    new_dna.append(dna)
            result.all_dna[gender] = new_dna

        return result

    @classmethod
    def fillRandomGrid(cls, group='32', grid_width=5, grid_height=5, horizontal_spacing=40, vertical_spacing=40):
        #male_faces = Face.allFaces(group, 'm')
        #female_faces = Face.allFaces(group, 'f')
        #faces = male_faces + female_faces
        faces = cls.allFaces(group)
        for gender in ['m', 'f']:
            print('{} {} faces.'.format(len(faces.all_dna[gender]), gender))
        #print(faces.all_dna)
        all_dna = faces.all_dna['m'] + faces.all_dna['f']
        random.shuffle(all_dna)
        selected = dict()
        for dna in all_dna:
            c = dna.split('-')
            if (c[6][1] == '1' or random.randint(0, 6) == 0) and (
                c[1][1] != '3' or c[5][3] not in ['2', '3']):
                key = '-'.join([c[1], c[2][1], c[3], c[4][:2], c[5], c[6][:2]])
                selected[key] = dna
        select_dna = list(selected.values())
        print('{} selected.'.format(len(selected)))
        print(select_dna)
        # random.shuffle(faces)
        # print("{} male faces and {} female faces.".format(len(male_faces), len(female_faces)))
        width, height = horizontal_spacing * grid_width, vertical_spacing * grid_height
        canvas = Image.new("RGBA", (width, height))
        for i in range(grid_width):
            for j in range(grid_height):
                # face = Face.randomFace('16')
                face_index = j * grid_width + i
                if face_index < len(select_dna):
                    #face = cls(group, faces[face_index])
                    faces.draw(canvas, select_dna[face_index], ((i * horizontal_spacing) + 4, (j * vertical_spacing) + 4))
        new_width, new_height = width * 2, height * 2
        resized_canvas = canvas.resize((new_width, new_height))
        opaque_canvas = Image.new("RGBA", (new_width, new_height))
        opaque_canvas.paste((190, 220, 250), [0, 0, opaque_canvas.size[0], opaque_canvas.size[1]])
        opaque_canvas.paste(resized_canvas, (0, 0), mask=resized_canvas)
        canvas.save('faces/images/output/composite_{}_{}x{}.png'.format(group, grid_width, grid_height))
        opaque_canvas.save('faces/images/output/composite_{}_{}x{}-large.png'.format(group, grid_width, grid_height))

    @classmethod
    def allBodies(cls, group, genders=['m', 'f']):
        lip_colours = [(240, 50, 20),
                        (250, 30, 200)]
        hair_colours = [(0, 0, 0),
                        (120, 60, 0),
                        (200, 50, 0),
                        (220, 200, 0)]
        eye_colours = [(100, 50, 0),
                       (0, 100, 240),
                       (0, 180, 70)]
        glasses_colours = [(0, 0, 0),
                           (200, 0, 0),
                           (0, 0, 220)]
        result = cls(genders)
        result.layers.append(layer.Layer(group, 'head', genders))
        result.layers.append(colourlayer.ColourLayer(group, 'eye', colours=eye_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'mouth', genders, colours=lip_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'beard', genders, colours=hair_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'hair', genders, colours=hair_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'glasses', genders, colours=glasses_colours))

        result.all_dna = result.getAllDna()

        # Now lose the dna with different coloured facial hair to hair
        new_dna = list()
        for gender in genders:
            for dna in result.all_dna[gender]:
                c = dna.split('-')
                if '.' not in c[4] or c[4].split('.')[1] == c[5].split('.')[1]:
                    new_dna.append(dna)
            result.all_dna[gender] = new_dna

        return result

    @classmethod
    def allHouses(cls, group='house32', genders=['']):
        flower_colours = [(240, 50, 20),
                          (230, 30, 200),
                          (230, 210, 30)]
        wall_colours = [(160, 160, 160),
                        (140, 100, 70),
                        (180, 120, 80),
                        (220, 200, 50)]
        roof_colours = [(140, 70, 40),
                       (200, 40, 20),
                       (50, 40, 30)]
        window_colours = [(0, 0, 0),
                           (250, 250, 250),
                           (240, 210, 50)]
        door_colours = [(120, 60, 20),
                        (100, 80, 40)]
        result = cls(genders)
        result.layers.append(colourlayer.ColourLayer(group, 'wall', colours=wall_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'roof', colours=roof_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'door', colours=door_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'window', colours=window_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'roofdeco', colours=window_colours))
        result.layers.append(colourlayer.ColourLayer(group, 'deco', colours=flower_colours))

        result.all_dna = result.getAllDna()

        # Now lose the dna with different coloured facial hair to hair
        # new_dna = list()
        # for dna in result.all_dna['m']:
        #     c = dna.split('-')
        #     if '.' not in c[4] or c[4].split('.')[1] == c[5].split('.')[1]:
        #         new_dna.append(dna)
        # result.all_dna['m'] = new_dna

        return result

    @classmethod
    def fillHouseGrid(cls, group='house32', grid_width=5, grid_height=5, horizontal_spacing=40, vertical_spacing=40):
        #male_faces = Face.allFaces(group, 'm')
        #female_faces = Face.allFaces(group, 'f')
        #faces = male_faces + female_faces
        faces = cls.allHouses(group)
        for gender in ['']:
            print('{} {} faces.'.format(len(faces.all_dna[gender]), gender))

        all_dna = faces.all_dna['']
        random.shuffle(all_dna)
        # selected = dict()
        # for dna in all_dna:
        #     c = dna.split('-')
        #     if (c[6][1] == '1' or random.randint(0, 6) == 0) and (
        #         c[1][1] != '3' or c[5][3] not in ['2', '3']):
        #         key = '-'.join([c[1], c[2][1], c[3], c[4][:2], c[5], c[6][:2]])
        #         selected[key] = dna
        # select_dna = list(selected.values())
        # print('{} selected.'.format(len(selected)))
        # print(select_dna)

        select_dna = all_dna
        width, height = horizontal_spacing * grid_width, vertical_spacing * grid_height
        canvas = Image.new("RGBA", (width, height))
        for i in range(grid_width):
            for j in range(grid_height):
                # face = Face.randomFace('16')
                face_index = j * grid_width + i
                if face_index < len(select_dna):
                    #face = cls(group, faces[face_index])
                    faces.draw(canvas, select_dna[face_index], ((i * horizontal_spacing) + 4, (j * vertical_spacing) + 4))
        new_width, new_height = width * 2, height * 2
        resized_canvas = canvas.resize((new_width, new_height))
        opaque_canvas = Image.new("RGBA", (new_width, new_height))
        opaque_canvas.paste((190, 220, 250), [0, 0, opaque_canvas.size[0], opaque_canvas.size[1]])
        opaque_canvas.paste(resized_canvas, (0, 0), mask=resized_canvas)
        print(glob.glob('*'))
        canvas.save('faces/images/output/composite_{}_{}x{}.png'.format(group, grid_width, grid_height))
        opaque_canvas.save('faces/images/output/composite_{}_{}x{}-large.png'.format(group, grid_width, grid_height))
