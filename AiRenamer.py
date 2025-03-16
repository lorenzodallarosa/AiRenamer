import os
import re
from langchain_ollama import OllamaLLM as OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
 

def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def rename_files(folder_path, old_filenames, new_filenames):
    """Renames files based on the mapping of old_filenames to new_filenames."""
    if len(old_filenames) != len(new_filenames):
        raise ValueError("The number of old filenames and new filenames must be the same.")
    
    for old_name, new_name in zip(old_filenames, new_filenames):
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f'Renamed: {old_name} -> {new_name}')
        else:
            print(f'File not found: {old_name}')

template = """
You are given a single filename: "{old_name}"
Do not use python nor RE, just return the file name
**Your task:**  
Rename this file using **this exact format**:  
  **YYYY-MM-DD.extension**  
  - `YYYY-MM-DD`: The date of the recording, with dashes.
  - `extension`: Keep the original file extension, always **preceded by a dot (`.`)**.  

**Rules:**  
1. **Strictly follow the naming template.**  
2. **Return only the new filename as a single string. No explanations, no extra words.**  
3. Ignore extra details like 'Recovery', 'General', 'Recording','lezione' or random numbers or word that do not fit the template.  
4. If the filename is already correctly formatted, return it as is.
5. Do not add any _specifier at the end of the date
6. If the date is written in words convert it to numbers.

### **Example Input & Output**
#### **Input:**  
`ADSA lecture (Recovery 1) - 20211220_105606-Registrazione della riunione.mp4`  
#### **Output:**  
`2021-12-20_1.mp4`
#### **Input:**  
`Riunione in _General_-20211202_103707-Registrazione della riunione.mp4` 
#### **Output:**  
`2021-12-02.mp4`
#### **Input:**
`lezione2020-12-19p1_.mp4`
#### **Output:**
`2020-12-19.mp4`
#### **Input:**
`Space propulsion  Lezione  13  dicembre  2020`
#### **Output:**
`2020-12-13`

"""

model = OllamaLLM(model="gemma3:4b", device="cuda")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model



def list_files(directory):
    """Returns a list of filenames in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def rename_files(folder_path, old_filenames, new_filenames):
    """Renames files based on the mapping of old_filenames to new_filenames."""
    if len(old_filenames) != len(new_filenames):
        raise ValueError("The number of old filenames and new filenames must be the same.")
    
    for old_name, new_name in zip(old_filenames, new_filenames):
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f'Renamed: {old_name} -> {new_name}')
        else:
            print(f'File not found: {old_name}')

if __name__ == "__main__":
    directory_path = input("Paste the path of the directory containing the files: ").strip()
    directory_path = os.path.normpath(directory_path)

    class_name = input("Enter the name of the university class: ").strip().replace(" ", "_")
    old_names = list_files(directory_path)

    new_names = []
    date_count = {}  # Dictionary to track occurrences of each date

    for old_name in old_names:
        new_name = chain.invoke({"old_name": old_name}).strip()

        # Extract date and extension
        date_part, ext = os.path.splitext(new_name)  # Splits filename into (name, .ext)
        ext = ext.lstrip(".")  # Remove leading dot from extension

        # Check if date_part already has `_X` at the end
        match = re.search(r"_(\d+)$", date_part)  # Looks for "_X" at the end
        if match:
            base_date = date_part[: match.start()]  # Remove the existing numbering
        else:
            base_date = date_part  # No numbering, use as is

        # Track occurrences of the same date
        if base_date in date_count:
            date_count[base_date] += 1
        else:
            date_count[base_date] = 1  # First occurrence

        # Construct the new filename with specifier before extension
        if date_count[base_date] > 1:
            new_name = f"{base_date}_{class_name}_{date_count[base_date]}.{ext}"
        else:
            new_name = f"{base_date}_{class_name}.{ext}"  # No specifier for first occurrence

        new_names.append(new_name)
        print(f"Renamed: {old_name} -> {new_name}")
        # create a  rename csv file with the old name and the new name in the same directory
        with open(os.path.join(directory_path, "rename.csv"), "a") as f:
            f.write(f"{old_name},{new_name}\n")


    rename_files(directory_path, old_names, new_names)


