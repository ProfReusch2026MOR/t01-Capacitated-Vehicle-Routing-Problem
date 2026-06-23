# Literature

This folder contains the academic sources and research notes used for the literature review of the TDHVRPTW project.

The project studies a regional delivery-routing problem from the Dr. Oetker depot in Bielefeld to 25 Lidl stores in the Ostwestfalen-Lippe region. The model combines several routing elements: vehicle capacity, heterogeneous fleet structure, delivery time windows, time-dependent travel assumptions, and scenario-based demand.

The purpose of this folder is to make the literature work traceable. The sources are not collected only as a bibliography list; they are connected to specific parts of the project, such as the routing problem class, heuristic methods, scalability, demand scenarios, and reproducibility.

## Folder contents

* `literature_review.md` contains the main written literature review.
* `literature_summary.md` gives a shorter overview of the literature areas.
* `sources.bib` contains the BibTeX references used in the project.
* `source_notes/` contains individual notes on selected sources.

## Source notes

The `source_notes/` folder contains short explanations of the most relevant papers. These notes describe why a source was useful, how it connects to the model, and where its limits are for our project.

The notes are meant to support the final literature review and make the source selection easier to understand. They are not full paper summaries.

## Use of older sources

The main focus is on recent literature from the last decade. Older sources are only used where they are necessary to identify the historical origin of important routing concepts or methods. They are not treated as the main methodological foundation of the project.

## Technical documentation

Technical documentation, such as solver manuals or software guides, should not be mixed with the academic source notes. If needed, those references should be stored separately in an implementation or documentation folder because they support the code rather than the academic literature review.

## Copyright note

This repository should not contain copyrighted books or papers unless they are legally shareable. If a source is used for the literature review, it should be cited through the bibliography instead of uploading the full PDF without permission.
