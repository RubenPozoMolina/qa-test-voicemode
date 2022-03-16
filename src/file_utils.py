import os
import glob
import filecmp


class FileUtils:

    @staticmethod
    def file_exists(directory, pattern):
        return_value = False
        file_list = glob.glob(directory + os.path.sep + pattern)
        if len(file_list) > 0:
            return_value = True
        return return_value

    @staticmethod
    def delete_files(directory, pattern):
        file_list = glob.glob(directory + os.path.sep + pattern)
        for f in file_list:
            os.remove(f)

    @staticmethod
    def are_file_equals(file1, file2):
        return filecmp.cmp(file1, file2, shallow=True)

