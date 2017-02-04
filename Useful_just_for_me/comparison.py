from pymei import *
from fractions import *
from os import listdir

# Pieces which transcription by Apel and a original transcription in Sibelius we are about to compare
pieces = ['bona_againstTrem', 'cum_venerint_againstIv', 'de_touz_against_Iv', 'decens_againstIv', 'diex_MT', 'durement_MT', 'postMisse_MT', 'hugo_against_Iv']
directory = './3_Apel_results/'
files = listdir(directory)

for file in files:
    if file.endswith('_STG3.mei'):
        for piece in pieces:
            if file.startswith(piece):
                print("\n" + piece.upper() + "\n")
                # Determining the files that contain the piece in the different formats: CMN MEI and Mensural MEI (the 2 transcriptions) 
                cmn_file = "./0_motets_corrected/2_cmn_mei/" + piece + ".mei"
                print(cmn_file)
                # The Mensural MEI files to compare: the transcription done by Apel and the one in Sibelius
                mensural_ApelTranscriptFile = "./3_Apel_results/" + file     #file2
                print(mensural_ApelTranscriptFile)
                mensural_SibTranscriptFile = "./1_ground_truth/" + file[:-9] + ".mei"   #file1
                print(mensural_SibTranscriptFile)
                print("")

                # Getting the Mei Documents for these files
                cmnDoc = documentFromFile(cmn_file).getMeiDocument()
                karenDoc = documentFromFile(mensural_SibTranscriptFile).getMeiDocument()
                apelDoc = documentFromFile(mensural_ApelTranscriptFile).getMeiDocument()

                # Getting all the notes and rests contained in them
                sib_notes = karenDoc.getElementsByName('note')
                sib_notes.extend(karenDoc.getElementsByName('rest'))

                # Compare the quality values (actual duration) values of these notes (and rests) in both transcriptions
                for sib_note in sib_notes:
                    apel_note = apelDoc.getElementById(sib_note.id)

                    sib_quality = sib_note.getAttribute('quality')
                    apel_quality = apel_note.getAttribute('quality')

                    if sib_quality is None and apel_quality is None:
                        pass

                    elif sib_quality is not None and apel_quality is None:
                        cmn_note = cmnDoc.getElementById(sib_note.id)
                        voice_number = cmn_note.getAncestor('staff').getAttribute('n').value
                        measure_number = cmn_note.getAncestor('measure').getAttribute('n').value
                        print("The note " + sib_note.id + " in measure " + measure_number + " and voice " + voice_number)
                        print("Has a quality '" + sib_quality.value + "'' in Sibelius\nthat is NOT PRESENT IN APEL\n")
                    
                    elif sib_quality is None and apel_quality is not None:
                        cmn_note = cmnDoc.getElementById(sib_note.id)
                        voice_number = cmn_note.getAncestor('staff').getAttribute('n').value
                        measure_number = cmn_note.getAncestor('measure').getAttribute('n').value
                        print("The note " + sib_note.id + " in measure " + measure_number + " and voice " + voice_number)
                        print("HAS A QUALITY '" + apel_quality.value + "'' IN APEL\nthat is not present in Sibelius\n")

                    elif sib_quality.value == apel_quality.value:
                        pass

                    else:
                        cmn_note = cmnDoc.getElementById(sib_note.id)
                        voice_number = cmn_note.getAncestor('staff').getAttribute('n').value
                        measure_number = cmn_note.getAncestor('measure').getAttribute('n').value
                        print("The note " + sib_note.id + " in measure " + measure_number + " and voice " + voice_number)
                        print("The QUALITY is DIFFERENT")
                        print("Sibelius' transcription: '" + sib_quality.value + "'")
                        print("Apel's algorithm: '" + apel_quality.value + "'\n")