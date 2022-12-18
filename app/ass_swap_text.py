# import system module for file io
import sys
# import regex module for string search
import re


# opens the original file (.ass) and returns two lists
# inputs
# file_path - path of the file
# outputs
# original_file_name - name of the file
# headers -  all lines above '[Events]\nFormat...'
# original_lines - actual lines to be replaced 'Dialogue:...'
def open_original(file_path):
    # open file stream
    original_file = open(file_path, encoding='utf-8')

    # extract data
    file_name = original_file.name  # name of file
    lines = original_file.readlines()

    # close file
    original_file.close()

    # split into headers and dialogue
    idx = lines.index('[Events]\n') + 1

    headers = lines[:idx+1]
    original_lines = [line.strip() for line in lines[idx+1:]]

    # return results
    return file_name, headers, original_lines


# opens the translated text file (.srt/.txt) and returns a list
# inputs
# file_path - path of the file
# outputs
# translate_lines - lines with translated text
def open_translate(file_path):
    # open file
    translate_file = open(file_path, encoding='utf-8')
    raw_lines = translate_file.readlines()
    # close file
    translate_file.close()

    # parse depending on extension
    if file_path.endswith(".txt"):
        translate_lines = txt_get_lines(raw_lines)
    else:
        translate_lines = srt_get_lines(raw_lines)

    return translate_lines


# takes the .txt file stream and returns a list of lines
# inputs
# txt_file - .txt filestream
# outputs
# txt_lines - list of lines
def txt_get_lines(lines):
    raw_string = "".join(lines)
    lines = raw_string.split("\n\n")
    txt_lines = [line.strip().replace("\n","\\N") for line in lines]
    return txt_lines


# takes the .srt file stream and returns a list of lines
# inputs
# srt_file - .srt filestream
# outputs
# srt_lines - list of lines
def srt_get_lines(lines):
    raw_string = "".join(lines)
    lines = raw_string.split("\n\n")
    txt_lines = ["\\N".join(line.split('\n')[2:])
                 for line in lines if line != '']
    return txt_lines


# for each line, does the following:
# 0. find all ass tags in original line {\...}
# 1. extract subtitle info
# 2. replace the non tag string with translate_string
# inputs
# original_line - line from original .ass file
# translate_line - line from translated .txt/.srt file
# outputs
# replaced_line - line with preserved ass tags but replaced text
def swap_lines(original_line, translate_line):
    # regex pattern to match ass tags
    regex = "{.*?}"
    # find all tags
    tags = re.findall(regex, original_line)
    # extract subtitle info 'Dialog: 0,...'
    pretext = re.split(regex, original_line)[0]
    # return line with tags preserved
    return pretext + "".join(tags) + translate_line + "\n"


# writes to a new file with the new replaced lines
# the filename will be 'original_filename' + '_replaced.ass'
# inputs
# original_filename - name of the original file
# lines - lines to be written to file
# outputs
# replaced_filename - name of the file with replaced lines
def write_output_file(file_name, lines):
    output_file = open(file_name, mode="w+", encoding='utf-8')
    output_file.writelines(lines)
    output_file.close()
    return


# checks the file type to be
# the one specified
# inputs
# file_path - path of the file
# type - file type
# outputs
# void (exits if check fails)
def verify_file_type(file_path, type):
    if not file_path.endswith(type):
        print("Unknown file type for " + file_path)
        print("Exiting...")
        return False
    return True

# GUI execution


def translate_files(original_file_name, translate_file_name, output_file_name):
    # obtain lines
    _, headers, original_lines = open_original(original_file_name)
    translate_lines = open_translate(translate_file_name)

    # swap lines
    replace_lines = original_lines.copy()
    for i in range(min(len(original_lines), len(translate_lines))):
        replace_lines[i] = swap_lines(original_lines[i], translate_lines[i])

    # write to file
    write_output_file(output_file_name, headers + replace_lines)

    return


# command line execution
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python3 " + sys.argv[0] + " input_file.ass output_file.[txt/srt]")
        sys.exit()

    # file paths
    original_file_path = sys.argv[1]
    translate_file_path = sys.argv[2]

    # check file types
    if not (verify_file_type(original_file_path, ".ass") or verify_file_type(translate_file_path, (".txt", ".srt"))):
        sys.exit()

    # obtain lines
    file_name, headers, original_lines = open_original(original_file_path)
    translate_lines = open_translate(translate_file_path)

    # swap lines
    replace_lines = original_lines.copy()
    for i in range(min(len(original_lines), len(translate_lines))):
        replace_lines[i] = swap_lines(original_lines[i], translate_lines[i])

    # write to file
    write_output_file(file_name + "_modified.ass", headers + replace_lines)
