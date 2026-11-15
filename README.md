# Supplier Selection Optimization using Multi-Criteria Analysis

A web-based supplier selection application developed using Python and Streamlit. The application uses the **Analytic Hierarchy Process (AHP)** to determine criteria weights and a weighted scoring approach to evaluate and rank suppliers.

**Project:** MAXD5163 – Modeling and Decision Making  
**Institution:** Universiti Teknikal Malaysia Melaka (UTeM)  
**Developer:** Naveed Ahmed Khatri  
**Year:** 2026

## Live Application

Access the deployed application here:

[Insert your Streamlit application URL here]

## Project Overview

Selecting the most suitable supplier involves evaluating multiple criteria, including cost, quality, delivery performance, and defect rate.

This application helps users evaluate suppliers systematically, calculate their scores, apply selection constraints, and identify the most suitable supplier.

## Evaluation Criteria

The application evaluates suppliers using five criteria:

| Criteria | Measurement | Type |
|---|---|---|
| Unit Price | RM | Cost |
| Quality Score | Out of 100 | Benefit |
| Delivery Time | Days | Cost |
| On-Time Delivery Rate | Out of 10 | Benefit |
| Defect Rate | Out of 10 | Cost |

## Methodology

1. **AHP:** Calculates the relative importance (weights) of the five evaluation criteria using a pairwise comparison matrix.
2. **Consistency Check:** Evaluates the consistency of the pairwise comparisons using the Consistency Ratio (CR).
3. **Normalization:** Converts supplier performance values into comparable normalized scores.
4. **Weighted Scoring:** Calculates the overall score for each supplier using the AHP-derived criteria weights.
5. **Supplier Ranking:** Ranks suppliers based on their overall scores.
6. **Constraint-Based Selection:** Identifies eligible suppliers based on the user's maximum price and minimum quality requirements.

## Sample Input Files

Two sample CSV files are provided in this repository for testing:

- `supplier_data.csv` – Contains supplier information and performance data.
- `ahp_pairwise_matrix.csv` – Contains the pairwise comparison matrix used for AHP weight calculation.

Users can download these files directly from the repository and upload them to the application.

## How to Use the Application

1. Open the [Live Application](INSERT_STREAMLIT_URL_HERE).
2. Download `supplier_data.csv` and `ahp_pairwise_matrix.csv` from this GitHub repository.
3. Upload both CSV files using the two file upload fields.
4. Review the uploaded supplier data.
5. Examine the AHP criteria weights and consistency results.
6. Review the supplier ranking.
7. Enter the maximum acceptable unit price and minimum required quality score.
8. View the eligible suppliers and final recommendation.
9. Download the ranking and eligible supplier results as CSV files.

## Input Data Requirements

**Supplier data CSV**

The supplier file must contain these columns:

- `Supplier_ID`
- `Unit_Price (RM)`
- `Quality_Score (out of 100)`
- `Delivery_Time (Days)`
- `On_Time_Delivery_Rate (out of 10)`
- `Defect_Rate (out of 10)`

**AHP comparison CSV**

The AHP file must contain a 5 × 5 pairwise comparison matrix using the following criteria in the correct order:

- Unit_Price
- Quality_Score
- Delivery_Time
- On_Time_Delivery_Rate
- Defect_Rate

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy

## Repository Contents

```text
supplier-selection-ahp/
│
├── app.py
├── requirements.txt
├── README.md
├── supplier_data.csv
└── ahp_pairwise_matrix.csv
```

## Project Purpose

This project demonstrates the application of multi-criteria decision-making techniques to supplier selection through a simple, interactive web application.
