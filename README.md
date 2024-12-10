# DPMFA-Release Model

This respository contains the **Dynamic Probabilistic Material Flow Analysis and Release model**. It is linked to the publication: **Using Dynamic Release Modeling to Predict Historic and Current Macro- and Microplastic Releases**

Zipeng Liu, Bernd Nowack,
Resources, Conservation and Recycling,
Volume 214, 2025, 108011, ISSN 0921-3449,
https://doi.org/10.1016/j.resconrec.2024.108011.
(https://www.sciencedirect.com/science/article/pii/S0921344924006025)

Abstract: Confronting the pervasive challenge of plastic pollution, our study pioneers a dynamic release model to quantify the historic and current plastic emissions. Utilizing Dynamic Probabilistic Material Flow Analysis (DPMFA) coupled to a release model, we comprehensively tracked emissions of macro- and microplastics in Switzerland from 1950 to 2022, covering 35 product categories and 183 release pathways for seven polymers (LDPE, HDPE, PP, PS, EPS, PVC, PET). The plastic usage exhibited a “Peak Plastic” around the year 2010 with a subsequent decrease in per capita use of plastics from 120±5 to 107±5 kg/cap in 2022. Over the considered timeframe, 27±1 kg/cap of macroplastics and 4 ± 1 kg/cap of microplastics were released to the environment, with the most substantial contributions coming from LDPE and PET. The overall emission factor was 0.66±0.07 % for macroplastics and 0.010±0.01 % for microplastics. The model can provide a crucial framework for crafting targeted interventions toward sustainable plastic lifecycle management.
Keywords: Plastic; MFA; Release; Dynamic; Microplastics


## Repository Structure

### **Main Folders and Files**

- **`DPMFA-Release/`**
  - `CaseStudy_Runner.py`: Main script to execute case studies using the DPMFA model.
  - `DPMFA_Plastic_CH.db`: Database generated from the SQL Import floder, containing data for Switzerland's plastic flow analysis.
  - `TruncatingFunctions.py`: Contains utility functions to process and truncate data.
  - `setup_model_new.py`: Script for setting up the DPMFA-Release model.

- **`Input/`**
  - Folder for input datasets used in simulations.

- **`Output/`**
  - Folder for storing model outputs, including results of simulations and visualizations.

- **`Plotting/`**
  - Folder for storing plotting and visualization scripts.

- **`SQL Import/`**
  - `Lifetimes_Summary.csv`: CSV file summarizing the lifetimes of materials.
  - `Product category.xlsx`: Excel file defining product categories.
  - `SQL_CH_1_setup.py`: Python script to set up initial SQL tables for the project.
  - `SQL_CH_2_import_TC.py`: Script for importing trade calculations data into the database.
  - `SQL_CH_3_import_input.py`: Script for importing input data into the database.
  - `SQL_CH_4_import_lifetimes.py`: Script for importing lifetimes data into the database.
  - `compartments.xlsx`: Excel file defining material compartments.

- **`Trade Calculation/`**
  - `Codes_and_attribution.xlsx`: File mapping codes and attributions for trade flows.
  - `PF_Inflows_Summary_updated.xlsx`: Updated summary of product inflows.
  - `Trade calculation.R`: R script for calculating trade flows.

- **Other Files**
  - `LICENSE`: License file for the repository.
  - `README.md`: Documentation for the project (this file).

---

### **Prerequisites**
- Python 3.8 or higher
- R programming language (for trade calculations)
- SQLite (for database operations)

