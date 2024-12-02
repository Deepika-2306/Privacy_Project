import pandas as pd
import matplotlib.pyplot as plt

file_path = 'CSC533_Survey.csv'
data = pd.read_csv(file_path)
survey_data_cleaned = data.iloc[2:].reset_index(drop=True) 
survey_data_cleaned.replace("", "No Response", inplace=True)
comfort_levels_columns = ['Q3', 'Q5_1', 'Q5_2', 'Q5_3', 'Q5_4', 'Q5_5', 'Q5_6', 'Q5_7', 'Q5_8', 'Q5_9', 'Q5_10', 'Q5_11']
pii_data = survey_data_cleaned[comfort_levels_columns].fillna("No Response")


comfort_summary = pii_data['Q3'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
comfort_summary.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Comfort Levels in Sharing PII', fontsize=16)
plt.xlabel('Comfort Level', fontsize=12)
plt.ylabel('Number of Respondents', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


preferred_pii_summary = pii_data.iloc[:, 1:].apply(pd.Series.value_counts).fillna(0).transpose()
preferred_pii_summary.index = [
    'SSN', 'Passport/Driver\'s License', 'Email', 'Phone', 'Home Address',
    'Date of Birth', 'Employment History', 'Income Level', 'Biometric Data',
    'Tax ID', 'Other'
]
preferred_pii_summary.plot(kind='bar', stacked=True, figsize=(12, 8), cmap='viridis', edgecolor='black')
plt.title('Preferences for Sharing Specific PII Types', fontsize=16)
plt.xlabel('PII Type', fontsize=12)
plt.ylabel('Count of Responses', fontsize=12)
plt.legend(title='Comfort Level', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

categories = ['Account Openings', 'Loan Applications', 'Regulatory Compliance', 'Marketing Purposes']
percentages = [82, 77, 40, 8]

plt.figure(figsize=(10, 6))
plt.bar(categories, percentages, color='skyblue', edgecolor='black')
plt.title('Willingness to Share PII for Various Purposes', fontsize=16)
plt.xlabel('Purpose', fontsize=12)
plt.ylabel('Percentage of Respondents (%)', fontsize=12)
plt.ylim(0, 100)  # Limit y-axis to 100%
plt.xticks(rotation=45, fontsize=10)
plt.tight_layout()
plt.show()

columns_of_interest = ['Q9', 'Q6']
cleaned_data = data[columns_of_interest].dropna().rename(columns={
    'Q9': 'Data_Transparency_Importance',
    'Q6': 'Technical_Background'
})

valid_responses = cleaned_data[~cleaned_data['Data_Transparency_Importance'].isin([
    "How important are a financial institution's data protection measures to you when deciding to share your personal information?",
    '{"ImportId":"QID9"}'
]) & ~cleaned_data['Technical_Background'].isin([
    'What is your technical background?',
    '{"ImportId":"QID4"}'
])]

valid_responses['Data_Transparency_Importance'] = valid_responses['Data_Transparency_Importance'].replace(
    {'Extremely important': 'Important', 'Very important': 'Important'}
)

response_counts = valid_responses.groupby(['Technical_Background', 'Data_Transparency_Importance']).size().reset_index(name='Counts')
pivot_data = response_counts.pivot(index='Technical_Background', columns='Data_Transparency_Importance', values='Counts').fillna(0)

color_mapping = {
    'Important': '#006400',
    'Moderately important': '#6ec007',
    'Slightly important': '#0D98BA',
    'Not at all important': '#FFA07A'
}
pivot_data = pivot_data[[col for col in color_mapping if col in pivot_data.columns]]
pivot_data.plot(kind='bar', stacked=True, figsize=(12, 8), color=[color_mapping[col] for col in pivot_data.columns])
plt.title('Importance of Data Transparency by Technical Background', fontsize=14)
plt.xlabel('Technical Background', fontsize=12)
plt.ylabel('Number of Respondents', fontsize=12)
plt.legend(title='Data Transparency Importance', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()