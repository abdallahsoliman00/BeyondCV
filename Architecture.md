# Architecture

The philosophy behind this piece of software is that everything is a table.
A paragraph is a table, a line is a table and, of course, a table is also a table.\
This provides the benefit of the whole system being modular. If a table for a new section needs to be added, it can easily be done.

This tool works as a pipeline. The pipeline is as follows:

![pipeline](assets/pipeline.png)

The pipeline contains two main modules:
- LLM Module
- Table Builder Module

## LLM
The LLM module takes in the PDF and a hardcoded prompt to extract all required information.
The LLM module outputs a JSON object that can then be fed into the Table Builder.

The PDF is first parsed and ONLY text is extracted. This text is passed to the LLM and an output is received.

The LLM used is the Capgemini Generative Engine (for now).
(Newer versions of this tool should allow for usage of different LLM providers)


## Table Builder
The Table Builder module consists of two submodules:
- Table maker
- Translation unit

### Table Maker 
This takes in the data from the JSON object produced by the LLM and converts it into the different tables for the different sections.

The table maker is where the output is configured. Each table shall have the following properties:
**Table**:
- A list of Rows

**Row**:
- A list of cells
- Row minimum height

**Cell**:
- A list of paragraphs: each paragraph is a block of text to be added to the cell.
- Cell configuration

**Paragraph**:
- Text
- Paragraph configuration

**Cell Configuration**:
- Width
- Colour
- Position of cell contents

**Paragraph Configuration**:
- Font Name
- Font Size
- Bold
- Italic
- Underline

The number of rows and columns shall be calculated dynamically. This is done by having the table be created by adding rows to an empty table object.
Each row added can have an arbitrary number of columns.

#### Heirarchy Overview
Paragraph -> Cell -> Row -> Table

### Translation Unit
This takes in the table classes from the table maker and acts as an interface, translating to whatever output file type is required.
The main output types will be Docx and TeX files.
