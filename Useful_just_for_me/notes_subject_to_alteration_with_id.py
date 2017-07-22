from pymei import *
from fractions import *
from os import listdir


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

# Functions related to dots
def followed_by_dot(target_element):
    next_element = get_next_element(target_element)
    if next_element is not None and next_element.name == 'dot':
        return True
    else:
        return False


# Functions related to the counting of minims in a sequence of notes
def counting_minims_in_an_undotted_sequence(sequence_of_notes, note_durs, undotted_note_gain):
    minim_counter = 0
    
    # All notes except the last one (of the middle notes)
    for note in sequence_of_notes[:-1]:
        dur = note.getAttribute('dur').value
        index = note_durs.index(dur)
        gain = undotted_note_gain[index]
        if note.hasAttribute('num') and note.hasAttribute('numbase'):
            ratio = Fraction(int(note.getAttribute('numbase').value), int(note.getAttribute('num').value))
            gain *= ratio
        else:
            pass
        minim_counter += gain

    # Last note (of the middle notes), we do not use the @num and @numbase
    # Because this note may be altered, 
    # and we want the exact value of notes between boundaries
    # without changes (the middle notes can't be changed, except for the last one).
    try:
        note = sequence_of_notes[-1]
    except:
        return minim_counter
    dur = note.getAttribute('dur').value
    index = note_durs.index(dur)
    gain = undotted_note_gain[index]
    minim_counter += gain

    return minim_counter

## MISSING:
### n % 3 == 0 and not 0
### also need to check (besides the last note being able to be altered)
### that imperfection app cannot be done:
### by checking if the start note is either a rest, or has a quality encoded (@num & @numbase, or @quality)

def minims_between_semibreves(start_note, middle_notes, end_note, note_durs, undotted_note_gain):
    # Let us figure out if there is an alteration candidate in this sequence:
    alteration_candidate = False
    alteration_candidate_id = None

    # Total of minims in the middle_notes
    minim_counter = counting_minims_in_an_undotted_sequence(middle_notes, note_durs, undotted_note_gain)
    # Lets see if the number of notes in between boundaries would allow for alteration
    if (minim_counter % 3 == 2) or (minim_counter % 3 == 0 and minim_counter != 0):
        # Now see if the LAST UNCOLORED NOTE note can be altered
        # This is, let us check if it is a "minima"
 
        # The last middle note is given by:
        last_middle_note = middle_notes[-1]
        # If this note is uncolored, it is a candidate for alteration
        last_uncolored_note = last_middle_note
        # But if it is colored, we need to find the last "uncolored" note, as this is the one that would be altered
        while last_uncolored_note.hasAttribute('colored'):
            last_uncolored_note = get_preceding_noterest(last_uncolored_note)

        # If it is a note and it is a minima: it is candidate to alteration
        if last_uncolored_note.getAttribute('dur').value == "minima" and last_uncolored_note.name == "note":
            alteration_candidate = True
            alteration_candidate_id = last_uncolored_note.id

    # #debug:
    # print ""

    # try:
    #     start_dur = start_note.getAttribute('dur').value
    # except:
    #     start_dur = None
    
    # print str(start_note) + " " + str(start_dur)

    # print alteration_candidate
    
    # try:
    #     end_dur = end_note.getAttribute('dur').value
    # except:
    #     end_dur = None
    
    # print str(end_note) + " " + str(end_dur)

    # Flag for alteration candidate is returned
    return [alteration_candidate, alteration_candidate_id]       

def sb_between_breves(start_note, middle_notes, end_note, prolatio, note_durs, undotted_note_gain):
    # Let us figure out if there is an alteration candidate in this sequence:
    alteration_candidate = False
    alteration_candidate_id = None

    # Total of semibreves in the middle_notes
    minim_counter = counting_minims_in_an_undotted_sequence(middle_notes, note_durs, undotted_note_gain)
    count_Sb = minim_counter / (prolatio)
    # Lets see if the number of notes in between boundaries would allow for alteration
    if (count_Sb % 3 == 2) or (count_Sb % 3 == 0 and count_Sb != 0):
        # Now see if the LAST UNCOLORED NOTE note can be altered
        # This is, let us check if it is a "semibrevis"

        # The last middle note is given by:
        last_middle_note = middle_notes[-1]
        # If this note is uncolored, it is a candidate for alteration
        last_uncolored_note = last_middle_note
        # But if it is colored, we need to find the last "uncolored" note, as this is the one that would be altered
        while last_uncolored_note.hasAttribute('colored'):
            last_uncolored_note = get_preceding_noterest(last_uncolored_note)

        # If it is a note and it is a semibrevis: it is candidate to alteration
        if last_uncolored_note.getAttribute('dur').value == "semibrevis" and last_uncolored_note.name == "note":
            alteration_candidate = True
            alteration_candidate_id = last_uncolored_note.id

    # #debug:
    # print ""

    # try:
    #     start_dur = start_note.getAttribute('dur').value
    # except:
    #     start_dur = None
    
    # print str(start_note) + " " + str(start_dur)

    # print alteration_candidate
    
    # try:
    #     end_dur = end_note.getAttribute('dur').value
    # except:
    #     end_dur = None
    
    # print str(end_note) + " " + str(end_dur)

    # Flag for alteration candidate is returned
    return [alteration_candidate, alteration_candidate_id]  

def breves_between_longas(start_note, middle_notes, end_note, prolatio, tempus, note_durs, undotted_note_gain):
    # Let us figure out if there is an alteration candidate in this sequence:
    alteration_candidate = False
    alteration_candidate_id = None

    # Total of breves in the middle_notes
    minim_counter = counting_minims_in_an_undotted_sequence(middle_notes, note_durs, undotted_note_gain)
    count_B = minim_counter / (tempus * prolatio)
    # Lets see if the number of notes in between boundaries would allow for alteration
    if (count_B % 3 == 2) or (count_B % 3 == 0 and count_B != 0):
        # Now see if the LAST UNCOLORED NOTE note can be altered
        # This is, let us check if it is a "brevis"

        # The last middle note is given by:
        last_middle_note = middle_notes[-1]
        # If this note is uncolored, it is a candidate for alteration (given that it is a note and not a rest and that it is a breve and not a smaller value)
        last_uncolored_note = last_middle_note
        # But if it is colored, we need to find the last "uncolored" note, as this is the one that would be altered
        while last_uncolored_note.hasAttribute('colored'):
            last_uncolored_note = get_preceding_noterest(last_uncolored_note)

        # If it is a note and it is a breve: it is candidate to alteration
        if last_uncolored_note.getAttribute('dur').value == "brevis" and last_uncolored_note.name == "note":
            alteration_candidate = True
            alteration_candidate_id = last_uncolored_note.id

    # #debug:
    # print ""

    # try:
    #     start_dur = start_note.getAttribute('dur').value
    # except:
    #     start_dur = None
    
    # print str(start_note) + " " + str(start_dur)

    # print alteration_candidate
    
    # try:
    #     end_dur = end_note.getAttribute('dur').value
    # except:
    #     end_dur = None
    
    # print str(end_note) + " " + str(end_dur)

    # Flag for alteration candidate is returned
    return [alteration_candidate, alteration_candidate_id]



def perfect_notes(modusmaior, modusminor, tempus, prolatio, layer):
    # You are in a voice --> <staffDef>, <staff>
    # Need the mensuration to determine which notes are perfect by default, 
    # because they are mutable (they can be kept perfect or they can be imperfected)
    # [If your implementation is correct: Only 'Notes', 
    #  and not 'Rests', are suppposed to be mutable]
    # Note: Do NOT consider COLORED NOTES, they are already included in their own function
    [count_maximas, count_longas, count_brevis, count_sb] = [0, 0, 0, 0]
    for note in layer.getChildrenByName('note'):
        dur = note.getAttribute('dur').value
        if modusmaior == 3 and dur == 'maxima' and not note.getAttribute('colored'):
            count_maximas += 1
        if modusminor == 3 and dur == 'longa' and not note.getAttribute('colored'):
            count_longas += 1
        if tempus == 3 and dur == 'brevis' and not note.getAttribute('colored'):
            count_brevis += 1
        if prolatio == 3 and dur == 'semibrevis' and not note.getAttribute('colored'):
            count_sb += 1

        if prolatio == 2:
            count_sb = None
        if tempus == 2:
            count_brevis = None
        if modusminor == 2:
            count_longas = None

    perfect_notes = [count_longas, count_brevis, count_sb]
    #count_perfnotes = sum(perfect_notes)
    #print str(perfect_notes) + " = " + str(count_perfnotes)
    return perfect_notes

def alteration_note_candidates(modusmaior, modusminor, tempus, prolatio, layer):
    # To determine the notes susceptible to alteration, we need to:
    #   1. Once we have the perfect notes identified (or maybe even bigger?)
    #   2. Take the notes in between and see if the last UNCOLORED is a "breve"
    #   3. If it is, count all the notes in between in terms of minims,
    #   using the @numbase/@num ratio to multiply the values (no dots considered)
    #   Except for the last note, in this one, DO NOT CONSIDER THE RATIO 
    #   we want to know the exact number of breves between the boundaries
    #   4. Convert them in breves
    #   5. If it is n % 3 == 2 or n % 3 == 0 and n != 0 and n != 3
    #   THEN, that "breve" is susceptible to Alteration. SO, COUNT IT!
    #   Else to whatever, Do Not Count It!

    # Individual note values and gains, according to the mensuration
    note_durs = ['semifusa', 'fusa', 'semiminima', 'minima', 'semibrevis', 'brevis', 'longa', 'maxima']
    undotted_note_gain = [Fraction(1,8), Fraction(1,4), Fraction(1,2), 1, prolatio, tempus * prolatio, modusminor * tempus * prolatio, modusmaior * modusminor * tempus * prolatio]

    # Getting all the notes and rests of one voice into a python list, in order.
    # This allows to retrieve the index, which is not possible with MEI lists.
    voice_content = layer.getChildren()
    voice_noterest_content = []
    for element in voice_content:
        name = element.name
        if name == 'note' or name == 'rest':
            voice_noterest_content.append(element)
        else:
            pass

    # Find indices for starting and ending points of each sequence of notes to be analyzed.
    # Each of the following is a list of indices of notes greater or equal than: a Semibreve, a Breve, a Long and a Maxima, respectively.
    list_of_indices_geq_Sb = []
    list_of_indices_geq_B = []
    list_of_indices_geq_L = []
    list_of_indices_geq_Max = []
    # Get the indices
    for noterest in voice_noterest_content:
        dur = noterest.getAttribute('dur').value
        if dur == 'semibrevis' or noterest.hasAttribute('colored'):
            list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
        if dur == 'brevis' or noterest.hasAttribute('colored'):
            list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
            list_of_indices_geq_B.append(voice_noterest_content.index(noterest))
        if dur == 'longa' or noterest.hasAttribute('colored'):
            list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
            list_of_indices_geq_B.append(voice_noterest_content.index(noterest))
            list_of_indices_geq_L.append(voice_noterest_content.index(noterest))
        if dur == 'maxima' or noterest.hasAttribute('colored'):
            list_of_indices_geq_Sb.append(voice_noterest_content.index(noterest))
            list_of_indices_geq_B.append(voice_noterest_content.index(noterest))
            list_of_indices_geq_L.append(voice_noterest_content.index(noterest))
            list_of_indices_geq_Max.append(voice_noterest_content.index(noterest))

    # Minims in between semibreves (or higher note values)
    if prolatio == 3:
        #print("\nSEMIBREVE GEQ")
        #print(list_of_indices_geq_Sb)
        #print ""

        minim_alt_candidate = 0
        minim_alt_candidate_ids = []

        if 0 not in list_of_indices_geq_Sb and list_of_indices_geq_Sb != []:
            start_note = None
            f = list_of_indices_geq_Sb[0]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[0:f]

            candidate = minims_between_semibreves(start_note, middle_notes, end_note, note_durs, undotted_note_gain)
            if candidate[0]:
                minim_alt_candidate += 1
                minim_alt_candidate_ids.append(candidate[1])


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

            candidate = minims_between_semibreves(start_note, middle_notes, end_note, note_durs, undotted_note_gain)
            if candidate[0]:
                minim_alt_candidate += 1
                minim_alt_candidate_ids.append(candidate[1])

    # prolatio = 2
    else:
        minim_alt_candidate = None
        minim_alt_candidate_ids = []
        pass

    # Semibreves in between breves (or higher note values)
    if tempus == 3:
        #print("\nBREVE GEQ")
        #print(list_of_indices_geq_B)
        #print ""

        semibreve_alt_candidate = 0
        semibreve_alt_candidate_ids = []


        if 0 not in list_of_indices_geq_B and list_of_indices_geq_B != []:
            start_note = None
            f = list_of_indices_geq_B[0]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[0:f]

            candidate = sb_between_breves(start_note, middle_notes, end_note, prolatio, note_durs, undotted_note_gain)
            if candidate[0]:
                semibreve_alt_candidate += 1
                semibreve_alt_candidate_ids.append(candidate[1])

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

            candidate = sb_between_breves(start_note, middle_notes, end_note, prolatio, note_durs, undotted_note_gain)
            if candidate[0]:
                semibreve_alt_candidate += 1
                semibreve_alt_candidate_ids.append(candidate[1])


    # tempus = 2
    else:
        semibreve_alt_candidate = None
        semibreve_alt_candidate_ids = []
        pass

    # Breves in between longas (or higher note values)
    if modusminor == 3:
        #print("\nLONGA GEQ")
        #print(list_of_indices_geq_L)
        #print ""

        breve_alt_candidate = 0
        breve_alt_candidate_ids = []

        if 0 not in list_of_indices_geq_L and list_of_indices_geq_L != []:
            start_note = None
            f = list_of_indices_geq_L[0]
            end_note = voice_noterest_content[f]
            try:
                following_note = voice_noterest_content[f+1]
            except:
                following_note = None
            middle_notes = voice_noterest_content[0:f]

            candidate = breves_between_longas(start_note, middle_notes, end_note, prolatio, tempus, note_durs, undotted_note_gain)
            if candidate[0]:
                breve_alt_candidate += 1
                breve_alt_candidate_ids.append(candidate[1])

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

            candidate = breves_between_longas(start_note, middle_notes, end_note, prolatio, tempus, note_durs, undotted_note_gain)
            if candidate[0]:
                breve_alt_candidate += 1
                breve_alt_candidate_ids.append(candidate[1])

    # modusminor = 2
    else:
        breve_alt_candidate = None
        breve_alt_candidate_ids = []
        pass


    alt_candidates_list = [breve_alt_candidate, semibreve_alt_candidate, minim_alt_candidate]
    alt_candidates_list_ids = [breve_alt_candidate_ids, semibreve_alt_candidate_ids, minim_alt_candidate_ids]
    # count_altcandidates = 0
    # for item in alt_candidates_list:
    #     try:
    #         count_altcandidates += item
    #     except:
    #         count_altcandidates += 0
    # print str(alt_candidates_list) + " = " + str(count_altcandidates)
    return [alt_candidates_list, alt_candidates_list_ids]

def colored_notes(layer):
    # To determine the colored notes --> look for @colored attribute (.hasAttribute)
    # Colored notes are susceptible to change its value 
    # (or not, they may keep the original value too)
    count_colored_notes = 0
    for element in layer.getChildren():
        if element.hasAttribute("colored") and element.getAttribute("colored").value == "true":
            count_colored_notes += 1
    return count_colored_notes

def notes_susceptible_to_augmentation(modusmaior, modusminor, tempus, prolatio, layer):
    # Notes followed by <dot> are susceptible to be augmented 
    # or, in the case of a dot of division (or perfection), 
    # they keep their default value.
    # We should not count the ones with a dot of perfection, 
    # since these are already counted in the perfect_notes function
    # Thus, only count:
    #   Notes followed by dot,
    #   And that are not perfect by default.
    count_subject_to_aug = 0
    for noterest in layer.getChildren():
        if followed_by_dot(noterest):
            dur = noterest.getAttribute('dur').value
            if dur == "semibrevis" and prolatio == 3:
                pass
            elif dur == "brevis" and tempus == 3:
                pass
            elif dur == "longa" and modusminor == 3:
                pass
            elif dur == "maxima" and modusmaior == 3:
                pass
            else:
                count_subject_to_aug += 1
    return(count_subject_to_aug)



def main(directory, filename, archivo, notelevel, archivoid):

    if filename == "IvTrem07.mei":
        pass
    else:
        #print(filename + "\n")
        mensural_gtdoc = documentFromFile(directory + filename).getMeiDocument()
        staves = mensural_gtdoc.getElementsByName('staff')
        stavesDef = mensural_gtdoc.getElementsByName('staffDef')
        
        cmn_gtdoc = documentFromFile('../Files/GroundTruth/cmn-mei/' + filename).getMeiDocument()

        for i in range(0, len(stavesDef)):
            #print "Voice # " + str(i)

            staffDef = stavesDef[i]
            modusmaior = int(staffDef.getAttribute('modusmaior').value)
            modusminor = int(staffDef.getAttribute('modusminor').value)
            tempus = int(staffDef.getAttribute('tempus').value)
            prolatio = int(staffDef.getAttribute('prolatio').value)

            staff = staves[i]
            layer = staff.getChildrenByName('layer')[0]

            perfimp = perfect_notes(modusmaior, modusminor, tempus, prolatio, layer)
            alt =alteration_note_candidates(modusmaior, modusminor, tempus, prolatio, layer)
            col = colored_notes(layer)
            #print("colored notes: " + str(col))
            aug = notes_susceptible_to_augmentation(modusmaior, modusminor, tempus, prolatio, layer)
            #print("Susceptible to augmentation: " + str(aug))
            #print ""
            
            for k in range(0, 3):
                archivo.write(filename[:-4] + ',' + ('Voice # ' + str(i+1)) + ',' + notelevel[k] + ',' + str(perfimp[k]) + ',' + str(alt[0][k]) + ',' + str(col) + ',' + str(aug) + '\n')

                alt_ids_list = alt[1][k]
                for alt_id in alt_ids_list:
                    mens_alt_note = mensural_gtdoc.getElementById(alt_id)
                    cmn_alt_note = cmn_gtdoc.getElementById(alt_id)
                    archivoid.write(filename[:-4] + ',' + str(i+1) + ',' + alt_id + ',' + mens_alt_note.getAttribute('dur').value + ',' + cmn_alt_note.getAncestor('measure').getAttribute('n').value + '\n')

def run():
    directory = "../Files/GroundTruth/mensural-mei/"
    files = listdir(directory)
    archivo = open('mutable_notes_2.csv','w')
    archivoid = open('notes_subject_to_alteration_with_id.csv', 'w')
    archivo.write('Piece,Voice,Note Level,Perfect / Imperfect,Regular / Altered,Colored,Regular / Augmented\n')
    archivoid.write('Piece,Voice,Id,Note Shape,Measure\n')
    notelevel = ['L - B', 'B - Sb', 'Sb - M']
    for filename in files:
        main(directory, filename, archivo, notelevel, archivoid)
