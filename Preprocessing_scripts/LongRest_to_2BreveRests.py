from pymei import *
from os import listdir


directory = "."
files = listdir(directory)

files_without_DotsOfDivision = []

# For each Ars Nova piece in Mensural MEI
for file in files:
    if file.endswith('_MENSURAL.mei'):
        doc = documentFromFile(file).getMeiDocument()
        
        # Changing the 2-breve rests <rest @dur = "longa" @EVENTUALDUR = "2B"> to 2 consecutive <rest @dur = "brevis"> elements

        # We assume that there is no need for changes
        long_to_2breveRests = False
        stavesDef = doc.getElementsByName('staffDef')
        staves = doc.getElementsByName('staff')
        for i in range(0, len(stavesDef)):
            staffDef = stavesDef[i]
            # Unless we are in perfect modusminor
            if staffDef.getAttribute('modusminor').value == '3':
                staff_layer = staves[i].getChildrenByName('layer')[0]
                rests = staff_layer.getChildrenByName('rest')
                for rest in rests:
                    # And there is a "long" rest that is supposed to be 2-breves long.
                    if rest.hasAttribute('EVENTUALDUR') and rest.getAttribute('EVENTUALDUR').value == '2B':
                        long_to_2breveRests = True
                        # First breve-rest
                        rest.getAttribute('dur').setValue('brevis')
                        rest.removeAttribute('num')
                        rest.removeAttribute('numbase')
                        # Second breve-rest (with the same attributes)
                        other_breve_rest = MeiElement('rest')
                        other_breve_rest.setAttributes(rest.getAttributes())
                        # Changing the xml ids for both rests
                        other_breve_rest.setId(rest.id + "_1st")
                        rest.setId(rest.id + "_2nd")
                        staff_layer.addChildBefore(rest, other_breve_rest)
        
        # Output File Part
        # If there were changes from long to 2breve-rests, then we create a new file with a different name to save these changes
        if long_to_2breveRests:
            print(file)
            output_file = file[:-4] + "_BreveRests.mei"
            documentToFile(doc, output_file)
        # If there were no changes, the output_file = file, so we don't create a new file
        else:
            output_file = file

        # Identifying which pieces don't have dots of division
        # And store them into one place
        if not doc.getElementsByName('dot'):
            files_without_DotsOfDivision.append(output_file)

print("\nPieces without dots of division:")
print(files_without_DotsOfDivision)