## MCG OSM Load Helper

### Overview
MCG OSM Load Helper is a SketchUp plugin that allows you to load OpenStreetMap (OSM) building data into SketchUp. It aims to reduce the initial time setup of importing building footprints and rendering them into 3D models within SketchUp.

### Features
- Fetches OSM data from the OpenStreetMap API.
- Imports building footprints as polygons into SketchUp.
- Extrudes the polygons to create 3D building models (meshed objects).
- Adjusts the orientation of the buildings based on their surface.

### Limitations
- Only buildings and polygons are loaded: The plugin focuses on loading buildings and polygons from OSM data. Other features like roads, vegetation, or points of interest are not imported.
- Scaling and conversion: The plugin assumes a default scale for the imported data and may not accurately represent real-world measurements. Users should consider adjusting the imported geometry to match the desired scale and units.
- Roofs: The plugin currently does not generate roof geometry. It extrudes the building footprints vertically, resulting in flat-topped structures. Users may need to manually add roofs or modify the models as needed.
- Materials: The plugin does not assign materials to the imported buildings. Users can apply materials manually within SketchUp to enhance the visual appearance.

### Installation
<!-- 1. Download the MCG OSM Load Helper plugin (`MCG3DBuildingHelper`) from the [TU Owncloud](https://owncloud.tuwien.ac.at/index.php/s/SdgyoyhJIfMFry6). -->
1. Download the MCG OSM Load Helper plugin (`MCG3DBuildingHelper`) from the <a href="https://owncloud.tuwien.ac.at/index.php/s/SdgyoyhJIfMFry6" target="_blank"> <span class="normal">TU Owncloud</span> <i style="font-size: 1em; color: #006699;" class="fa-solid fa-download fa-sm"></i> </a>.
2. In SketchUp, go to **Window > Extension Manager**.
3. Click the **Install Extension** button.
4. Locate and select the downloaded `MCG3DBuildingHelper.rbz`.
5. Follow the prompts to install the plugin.
6. The MCG OSM Load Helper plugin will appear under the **Plugins** menu.

### Usage
To use the MCG OSM Load Helper plugin, follow these steps:
1. Open SketchUp and your project.
2. Use the SketchUp viewport to navigate to the area you want to work on.
3. From the menu, select **Plugins > MCG OSM Load Helper**.
4. The plugin will retrieve OSM data from the OpenStreetMap API based on your current location in the viewport.
5. SketchUp will import building footprints as polygons, representing building outlines.
6. You can extrude the polygons to create 3D models of buildings. Adjust the extrusion height as desired.
7. Make any necessary changes or additions to the imported buildings.
8. Add materials and textures to improve your models.


<!-- ### Support and Contributions
- For support or to report issues, please visit the [repository](https://github.com/your-plugin-repository) and create a new issue. -->

### License
This plugin is released under the [MIT License](https://opensource.org/licenses/MIT).