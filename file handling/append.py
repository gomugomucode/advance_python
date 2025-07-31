import pandas as pd

# Files
file_name = "JobFair_Filtered_Final.xlsx"
source_file = "Butwal Job Fair-2082(1).xlsx"

# Load source data
df = pd.read_excel(source_file)

identity_col = "Choose your Identity"
qual_col = "5.  Educational Qualification"

# Get Job Seekers
df_js = df[df[identity_col].str.strip().str.lower() == "job seeker"]

# Needed qualifications
missing_quals = ["Master", "+2", "SLC"]

# Load existing sheet names safely
try:
    existing_sheets = pd.ExcelFile(file_name).sheet_names
except Exception as e:
    print(f"❌ Error: Cannot open {file_name}. Is it a valid .xlsx? Error:\n{e}")
    exit()

# Append new sheets ONLY
with pd.ExcelWriter(file_name, engine='openpyxl', mode='a') as writer:
    for qual in missing_quals:
        sheet_name = qual.replace("+", "Plus").replace(" ", "")[:31]
        if sheet_name in existing_sheets:
            print(f"⚠️ Sheet '{sheet_name}' already exists. Skipping.")
            continue
        # ✅ Safe: contains with regex=False
        df_q = df_js[df_js[qual_col].str.contains(qual, case=False, na=False, regex=False)]
        df_q.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"✅ Added sheet '{sheet_name}' with {len(df_q)} rows.")

print(f"✅ Done! Appended sheets to: {file_name}")
