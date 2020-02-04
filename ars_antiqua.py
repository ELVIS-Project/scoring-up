# Ars Antiqua is characterized by the following:
# 1. Absence of 'minims'
# 2. Absence of 'prolatio'
# 3. The 'breve' can't be identified as 'perfect' or 'imperfect'.
#    It is just considered to be equal to 3 minor semibreves, or a pair of minor-major semibreves,
#    or it is equal to 2 equal-duration semibreves.
# 4. The fact that the 'breve' can't be catalogued as 'perfect' or 'imperfect', implies that the 'semibreve' can't be 'altered.
#    It just can be 'major' or 'minor'.
# 5. There are no 'maximas' just 'duplex longas'
# 6. There is no dot of augmentation (this was introduced in the Ars nova). 
# Therefore, thre is no issue regarding the distiction between dot's functionality (division vs. augmentation).
# In other words, in Ars antiqua, all dots are dots of division.
# 7. All breves are proper (?) They cannot be altered (?)
from pymei import *
from fractions import *

# Functions about preceeding and suceeding elements
def get_peer_index(target_element):
    peers = target_element.getPeers()
    i = 0
    for element in peers:
        if element == target_element:
            index = i
            break
        i += 1
    return [index, peers]

def get_next_element(target_element):
    [index, peers] = get_peer_index(target_element)
    try:
        next_element = peers[index + 1]
    except:
        next_element = None
    return next_element

def get_preceding_element(target_element):
    [index, peers] = get_peer_index(target_element)
    try:
        preceding_element = peers[index - 1]
    except:
        preceding_element = None
    return preceding_element

def get_preceding_noterest(target_element):
    preceeding_element = get_preceding_element(target_element)
    while preceeding_element.name != 'note' and preceeding_element.name != 'rest':
        preceeding_element = get_preceding_element(preceeding_element)
    return preceeding_element

# Functions related to the counting of minims in a sequence of notes
def counting_semibreves(sequence_of_notes, note_durs, undotted_note_gain):
    sb_counter = 0
    print ""
    for note in sequence_of_notes:
        dur = note.getAttribute('dur').value
        try:
            index = note_durs.index(dur)
        except:
            print("MISTAKE\nNote/Rest element not considered: " + str(note) + ", with a duration @dur = " + dur)
        gain = undotted_note_gain[index]
        if note.hasAttribute('num') and note.hasAttribute('numbase'):
            ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
            gain *= ratio
        else:
            pass
        sb_counter += gain
        print(dur + ", " + str(gain) + ", " + str(sb_counter))
    return sb_counter

def has_been_modified(note):
    return (note.hasAttribute('num') and note.hasAttribute('numbase'))

# Given the total amount of "breves" in-between the "longs", see if they can be arranged in groups of 3
# According to how many breves remain ungrouped (1, 2 or 0), modifiy the duration of the appropriate note of the sequence ('imperfection', 'alteration', no-modification)
def modification(counter, start_note, middle_notes, end_note, following_note, short_note, long_note):
    # 1 breve left out:
    if counter % 3 == 1:
        # Default Case
        if start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not has_been_modified(start_note):
            # Imperfection a.p.p.
            start_note.addAttribute('quality', 'i')
            start_note.addAttribute('num', '3')
            start_note.addAttribute('numbase', '2')
        # Exception Case
        elif end_note is not None and end_note.name == 'note' and end_note.getAttribute('dur').value == long_note and not has_been_modified(end_note):
            # Imperfection a.p.a.
            end_note.addAttribute('quality', 'i')
            end_note.addAttribute('num', '3')
            end_note.addAttribute('numbase', '2')
            # Raise a warning when this imperfect note is followed by a perfect note (contradiction with the first rule)
            if following_note is not None and following_note.getAttribute('dur').value == long_note:
                print("WARNING 1! An imperfection a.p.a. is required, but this imperfect note is followed by a perfect note, this contradicts the fundamental rule: 'A note is perfect before another one of the same kind'.")
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
        # One of he possibilities when 2 breves are left out, is alteration
        # One must alter the last (uncolored) note from the middle_notes of the sequence
        # The last middle note is given by:
        last_middle_note = middle_notes[-1]
        # If this note is uncolored, it is a candidate for alteration (given that it is a note and not a rest and that it is a breve and not a smaller value)
        last_uncolored_note = last_middle_note
        # But if it is colored, we need to find the last "uncolored" note, as this is the one that would be altered
        while last_uncolored_note.hasAttribute('colored'):
            last_uncolored_note = get_preceding_noterest(last_uncolored_note)
        # 2 exact breves between the longs
        if counter == 2:
            # Default case
            if last_uncolored_note.name == 'note' and last_uncolored_note.getAttribute('dur').value == short_note and not has_been_modified(last_uncolored_note):
                # Alteration
                last_uncolored_note.addAttribute('quality', 'a')
                last_uncolored_note.addAttribute('num', '1')
                last_uncolored_note.addAttribute('numbase', '2')
            # Exception Case
            elif (start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not has_been_modified(start_note)) and (end_note is not None and end_note.name == 'note' and end_note.getAttribute('dur').value == long_note and not has_been_modified(end_note)):
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
                    print("WARNING 2! An imperfection a.p.a. is required, but this imperfect note is followed by a perfect note, this contradicts the fundamental rule: 'A note is perfect before another one of the same kind'.")
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
            print(last_uncolored_note)
            # Default Case: Check the conditions to apply the 'default interpretation', which implies imperfection a.p.a.
            if (start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not has_been_modified(start_note)) and (end_note is not None and end_note.name == 'note' and end_note.getAttribute('dur').value == long_note and not has_been_modified(end_note)):
                # Check if imperfection a.p.a. enters or not in conflict with rule # 1.
                if following_note is not None and following_note.getAttribute('dur').value == long_note:
                    # If it does, imperfection a.p.a. is discarded, except if the "alterantive interpretation" (the 'Exception Case') is also forbidden
                    # Exception Case
                    if last_uncolored_note.name == 'note' and last_uncolored_note.getAttribute('dur').value == short_note and not has_been_modified(last_uncolored_note):
                        # Alteration
                        last_uncolored_note.addAttribute('quality', 'a')
                        last_uncolored_note.addAttribute('num', '1')
                        last_uncolored_note.addAttribute('numbase', '2')
                    # Default + Warning Case
                    else:
                        # If the "alternative interpretation" is forbidden, and imperfection imp. a.p.a. was discarded just because it entered in conflict with rule # 1
                        # (this is, impapa_against_rule1 flag is True), then we force imperfection a.p.a. as it is the only viable option. But we also raise a 'warning'
                        # Imperfection a.p.p. 
                        start_note.addAttribute('quality', 'i')
                        start_note.addAttribute('num', '3')
                        start_note.addAttribute('numbase', '2')
                        # Imperfection a.p.a.
                        end_note.addAttribute('quality', 'i')
                        end_note.addAttribute('num', '3')
                        end_note.addAttribute('numbase', '2')
                        # Raise a warning when this imperfect note is followed by a perfect note (contradiction with the first rule)
                        print("WARNING 3n + 2! An imperfection a.p.a. is required, but this imperfect note is followed by a perfect note, this contradicts the fundamental rule: 'A note is perfect before another one of the same kind'.")
                        print("The imperfected note is " + str(end_note) + " and is followed by the perfect note " + str(following_note))
                        print("")
                # If it does not enter in conflict, we go with the "Default interpretation" of the notes
                # Default Case
                else:
                    # Imperfection a.p.p. 
                    start_note.addAttribute('quality', 'i')
                    start_note.addAttribute('num', '3')
                    start_note.addAttribute('numbase', '2')
                    # Imperfection a.p.a.
                    end_note.addAttribute('quality', 'i')
                    end_note.addAttribute('num', '3')
                    end_note.addAttribute('numbase', '2')
            # Exception Case
            elif last_uncolored_note.name == 'note' and last_uncolored_note.getAttribute('dur').value == short_note and not has_been_modified(last_uncolored_note):
                # Alteration
                last_uncolored_note.addAttribute('quality', 'a')
                last_uncolored_note.addAttribute('num', '1')
                last_uncolored_note.addAttribute('numbase', '2')
            # Mistake Case
            else:
                print("MISTAKE 3n + 2 - Imperfections a.p.p. and a.p.a. are impossible - Alteration is also impossible")
                print(start_note)
                print(end_note)
                print("")
    
    # 0 breves left out:
    else:
        if counter <= 3:
            pass
        else:
            # One of the possibilities when 6,9,12,etc. breves are left out, involves alteration
            # One must alter the last (uncolored) note from the middle_notes of the sequence
            # The last middle note is given by:
            last_middle_note = middle_notes[-1]
            # If this note is uncolored, it is a candidate for alteration (given that it is a note and not a rest and that it is a breve and not a smaller value)
            last_uncolored_note = last_middle_note
            # But if it is colored, we need to find the last "uncolored" note, as this is the one that would be altered
            while last_uncolored_note.hasAttribute('colored'):
                last_uncolored_note = get_preceding_noterest(last_uncolored_note)
            # Default Case:
            if (start_note is not None and start_note.name == 'note' and start_note.getAttribute('dur').value == long_note and not has_been_modified(start_note)) and (last_uncolored_note.name == 'note' and last_uncolored_note.getAttribute('dur').value == short_note and not has_been_modified(last_uncolored_note)):
                # Imperfection a.p.p.
                start_note.addAttribute('quality', 'i')
                start_note.addAttribute('num', '3')
                start_note.addAttribute('numbase', '2')
                # Alteration
                last_uncolored_note.addAttribute('quality', 'a')
                last_uncolored_note.addAttribute('num', '1')
                last_uncolored_note.addAttribute('numbase', '2')
            # Exception Case:
            else:
                # Start note remains perfect
                pass

def modification_semibreve_level(start_note, middle_notes, end_note, following_note):
    # If there are 3 semibreves:
    counter = len(middle_notes)
    if counter == 3:
        # All of them are minor (1/3 of breve)
        for note in middle_notes:
            note.addAttribute('dur.quality', 'minor')
    # If there are 2 semibreves:
    elif counter == 2:
        note1 = middle_notes[0]
        note2 = middle_notes[1]
        # If the first note has a downward stem, we have a major-minor pair of semibreves
        if note1.hasAttribute('stem.dir') and note1.getAttribute('stem.dir').value == 'down':
            note1.addAttribute('dur.quality', 'major')
            note1.addAttribute('num', '1')
            note1.addAttribute('numbase', '2')
            note2.addAttribute('dur.quality', 'minor')
        # On the other hand, if there is no additional markings, we have a minor-major pair of semibreves (default case) 
        else:
            note1.addAttribute('dur.quality', 'minor')
            note2.addAttribute('dur.quality', 'major')
            note2.addAttribute('num', '1')
            note2.addAttribute('numbase', '2')
    # For more than three semibreves:
    elif counter > 3:
        for note in middle_notes:
            note.addAttribute('num', str(counter))
            note.addAttribute('numbase', '3')

def breves_between_longas(start_note, middle_notes, end_note, following_note, tempus, note_durs, undotted_note_gain):
    # Total of breves in the middle_notes        
    # 1. Pre-processing: Filtering. Remove the 'dot' elements from the middle_notes list 
    #(so that this list only contains notes and rests that lie between the longs)
    sequence_of_middle_notes = []
    for element in middle_notes:
        if element.name != 'dot':
            sequence_of_middle_notes.append(element)
    # 2. Use the counter of semibreves to determine the total of breves in the middle_notes
    sb_counter = counting_semibreves(sequence_of_middle_notes, note_durs, undotted_note_gain)
    count_B = sb_counter / tempus
    
    modification(count_B, start_note, middle_notes, end_note, following_note, 'brevis', 'longa')

# Main function
def lining_up(quasiscore_mensural_doc):
    # For each voice (staff element) in the "score"
    staves = quasiscore_mensural_doc.getElementsByName('staff')
    stavesDef = quasiscore_mensural_doc.getElementsByName('staffDef')
    for i in range(0, len(stavesDef)):
        print("Voice # " + str(i+1) + " results:\n")
        staffDef = stavesDef[i]
        staff = staves[i]

        # Getting the mensuration information of the voice (prolatio is irrelevant in Ars antiqua)
        tempus = int(staffDef.getAttribute('tempus').value)
        modusminor = int(staffDef.getAttribute('modusminor').value)
        modusmaior = int(staffDef.getAttribute('modusmaior').value)

        # Individual note values and gains, according to the mensuration
        note_durs = ['semibrevis', 'brevis', 'longa', 'maxima']
        undotted_note_gain = [1, tempus, modusminor * tempus, modusmaior * modusminor * tempus]

        # Getting all the notes, rests, and dots of one voice into a python list, in order.
        # This allows to retrieve the index, which is not possible with MEI lists.
        voice_content = staff.getChildrenByName('layer')[0].getChildren()
        voice_noterest_dots_content = []
        for element in voice_content:
            name = element.name
            if name == 'note' or name == 'rest' or name == 'dot':
                voice_noterest_dots_content.append(element)
            else:
                #print(name)
                #print(element)
                #print ""
                pass
        #print(voice_noterest_dots_content)

        # Find indices for starting and ending points of each sequence of notes to be analyzed.
        # Each of the following is a list of indices of notes greater or equal than: a Semibreve, a Breve, a Long and a Maxima, respectively.
        list_of_indices_geq_B_and_dots = []
        list_of_indices_geq_L = []
        # Get the indices
        for noterest in voice_noterest_dots_content:
            if noterest.name == 'dot' or noterest.getAttribute('dur').value == 'brevis':
                list_of_indices_geq_B_and_dots.append(voice_noterest_dots_content.index(noterest))
            elif noterest.getAttribute('dur').value == 'longa':
                list_of_indices_geq_B_and_dots.append(voice_noterest_dots_content.index(noterest))
                list_of_indices_geq_L.append(voice_noterest_dots_content.index(noterest))

        # Semibreves in between breves (or higher note values)
        if tempus == 3:
            #print("\nBREVE GEQ")
            #print(list_of_indices_geq_B_and_dots)
            #print ""

            if 0 not in list_of_indices_geq_B_and_dots and list_of_indices_geq_B_and_dots != []:
                start_note = None
                f = list_of_indices_geq_B_and_dots[0]
                end_note = voice_noterest_dots_content[f]
                try:
                    following_note = voice_noterest_dots_content[f+1]
                except:
                    following_note = None
                middle_notes = voice_noterest_dots_content[0:f]
                #print(start_note)
                #print(middle_notes)
                #print(end_note)
                modification_semibreve_level(start_note, middle_notes, end_note, following_note)

            for i in range(0, len(list_of_indices_geq_B_and_dots)-1):
                # Define the sequence of notes
                o = list_of_indices_geq_B_and_dots[i]
                start_note = voice_noterest_dots_content[o]
                f = list_of_indices_geq_B_and_dots[i+1]
                end_note = voice_noterest_dots_content[f]
                try:
                    following_note = voice_noterest_dots_content[f+1]
                except:
                    following_note = None
                middle_notes = voice_noterest_dots_content[o+1:f]
                # print(start_note)
                # print(middle_notes)
                # print(end_note)
                modification_semibreve_level(start_note, middle_notes, end_note, following_note)

        # tempus = 2
        else:
            pass

        # Breves in between longas (or higher note values)
        if modusminor == 3:
            #print("\nLONGA GEQ")
            #print(list_of_indices_geq_L)
            #print ""

            if 0 not in list_of_indices_geq_L and list_of_indices_geq_L != []:
                start_note = None
                f = list_of_indices_geq_L[0]
                end_note = voice_noterest_dots_content[f]
                try:
                    following_note = voice_noterest_dots_content[f+1]
                except:
                    following_note = None
                middle_notes = voice_noterest_dots_content[0:f]
                #print(start_note)
                #print(middle_notes)
                #print(end_note)
                breves_between_longas(start_note, middle_notes, end_note, following_note, tempus, note_durs, undotted_note_gain)

            for i in range(0, len(list_of_indices_geq_L)-1):
                # Define the sequence of notes
                o = list_of_indices_geq_L[i]
                start_note = voice_noterest_dots_content[o]
                f = list_of_indices_geq_L[i+1]
                end_note = voice_noterest_dots_content[f]
                try:
                    following_note = voice_noterest_dots_content[f+1]
                except:
                    following_note = None
                middle_notes = voice_noterest_dots_content[o+1:f]
                #print(start_note)
                #print(middle_notes)
                #print(end_note)
                breves_between_longas(start_note, middle_notes, end_note, following_note, tempus, note_durs, undotted_note_gain)

        # modusminor = 2
        else:
            pass

    return quasiscore_mensural_doc

# Comparison function
def comparison(out_doc, gt_doc):

    gt_staves = gt_doc.getElementsByName('staff')
    accuracy_list = []
    for gt_staff in gt_staves:
        diff = 0
        
        voice_number = gt_staff.getAttribute('n').value
        gt_layer = gt_staff.getChildrenByName('layer')[0]
        # Getting all the notes and rests for each voice in the ground truth mensural-mei document
        gt_notes = gt_layer.getChildrenByName('note')
        gt_notes.extend(gt_layer.getChildrenByName('rest'))

        # Compare the duration of the notes (and rests) in the ground truth and in the output of the Apel script.
        # The duration is given by the three attributes: @dur, @num, and @numbase.
        for gt_note in gt_notes:
            # Gettting the notes from the output of the Apel script that correspond (i.e., share the same @xml:id) to each note in the ground truth
            out_note = out_doc.getElementById(gt_note.id)

            # Getting the @dur, @num, and @numbase attributes for all the ground truth notes (and rests)
            gtval_dur = gt_note.getAttribute('dur').value
            try:
                gtval_num = gt_note.getAttribute('num').value
            except:
                gtval_num = 1
            try:
                gtval_numbase = gt_note.getAttribute('numbase').value
            except:
                gtval_numbase = 1

            # Getting the @dur, @num, and @numbase attributes for all the notes (and rests) in the output file from the Apel script
            outval_dur = out_note.getAttribute('dur').value
            try:
                outval_num = out_note.getAttribute('num').value
            except:
                outval_num = 1
            try:
                outval_numbase = out_note.getAttribute('numbase').value
            except:
                outval_numbase = 1

            # Determine if both notes (ground truth's and Apel's) share the same value (same figure and quality)
            if (gtval_dur == outval_dur) and (gtval_num == outval_num) and (gtval_numbase == outval_numbase):
                pass
            else:
                print("NOT EQUAL: the " + gt_note.name.upper() + " " + gt_note.id + " in voice " + voice_number)
                print("In GROUND TRUTH: " + gtval_dur.upper() + ", with " + str(Fraction(int(gtval_numbase), int(gtval_num))) + " x default value")
                print("In APEL  OUTPUT: " + outval_dur.upper() + ", with " + str(Fraction(int(outval_numbase), int(outval_num))) + " x default value")
                diff += 1
                if (gt_note.hasAttribute('colored')):
                    print("COLORED!\n")
                else:
                    print ""

        accuracy_ratio_per_voice = 1 - Fraction(diff,len(gt_notes))
        accuracy_list.append(accuracy_ratio_per_voice)

    return accuracy_list
