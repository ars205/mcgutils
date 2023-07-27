## BlendSkp Converter

### Overview
MCG STL to SKP Converter is a SketchUp plugin that allows you to convert STL files generated from, e.g., Blender to SKP files for SketchUp. It simplifies the importing of STL files and saving them in the SketchUp-specific SKP file format.

### Features
- Converts STL files to SKP files within SketchUp.
- Supports batch conversion for all STL files in a selected directory.
- Scales the imported models uniformly size.
- Assigns random materials to the faces of the converted models.
- Provides progress updates during the conversion process.

### Limitations
- STL file format: The plugin is specifically designed to handle STL files and may not work with other file formats.
- Compatibility: The converted SKP files are intended for use within SketchUp. They may not be compatible with other 3D modeling software or applications.
- Geometry complexity: Highly complex or problematic STL files may encounter issues during conversion.
- File size: Each converted SKP file may be larger due to the nature of SketchUp file structure, but this is not specific to the plugin itself. Geometry seems to be intact.

### Installation
1. Download the `MCGconverterSTL2SKP.rbz` plugin file from the <a href="https://owncloud.tuwien.ac.at/index.php/s/uKwHkJSh9lRKuHB" target="_blank"> <span class="normal">TU Owncloud</span> <i style="font-size: 1em; color: #006699;" class="fa-solid fa-download fa-sm"></i> </a>.
2. In SketchUp, go to **Window > Extension Manager**.
3. Click the **Install Extension**.
4. Locate and select the downloaded `MCGconverterSTL2SKP.rbz` file.
5. Follow the prompts to install the plugin.
6. The "MCG - STL to SKP Converter" plugin will be installed and available under the **Extensions** menu.
  
### Usage
1. Open SketchUp and ensure the "MCG - STL to SKP Bulk Converter" plugin is installed and activated.
2. Go to **Extensions > MCG - STL to SKP Bulk Converter** in the SketchUp menu.
3. A dialog box will appear, prompting you to select the directory containing the STL files you want to convert.
4. Choose the desired directory.
5. Another dialog box will appear, asking you to select the directory where you want to save the converted SKP files.
6. Select the desired directory.
7. Another dialog will ask to write three materials to the model.
8. The plugin will automatically convert each STL file in the selected directory to the SKP format.
9. The imported models will be scaled to a uniform size.
10. Random materials will be assigned to the faces of the converted models.
11. The converted SKP files will be saved in the specified SKP directory.
12. Progress updates will be displayed during the conversion process.
13. Once the conversion is complete, you will have the SKP files ready for use within SketchUp.


### License
This plugin is released under the [MIT License](https://opensource.org/licenses/MIT).
