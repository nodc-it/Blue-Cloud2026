# Eutrophication Workbench (EWB)

## Quick Start

The **Eutrophication Workbench (EWB)** workspace provides a self-contained workflow for generating harmonised Essential Ocean Variable (EOV) datasets, running duplicate detection, and converting results for webODV exploration.

This repository contains the current EWB workflow components used in the Blue-Cloud VLab:
- `Public/user_workflow/v2.0.0/` — latest workflow setup notebook
- `Public/Beacon_queries/Merged_notebooks/latest/` — latest BEACON query notebook version
- `Public/FileForge_config/conf/latest/` — latest FileForge configuration templates
- `Datasets/Global/v1.0.0/` — current global dataset package

---

## Current Recommended Versions

- Workflow starter notebook: `Public/user_workflow/v2.0.0/0_Start_Here_RUNME.ipynb`
- Latest merged BEACON query notebook: `Public/Beacon_queries/Merged_notebooks/latest/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-TS-PR_VAR=allEOV_OUT=parquet_v2.1.0.ipynb`
- Stable merged BEACON query notebook: `Public/Beacon_queries/Merged_notebooks/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-FeatureType_VAR=allEOV_OUT=parquet.ipynb`
- Latest FileForge configuration templates: `Public/FileForge_config/conf/latest/`
- Current dataset release: `Datasets/Global/v1.0.0/`

---

## Workflow Overview

The workspace is organised into separate execution stages for reproducibility:
- `Public/Beacon_queries/` — BEACON data access and query notebooks
- `Public/user_workflow/` — setup and workflow automation notebooks
- `Public/FileForge_config/` — cleanup and conversion configuration files
- `Public/Beacon_queries/Monolith_notebooks/` — monolithic BEACON query notebooks for individual BDIs

---

## Step 0 – Setup the Workflow Folder Structure

**Environment:** JupyterLab  
**Purpose:** Create the project folder structure and generate the necessary configuration files.

1. Open **JupyterLab** in the EWB VLab.
2. Navigate to `Public/user_workflow/v2.0.0/`
3. Open and run `0_Start_Here_RUNME.ipynb`.
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
- `cw_user_config.yaml`

> **Important:** Step 0 must be run before the BEACON query and CW/FileForge steps.

---

## Step 1 – Access & Harmonise Data with BEACON

**Environment:** JupyterLab  
**Purpose:** Query the merged BEACON instance and export harmonised EOV datasets.

1. Open `Public/Beacon_queries/Merged_notebooks/latest/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-TS-PR_VAR=allEOV_OUT=parquet_v2.1.0.ipynb`.
2. If needed, use the stable notebook at `Public/Beacon_queries/Merged_notebooks/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-FeatureType_VAR=allEOV_OUT=parquet.ipynb`.
3. Set your **D4Science / Blue-Cloud token** and configure the query options.
4. Run the notebook to generate Parquet outputs.

### Output

Harmonised Parquet files are produced for downstream duplicate detection and are typically saved to the notebook's output folder.

---

## Step 2 – Detect Duplicates with CW

**Environment:** Cloud Computing Platform (CCP)  
**Purpose:** Run the CW Duplicate Tool to identify duplicate records across BDIs.

1. Launch the **CW Duplicate Tool** in CCP.
2. Use the generated CW configuration file from Step 0: `cw_user_config.yaml`.
3. Run the duplicate detection process.

### Output

Duplicate detection results are written to:
- `2_CWduplicates-tool/outputs/`

---

## Step 3 – Remove Duplicates & Convert with FileForge

**Environment:** Cloud Computing Platform (CCP)  
**Purpose:** Apply CW decisions and convert harmonised data into ODV / text outputs.

1. Launch **FileForge** in CCP.
2. Select CW outputs from Step 2.
3. Select FileForge configuration files from `Public/FileForge_config/conf/latest/` or the versioned configs under `Public/FileForge_config/conf/v2.0.0/`.
4. Run FileForge.

### Output

Converted outputs are written to the CCP execution output folder, for example:
```
/Workspace/CCP/executions/.../outputs/output/
└── wb2_merged.txt
```

---

## Step 4 – Explore & Validate with webODV

**Environment:** webODV  
**Purpose:** Visualise and quality-control the ODV outputs.

1. Open **webODV** from the EWB interface.
2. Load the ODV file produced by FileForge.
3. Use the tool to:
   - visualise profiles and time series
   - perform QC checks
   - export subsets for analysis

---

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

## Latest Versions Used in This Workflow

- `Public/user_workflow/v2.0.0/0_Start_Here_RUNME.ipynb`
- `Public/Beacon_queries/Merged_notebooks/latest/01_EWB_BEACON=merged-v1.5.4_FILTER=BDI-TS-PR_VAR=allEOV_OUT=parquet_v2.1.0.ipynb`
- `Public/FileForge_config/conf/latest/` and `Public/FileForge_config/conf/v2.0.0/`
- `Datasets/Global/v1.0.0/`

---

## Notes

- The latest BEACON query notebook is based on the merged BEACON instance version `v1.5.4`.
- The workflow starter notebook `v2.0.0` is the current recommended entry point.
- Use `Public/FileForge_config/conf/latest/` for the newest FileForge settings, or fall back to versioned config directories when needed.

---

## Documentation & Support

For additional instructions and reference materials:
- Browse `Documentation/`
- Use the README files in `Public/Beacon_queries/`, `Public/FileForge_config/`, and `Public/user_workflow/`

---

## Citation & Acknowledgement

Please acknowledge:
- **Blue‑Cloud**
- Contributing BDIs: Copernicus Marine, EMODnet Chemistry, World Ocean Database
- The Eutrophication Workbench VLab