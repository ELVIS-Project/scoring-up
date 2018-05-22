from pymei import *
import argparse


def remove_quality_info(meidoc):
    listNotesRests = meidoc.getElementsByName('note')
    listNotesRests.extend(meidoc.getElementsByName('rest'))
    for note_or_rest in listNotesRests:
        note_or_rest.removeAttribute('num')
        note_or_rest.removeAttribute('numbase')
        note_or_rest.removeAttribute('quality')
    return meidoc

def score_to_parts(input_meidoc, input_file):
    staffDefs_0 = input_meidoc.getElementsByName('staffDef')
    nvoices = len(staffDefs_0)

    meidocs = []
    for i in range(0, nvoices):
        doc = documentFromFile(input_file).getMeiDocument()
        section = doc.getElementsByName('section')[0]
        section.deleteAllChildren()
        section.addChild(input_meidoc.getElementsByName('staff')[i])
        staffGrp = doc.getElementsByName('staffGrp')[0]
        staffGrp.deleteAllChildren()
        staffGrp.addChild(input_meidoc.getElementsByName('staffDef')[i])
        meidocs.append(doc)
    return meidocs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Here you can chose to get 2 different kinds of files from the ground_truth_score_file to be used as input data in either the 'score_up.py' program or the 'ApelAlg.py' module implemented in the 'score_up.py' program. \nThe options (activated by the flags -quasiscore and -parts, respectively) and the 'ground_truth_score_file' parameter are explained later. \nYOU NEED TO USE ONE AND ONLY ONE FLAG")
    parser.add_argument('ground_truth_score_file', help="Ground truth Mensural MEI file that encodes the piece as a score, with the right values for each note ('perfect', 'imperfect', 'altered').")
    parser.add_argument('-quasiscore', '--target_file', help="When using this flag, one obtains a 'quasiscore' version of the score encoded in 'ground_truth_score_file', this means a single mensural-mei file that includes all the voices, just as the ground_truth_score_file, but without the duration information (i.e., removing any information accounting for 'perfections', 'imperfections', 'alterations', etc). \nThis result is useful when testing the 'ApelAlg' module implemented in the 'scoring_up.py' program, which is done by running the 'scoring_up.py' program with the flag '-apel' followed by this 'quasiscore' file, and the flag '-comparison' followed by the 'ground_truth_score_file'.\nWhen using this flag, one has to give a file path ('target_file') to save the resulting 'quasiscore' file.")
    parser.add_argument('-parts', '--target_directory', help="When using this flag, one obtains the individual parts with no duration information (i.e., removing any information accounting for 'perfections', 'imperfections', 'alterations', etc). \nThis individual parts are used as the input_files in the 'scoring_up.py' program; by additionally using the '-compare' flag, one can compare the scored-up result from the 'scoring_up.py' program against the 'ground_truth_score_file'. \nWhen using this flag, one has to give a directory ('target_directory') to save the resulting 'parts' files.")
#    parser.add_argument('option', choices=["1", "2"], default="3", help="Pick an option based on what you want to obtain from the ground_truth_score_file. \n Choose '1' for getting a quasiscore, which is useful when testing the 'ApelAlg' module implemented in the 'scoring_up.py' program (this is done by running the 'scoring_up.py' program with the flag '-apel' followed by this 'quasiscore' file, and the flag '-comparison' followed by the 'ground_truth_score_file').\nThe quasiscore obtained here is a single mensural-mei file that includes all the voices, just as the ground_truth_score_file, but without the duration information (i.e., removing any information accounting for 'perfections', 'imperfections', 'alterations', etc). \n Choose '2' for getting the individual parts (with no duration information). This individual parts are used to run the 'scoring_up.py' program (by additionally using the '-compare' flag you will be able to compare the scored-up result to the 'ground_truth_score_file')")
    args = parser.parse_args()

    if args.target_file != None and args.target_directory != None:
        parser.error("Use of more than one flag at a time")
    elif args.target_file == None and args.target_directory == None:
        parser.error("No flag was used. You must use a flag for the program to work.")
    else:
        ground_truth_score_meidoc = documentFromFile(args.ground_truth_score_file).getMeiDocument()
        quasiscore_meidoc = remove_quality_info(ground_truth_score_meidoc)
        
        if args.target_file != None:
            documentToFile(quasiscore_meidoc, args.target_file)
        
        if args.target_directory != None:
            filename = args.ground_truth_score_file.split('/')[-1]
            if args.target_directory[-1] == '/':
                new_path = args.target_directory + filename
            else:
                new_path = args.target_directory + '/' + filename
            
            part_number = 0
            parts_meidocs_list = score_to_parts(quasiscore_meidoc, args.ground_truth_score_file)
            for meipart in parts_meidocs_list:
                part_number += 1
                documentToFile(meipart, new_path[:-4] + "_Part" + str(part_number) + ".mei")