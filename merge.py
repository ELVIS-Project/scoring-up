from pymei import *


def merge_music_section(input_files):
    meiDocs = []
    for input_file in input_files:
        meiDocs.append(documentFromFile(input_file).getMeiDocument())

    # Using the first file as foundation for the output document
    outdoc = meiDocs[0]
    staffGrp = outdoc.getElementsByName('staffGrp')[0]
    section = outdoc.getElementsByName('section')[0]

    # Adding the staves from the other voices (by adding the <staffDef> and <staff> elements) and modifying the information related to the staff number (@n)
    for i in range(1, len(input_files)):

        staffDef = meiDocs[i].getElementsByName('staffDef')[0]
        # <staffDef>
        if staffDef.hasAttribute('n'):
            staffDef.getAttribute('n').setValue(str(i+1))
        staffGrp.addChild(staffDef)
        
        staff = meiDocs[i].getElementsByName('staff')[0]
        # <staff>
        staff.addAttribute('n', str(i+1))
        section.addChild(staff)

    return(outdoc)