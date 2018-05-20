# Scoring-up Script
The scoring-up script takes a finite number of Mensural MEI files, each of which only contains one part (i.e., voice) from a mensural piece and merge them into just one Mensural MEI file in which all the parts are lined up into a score. The alignment of the parts is a complex issue in mensural notation, since the same note-shape can have different durational values (_perfect_ / _imperfect_ / _altered_) depending on the context.

This scoring-up script consists in two modules: _merge_ and _apel_. The _merge module_ merges the various Mensural MEI files encoding each part into a single Mensural MEI file that encodes the whole piece in a "quasiscore" format (i.e., without any vertical alignment of the parts). The _apel module_ deals with the context-dependent nature of the notation to determine the durational value of the notes by implementing Apel's / Franco's _principles of imperfection and alteration_. In addition to Apel's principles, this module includes functions for: distinguishing between dots of division and dots of augmentation, handling hemiola coloration, and dealing with the simultaneous use of perfect mensurations at different note levels. 

## Usage
The main program is contained in the ```score_up.py``` file. This program takes a list of Mensural MEI files that encode each of the individual parts (i.e., voices) of the piece and scores them up by running the following steps:
1. Merging the Mensural MEI files that encode each part into a single Mensural MEI file (encoding a sort of 'quasi-score')
2. Finding out the duration of each note in the 'quasi-score' MEI file. This completes the scoring up process.

You can run the whole "scoring_up" script or you could run one of its two steps individually. If you want to run the whole scoring-up process, use the command ```python score_up.py``` followed by the list of files encoding each of the parts and the filepath in which you want to store the output score. For example, to score-up a four-voice mensural piece use:
```
$ python score_up.py <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for score>
```

If, on the other hand, you want to run only one of the two steps of the scoring-up process, either merging or note-duration finding, use the following flags:
- ```-merge```
  
  Use this flag to merge all the Mensural MEI files into a single Mensural MEI file. 
  
  Example: 
  ```
  $ python score_up.py -merge <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for quasi-score>
  ```
  
- ```-apel```

  Use this flag to find out the durational value of each note in a single Mensural MEI file (regardless of whether this file is encoding one or multiple parts). 

  Example: 
  ```
  $ python score_up.py -apel <input file> <output file>
  ```

You have an additional third flag that you can use to evaluate the results of the scoring-up tool if you happen to have a ground truth Mensural MEI file:
- ```-compare```

  Use this flag to compare the output of the ```scoring_up``` process, or just the output of the second part of it (```-apel```), against a ground truth file. 
    
    Example:
    ```
    $ python score_up.py <filepath of part 1> <filepath of part 2> <filepath of part 3> <filepath of part 4> <filepath for score> -compare <filepath of ground truth>
    ```

## Experiment
The algorithm is tested on some Ars Nova pieces from the Ivrea Codex and fifteenth-century pieces from Du Fay and Ockeghem.
