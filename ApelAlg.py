from pymei import *
from fractions import *

# Given the total amount of "breves" in-between the "longs", see if they can be arranged in groups of 3
# According to how many breves remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
def modification(counter, start_note, middle_notes, end_note, following_note, short_note, long_note):
    # 1 breve left out:
    if counter % 3 == 1:
        # Default Case
        if start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not start_note.hasAttribute('quality'):
            # Imperfection a.p.p.
            start_note.addAttribute('quality', 'i')
            start_note.addAttribute('num', '3')
            start_note.addAttribute('numbase', '2')
        # Exception Case
        elif end_note.name == 'note' and end_note.getAttribute('dur').value == long_note and not end_note.hasAttribute('quality'):
            # Imperfection a.p.a.
            end_note.addAttribute('quality', 'i')
            end_note.addAttribute('num', '3')
            end_note.addAttribute('numbase', '2')
            # Raise a warning when this imperfect note is followed by a perfect note (contradiction with the first rule)
            if following_note is not None and following_note.getAttribute('dur').value == long_note:
                print("WARNING! An imperfection a.p.a. is required, but this imperfect note is followed by a perfect note, this contradicts the fundamental rule: 'A note is perfect before another one of the same kind'.")
                print("The imperfected note is " + str(end_note) + " and is followed by the perfect note " + str(following_note))
                print("")
        # Mistake Case
        else:
            print("MISTAKE 1 - Impossible to do Imperfection a.p.p. and also Imperfection a.p.a.")
            print(start_note)
            print(end_note)
            print("")

    # 2 breves left out:
    elif counter % 3 == 2:
        before_last = middle_notes[-1]
        # 2 exact breves between the longs
        if counter == 2:
            # Default case
            if before_last.name == 'note' and before_last.getAttribute('dur').value == short_note and not before_last.hasAttribute('quality'):
                # Alteration
                before_last.addAttribute('quality', 'a')
                before_last.addAttribute('num', '1')
                before_last.addAttribute('numbase', '2')
            # Exception Case
            elif (start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not start_note.hasAttribute('quality')) and (end_note.name == 'note' and end_note.getAttribute('dur').value == long_note and not end_note.hasAttribute('quality')):
                # Imperfection a.p.p. 
                start_note.addAttribute('quality', 'i')
                start_note.addAttribute('num', '3')
                start_note.addAttribute('numbase', '2')
                # Imperfection a.p.a.
                end_note.addAttribute('quality', 'i')
                end_note.addAttribute('num', '3')
                end_note.addAttribute('numbase', '2')
                # Raise a warning when this imperfect note is followed by a perfect note (contradiction with the first rule)
                if following_note is not None and following_note.getAttribute('dur').value == long_note:
                    print("WARNING! An imperfection a.p.a. is required, but this imperfect note is followed by a perfect note, this contradicts the fundamental rule: 'A note is perfect before another one of the same kind'.")
                    print("The imperfected note is " + str(end_note) + " and is followed by the perfect note " + str(following_note))
                    print("")
            # Mistake Case
            else:
                print("MISTAKE 2 - Alteration is impossible - Imperfections a.p.p. and a.p.a. are also impossible")
                print(start_note)
                print(end_note)
                print("")
        # 5, 8, 11, 14, 17, 20, ... breves between the longs
        else:
            # Default case
            if (start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not start_note.hasAttribute('quality')) and (end_note.name == 'note' and end_note.getAttribute('dur').value == long_note and not end_note.hasAttribute('quality')):
                # Imperfection a.p.p. 
                start_note.addAttribute('quality', 'i')
                start_note.addAttribute('num', '3')
                start_note.addAttribute('numbase', '2')
                # Imperfection a.p.a.
                end_note.addAttribute('quality', 'i')
                end_note.addAttribute('num', '3')
                end_note.addAttribute('numbase', '2')
                # Raise a warning when this imperfect note is followed by a perfect note (contradiction with the first rule)
                if following_note is not None and following_note.getAttribute('dur').value == long_note:
                    print("WARNING! An imperfection a.p.a. is required, but this imperfect note is followed by a perfect note, this contradicts the fundamental rule: 'A note is perfect before another one of the same kind'.")
                    print("The imperfected note is " + str(end_note) + " and is followed by the perfect note " + str(following_note))
                    print("")
            # Exception Case
            elif before_last.name == 'note' and before_last.getAttribute('dur').value == short_note and not before_last.hasAttribute('quality'):
                # Alteration
                before_last.addAttribute('quality', 'a')
                before_last.addAttribute('num', '1')
                before_last.addAttribute('numbase', '2')
            # Mistake Case
            else:
                print("MISTAKE 2 - Imperfections a.p.p. and a.p.a. are impossible - Alteration is also impossible")
                print(start_note)
                print(end_note)
                print("")
    
    # 0 breves left out:
    else:
        pass

def minims_between_semibreves(start_note, middle_notes, end_note, following_note):
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
    modification(minim_counter, start_note, middle_notes, end_note, following_note, 'minima', 'semibrevis')

def sb_between_breves(start_note, middle_notes, end_note, following_note):
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
        #print("GOOD")
        pass
    else:
        print("BAD! THE DIVISION IS NOT AN INTEGER NUMBER - not an integer number of Semibreves!")

    # Given the total amount of semibreves in-between the "breves", see if they can be arranged in groups of 3
    # According to how many semibreves remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
    modification(count_Sb, start_note, middle_notes, end_note, following_note, 'semibrevis', 'brevis')

def breves_between_longas(start_note, middle_notes, end_note, following_note):
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

    count_B = minim_counter / (tempus * prolatio)
    if(minim_counter % (tempus * prolatio) == 0):
        #print("GOOD")
        pass
    else:
        print("BAD! THE DIVISION IS NOT AN INTEGER NUMBER - not an integer number of Breves!")

    # Given the total amount of breves in-between the "longas", see if they can be arranged in groups of 3
    # According to how many breves remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
    modification(count_B, start_note, middle_notes, end_note, following_note, 'brevis', 'longa')

# Remove the @quality, @num and @numbase attributes
file = raw_input("Piece: ")
doc = documentFromFile(file).getMeiDocument()
listNotesRests = doc.getElementsByName('note')
listNotesRests.extend(doc.getElementsByName('rest'))
for note_or_rest in listNotesRests:
    note_or_rest.removeAttribute('num')
    note_or_rest.removeAttribute('numbase')
    note_or_rest.removeAttribute('quality')
documentToFile(doc, file[:-4] + "_stg0.mei")

# For each voice (staff element) in the "score"
staves = doc.getElementsByName('staff')
stavesDef = doc.getElementsByName('staffDef')
for i in range(0, len(stavesDef)):
    staffDef = stavesDef[i]
    staff = staves[i]

    # Getting the mensuration information of the voice
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
            #print(name)
            #print(element)
            #print ""
            pass
    #print(voice_noterest_content)

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
            #print("SHOULD BE A MINIM, IS IT?  It is " + dur)
            #print(noterest)
            #print ""
            pass

    #########################################################################
    # MISSING THE PRESENCE OF A DOT                                         #
    # Measure 2 - in Flos                                                   #
    #########################################################################

    # Minims in between semibreves (or higher note values)
    if prolatio == 3:
        print("\nSEMIBREVE GEQ")
        #print(list_of_indices_geq_Sb)
        #print ""

        if 0 not in list_of_indices_geq_Sb and list_of_indices_geq_Sb != []:
            start_note = None
            f = list_of_indices_geq_Sb[0]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[0:f]
            #print(start_note)
            #print(middle_notes)
            #print(end_note)
            minims_between_semibreves(start_note, middle_notes, end_note, following_note)

        for i in range(0, len(list_of_indices_geq_Sb)-1):
            # Define the sequence of notes
            o = list_of_indices_geq_Sb[i]
            start_note = voice_noterest_content[o]
            f = list_of_indices_geq_Sb[i+1]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[o+1:f]
            #print(start_note)
            #print(middle_notes)
            #print(end_note)
            minims_between_semibreves(start_note, middle_notes, end_note, following_note)
    
    # prolatio = 2
    else:
        pass

    # Semibreves in between breves (or higher note values)
    if tempus == 3:
        print("\nBREVE GEQ")
        #print(list_of_indices_geq_B)
        #print ""

        if 0 not in list_of_indices_geq_B and list_of_indices_geq_B != []:
            start_note = None
            f = list_of_indices_geq_B[0]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[0:f]
            #print(start_note)
            #print(middle_notes)
            #print(end_note)
            sb_between_breves(start_note, middle_notes, end_note, following_note)

        for i in range(0, len(list_of_indices_geq_B)-1):
            # Define the sequence of notes
            o = list_of_indices_geq_B[i]
            start_note = voice_noterest_content[o]
            f = list_of_indices_geq_B[i+1]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[o+1:f]
            #print(start_note)
            #print(middle_notes)
            #print(end_note)
            sb_between_breves(start_note, middle_notes, end_note, following_note)

    # tempus = 2
    else:
        pass

    # Breves in between longas (or higher note values)
    if modusminor == 3:
        print("\nLONGA GEQ")
        #print(list_of_indices_geq_L)
        #print ""

        if 0 not in list_of_indices_geq_L and list_of_indices_geq_L != []:
            start_note = None
            f = list_of_indices_geq_L[0]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[0:f]
            #print(start_note)
            #print(middle_notes)
            #print(end_note)
            breves_between_longas(start_note, middle_notes, end_note, following_note)

        for i in range(0, len(list_of_indices_geq_L)-1):
            # Define the sequence of notes
            o = list_of_indices_geq_L[i]
            start_note = voice_noterest_content[o]
            f = list_of_indices_geq_L[i+1]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[o+1:f]
            #print(start_note)
            #print(middle_notes)
            #print(end_note)
            breves_between_longas(start_note, middle_notes, end_note, following_note)

    # modusminor = 2
    else:
        pass

    documentToFile(doc, file[:-4] + "_STG3.mei")