#!/usr/bin/python

from subprocess import call
import sys
import os
import pipes

video_files = [".avi", ".mkv", ".m4v", ".wmv", ".mp4"]
acceptable_files = [".avi", ".mkv", ".m4v", ".wmv"]

# return a list of all files in a directory (and sub-directories)
def list_files(directory):
    file_list = []
    for root,dirs,files in os.walk(directory):
        for file in files:
            if (len(root+"/"+file) > 0):
                file_list.append(root+"/"+file)
    return file_list

# find the largest file (by size) with acceptable extensions from a list of files
def find_largest(files):
    f_largest = ""
    f_largest_size = -1
    for f in files:
        size = os.path.getsize(f)
        ext = os.path.splitext(f)[1]
        if (size > f_largest_size and ext in video_files):
            f_largest_size = size
            f_largest = f
    return f_largest

# handle the file conversion
def convert(f):
    ext = os.path.splitext(f)[1]
    if (ext in acceptable_files):
        call(["HandBrakeCLI", "-i", f, "-o", "/var/www/files/movies/"+os.path.splitext(os.path.basename(f))[0]+".mp4"])
    else:
        print("copying file "+f)
        # nothing to convert, just copy the file
        call(["cp", f, "/var/www/files/movies/"+os.path.basename(f)])

t_dir = sys.argv[1]
t_name = sys.argv[2]
t_id = sys.argv[3]
t_abs = t_dir+t_name

# remove deleted torrent
call(["transmission-remote", "-t", t_id, "--remove"])

if (os.path.isfile(t_abs)):
    convert(t_abs)
elif (os.path.isdir(t_abs)):
    f = find_largest(list_files(t_abs))
    convert(f)
else:
    print("param is neither file nor directory")
