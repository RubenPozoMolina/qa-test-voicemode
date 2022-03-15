import os
import glob


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
