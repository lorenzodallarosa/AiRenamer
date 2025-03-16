# AiRenamer

**AI-powered University Lectures Recordings Renamer**

AiRenamer is designed to automatically standardize lecture recording filenames from various platforms into a unified format: `YYYY-MM-DD_lecture-id`. This ensures chronological ordering of files within the filesystem.

Powered by **Gemma3:4b** running on **Ollama**, AiRenamer handles various date formats (including spelled-out dates) and supports multiple lectures recorded on the same date. The script also generates a backup file that maps old filenames to new ones and includes a recovery script for easy restoration.

## Features
- **Automatic renaming**: Converts diverse filename formats into a structured format.
- **Multi-date handling**: Recognizes different date formats and multiple lectures per day.
- **Backup & Recovery**: Generates a backup file with the old-new name mapping and a recovery script for easy rollback.
- **AI-Powered Processing**: Utilizes **Gemma3:4b** with **Ollama** to parse and extract relevant information from filenames.

## Setup

1. **Install Ollama**: Download and install it from [Ollama's website](https://ollama.com/).
2. **Download the AI model**: Run the command below to install **Gemma3:4b**:
   ```sh
   ollama pull gemma3:4b
   ```
3. **Install dependencies**:
   ```sh
   pip install langchain langchain-ollama ollama
   ```

## Usage

Run the script and follow the on-screen instructions:
```sh
python AiRenamer.py
```
If the renaming process fails, no changes will be made to your files.

To revert to the original filenames, simply run:
```sh
python recovery.py
```

## Examples

| Original Filename | Renamed Filename |
|------------------|-----------------|
| `TEST lecture (Recovery 1) - 20211220_105606-Meeting Recording.mp4` | `2021-12-20_TEST.mp4` |
| `Meeting in _General_-20210316_083814-Enregistrement de la réunion.mp4` | `2021-03-16_RP.mp4` |
| `Space propulsion  Lezione  13  dicembre  2020.mp4` | `2020-12-13_space_propulsion.mp4` |

---

