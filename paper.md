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
affiliations:
 - name: Department of Physics, [Your University], City, Country
   index: 1
 - name: Department of Materials Science, [Your University], City, Country
   index: 2
 - name: Department of Chemistry, [Your University], City, Country
   index: 3
 - name: Department of Applied Physics, [Your University], City, Country
   index: 4
 - name: School of Engineering, [Your University], City, Country
   index: 5
date: 5 September 2025
bibliography: paper.bib
---

# Summary

Glass formulation requires precise calculations of raw material proportions and derived physical and optical properties. Manual computation is often error-prone and time-consuming.  
**Glass Properties Calculator** is an open-source Python application that simplifies this process. It provides an intuitive interface to compute raw material ratios, weight fractions, gravimetric factors, molar volume, packing density, oxygen packing density, dielectric constants, and rare-earth element effects.  

The software is available both as Python source code and as a standalone Windows executable, making it accessible to researchers and students without programming expertise.

# Statement of need

Accurate design of glass compositions is crucial for research in materials science and photonics. Small errors in composition can significantly affect physical and optical behavior. Traditional methods rely on lengthy manual calculations or closed-source commercial tools, which limits reproducibility and accessibility.  

The **Glass Properties Calculator** addresses this gap by offering a free, open-source, cross-platform solution. With minimal inputs (batch equation, density, refractive index, and optional coordination numbers), the tool generates multiple derived properties for analysis. This improves reproducibility, reduces human error, and accelerates research in photonic glass design.

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

![Flow chart of the estimation procedure.\label{fig:flowchart}](figure.png){ width=60% }

# Acknowledgements

We thank our colleagues and institutions who supported the development of this tool. Funding sources (if any) should be acknowledged here.

# References
