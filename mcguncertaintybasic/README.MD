# MCG Uncertainty Basic Add-on Documentation

## Overview

The ``MCGUncertaintyBasic`` add-on is a tool for the non-additive uncertainty system model as in [WiT](https://arxiv.org/pdf/2203.10506.pdf) and [SWiT](https://arxiv.org/abs/2302.07000). It implements an time-varying model, allowing you to simulate additional statistics in the 'scattering' positions over the time. The add-on provides a simple interface to specify the number of keyframes (T) and the standard deviation (sigma) of the noise. You can easily add noise to the object locations for the specified number of keyframes.

## Features

- Add noise to object locations based on a Gaussian noise only for now.
- Control the number of keyframes (T) for the uncertainty simulation.
- Adjust the standard deviation (sigma) to control the magnitude of the noise in x-y-z directions.
- Works with selected objects in the Blender scene.
- Not yet implemented for the rotation of the objects and imported stl files.

 
## Limitations

- The add-on does not support other types of uncertainty models or noise distributions.
- Limited to selectable objects only.


## Installation
To install the MCG Uncertainty Basic add-on in Blender, follow these steps:


1. Download the add-on script (Python file) to your local machine.
2. Open Blender and go to Edit > Preferences.
3. In the Preferences window, click on the "Add-ons" tab.
4. Click the "Install..." button located at the top right of the Preferences window.
5. Locate the downloaded add-on script on your machine and select it.
6. Click the "Install Add-on" button to install the add-on.
7. Once installed, you should see a checkbox next to the add-on name. Make sure the checkbox is checked to enable the add-on.
8. The add-on should now be available in the View3D > Sidebar > MCG Uncertainty Basic.

**Alternatively, if the add-on does not show up in the sidebar after installation, you can run the script directly from the Blender Scripting workspace. Follow these steps:**

1. Open Blender and switch to the Scripting workspace.
2. Click on the "Open" button and locate the add-on script on your machine.
3. Open the add-on script in the Scripting Editor.
4. Press the "Run Script" button or use the shortcut "Alt+P" to run the script.
5. The add-on should now be available in the View3D > Sidebar > MCG Uncertainty Basic category.

Alternatively, if the add-on does not show up in the sidebar after installation, you can run the script directly from the Blender Scripting workspace. Follow these steps:

1. Open Blender and switch to the Scripting workspace.
2. Click on the "Open" button and locate the add-on script on your machine.
3. Open the add-on script in the Scripting Editor.
4. Press the "Run Script" button or use the shortcut "Alt+P" to run the script.
5. The add-on should now be available in the View3D > Sidebar > MCG Uncertainty Basic category.

## Usage
1. Launch Blender and make sure the MCG Uncertainty Basic add-on is installed and enabled.
2. In the View3D editor, find the sidebar panel labeled "MCG Uncertainty Basic."
3. Inside the panel, you will find two properties: "T" and "sigma."
   - "T" represents the number of keyframes for the uncertainty simulation. Adjust this value as desired.
   - "sigma" represents the standard deviation of the Gaussian noise. Higher values result in larger random variations.
4. Set the desired values for "T" and "sigma."
5. Click the "Add Noise" button to add noise to the selected object locations for the specified number of keyframes.
6. The objects' locations will be modified with random variations based on the specified standard deviation.
7. The modified locations will be keyframed at each frame, allowing you to animate the uncertain object positions.


## License
`MCGUncertaintyBasic` is licensed under the MIT [license](LICENSE).

## Check research work
```shell
website: https://artansalihu.com/
```