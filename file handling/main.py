import pandas as pd

# Load file
file_name = "Butwal Job Fair-2082(1).xlsx"
df = pd.read_excel(file_name)

# Columns
identity_col = "Choose your Identity"
qual_col = "5.  Educational Qualification"
sector_col = "7. Interested Sector"

# Fix spelling map
fix_map = {
    "Information Technolgy": "Information Technology",
    "Food and Baverages": "Food and Beverage",
    "Healthcare": "Health Care"
}

# Target values
qualifications = ["Master", "Bachelor", "+2", "SLC"]
sectors = [
    "Information Technology",
    "Food and Beverage",
    "Education",
    "Health Care",
    "Public Service",
    "Other"
]

# Output file
output_file = "JobFair_Filtered_Final.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 1️⃣ Full form data
    df.to_excel(writer, sheet_name="FormData", index=False)

    # 2️⃣ Employee Seeker
    df_emp = df[df[identity_col].str.strip().str.lower() == 'employee seeker']
    df_emp.to_excel(writer, sheet_name="EmployeeSeeker", index=False)

    # 3️⃣ Job Seeker
    df_js = df[df[identity_col].str.strip().str.lower() == 'job seeker']
    df_js.to_excel(writer, sheet_name="JobSeeker", index=False)

    # 4️⃣–7️⃣ By qualification
    for qual in qualifications:
        df_q = df_js[df_js[qual_col].str.strip().str.lower() == qual.lower()]
        df_q.to_excel(writer, sheet_name=qual.replace("+", "Plus"), index=False)

    # 8️⃣–1️⃣3️⃣ By sector (split multi-value)
    for sector in sectors:
        matches = []
        for idx, row in df_js.iterrows():
            field = str(row[sector_col]) if not pd.isna(row[sector_col]) else ""
            sectors_list = [fix_map.get(x.strip(), x.strip()) for x in field.split(",")]
            sectors_list = [s.title() for s in sectors_list]
            if sector in sectors_list:
                matches.append(row)
        if matches:
            df_s = pd.DataFrame(matches)
            # Excel sheet name safe
            safe_name = sector.replace(" ", "")
            df_s.to_excel(writer, sheet_name=safe_name[:31], index=False)

print(f"✅ Done! All sheets saved to {output_file}")
