""" This script reads creates labels of golf shots stored in the Metrics csv files"""

import os
from labelExtraction import extractLabel


def main():
    # Specify the directory path
    metricsFolder = (
        "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/raw/Metrics"
    )
    labelsFolder = "/Users/rokbohinc/Documents/Work/Golf_AI/Golfshot_Categoriser/data/extracted/labels"

    # List all files in the directory
    files = [file for file in os.listdir(metricsFolder) if file.endswith(".csv")]

    filePaths = [
        (os.path.join(metricsFolder, file), os.path.join(labelsFolder, file))
        for file in files
    ]

    # Generate lables
    for importPath, exportPath in filePaths:
        extractLabel(import_path=importPath, export_path=exportPath)


if __name__ == "__main__":
    main()
