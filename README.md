# Scoring-up Script
The scoring-up script takes a finite number of Mensural MEI files, each of which only contains one part (i.e., voice) from a mensural piece and merge them into just one Mensural MEI file in which all the parts are lined up into a score. The alignment of the parts is a complex issue in mensural notation, since the same note-shape can have different durational values (_perfect_ / _imperfect_ / _altered_) depending on the context.

This scoring-up script consists of a **merge module** and a **set of duration-finder modules**. The **merge module** merges the various Mensural MEI files encoding each part into a single Mensural MEI file that encodes the whole piece in a "quasiscore" format (i.e., without any vertical alignment of the parts). The set of **duration-finder modules** deal with the context-dependent nature of the notation to determine the durational value of the notes according to different styles of mensural notation (namely, _Ars antiqua_, _Ars nova_, and _white mensural notation_). The **ArsNova_and_WhiteMensural module** deals with the context-dependent nature of the notation by implementing the _principles of imperfection and alteration_—outlined by Franco of Cologne (ca. 1280) and Willi Apel. It also includes functions for: distinguishing between dots of division and dots of augmentation, handling hemiola coloration, and dealing with the simultaneous use of perfect mensurations at different note levels. The **ArsAntiqua module** handles Franconian notation, interpreting groups of semibreves as pointed out by Franco's _Ars cantus mensurabilis_ (ca. 1280) for ternary division of the breve.

## Requirements 
- The [LibMEI library](https://github.com/DDMAL/libmei). The wiki contains instructions on both the installation of the LibMEI C++ library, and the installation of the python bindings.

## Usage
The main program is contained in the ```score_up.py``` file. This program takes a list of Mensural MEI files that encode each of the individual parts (i.e., voices) of the piece and scores them up by running the following steps:
1. Merging the Mensural MEI files that encode each part into a single Mensural MEI file (encoding a sort of 'quasi-score')
2. Finding out the duration of each note in the 'quasi-score' MEI file. This completes the scoring up process.

You can run the whole "scoring_up" script or you could run one of its two steps individually. If you want to run the whole scoring-up process, use the command ```python score_up.py``` followed by the list of files encoding each of the parts and the filepath in which you want to store the output score. For example, to score-up a four-voice mensural piece use:
```
$ python3 score_up.py <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for score>
```

If, on the other hand, you want to run only one of the two steps of the scoring-up process, either merging or note-duration finding, use the following flags:
- ```-merge```
  
  Use this flag to merge all the Mensural MEI files into a single Mensural MEI file. 
  
  Example: 
  ```
  $ python3 score_up.py -merge <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for quasi-score>
  ```
  
- ```-apel```

  Use this flag to find out the durational value of each note in a single Mensural MEI file (regardless of whether this file is encoding one or multiple parts). 

  Example: 
  ```
  $ python3 score_up.py -apel <input file> <output file>
  ```

You have an additional third flag that you can use to evaluate the results of the scoring-up tool if you happen to have a ground truth Mensural MEI file:
- ```-compare```

  Use this flag to compare the output of the ```scoring_up``` process, or just the output of the second part of it (```-apel```), against a ground truth file. 
    
    Example:
    ```
    $ python3 score_up.py <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for score> -compare <filepath of ground truth>
    ```
    
And an additional fourth flag:
- ```-style```

  Use this flag to indicate the notation style of the music. Three values are available: ```ars_antiqua```, ```ars_nova```, and ```white_mensural```. This flag will indicate which module should be used to compute the duration of the notes (either _ArsAntiqua_ or _ArsNova_and_WhiteMensural_). If this flag is not present, the music is considered to be written in white mensural notation (i.e., the default value of the ```-style``` flag is ```white_mensural```).
    
    Example:
    ```
    $ python3 score_up.py <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for score> -style ars_antiqua -compare <filepath of ground truth>
    ```
## Experiment
The algorithm is tested on a small set of fourteenth-century Ars Nova pieces from the Ivrea Codex<sup>[1](#one)</sup> and fifteenth-century pieces from Du Fay and Ockeghem<sup>[2](#two)</sup>.
The files involved in this experiment are distributed in the _Files_ directory as follows:
- The ground truth Mensural MEI files are in the _Files/GroundTruth/mensural-mei_ directory and their modern transcriptions in CMN MEI are at _Files/GroundTruth/cmn-mei_
- The output of the scoring-up tool is found in _Files/Output_ScUp_. Here you can find the Mensural MEI score for each piece as well as a text file that lists all the notes (with their _ids_ and _voice number_) that were misclassified as _perect_ / _imperfect_ / _altered_ by the algorithm. This information is at the bottom of the text file, here it is an example of how it is presented:

> NOT EQUAL: the NOTE m-213 in voice 1
>
> In GROUND TRUTH: SEMIBREVIS, with 1 x default value
>
> In APEL OUTPUT: SEMIBREVIS, with 2/3 x default value

This means that the note in _voice 1_ with _id m-213_ was imperfected (i.e., multiplied by _2/3_) when, according to the ground truth, it should not. Regular imperfections are represented by _2/3 x default value_, alterations are represented by _2 x default value_, and augmentations are represented by _3/2 x default value_. (Note: the _5/6_ fraction that appears in the second voice of _Duf22518_, _Duf3025_, and _Iv004_ represents a _partial imperfection_, which is a feature yet to be implemented in the scoring-up tool.)

For more details regarding the pieces, the algorithm behind the scoring-up tool, and the results of this experiment, please consult Chapters 3 and 4 of the thesis [Automatic Scoring Up of Mensural Music Using Perfect Mensurations, 1300–1550](http://digitool.Library.McGill.CA:80/R/-?func=dbin-jump-full&object_id=151045&silo_library=GEN01). A summary of all misclassified notes for all the pieces can be found at _Summary_of_results/comparison.csv_. The _Measure Number_ and the _Position in Measure_ refer to the modern transcriptions found in _Files/GroundTruth/cmn-mei_. A summary of all the notes that were subject to some kind of modification in their durational value (due to imperfection, alteration, the presence of a dot, or coloration) is shown in _Summary_of_results/mutable_notes.csv_.

## Notes

<a name="one">1</a>: The _Ars Nova_ pieces were obtained from the [Measuring Polyphony Project](http://measuringpolyphony.org).

<a name="two">2</a>: Du Fay's and Ockeghem's pieces were obtained by using modern transcriptions provided in the [Josquin Research Project](http://josquin.stanford.edu), converted them into CMN MEI files through the Sibelius' [SibMEI plugin](https://github.com/music-encoding/sibmei), and translate these CMN MEI files into Mensural MEI by using the [Mensural MEI Translator](https://github.com/DDMAL/CMN-MEI_to_MensuralMEI_Translator).
