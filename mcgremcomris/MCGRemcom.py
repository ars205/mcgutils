'''
name: MCGRemcom.py
author: Artan Salihu, Le Hao
version: 1.0
status: development
contact: artan.salihuATtuwien.ac.at
website: https://www.artansalihu.com, https://mcg-deep-wrt.netlify.app/deep-wrt/utilities/, https://www.remcom.com
date: 2023-07-25
license: MIT
dependencies: numpy, xml, os, subprocess, re, argparse, sys, time
acknowledgements: Remcom Inc.
description: This script automates the creation of a Wireless InSite study area and setup file for a given model.
                Takes a study area a setup as input and creates a new file with changes to the study area and setup file. It runs the simulation using wibatch.exe and supports command line arguments based on the version of WI.
                For CLI it uses the following arguments:
                    --studyArea: Study area XML file (only valid for X3D model)
                    --setup: Setup file name
                    --wibatchLocation: Location of wibatch.exe
                    --licenseLocation: License location
                    --baseVersion: Base version of WI
                    --TxRxSet: TxRxSet can be PointSet, ArcSet, or GridSet, None, etc.
                    --AntennaType: AntennaType can be LinearDipole, UserDefined, etc.
                    --WaveCarrierFrequency: Change WaveCarrierFrequency values in Hz, e.g., 25000000, 30000000, 35000000
                    --CarrierFrequencyTx: Change CarrierFrequencyTx values in Hz, e.g., 25000000, 30000000, 35000000
                    --CarrierFrequencyRx: Change CarrierFrequencyRx values in Hz, e.g., 25000000, 30000000, 35000000
                    --spacingValues: Change spacing values in meters, e.g., 1, 2, 3, 4. Useful for ArcSet, or GridSet. Not useful for PointSet.
                    --RISPatternRX: Change RIS Pattern files for RX from BS in a list, e.g., ["RISPatternRX_1", "RISPatternRX_2", "RISPatternRX_3"]
                    --RISPatternTX: Change RIS Pattern files for TX from BS in a list, e.g., ["RISPatternTX_1", "RISPatternTX_2", "RISPatternTX_3"]
                    --help_options: Print options

                Example for CLI:
                    python MCGRemcom.py --studyArea 03_Automate_WIS.Study_Zero.xml --setup 03_Automate_WIS.setup --wibatchLocation "C:\Program Files\Remcom\Wireless InSite 3.3.5\bin\calc\wibatch.exe" --licenseLocation 111@1.1.2.3 --baseVersion 3.3.3.5 ---RISPatternRX ["RISPatternRX_1", "RISPatternRX_2", "RISPatternRX_3"] --RISPatternTX ["RISPatternTX_1", "RISPatternTX_2", "RISPatternTX_3"] --help_options
'''
import re
import xml.etree.ElementTree as ET
import os
import subprocess
from pkg_resources import parse_version
import argparse
import sys
import time

class RegexContainer:
    """
    Create a class to hold all of the regexes for the script
    """
    def __init__(self):
        self.objectFilenameRegex = re.compile(r'begin_<object> ')
        self.objectVertexRegex = re.compile(r'^-?\d*\.?\d*\s-?\d*\.?\d*\s-?\d*\.?\d*')
        self.objectSectionRegex = re.compile(r"begin_<feature>.*?end_<feature>", re.DOTALL)
        self.objectPlacementRegex = re.compile(r"(end_<feature>)\n(begin_<txrx_sets>)", re.DOTALL)
        self.studyAreaPlacementRegex = re.compile(r"(end_<studyarea>)\n(begin_<feature>)")
        self.studyAreaSectionRegex = re.compile(r"begin_<studyarea>.*?end_<studyarea>", re.DOTALL)
        self.studyAreaPrefixRegex = re.compile(r"remcom::rxapi::", re.DOTALL)
        self.studyAreaRevertRegex =re.compile(r"SCRIPTPLACEHOLDER", re.DOTALL)

def check_version(editedStudyArea, baseVersion="3.3.5.6"):
    '''
    Check the version of the software to see if we need to specify the license

    Parameters
    ----------
    editedStudyArea : str
        The study area XML file as a string
    baseVersion : str, optional
        The base version of WI to compare against. The default is 3.3.5.6"
    Returns
    -------
    newVersion : bool
        True if the version is greater than or equal to the base version    
    '''
    version = re.search('(version=\")(.{7})(\")',editedStudyArea) # If verion 3.4.4.11 then  parse {8} instead of {7}
    newVersion = parse_version(version[2]) >= parse_version(baseVersion)
    return newVersion

def run_simulation_study(newVersion, wibatchLocation, licenseLocation, initialStudyAreaPath, newStudyArea, studyAreaFilenameSplit):
    '''
    Run the simulation using wibatch.exe and the appropriate command line arguments based on the version of WI.
    '''
    #run simulation
    wibatch = "wibatch.exe"
    #run initial simulation first time through
    if i == 1:
        cmdFileInput = " -f " + (f'"{initialStudyAreaPath}"')
        cmdFileOutput = " -out " + (f'"{studyAreaFilenameSplit[1]}"')
        if newVersion:
            cmdFileLicense = " -set_licenses " + licenseLocation
            commandLine = wibatch + cmdFileInput + cmdFileOutput + cmdFileLicense
        else:
            commandLine = wibatch + cmdFileInput + cmdFileOutput
            print("Running initial position simulation")
            print(commandLine)
            subprocess.run(commandLine, executable=wibatchLocation)
    newStudyAreaNameSplit = newStudyArea.name.split(".")
    cmdFileInput = " -f " + (f'"{newStudyArea.name}"')
    cmdFileOutput = " -out " + (f'"{newStudyAreaNameSplit[1]}"')
    if newVersion:
        cmdFileLicense = " -set_licenses " + licenseLocation
        commandLine = wibatch + cmdFileInput + cmdFileOutput + cmdFileLicense
    else:
        commandLine = wibatch + cmdFileInput + cmdFileOutput
    print(commandLine)
    subprocess.run(commandLine, executable=wibatchLocation)
    

# Create a method for defining regexes below:
if __name__ == "__main__":
        # Define Arguments
    parser = argparse.ArgumentParser(description='Automate WIS Study - MCG-Remcom - www.artansalihu.com')
    parser.add_argument('--studyArea', default="RIS_Remcom_Le.RIS_Remcom_Le_Zero.xml", help='Study area XML file (only valid for X3D model)')
    parser.add_argument('--setup', default="RIS_Remcom_Le.setup", help='Setup file name')
    parser.add_argument('--wibatchLocation', default=r"C:\Program Files\Remcom\Wireless InSite 3.3.5\bin\calc\wibatch.exe",help='Location of wibatch.exe')
    parser.add_argument('--licenseLocation', default=r"111@1.2.3.4", help='License location')
    parser.add_argument('--baseVersion', default="3.3.5.6", help='Base version of WI')
    parser.add_argument('--TxRxSet', default="ArcSet", help='TxRxSet can be PointSet, ArcSet, or GridSet, None, etc.')
    parser.add_argument('--AntennaType', default="HalfWaveDipole", help='AntennaType can be LinearDipole, UserDefined, HalfWaveDipole, etc.')
    parser.add_argument('--WaveCarrierFrequency',  nargs='+', type=int, default=None, help='Change WaveCarrierFrequency values in Hz, e.g., 25000000, 30000000, 35000000')
    parser.add_argument('--CarrierFrequencyTx',  nargs='+', type=int, default=None, help='Change CarrierFrequencyTx values in Hz, e.g., 25000000, 30000000, 35000000')
    parser.add_argument('--CarrierFrequencyRx',  nargs='+', type=int, default=None, help='Change CarrierFrequencyRx values in Hz, e.g., 25000000, 30000000, 35000000')
    parser.add_argument('--spacingValues', nargs='+', type=int, default=None, help='Change spacing values in meters, e.g., 1, 2, 3, 4. Useful for ArcSet, or GridSet. Not useful for PointSet.')
    parser.add_argument('--RISPatternsRX', nargs='+', type=str, default=None, help='List of RIS RX File Patterns converted from MCGst2UanConverter.py')
    parser.add_argument('--RISPatternsTX', nargs='+', type=str, default=['HalfWaveDipoleTest'], help='List of RIS TX File Patterns converted from MCGst2UanConverter.py')
    


    parser.add_argument('--help_options', action='store_true', help='Print options')
    # Parse the arguments
    args = parser.parse_args()
    # Print the available options if requested
    if args.help_options:
        parser.print_help()
        sys.exit()
    # if args.verbose:
    #     print("Verbose enabled")
    # Run the main function with the arguments    
    start_time = time.time() 

    # Use arguments
    studyArea = args.studyArea
    setup = args.setup
    wibatchLocation = args.wibatchLocation
    licenseLocation = args.licenseLocation
    baseVersion = args.baseVersion
    TxRxSet = args.TxRxSet
    AntennaType = args.AntennaType
    WaveCarrierFrequency = args.WaveCarrierFrequency
    CarrierFrequencyTx = args.CarrierFrequencyTx
    CarrierFrequencyRx = args.CarrierFrequencyRx
    spacingValues = args.spacingValues
    RISPatternsRX = args.RISPatternsRX
    RISPatternsTX = args.RISPatternsTX

    # Create a help message for the user for arguments
    helpMessage = "Running script with the following arguments:\n"
    helpMessage += "Study Area: " + studyArea + "\n"
    helpMessage += "Setup File: " + setup + "\n"
    helpMessage += "Wibatch Location: " + wibatchLocation + "\n"
    helpMessage += "License Location: " + licenseLocation + "\n"
    helpMessage += "Spacing Values: " + str(spacingValues) + "\n"
    helpMessage += "Base Version: " + baseVersion + "\n"
    helpMessage += "TxRxSet: " + TxRxSet + "\n"
    helpMessage += "AntennaType: " + AntennaType + "\n"
    helpMessage += "WaveCarrierFrequency: " + str(WaveCarrierFrequency) + "\n"
    helpMessage += "CarrierFrequencyTx: " + str(CarrierFrequencyTx) + "\n"
    helpMessage += "CarrierFrequencyRx: " + str(CarrierFrequencyRx) + "\n"
    helpMessage += "RISPatterns: " + str(RISPatternsRX) + "\n"
    helpMessage += "RISPatterns: " + str(RISPatternsTX) + "\n"
    
    print(helpMessage)

    # Gather all of your lists into a larger list
    all_lists = [spacingValues, WaveCarrierFrequency,RISPatternsRX,RISPatternsTX]  # add any additional lists here

    # Determine the maximum length among all lists
    max_len_changes = max(len(lst) for lst in all_lists if lst is not None)

    # Create regexes object
    regexes = RegexContainer()

    # Define variables for the loop
    studyAreaFilepath = os.path.basename(studyArea)
    studyAreaFilepathSplit = os.path.splitext(studyArea)
    studyAreaFilenameSplit = studyAreaFilepath.split(".")

    setupFilepath = os.path.basename(setup)
    setupFilepathSplit = os.path.splitext(setup)
    setupFilenameSplit = setupFilepath.split(".")
    newSetupFile = setupFilenameSplit[0] + "_ARTAN." + setupFilenameSplit[1]

    newSetupFilenameSplit = newSetupFile.split(".")
    newSetupFilename = newSetupFilenameSplit[0]
    #clear the contents of an existing .setup file created by the script
    open(newSetupFile, 'w+').close()

    studyAreaContent = open(studyArea, 'r')  # Explicitly mentioning the mode of opening can sometimes help
    #use a regex on the xml so that it is suitable for parsing using ETree
    editedStudyArea = ''    
    for line in studyAreaContent:
        editedStudyArea += regexes.studyAreaPrefixRegex.sub("SCRIPTPLACEHOLDER", line)
        #print(editedStudyArea)
    studyAreaContent.close() 

    # Check version
    newVersion = check_version(editedStudyArea, baseVersion=baseVersion)
    print("Running on version " + str(newVersion))

    studyAreaContent = open(studyArea)
    #use a regex on the xml so that it is suitable for parsing using ETree
    editedStudyArea = ''    
    for line in studyAreaContent:
        editedStudyArea += regexes.studyAreaPrefixRegex.sub("SCRIPTPLACEHOLDER", line, re.MULTILINE)
        #print(editedStudyArea)

    #create a copy of the original and modify it so we can view the results in the new setup file
    tree = ET.fromstring(editedStudyArea)       
    #convert the xml to a string to be parsed
    treeString = ET.tostring(tree, encoding='unicode', method='xml')
    #undo the modifications to the xml so that it is a valid WI study area again
    editedTreeString = ""
    editedTreeString += regexes.studyAreaRevertRegex.sub("remcom::rxapi::", treeString)
    newStudyAreaPath = newSetupFilename + "." + studyAreaFilenameSplit[1] + studyAreaFilepathSplit[1]
    initialStudyAreaPath = newStudyAreaPath
    newStudyArea = open(newStudyAreaPath, "w")
    newStudyArea.write(editedTreeString)
    newStudyArea.close()    

    with open(setup) as f:
        setupContent = f.read()

    fileIndex = 1
    displayIndex = 2
    i=0

    # Loop through spacing values
    for i in range(max_len_changes):
        tree = ET.fromstring(editedStudyArea)
        for elementOutputLocation in tree.find("SCRIPTPLACEHOLDERJob/OutputLocation"):
            elementOutputLocation.set("Value", elementOutputLocation.get("Value") + " " + str(displayIndex))
        for elementOutputPrefix in tree.find("SCRIPTPLACEHOLDERJob/OutputPrefix"):
            elementOutputPrefix.set("Value",newSetupFilename)
        for elementDatabaseLocation in tree.find("SCRIPTPLACEHOLDERJob/PathResultsDatabase/SCRIPTPLACEHOLDERPathResultsDatabase/Filename/SCRIPTPLACEHOLDERFileDescription/Filename"):
            elementDatabaseLocation.set("Value", "./" + elementOutputLocation.get("Value")+ "/" + elementOutputPrefix.get("Value") + "." + elementOutputLocation.get("Value") + ".sqlite")   
            print(elementDatabaseLocation.get("Value"), elementOutputLocation.get("Value"), elementOutputPrefix.get("Value"))
        
        if spacingValues is not None:
            for elementSpacingValue in tree.find(f"SCRIPTPLACEHOLDERJob/Scene/SCRIPTPLACEHOLDERScene/TxRxSetList/SCRIPTPLACEHOLDERTxRxSetList/TxRxSet/SCRIPTPLACEHOLDER{TxRxSet}/Spacing"):
                elementSpacingValue.set("Value", str(spacingValues[i]))              

        if WaveCarrierFrequency is not None:
            for elementCarrierValue in tree.find(f"SCRIPTPLACEHOLDERJob/Scene/SCRIPTPLACEHOLDERScene/AntennaList/SCRIPTPLACEHOLDERAntennaList/Antenna/SCRIPTPLACEHOLDER{AntennaType}/Waveform/SCRIPTPLACEHOLDERSinusoid/CarrierFrequency"):
                elementCarrierValue.set("Value", str(WaveCarrierFrequency[i]))   
                print('Frequency Carrier Value: ',elementCarrierValue.get("Value"))  

        if CarrierFrequencyTx is not None:
            for elementCarrierValueTx in tree.find(f"SCRIPTPLACEHOLDERJob/Scene/SCRIPTPLACEHOLDERScene/TxRxSetList/SCRIPTPLACEHOLDERTxRxSetList/TxRxSet/SCRIPTPLACEHOLDERPointSet/Transmitter/SCRIPTPLACEHOLDERTransmitter/Antenna/SCRIPTPLACEHOLDER{AntennaType}/Waveform/SCRIPTPLACEHOLDERSinusoid/CarrierFrequency"):
                print('Frequency Carrier Value of Tx: ',elementCarrierValueTx.get("Value"))
                elementCarrierValueTx.set("Value", str(CarrierFrequencyTx[i]))

        if RISPatternsRX is not None:
            # for elementRISPatternRX in tree.find(f"SCRIPTPLACEHOLDERJob/Scene/SCRIPTPLACEHOLDERScene/AntennaList/SCRIPTPLACEHOLDERAntennaList/Antenna/SCRIPTPLACEHOLDERUserDefinedAntenna/Filename/SCRIPTPLACEHOLDERFileDescription/Filename"):
            #     elementRISPatternRX.set("Value", "./"+RISPatternsRX[i] + ".uan")
            #     print('RIS Pattern Value: ',elementRISPatternRX.get("Value"))
            for elementRISPatternReceiver in tree.find(f"SCRIPTPLACEHOLDERJob/Scene/SCRIPTPLACEHOLDERScene/TxRxSetList/SCRIPTPLACEHOLDERTxRxSetList/TxRxSet/SCRIPTPLACEHOLDERPointSet/Receiver/SCRIPTPLACEHOLDERReceiver/Antenna/SCRIPTPLACEHOLDERUserDefinedAntenna/Filename/SCRIPTPLACEHOLDERFileDescription/Filename"):
                print('RIS Pattern Value of RX: ',elementRISPatternReceiver.get("Value"))
                elementRISPatternReceiver.set("Value", "./"+RISPatternsRX[i] + ".uan")
                print('RIS Pattern Value of RX: ',elementRISPatternReceiver.get("Value"))

            
        if RISPatternsTX is not None:
            for elementRISPatternTransmitter in tree.find(f"SCRIPTPLACEHOLDERJob/Scene/SCRIPTPLACEHOLDERScene/TxRxSetList/SCRIPTPLACEHOLDERTxRxSetList/TxRxSet/SCRIPTPLACEHOLDERPointSet/Transmitter/SCRIPTPLACEHOLDERTransmitter/Antenna/SCRIPTPLACEHOLDERUserDefinedAntenna/Filename/SCRIPTPLACEHOLDERFileDescription/Filename"):
                print('RIS Pattern Value of Tx: ',elementRISPatternTransmitter.get("Value"))
                elementRISPatternTransmitter.set("Value", "./"+RISPatternsTX[i] + ".uan")
                print('RIS Pattern Value of Tx: ',elementRISPatternTransmitter.get("Value"))

              

        #modify .setup to add the new study area to the project
        #duplicate existing study area and increment index
        setupContent = re.sub(r"FirstAvailableStudyAreaNumber.+", "FirstAvailableStudyAreaNumber " + str(fileIndex), setupContent)
        match = regexes.studyAreaSectionRegex.search(setupContent)
        studyAreaMatch = "\n"+match.group(0)+"\n"
        studyAreaMatch = re.sub(r"(begin_<studyarea>.+)", r"\g<0> " + str(displayIndex), studyAreaMatch)
        studyAreaMatch = re.sub(r"(StudyAreaNumber\s)(\d+)", r"StudyAreaNumber " + str(fileIndex), studyAreaMatch)
        #insert new study area after the last one in the file
        for studyAreaPlacementBounds in regexes.studyAreaPlacementRegex.finditer(setupContent):
            studyAreaMatchTop, studyAreaMatchBottom = studyAreaPlacementBounds.groups()
        setupContent = regexes.studyAreaPlacementRegex.sub(studyAreaMatchTop + studyAreaMatch + studyAreaMatchBottom, setupContent)        

        #convert the xml to a string to be parsed
        treestring = ET.tostring(tree, encoding='unicode', method='xml')
        #undo the modifications to the xml so that it is a valid WI study area again
        editedTreestring = ""
        editedTreestring += regexes.studyAreaRevertRegex.sub("remcom::rxapi::", treestring)
        #save the new study area to a new file
        newStudyAreaPath = newSetupFilename + "." + studyAreaFilenameSplit[1] + " " + str(displayIndex) + studyAreaFilepathSplit[1]
        newStudyArea = open(newStudyAreaPath, "w")
        newStudyArea.write(editedTreestring)
        newStudyArea.close()
        i += 1
        fileIndex += 1
        displayIndex += 1
        #delete any existing cache files to prevent them from being used.
        projectFiles = os.listdir(os.getcwd())
        for file in projectFiles:
            if file.endswith(".cache"):
                os.remove(file)
        
        # Run simulation
        run_simulation_study(newVersion, wibatchLocation, licenseLocation, initialStudyAreaPath, newStudyArea, studyAreaFilenameSplit)

    #modified setup file
    outSetup = open(newSetupFile,'w')
    #print(setupContent)
    outSetup.writelines(setupContent)
    outSetup.close()
    print("Created new setup file " + newSetupFile)
    
    print("--- %s seconds ---" % (time.time() - start_time))