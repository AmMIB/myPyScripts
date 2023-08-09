#!/usr/bin/env python
# coding: utf-8

# In[20]:


import os


# In[21]:


def remove_files_between(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    files.sort()  # Sort files alphabetically

    if len(files) >= 1:
        # Keep the first and last files, remove the rest
        for file_name in files[1:-1]:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
    else:
        print(f"Not enough files to remove in: {folder_path}")


# In[22]:


def main(root_folder):
    for root, subdir, filenames in os.walk(root_folder):
        folder_name = os.path.basename(root)
        if folder_name=='target':  # To skip the root folder itself
            print(f"Processing folder: {root}")
            remove_files_between(root)


# In[23]:


if __name__ == "__main__":
    root_folder = "D:\jcode"  # Replace with the actual path
    main(root_folder)


# In[ ]:




