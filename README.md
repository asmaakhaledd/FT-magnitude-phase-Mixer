# FT-magnitude-phase-Mixer
## Table of contents:
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Project Features](#project-features)
- [Getting Started](#getting-started)
- [Team](#team)


### Introduction
A digital signal processing website to mix fourier magnitude and phase of 2 different images in the Fourier domain and display the mixed image in the time domain. 

### Project Structure
The Web Application is built using:
- Frontend:
  - BootStrap
  - HTML
  - CSS
  - JavaScript
- Backend framework:
  - Flask (Python)

The Frontend main function to set the structure of the page and plot the signals and manage
the user interface, while the Backend is responsible for performing signal fft operations.

```
master
├─ images (contians sample images)
├─ static (JS & CSS files)
│  ├─  css
│  └─  js
├─ templates (HTML file)
├─ app.py (Back-End Server)
├─ ImageProcessor.py 
├─ Task 4 pdf (project document)
└─ README.md
```

### Project Features
Website has the following features:
> 1. Ability to open and show two images. For each image, the software should have two displays (one fixed display 
for the image, while the second display can show several components based on a combo-box/drop-menu 
selection of 1) FT Magnitude, 2) FT Phase, 3) FT Real component, 4) FT Imaginary component.

> 2.  The web app should impose that the two images have the same size. i.e. when opening the second image, 
the sw should check it has the same size of the one previously opened. Otherwise, give an error message.

> 3.A mixing panel where an output will be formed based on the mix of two components. Each one of these 
components should be determined from:
a. which image (via a combo or drop-menu). Available images are image 1, and image 2.
b. Which component of the image FT (via a combo or drop-menu). Available components are: Magnitude, 
Phase, Real, Imaginary, uniform magnitude , uniform phase (i.e. all 
phase values are set to 0).
c. the mixing ratio (via a slider ranging from 0 to 100%).

> 4. Based on the mixing panel, an output image should be generated and displayed for the user. There should be 
two available displays, each for one output. The mixing panel should be sending the output to either display Output 1 or 2. The display is determined using a drop-menu in the mixing panel. And the output image should be updated whenever the user makes a change in the mixing options

### Getting Started
To get started with the FT magnitude phase Mixer web app, follow these steps:

1. Clone the repository:
``` 
git clone https://github.com/asmaakhaledd/FT-magnitude-phase-Mixer/.git
``` 
2. Install Python3 from:
``` 
www.python.org/downloads/
```
3. Install the following packages:-
   - Flask
   - scipy
   - numpy
 - Open Project Terminal & Run:
```
pip install -r requirements.txt
```
4. Open the application in your web browser by writing this in your terminal:
```
python app.py
```

### Note
The application has been tested on Google Chrome, Microsoft Edge and Mozilla Firefox web browsers.

### Team
Biomedical Signal Processing (SBEN311) class task created by:

| Team Members                                  
|-------------------------------------------------------
| [Nada Mohamed](https://github.com/NadaAlfowey)
| [Abdulmonem Elsherif](https://github.com/AbdulmonemElsherif)   
| [Asmaa Khalid](https://github.com/asmaakhaledd) 
| [Mariam Gamal](https://github.com/mariamgamal70)
      

     

### Submitted to:
- Dr. Tamer Basha & Eng. Christina Adly
