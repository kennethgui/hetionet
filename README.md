# Graph Database Analysis Project
## Overview
This project leverages Hetionet’s Neo4j graph database to analyze biomedical data. Using Python tools and Cypher queries, the project identifies potential drug candidates for untreated diseases by analyzing complex interactions between genes, anatomical data, and compounds.

Read more about Hetionet [here](https://het.io/)

## Key Features
Data Source: Hetionet (230K nodes, 1.3M edges)
Technologies: Python, Neo4j, Cypher, Py2Neo
Focus Areas:
Drug-disease interaction analysis
Gene and anatomical data extraction
Query optimization

## Command-Line Tool Usage
This project includes a Python command-line tool that interacts with the Neo4j database to extract insights on biomedical data. Below is the step-by-step guide on how to use it:

### Launch the tool:
Run the following command to start the main script:

```python neo4jCLC.py```

## User Input:
After launching, the tool will prompt you to input a disease ID in the format `Disease::DOID:xxxx`. You can use identifiers such as `'Disease::DOID:1324'`.

## Functionality:

The tool queries the database to retrieve related anatomical data, genes, and compounds associated with the specified disease.
It checks for potential new drug candidates that haven’t been linked to the disease.
Sample Output:
The results will display new compounds for potential treatment, associated genes, and anatomical locations in a user-friendly format.

Example:

```
Enter a disease ID: Disease::DOID:1324
Querying database...

Results:
- Disease: Lung Cancer
- New Treatment Compounds: Compound1, Compound2, ...
- Related Genes: Gene1, Gene2, ...
- Anatomical Locations: Lung, ...
``

Make sure to modify neo4jCLC.py to customize any specific queries you wish to run!

## Results
Provides actionable insights into disease-treatment pathways.
Identifies potential drug candidates for diseases lacking treatments.
