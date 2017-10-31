from os import listdir
import subprocess

gtdirectory = "../Files/GroundTruth/mensural-mei/"
files = listdir(gtdirectory)
for filename in files:
    ground_truth_file = gtdirectory + filename
    target_file = "../Files/Input/QuasiScore/" + filename
    subprocess.call(["python", "../UsefulScripts/generate_input_data.py", ground_truth_file, "-quasiscore", target_file])