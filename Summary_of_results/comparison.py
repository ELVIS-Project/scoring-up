from os import listdir
from pymei import *
from fractions import *
import sys


# Comparison function
def comparison(out_doc, gt_doc, cmn_doc, archivo, filename):

    gt_staves = gt_doc.getElementsByName('staff')
    accuracy_list = []
    string = filename
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
                cmn_note = cmn_doc.getElementById(gt_note.id)
                measure = cmn_note.getAncestor('measure')
                measure_number = measure.getAttribute('n').value
                cmn_note_index_in_measure = 0
                for note in cmn_note.getPeers():
                    cmn_note_index_in_measure += 1
                    if note == cmn_note:
                        break
                string = string + ',' + voice_number + ',' + gt_note.name.upper() + ',' + gt_note.id + ',' + measure_number + ',' + str(cmn_note_index_in_measure)
                string = string + ',' + gtval_dur + ',' + str(float(gtval_numbase)/float(gtval_num))
                string = string + ',' + outval_dur + ',' + str(float(outval_numbase)/float(outval_num)) + '\n'
                archivo.write(string)
                diff += 1
                string = ''

        accuracy_ratio_per_voice = 1 - Fraction(diff,len(gt_notes))
        accuracy_list.append(accuracy_ratio_per_voice)

    return accuracy_list

archivo = open("comparison.csv", "w")
archivo.write("Piece,Voice,Note/Rest,Id,Measure Number,Position in Measure,Ground truth,,Script,\n")
archivo.write(",,,,,,Note Shape,Quality,Note Shape,Quality\n")
cmn_gtdirectory = "../Files/GroundTruth/cmn-mei/"
files = listdir(cmn_gtdirectory)
for filename in files:
    if filename.endswith('.mei'):
        cmn_gtfile = cmn_gtdirectory + filename
        mensural_gtfile = "../Files/GroundTruth/mensural-mei/" + filename
        scored_up_result = "../Files/Output_ScUp/" + filename

        cmn_gtdoc = documentFromFile(cmn_gtfile).getMeiDocument()
        mens_gtdoc = documentFromFile(mensural_gtfile).getMeiDocument()
        scup_doc = documentFromFile(scored_up_result).getMeiDocument()
        
        comparison(scup_doc, mens_gtdoc, cmn_gtdoc, archivo, filename)

        #subprocess.call(["python", "../score_up.py", "-apel", quasiscore_file, scored_up_result, "-compare", ground_truth_file])

        
