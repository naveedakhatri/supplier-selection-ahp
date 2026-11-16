import streamlit as st
import pandas as pd
import numpy as np

# Application title
st.title("Supplier Selection Optimization")

st.write(
    "This application evaluates and ranks suppliers using "
    "the Analytic Hierarchy Process (AHP)."
)

st.caption(
    "Project created by Naveed Ahmed Khatri | "
    "MAXD5163 Modeling and Decision Making"
)

st.caption(
    "Universiti Teknikal Malaysia Melaka (UTeM) | 2026"
)

st.subheader("How to Use This Application?")

st.markdown("""
**Step 1:** Upload the supplier data and AHP comparison files.  
**Step 2:** Verify the uploaded data.  
**Step 3:** Review the AHP weights and consistency result.  
**Step 4:** View the supplier ranking.  
**Step 5:** Apply your price and quality constraints.  
**Step 6:** Get  the recommended supplier.  
**Step 7:** Download the results.
""")

st.markdown("### Don't have sample CSV files?")

st.info(
    "You can download the sample CSV files from our "
    "[GitHub repository](https://github.com/naveedakhatri/supplier-selection-ahp/)."
    "\n\nDownload both supplier_data.csv and ahp_pairwise_matrix.csv "
    "before using the application."
)

# Required columns for supplier data
required_columns = [
    "Supplier_ID",
    "Unit_Price (RM)",
    "Quality_Score (out of 100)",
    "Delivery_Time (Days)",
    "On_Time_Delivery_Rate (out of 10)",
    "Defect_Rate (out of 10)"
]

# Expected criteria for the AHP matrix
expected_criteria = [
    "Unit_Price",
    "Quality_Score",
    "Delivery_Time",
    "On_Time_Delivery_Rate",
    "Defect_Rate"
]

st.divider()
st.header("Step 1: Upload Required Files")

# Upload supplier data
supplier_file = st.file_uploader(
    "Upload Supplier Data CSV",
    type=["csv"]
)

# Upload AHP matrix
matrix_file = st.file_uploader(
    "Upload AHP Pairwise Comparison Matrix CSV",
    type=["csv"]
)

# Process files only when both have been uploaded
if supplier_file is not None and matrix_file is not None:

    try:
        # Read uploaded files
        supplier_df = pd.read_csv(supplier_file)
        matrix_df = pd.read_csv(matrix_file, index_col="Criteria")

        # Validate supplier CSV columns
        missing_columns = [
            column for column in required_columns
            if column not in supplier_df.columns
        ]

        # Validate AHP matrix
        valid_matrix = (
            matrix_df.shape == (5, 5)
            and list(matrix_df.index) == expected_criteria
            and list(matrix_df.columns) == expected_criteria
        )

        # Display validation results
        if missing_columns:
            st.error(
                "Supplier CSV validation failed. "
                f"Missing columns: {missing_columns}"
            )

        elif not valid_matrix:
            st.error(
                "AHP matrix validation failed. "
                "Please check the matrix size, criteria names, and order."
            )

        else:
            st.success("Both CSV files are valid and ready for evaluation.")

            # Display uploaded data
            st.divider()
            st.header("Step 2: Verify Uploaded Data")

            st.subheader("Supplier Data")
            st.dataframe(supplier_df)

            st.subheader("AHP Pairwise Comparison Matrix")
            st.dataframe(matrix_df)

            # Convert AHP matrix to a NumPy array
            matrix = matrix_df.to_numpy(dtype=float)

            # Calculate eigenvalues and eigenvectors
            eigenvalues, eigenvectors = np.linalg.eig(matrix)

            # Find the largest eigenvalue
            max_index = np.argmax(eigenvalues.real)
            lambda_max = eigenvalues[max_index].real

            # Extract and normalize the principal eigenvector
            principal_eigenvector = eigenvectors[:, max_index].real
            weights = principal_eigenvector / principal_eigenvector.sum()

            # Create criteria weights table
            weights_df = pd.DataFrame({
                "Criterion": matrix_df.index,
                "AHP Weight": weights
            })

            # Display AHP weights
            st.divider()
            st.header("Step 3: AHP Analysis")
            st.subheader("AHP Criteria Weights")
            st.dataframe(weights_df)

            # Consistency check
            n = matrix.shape[0]
            CI = (lambda_max - n) / (n - 1)

            RI_values = {
                1: 0.00,
                2: 0.00,
                3: 0.58,
                4: 0.90,
                5: 1.12,
                6: 1.24,
                7: 1.32,
                8: 1.41,
                9: 1.45,
                10: 1.49
            }

            RI = RI_values[n]
            CR = CI / RI if RI != 0 else 0

            # Display consistency results
            st.subheader("AHP Consistency Check")

            consistency_results = pd.DataFrame({
                "Measure": [
                    "Maximum Eigenvalue (λmax)",
                    "Consistency Index (CI)",
                    "Random Index (RI)",
                    "Consistency Ratio (CR)"
                ],
                "Value": [
                    round(lambda_max, 4),
                    round(CI, 4),
                    round(RI, 4),
                    round(CR, 4)
                ]
            })

            st.dataframe(consistency_results)

            # Check whether comparisons are consistent
            if CR <= 0.10:
                st.success(
                    "AHP consistency check passed. "
                    "The pairwise comparisons are acceptably consistent."
                )
            else:
                st.error(
                    "AHP consistency check failed. "
                    "Please review the pairwise comparison matrix."
                )
            # Only continue if the AHP comparisons are consistent
            if CR <= 0.10:

                # Define benefit and cost criteria
                benefit_criteria = [
                    "Quality_Score (out of 100)",
                    "On_Time_Delivery_Rate (out of 10)"
                ]

                cost_criteria = [
                    "Unit_Price (RM)",
                    "Delivery_Time (Days)",
                    "Defect_Rate (out of 10)"
                ]

                # Create a copy for normalized supplier data
                normalized_df = supplier_df.copy()

                # Normalize benefit criteria: higher is better
                for column in benefit_criteria:
                    min_value = supplier_df[column].min()
                    max_value = supplier_df[column].max()

                    if max_value == min_value:
                        normalized_df[column] = 1.0
                    else:
                        normalized_df[column] = (
                            (supplier_df[column] - min_value) /
                            (max_value - min_value)
                        )

                # Normalize cost criteria: lower is better
                for column in cost_criteria:
                    min_value = supplier_df[column].min()
                    max_value = supplier_df[column].max()

                    if max_value == min_value:
                        normalized_df[column] = 1.0
                    else:
                        normalized_df[column] = (
                            (max_value - supplier_df[column]) /
                            (max_value - min_value)
                        )

                # Map AHP weights to supplier data columns
                weight_mapping = {
                    "Unit_Price (RM)": weights[0],
                    "Quality_Score (out of 100)": weights[1],
                    "Delivery_Time (Days)": weights[2],
                    "On_Time_Delivery_Rate (out of 10)": weights[3],
                    "Defect_Rate (out of 10)": weights[4]
                }

                # Calculate weighted score for each supplier
                weighted_df = normalized_df[["Supplier_ID"]].copy()

                weighted_df["Weighted_Score"] = sum(
                    normalized_df[column] * weight
                    for column, weight in weight_mapping.items()
                )

                # Sort suppliers by weighted score
                ranking_df = weighted_df.sort_values(
                    by="Weighted_Score",
                    ascending=False
                ).reset_index(drop=True)

                # Add ranking position
                ranking_df.insert(
                    0,
                    "Rank",
                    range(1, len(ranking_df) + 1)
                )

                # Display supplier ranking
                st.divider()
                st.header("Step 4: Supplier Ranking")
                st.dataframe(ranking_df)

                # User-defined selection constraints
                st.divider()
                st.header("Step 5: Selection Constraints")

                max_price = st.number_input(
                    "Maximum acceptable unit price (RM)",
                    min_value=0.0,
                    value=25.0,
                    step=0.5
                )

                min_quality = st.number_input(
                    "Minimum acceptable quality score (out of 100)",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0,
                    step=1.0
                )

                # Combine supplier data with ranking results
                results_df = supplier_df.merge(
                    ranking_df[
                        ["Supplier_ID", "Rank", "Weighted_Score"]
                    ],
                    on="Supplier_ID"
                )

                # Filter suppliers based on user-defined constraints
                eligible_df = results_df[
                    (results_df["Unit_Price (RM)"] <= max_price) &
                    (
                        results_df["Quality_Score (out of 100)"]
                        >= min_quality
                    )
                ].copy()

                # Sort eligible suppliers by weighted score
                eligible_df = eligible_df.sort_values(
                    by="Weighted_Score",
                    ascending=False
                )

                # Display final results
                st.divider()
                st.header("Step 6: Final Recommendation")
                st.subheader("Eligible Suppliers")

                if eligible_df.empty:
                    st.warning(
                        "No suppliers satisfy both the price and "
                        "quality constraints."
                    )
                else:
                    # Display eligible suppliers
                    st.dataframe(
                        eligible_df[
                            [
                                "Rank",
                                "Supplier_ID",
                                "Unit_Price (RM)",
                                "Quality_Score (out of 100)",
                                "Weighted_Score"
                            ]
                        ]
                    )

                    # Select the highest-scoring eligible supplier
                    selected_supplier = eligible_df.iloc[0]

                    st.subheader("Recommended Supplier")

                    st.success(
                        f"Recommended Supplier: "
                        f"{selected_supplier['Supplier_ID']}"
                    )

                    st.write(
                        f"**Overall Rank:** "
                        f"{selected_supplier['Rank']}"
                    )
                    st.write(
                        f"**Weighted Score:** "
                        f"{selected_supplier['Weighted_Score']:.6f}"
                    )
                    st.write(
                        f"**Unit Price:** RM "
                        f"{selected_supplier['Unit_Price (RM)']:.2f}"
                    )
                    st.write(
                        f"**Quality Score:** "
                        f"{selected_supplier['Quality_Score (out of 100)']}"
                    )
                # Download results
                st.divider()
                st.header("Step 7: Download Results")
                # Convert complete ranking to CSV
                ranking_csv = ranking_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Download Complete Supplier Ranking",
                    data=ranking_csv,
                    file_name="supplier_ranking_results.csv",
                    mime="text/csv"
                )

                # Allow eligible suppliers to be downloaded
                if not eligible_df.empty:
                    eligible_csv = eligible_df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(
                        label="Download Eligible Suppliers",
                        data=eligible_csv,
                        file_name="eligible_suppliers.csv",
                        mime="text/csv"
                    )

    except Exception as e:
        st.error(f"An error occurred while reading the files: {e}")