from os import listdir
import subprocess

qs_directory = "../Files/Input/QuasiScore/"
files = listdir(qs_directory)
for filename in files:
    quasiscore_file = qs_directory + filename
    ground_truth_file = "../Files/GroundTruth/mensural-mei/" + filename
    scored_up_result = "../Files/Output_ScUp/" + filename
    subprocess.call(["python", "../score_up.py", "-apel", quasiscore_file, scored_up_result, "-compare", ground_truth_file])