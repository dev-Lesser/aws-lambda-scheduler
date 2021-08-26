import os
import argparse
import zipfile

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process Create Zip file')
    parser.add_argument('--zipPath', required=True, help="zip folder path")
    parser.add_argument('--output', default="output.zip", help="output zip name [output.zip]")

    args = parser.parse_args()
    FILE_PATH = args.zipPath
    OUTPUT_NAME = args.output

    zip_file = zipfile.ZipFile(OUTPUT_NAME, 'w')
    for file in os.listdir(FILE_PATH):
        if not file.endswith('.zip'):
            zip_file.write(os.path.join(FILE_PATH, file), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()