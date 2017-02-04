from pymei import *


def merge_music_section(input_files):
    meiDocs = []
    for input_file in input_files:
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
    for i in range(1, len(input_files)):

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

    # output_file = input_files[0].split('/')[-1][:10] + ".mei"
    # print(output_file)
    # documentToFile(outdoc, output_file)
    return(outdoc)