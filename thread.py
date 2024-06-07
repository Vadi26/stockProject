def update_company_dataframes(new_data):
    global company_dataframes

    # Convert new data to a DataFrame
    new_df = pd.DataFrame(new_data)

    # Iterate over each row in the new data
    for index, row in new_df.iterrows():
        company_id = row['companyId']

        # Check if the companyId is already in the dictionary
        if company_id in company_dataframes:
            # Append the new row to the existing DataFrame
            company_dataframes[company_id] = pd.concat([company_dataframes[company_id], row.to_frame().T], ignore_index=True)
        else:
            # Create a new DataFrame for this company
            company_dataframes[company_id] = row.to_frame().T

# Example usage with new 5 rows of data
new_data = [
    {'companyId': 'A', 'open': 100, 'high': 110, 'low': 90, 'close': 105},
    {'companyId': 'B', 'open': 200, 'high': 220, 'low': 190, 'close': 210},
    {'companyId': 'A', 'open': 106, 'high': 115, 'low': 95, 'close': 110},
    {'companyId': 'C', 'open': 300, 'high': 330, 'low': 290, 'close': 320},
    {'companyId': 'B', 'open': 211, 'high': 230, 'low': 200, 'close': 220}
]

update_company_dataframes(new_data)

# Display the dataframes for each company
for company_id, df in company_dataframes.items():
    print(f"Data for company {company_id}:")
    print(df)
    print()