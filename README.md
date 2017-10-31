# Scoring-up Script
The scoring-up script takes a finite number of mensural-mei files, each of which only contains one part (i.e., voice) from a mensural piece, and merge them into just one mensural-mei file in which all the parts are lined up into a score. The alignment of the parts is a complex issue, since the same note-shape in mensural notation can have different durational values ('perfect'/'imperfect'/'altered') depending on the context.

This scoring-up script consists in two modules: 'merge' and 'apel'. The 'merge' module merges the various mensural-mei files encoding each part into a single mensural-mei file that encodes the whole piece in a 'quasiscore' format (i.e., without any vertical alignment of the parts). The 'apel' module deals with the context-dependent nature of the notation to determine the durational value of the notes by implementing Apel's / Franco's principles of "imperfection" and "alteration". In addition to Apel's principles, this module includes functions for: distinguishing between dots of division and dots of augmentation, handling hemiola coloration, and dealing with the simultaneous use of perfect mensurations at different note levels. 

## Experiment
The algorithm is tested on some Ars Nova pieces from the Ivrea Codex and fifteenth-century pieces from Du Fay and Ockeghem.
