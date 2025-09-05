---
title: 'Glass Properties Calculator: An open-source tool for glass formulation and property estimation'
tags:
  - Python
  - Glass Science
  - Optical Properties
  - Materials Science
authors:
  - name: "Dr. Madhu A"
    orcid: 0000-000X-XXXX-XXXX
    affiliation: 1
  - name: "Nikhita Thupakula"
    orcid: 0000-000Y-YYYY-YYYY
    affiliation: 2
  - name: "Samarth BC"
    orcid: 0000-000Z-ZZZZ-ZZZZ
    affiliation: 3
  - name: "Dhruthi G P"
    orcid: 0000-000A-AAAA-AAAA
    affiliation: 4
  - name: "Kanishk Singh"
    orcid: 0000-000B-BBBB-BBBB
    affiliation: 5
  - name: "Harni R"
    orcid: 0000-000B-BBBB-BBBB
    affiliation: 6
affiliations:
 - name: Department of Physics, [Dayananda Sagar College of Engineering], Bangalore, India
   index: 1
 - name: Department of Computer Science Engineering(Cybersecurity), [Dayananda Sagar College of Engineering], Bangalore, India
   index: 2
 - name: Department of Computer Science Engineering(Cybersecurity), [Dayananda Sagar College of Engineering], Bangalore, India
   index: 3
 - name: Department of Computer Science Engineering(Cybersecurity), [Dayananda Sagar College of Engineering], Bangalore, India
   index: 4
 - name: Computer Science Engineering(Cybersecurity), [Dayananda Sagar College of Engineering], Bangalore, India
   index: 5
  -name: Computer Science Engineering(Data Science), [Dayananda Sagar College of Engineering], Bangalore, India
   index: 6
date: 5 September 2025
bibliography: paper.bib
---

# Summary

Glass formulation requires calculations of raw material proportions and expected physical and optical properties. Manual calculations are often tedious and prone to errors.  
**Glass Properties Calculator** is an open-source Python application that enables users to input relevant data, such as the Batch Equation and Weight, producing detailed outputs. Its straightforward design allows for easy resetting and repetition of calculations, making it an essential tool for accurate glass composition analysis and production. 

The software is available both as Python source code and as a standalone Windows executable, making it accessible to researchers and students without programming expertise.

# Statement of need
For the manufacture of Glass, accurate and precise calculations of ratios of raw materials is very important. Manual computation is very time-consuming and error-prone. Small errors in the ratio calculations can lead to significant changes in the properties of glass.

Existing tools are either too closed-source require programming skills for use. **Glass Properties Calculator** is an open-source easy to use software designed to fill this gap. The app also calculates the physical and oprical properties of the glass for given ratios to help decide on the raw materials.

# Functionality

Inputs:
- Batch equation (coefficients summing to 100)  
- Batch weight  
- Glass density  
- Refractive index  
- Optional: coordination numbers of oxides  

Outputs:
- Raw and derived masses of compounds  
- Weight fractions and gravimetric factors  
- Molar volume, metal-metal separations, packing density, oxygen packing density  
- Average coordination number and bonds per unit volume  
- Rare-earth element effects  
- Optical properties: polarizability, dielectric constants, and optical basicity  

Implementation:
- Developed in Python using `Tkinter` (GUI) and `Chempy` (chemical computations).  
- Distributed as both source code and a precompiled `.exe`.  
- Accessible at: [Batch Calculator Website](https://batch-calculator.vercel.app/).  

# Figures

![Flow chart of the estimation procedure.\label{fig:flowchart}](flowchart.jpg){ width=60% }

# Acknowledgements

We thank our colleagues and institutions who supported the development of this tool. Funding sources (if any) should be acknowledged here.
