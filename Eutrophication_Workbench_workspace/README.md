# Eutrophication Workbench Virtual Laboratory (EWB VLab)

## Quick Start

The **Eutrophication Workbench (EWB)** workspace provides a self-contained workflow for generating harmonised and standardized Essential Ocean Variable (EOV) datasets, running duplicate detection, converting format results and webODV exploration.

## Workspace Folder Structure

```
Eutrophication_Workbench_workspace/
├── Datasets/
│   └── Global/
│       └── v1.0.0/
├── Documentation/
├── Private/
└── Public/
    ├── Beacon_queries/
    │   ├── Merged_notebooks/
    │   │   ├── latest/
    │   │   └── *.ipynb
    │   └── Monolith_notebooks/
    ├── FileForge_config/
    │   └── conf/
    │       ├── latest/
    │       ├── v1.0.0/
    │       └── v2.0.0/
    └── user_workflow/
        ├── v1.0.0/
        └── v2.0.0/
```

| Folder | Role |
|---|---|
| `Public/Beacon_queries/` | BEACON query notebooks and exports |
| `Public/FileForge_config/conf/` | FileForge configuration templates |
| `Public/user_workflow/` | Workflow starter notebooks and setup automation |
| `Datasets/Global/v1.0.0/` | Current global dataset release |
| `Documentation/` | User and technical guides |

---

This repository also contains the current EWB workflow components used in the EWB VLab:
- `Public/user_workflow/latest/` — latest workflow setup notebook
- `Public/Beacon_queries/Merged_notebooks/latest/` — latest BEACON merged query notebooks
- `Public/FileForge_config/conf/latest/` — latest FileForge configuration files
- `Datasets/Global/v1.0.0/` — current global dataset package

---

## Current Recommended Versions

- Workflow starter notebook: `Public/user_workflow/latest/0_Start_Here_RUNME.ipynb`
- Latest merged BEACON query notebook: `Public/Beacon_queries/Merged_notebooks/latest/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-TS-PR_VAR=allEOV_OUT=parquet_v2.1.0.ipynb`
- Latest FileForge configuration templates: `Public/FileForge_config/conf/latest/`
- Current dataset release: `Datasets/Global/v1.0.0/`

---

## EWB Workflow Overview

Each step runs in a **dedicated execution environment**.

---

## Step 0 – Setup the Workflow Folder Structure

**Environment:** JupyterLab  
**Purpose:** Creates the workflow folder structure and copy the necessary query notebooks and configuration files from the `Public\` folder.

1. Open **JupyterLab** in the EWB VLab.
2. Navigate to `Public/user_workflow/latest/`
3. **COPY** `0_Start_Here_RUNME.ipynb` and run it in in your `/home/jovyan/workspace/<myfolder>`.
4. Provide the requested values when prompted:
   - user identifier / initials
   - start year and month (YYYYMM)
   - end year and month (YYYYMM)
   - minimum and maximum depth ranges (metres)

### Result

The notebook creates the local workflow folders and supporting configuration files, including:
- `1_DatalakeQuery/`
- `2_CWduplicates-tool/`
- `3_FileForge/`

> **Important:** Step 0 must be run before the BEACON query and CWdt/FileForge steps.

---

## Step 1 – Access & Harmonise Data with BEACON

**Environment:** JupyterLab  
**Purpose:** Query the merged BEACON instance and export harmonised EOV datasets.

1. From the previously creted folder tree navigate to: `1_DatalakeQuery/Merged_notebooks/`
2. Open and run `01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-TS-PR_VAR=allEOV_OUT=parquet_v2.1.0.ipynb`.
3. Set your **D4Science / Blue-Cloud token** and configure the query options.
4. Run the notebook to generate Parquet outputs.

### Output

Harmonised and standardized Parquet files are produced for downstream duplicate detection and are saved to the notebook's output folder `1_DatalakeQuery/Merged_notebooks/outputs/`.

---

## Step 2 – Detect Duplicates with CW

**Environment:** Cloud Computing Platform (CCP)  
**Purpose:** Run the CWdt Duplicate Tool to identify duplicate records across BDIs.

1. Launch the **CW Duplicate Tool** in CCP.
2. Use the generated CW configuration file from Step 0: `2_CWduplicates-tool/Configuration_files/cw_user_config.yaml`.
3. Run the duplicate detection process (Documentation can be found in the folder `/Eutrophication-Workbench/Documentation/DuplicatesTool_cwdt/ or at the following DOI: [https://doi.org/10.5281/zenodo.20605786](https://doi.org/10.5281/zenodo.20605786)`).

### Output

Duplicate detection results are written to:
- `2_CWduplicates-tool/outputs/`

---

## Step 3 – Remove or annotate duplicates and conver to desired format with FileForge

**Environment:** Cloud Computing Platform (CCP)  
**Purpose:** Apply CWdt decisions and convert output data into desired format.

1. Launch **FileForge** in CCP.
2. Select CW outputs from Step 2.
3. Select FileForge configuration files from `3_FileForge/Configuration_files/`.
4. Run FileForge (Documentation can be found in the folder `/Eutrophication-Workbench/Documentation/FileForge/ or at the following DOI: [https://doi.org/10.5281/zenodo.20605786](https://doi.org/10.5281/zenodo.20596096)`).

### Output

Converted outputs are written to 
- `3_FileForge/output/`

---

## Step 4 (optional) – Explore & Validate with webODV

**Environment:** webODV  
**Purpose:** Visualise and quality-control the **ODV outputs**.

> **Important:** this step is ONLY valid if you have run FileForge with an odv configuration file for example 
`wb2_odv_config.yaml`.

1. Open **webODV** from the EWB interface.
2. use the import option with the .txt file produced by FileForge to create the ODV collection.
3. Use the tool to:
   - visualise profiles and time series
   - perform QC checks
   - export subsets for analysis

---

## Versions used in to obtain the Global dataset v1.0.0: 

- `Public/user_workflow/latest/0_Start_Here_RUNME.ipynb`
- `Public/Beacon_queries/Merged_notebooks/latest/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-TS-PR_VAR=allEOV_OUT=parquet_v2.1.0.ipynb`
- `Public/FileForge_config/conf/latest/`


---

## Notes

- The latest BEACON query notebook is based on the merged BEACON instance version `v1.5.4`.
- The workflow starter notebook `v2.0.0` is the current recommended entry point.
- Use `Public/FileForge_config/conf/latest/` for the newest FileForge settings, or fall back to versioned config directories when needed.
- The EWB workflow is **hybrid**:
  - Not all steps are automated
  - Some steps require **user decisions**
- Execution environments are **intentionally separated** to ensure:
  - Transparency
  - Reproducibility
  - Scientific control
- **Always run Step 0 first** to create the necessary folder structure and configuration files before proceeding with subsequent steps.

---

## Documentation & Support

For additional instructions and reference materials:
- Browse `/Eutrophication-Workbench/Documentation/`
- Eutrophication Workbench Users Handbook: [text](https://data.d4science.org/ctlg/Eutrophication-Workbench/eutrophication_workbench_users_handbook)

---

## Citation & Acknowledgement

Please acknowledge:
- **Blue‑Cloud**
- Contributing BDIs: Copernicus Marine, EMODnet Chemistry, World Ocean Database
- The Eutrophication Workbench VLab: Reyes Suarez Nydia Catalina, Robin Kooyman, Gwenaëlle Moncoiffé, Alessandra Giorgetti, Virginie Racapé, Maxence Couppey, Julie Gatti, Athanasia (Sissy) Iona& Karin Wesslander. (2026). Eutrophication Workbench VLab (Version 2). Zenodo. https://doi.org/10.5281/zenodo.20040219
