# Duplicate File Manager
## Description
This is a Python program with a graphical interface to verify, identify, and manage duplicate files in a selected folder. It uses hashing (xxHash) to efficiently detect duplicate files, offering options to move them either automatically or based on the user's selection.
## Features 💡
- **Scan for duplicate files by hash**: The program calculates the hashes (xxHash) of files to identify duplicates.
- **Display duplicates in a paginated list**: Results are displayed with pagination for easier navigation through multiple duplicates.
- **Automatically move duplicate files**: Duplicates can be moved to a subfolder named `duplicados`.
- **Move files based on manual selection**: Users can select specific duplicate files to move to a separate folder.
- **User-friendly graphical interface**: Built with Tkinter to make it easy to use.

## Tech Stack 🚀
- Python 3.x
- Graphical interface created with **Tkinter**
- File management with **os**, **shutil**
- **xxHash** for fast hashing
- Threads for parallel file processing with **multiprocessing.pool.ThreadPool**

## How to Use
1. **Install the required dependencies**: Make sure to have the `xxhash` module installed:
``` bash
   pip install xxhash
```
1. **Run the program**: Execute the Python file:
``` bash
   python duplicate_manager.py
```
1. **Select a folder**: Click on the "Select Folder" button in the interface and choose the folder you want to scan.
2. **Wait for processing**: The program will analyze the files using hashing to detect duplicates and display the results in a paginated interface.
3. **Manage the duplicates**:
    - You can move files automatically to a subfolder named `duplicados`.
    - Or move specific files by marking them manually in the interface.

## Code Structure 🛠
### Key Functions
1. **`calcular_xxhash_completo(file_path)`**: Calculates the full hash of a file using the xxHash algorithm, ensuring efficient duplicate detection.
2. **`obter_data_criacao_pasta(filepath)`**: Gets the creation date of the folder containing the file.

### Primary Class: `AppDuplicados`
The main logic is encapsulated in the `AppDuplicados` class.
**Main Components**:
- **Graphical Interface**:
    - Built with Tkinter, includes a progress bar, navigation buttons, and a selection for duplicate files.

- **Pagination**:
    - The class supports pagination for better handling and viewing of a large number of duplicate files.

- **Action Functions**:
    - Verifying duplicates
    - Automatically moving files
    - Manually moving duplicates based on user selection

**Key Methods**:
- `verificar_duplicados()`: Analyzes the files to detect duplicates.
- `mover_duplicados_por_pasta()`: Automatically moves duplicate files based on the folder creation date.
- `mover_arquivos()`: Moves files manually, as selected by the user.
- `exibir_pagina()`: Displays results in a paginated list.

## Example Execution
Below are the main screens during the program's execution:
1. **Initial Screen**:
    - A button to select the folder for analysis.
    - A progress bar to indicate scanning progress.

2. **Results Screen**: Displays duplicates in a paginated format with checkboxes for easy selection.
3. **Options for Managing Duplicates**:
    - Automatically move duplicates to a specific folder.
    - Move duplicates manually based on user selection.

## Future Improvements ✨
- Add options to delete duplicate files directly from the interface.
- Support for exporting results in CSV or JSON formats.
- Improved recursive analysis with customizable settings.
- Better visual feedback, such as real-time hash processing indicators.

## License 📜
This project is open-source and licensed under the [MIT License]().
Enjoy and make good use of it! 😊
