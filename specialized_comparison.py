from pymei import *
from fractions import *

file1 = raw_input("Piece # 1: ")
doc1 = documentFromFile(file1).getMeiDocument()
file2 = raw_input("Piece # 2: ")
doc2 = documentFromFile(file2).getMeiDocument()

notes1 = doc1.getElementsByName('note')
notes1.extend(doc1.getElementsByName('rest'))

for note1 in notes1:
    note2 = doc2.getElementById(note1.id)

    quality1 = note1.getAttribute('quality')
    quality2 = note2.getAttribute('quality')

    if quality1 is None and quality2 is None:
        pass
    elif quality1 is not None and quality2 is None:
        print(note1)
        print("The result of Apel's algorithm is MISSING Quality")
        print(quality1)
        print ""
    elif quality1 is None and quality2 is not None:
        print(note1)
        print("The result of Apel's algorithm contains an EXTRA Quality")
        print(quality2)
        print ""
    elif quality1.value == quality2.value:
        pass
    else:
        print(note1)
        print("The QUALITY is DIFFERENT")
        print("Karen's transcription: " + str(quality1))
        print("Apel's algorithm: " + str(quality2))
        print ""
