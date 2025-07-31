import pandas as pd

# Load your Excel file
df = pd.read_excel('job_data.xlsx')

# Filter for Job Seekers only
job_seekers = df[df['Type'] == 'Job Seeker']

#  Filter by Field of Interest
it_seekers = job_seekers[job_seekers['Field of Interest'] == 'IT']
food_seekers = job_seekers[job_seekers['Field of Interest'] == 'Food and Beverage']
health_seekers = job_seekers[job_seekers['Field of Interest'] == 'Health']
management_seekers = job_seekers[job_seekers['Field of Interest'] == 'Management']
education_seekers = job_seekers[job_seekers['Field of Interest'] == 'Education']
other_seekers = job_seekers[job_seekers['Field of Interest'] == 'Other']



# Save filtered data to new sheets in one Excel file
with pd.ExcelWriter('filtered_job_data_by_field.xlsx') as writer:
    job_seekers.to_excel(writer, sheet_name='Job Seekers', index=False)
    it_seekers.to_excel(writer, sheet_name='IT', index=False)
    food_seekers.to_excel(writer, sheet_name='Food_Beverage', index=False)
    health_seekers.to_excel(writer, sheet_name='Health', index=False)
    management_seekers.to_excel(writer, sheet_name='Management', index=False)
    education_seekers.to_excel(writer, sheet_name='Education', index=False)
    other_seekers.to_excel(writer, sheet_name='Other', index=False)

# print("\nFiltered sheets saved as 'filtered_job_data_by_field.xlsx'")
print('file created sucessfully')
