# -*- coding: utf-8 -*-
"""
Created on Wed May  1 17:30:39 2024

@author: tug03166
"""
import os

def delete_trash(files):
    # gather paths
    path = os.getcwd()
    
    for file in files:
        # Construct the full file path
        file_path = os.path.join(path, file)
        
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"{file} deleted successfully.")
            except Exception as e:
                print(f"Error deleting {file}: {e}")
        else:
            print(f"{file} does not exist.")

'''
# Call the function to delete the files
delete_trash(['clip_copy.tif', 'mask.tif', 'temperature.tif'])
'''