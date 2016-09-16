from pymei import *
from fractions import *

file = raw_input("Piece: ")
doc = documentFromFile(file).getMeiDocument()
# listNotesRests = doc.getElementsByName('note')
# listNotesRests.extend(doc.getElementsByName('rest'))
# for note_or_rest in listNotesRests:
#     note_or_rest.removeAttribute('num')
#     note_or_rest.removeAttribute('numbase')
#     note_or_rest.removeAttribute('quality')
# documentToFile(doc, "stg0" + file[:-4] + ".mei")

staff = doc.getElementsByName('staff')[0]
staffDef = doc.getElementsByName('staffDef')[0]
prolatio = int(staffDef.getAttribute('prolatio').value)
tempus = int(staffDef.getAttribute('tempus').value)
modusminor = int(staffDef.getAttribute('modusminor').value)
modusmaior = int(staffDef.getAttribute('modusmaior').value)


# Getting all the notes and rests of one voice into a python list, in order.
# This allows to retrieve the index, which is not possible with MEI lists.
voice_content = staff.getChildrenByName('layer')[0].getChildren()
voice_noterest_content = []
for element in voice_content:
    name = element.name
    if name == 'note' or name == 'rest':
        voice_noterest_content.append(element)
    else:
        print(name)
        print(element)
        print ""
print(voice_noterest_content)

# Find indices for starting and ending points of each sequence of notes to be analyzed.
# Each of the following is a list of indices of notes greater or equal than: a Semibreve, a Breve, a Long and a Maxima, respectively.
list_of_indices_geq_Sb = []
list_of_indices_geq_B = []
list_of_indices_geq_L = []
list_of_indices_geq_Max = []
# Get the indices
for noterest in voice_noterest_content:
    dur = noterest.getAttribute('dur').value
    if dur == 'semibrevis':
        list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
    elif dur == 'brevis':
        list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
        list_of_indices_geq_B.append(voice_noterest_content.index(noterest))
    elif dur == 'longa':
        list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
        list_of_indices_geq_B.append(voice_noterest_content.index(noterest))
        list_of_indices_geq_L.append(voice_noterest_content.index(noterest))
    elif dur == 'maxima':
        list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
        list_of_indices_geq_B.append(voice_noterest_content.index(noterest))
        list_of_indices_geq_L.append(voice_noterest_content.index(noterest))
        list_of_indices_geq_Max.append(voice_noterest_content.index(noterest))
    else:
        print("SHOULD BE A MINIM, IS IT?  It is " + dur)
        print(noterest)
        print ""
        pass

#########################################################################
# MISSING THE CASE WERE THERE IS A NOTE BEFORE THE FIRST ONE INDEXED    #
# Measure 3 - in Flos                                                   #
# Sb - B --> The first semibreve is part of the middle_notes            #
# and the starting_note doesn't exist (its index is out of range: '-1') #
# MISSING THE PRESENCE OF A DOT                                         #
# Measure 2 - in Flos                                                   #
#########################################################################

# Minims in between semibreves (or higher note values)
if prolatio == 3:
    for i in range(0, len(list_of_indices_geq_Sb)-1):
        # Define the sequence of notes
        o = list_of_indices_geq_Sb[i]
        f = list_of_indices_geq_Sb[i+1]
        start_note = voice_noterest_content[o]
        end_note = voice_noterest_content[f]
        middle_notes = voice_noterest_content[o+1:f]
        print(start_note)
        print(middle_notes)
        print(end_note)

        # Counting notes in between the extremes
        minim_counter = 0
        for note in middle_notes:
            dur = note.getAttribute('dur').value
            if dur == 'minima':
                gain = 1
            else:
                print("MISTAKE \nNote/Rest element not considered: " + str(note) + ", with a duration @dur = " + dur)
            minim_counter += gain

        # Given the total amount of minims in-between the "semibreves", see if they can be arranged in groups of 3
        # According to how many minims remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
        if minim_counter % 3 == 1:
            start_note.addAttribute('num', '3')
            start_note.addAttribute('numbase', '2')
            start_note.addAttribute('quality', 'i')
        elif minim_counter % 3 == 2:
            middle_notes[-1].addAttribute('num', '1')
            middle_notes[-1].addAttribute('numbase', '2')
            middle_notes[-1].addAttribute('quality', 'a')
        else:
            pass
# prolatio = 2
else:
    pass

# Semibreves in between breves (or higher note values)
if tempus == 3:
    for i in range(0, len(list_of_indices_geq_B)-1):
        # Define the sequence of notes
        o = list_of_indices_geq_B[i]
        f = list_of_indices_geq_B[i+1]
        start_note = voice_noterest_content[o]
        end_note = voice_noterest_content[f]
        middle_notes = voice_noterest_content[o+1:f]
        print(start_note)
        print(middle_notes)
        print(end_note)

        # Counting notes in between the extremes
        minim_counter = 0
        for note in middle_notes:
            dur = note.getAttribute('dur').value
            if dur == 'minima':
                gain = 1
                if note.hasAttribute('num') and note.hasAttribute('numbase'):
                    ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
                    gain *= ratio
                else:
                    pass
            elif dur == 'semibrevis':
                gain = prolatio
                if note.hasAttribute('num') and note.hasAttribute('numbase'):
                    ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
                    gain *= ratio
                else:
                    pass
            else:
                print("MISTAKE \nNote/Rest element not considered: " + str(note) + ", with a duration @dur = " + dur)
            minim_counter += gain

        count_Sb = minim_counter / prolatio
        if(minim_counter % prolatio == 0):
            print("GOOD")
        else:
            print("BAD! THE DIVISION IS NOT AN INTEGER NUMBER - not an integer number of Semibreves!")

        # Given the total amount of semibreves in-between the "breves", see if they can be arranged in groups of 3
        # According to how many semibreves remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
        if count_Sb % 3 == 1:
            start_note.addAttribute('num', '3')
            start_note.addAttribute('numbase', '2')
            start_note.addAttribute('quality', 'i')
        elif count_Sb % 3 == 2:
            middle_notes[-1].addAttribute('num', '1')
            middle_notes[-1].addAttribute('numbase', '2')
            middle_notes[-1].addAttribute('quality', 'a')
        else:
            pass
# tempus = 2
else:
    pass

# Breves in between longas (or higher note values)
if modusminor == 3:
    for i in range(0, len(list_of_indices_geq_L)-1):
        # Define the sequence of notes
        o = list_of_indices_geq_L[i]
        f = list_of_indices_geq_L[i+1]
        start_note = voice_noterest_content[o]
        end_note = voice_noterest_content[f]
        middle_notes = voice_noterest_content[o+1:f]
        print(start_note)
        print(middle_notes)
        print(end_note)

        # Counting notes in between the extremes
        minim_counter = 0
        for note in middle_notes:
            dur = note.getAttribute('dur').value
            if dur == 'minima':
                gain = 1
                if note.hasAttribute('num') and note.hasAttribute('numbase'):
                    ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
                    gain *= ratio
                else:
                    pass
            elif dur == 'semibrevis':
                gain = prolatio
                if note.hasAttribute('num') and note.hasAttribute('numbase'):
                    ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
                    gain *= ratio
                else:
                    pass
            elif dur == 'brevis':
                gain = tempus * prolatio
                if note.hasAttribute('num') and note.hasAttribute('numbase'):
                    ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
                    gain *= ratio
                else:
                    pass
            else:
                print("MISTAKE \nNote/Rest element not considered: " + str(note) + ", with a duration @dur = " + dur)
            minim_counter += gain

        count_L = minim_counter / (tempus * prolatio)
        if(minim_counter % (tempus * prolatio) == 0):
            print("GOOD")
        else:
            print("BAD! THE DIVISION IS NOT AN INTEGER NUMBER - not an integer number of Breves!")

        # Given the total amount of breves in-between the "longas", see if they can be arranged in groups of 3
        # According to how many breves remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
        if count_L % 3 == 1:
            start_note.addAttribute('num', '3')
            start_note.addAttribute('numbase', '2')
            start_note.addAttribute('quality', 'i')
        elif count_L % 3 == 2:
            middle_notes[-1].addAttribute('num', '1')
            middle_notes[-1].addAttribute('numbase', '2')
            middle_notes[-1].addAttribute('quality', 'a')
        else:
            pass
# modusminor = 2
else:
    pass

documentToFile(doc, "stage1" + file[:-4] + ".mei")