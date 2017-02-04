from pymei import *
import argparse


def score_to_parts(input_file):
    scoredoc_0 = documentFromFile(input_file).getMeiDocument()
    staffDefs_0 = scoredoc_0.getElementsByName('staffDef')
    nvoices = len(staffDefs_0)

    for i in range(0, nvoices):
        doc = documentFromFile(input_file).getMeiDocument()
        section = doc.getElementsByName('section')[0]
        section.deleteAllChildren()
        section.addChild(scoredoc_0.getElementsByName('staff')[i])
        staffGrp = doc.getElementsByName('staffGrp')[0]
        staffGrp.deleteAllChildren()
        staffGrp.addChild(scoredoc_0.getElementsByName('staffDef')[i])
        documentToFile(doc, input_file[:-4] + "_Part" + str(i+1) + ".mei")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    score_to_parts(args.input_file)