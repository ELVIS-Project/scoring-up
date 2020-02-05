import merge
import ArsNova_and_WhiteMensural
import ArsAntiqua
import argparse
import pymei
from fractions import *

import sys

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program takes a list of Mensural MEI files (list_of_input_files) that encode each of the individual parts (i.e., voices) of the piece and scores them up by running the following steps:\n1. Merging the Mensural MEI files that encode each part into a single Mensural MEI file (encoding a sort of 'quasiscore')\n2. Finding out the duration of each note in the 'quasiscore' MEI file. This completes the scoring up process.\nYou can run the whole 'scoring_up' script by just entering the list_of_input_files (together with the program name 'scoring_up.py'), or you could run one of the two steps by using the flags '-merge' and '-apel'. \nNote # 1: you are not allowed to use the two flags '-merge' and '-apel' together.\nNote # 2: You can use the '-compare' flag with either the '-apel' flag or with no flag at all, as '-compare GROUND_TRUTH_FILE' would compare the output of the 'apel script', or of the whole 'scoring_up' process, against the 'ground_truth_file'.")
    parser.add_argument('list_of_input_files', help="List of Mensural MEI files that encode each of the individual parts (i.e., voices) of the piece. \nEach file must include the extension (.mei). There should be a space separating each of the individual files. \nThese files will be merged into a single file, and then the right duration of each of its notes will be found. These two processes (1. merging and 2. apel) conform the scoring_up process.", nargs='+')
    parser.add_argument('-merge', help="Use this flag to merge all the mensural MEI files into a single Mensural MEI file.", action='store_true')
    parser.add_argument('-apel', help="Use this flag to find out the duration value of each note in a single Mensural MEI file (doesn't matter if this file is encoding a single part, or a quasiscore).", action='store_true')
    parser.add_argument('-compare', help="Use this flag to compare the output of the 'scoring_up' process, or just the output of the second part of it ('-apel') against a ground truth file.")
    parser.add_argument('output_file', help="File path to store the output (could be the output of the whole 'scoring_up.py' program, or just the 'merge' or 'apel' parts, when using the corresponding flags '-merge' and '-apel').")
    parser.add_argument('-style', choices=["ars_antiqua", "ars_nova", "white_mensural"], default="white_mensural", help="Use this flag to indicate the notational style of the piece. By default, the flag's value is white_mensural.")
    args = parser.parse_args()

    sys.stdout = open(args.output_file[:-4] + ".txt", "w")

    # Error in the parameters
    if args.apel and len(args.list_of_input_files)>1:
        parser.error("Must use only one 'input_file' with the flag '-apel'")
    if args.merge and args.compare:
        parser.error("The '-compare' flag must not be used together with the '-merge' flag.\nThe '-compare' flag is only to be used together with the '-apel' flag or with no flag at all, as '-compare' is used to compare the output of the 'apel script' (just by itself, or within the context of the 'scoring up' process) against the 'ground truth file'.")
    if args.merge and args.apel:
        parser.error("Don't use both flags '-merge' and '-apel' at the same time. If you want to perform the whole 'scoring_up' script (doing both the 'merging' of the parts and find the 'actual duration of the notes using apel's rules'), you should not use any flag at all.")
    
    # Running the modules according to the parameters specified by the user
    if args.merge:
        quasiscore = merge.merge_music_section(args.list_of_input_files)
        pymei.documentToFile(quasiscore, args.output_file)

    elif args.apel:
        print("\nAPEL RESUTLS - Warnings with respect to rules in conflict\n")
        input_quasiscore_doc = pymei.documentFromFile(args.list_of_input_files[0]).getMeiDocument()
        # Style specification
        if args.style == "ars_antiqua":
            out_apel = ArsAntiqua.lining_up(input_quasiscore_doc)
        else:   
            out_apel = ArsNova_and_WhiteMensural.lining_up(input_quasiscore_doc)
        # Comparison flag
        if args.compare:
            print("\nCOMPARISON RESUTLS - Notes/Rests (with their xml:id and voice number) that don't match with the ground truth\n")
            accuracy_results = comparison(out_apel, pymei.documentFromFile(args.compare).getMeiDocument())
            print("\nACCURACY:")
            for i in range (0, len(accuracy_results)):
                print("Voice # " + str(i) + ":\t" + str(accuracy_results[i]) + " = " + str(float(accuracy_results[i])*100))
        pymei.documentToFile(out_apel, args.output_file)

    else:
        quasiscore = merge.merge_music_section(args.list_of_input_files)
        print("\nAPEL RESUTLS - Warnings with respect to rules in conflict\n")
        # Style specification        
        if args.style == "ars_antiqua":
            score = ArsAntiqua.lining_up(quasiscore)
        else:   
            score = ArsNova_and_WhiteMensural.lining_up(quasiscore)
        pymei.documentToFile(score, args.output_file)
        # Comparison flag
        if args.compare:
            print("\nCOMPARISON RESUTLS - Notes/Rests (with their xml:id and voice number) that don't match with the ground truth\n")
            accuracy_results = comparison(pymei.documentFromFile(args.output_file).getMeiDocument(), pymei.documentFromFile(args.compare).getMeiDocument())
            print("\nACCURACY:")
            for i in range (0, len(accuracy_results)):
                print("Voice # " + str(i) + ":\t" + str(accuracy_results[i]) + " = " + str(float(accuracy_results[i])*100))

    sys.stdout.close()
