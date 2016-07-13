import argparse

from pymei import *


class ScoreUpper:

    def __init__(self, input_files, output_file):
        self.input_files = input_files
        self.output_file = output_file

    def merge(self):
    	# Converting all input files to Mei Document Objects
        meiDocs = []
        for input_file in self.input_files:
            meiDocs.append(documentFromFile(input_file).getMeiDocument())

        # Using the first file as foundation for the output document
        outdoc = meiDocs[0]
        staffGrp = outdoc.getElementsByName('staffGrp')[0]
        section = outdoc.getElementsByName('section')[0]

        # Changing the @xml:id of the elmeents to include the information about the part they belong to: part 1 (P1)
        staffDef = outdoc.getElementsByName('staffDef')[0]
        staffDef.id = staffDef.id + "_P1"
        for element in staffDef.getDescendants():
            element.id = element.id + "_P1"
        staves = outdoc.getElementsByName('staff')
        for staff in staves:
            staff.id = staff.id + '_P1'
            for element in staff.getDescendants():
                element.id = element.id + "_P1"

        # Adding the staves from the other voices (by adding the <staffDef> and <staff> elements) and modifying the information related to the staff number (@n)
        # Also, change the @xml:id of all the elements to include the Part they belong to (for example: P2 and P3 stand for part 2 and part 3, respectively)
        for i in range(1, len(self.input_files)):

            staffDef = meiDocs[i].getElementsByName('staffDef')[0]
            # @xml:id
            staffDef.id = staffDef.id + '_P' + str(i+1)
            for element in staffDef.getDescendants():
                element.id = element.id + "_P" + str(i+1)
            # <staffDef>
            if staffDef.hasAttribute('n'):
                staffDef.getAttribute('n').setValue(str(i+1))
            staffGrp.addChild(staffDef)
            
            staff = meiDocs[i].getElementsByName('staff')[0]
            # @xml:id
            staff.id = staff.id + '_P' + str(i+1)
            for element in staff.getDescendants():
                element.id = element.id + "_P" + str(i+1)
            # <staff>
            if staff.hasAttribute('n'):
                staff.getAttribute('n').setValue(str(i+1))
            section.addChild(staff)

        documentToFile(outdoc, self.output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scores-up the MEI part/voice files")
    parser.add_argument("input_files", help="A list of MEI files to score-up. Every file has to be of the form fileName.mei (don't forget the extension) and each file of the list must be separated from each other by a blank space (nothing else).", nargs='+')
    parser.add_argument("output_file", help="The name of the output MEI file whre you want to save the score. It should be in the form fileName.mei (don't forget the extension).", type=str)
    args = parser.parse_args()
    # print(args.input_files)
    # for input_file in args.input_files:
    #     print("input file: " + input_file)
    # print("output file: " + args.output_file)
    parts_to_score = ScoreUpper(args.input_files, args.output_file)
    parts_to_score.merge()