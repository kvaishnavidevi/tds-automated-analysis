import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import openai

# Initialize OpenAI API (replace 'your_api_key' with your OpenAI key)
#openai.api_key = "your_api_key"

# Function to generate a narrative using LLM
def generate_narrative(summary):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Based on the following data analysis summary, write an insightful narrative:\n{summary}",
        max_tokens=300,
        temperature=0.7
    )
    return response['choices'][0]['text'].strip()

# Step 1: Load the dataset
#file_path = input("Enter the path to your dataset (CSV file): ")
try:
    data = pd.read_csv("happiness.csv", encoding='latin1')
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Step 2: Display dataset information
print("\n--- Dataset Overview ---")
print("Shape of the dataset:", data.shape)
print("Columns and Data Types:")
print(data.dtypes)

# Show sample rows
print("\nSample Rows:")
print(data.head())

# Step 3: Basic statistics and missing values
print("\n--- Basic Statistics ---")
print(data.describe(include='all'))

print("\n--- Missing Values ---")
missing_values = data.isnull().sum()
print(missing_values[missing_values > 0])

# Step 4: Correlation Matrix (for numerical features)
numerical_cols = data.select_dtypes(include=np.number).columns.tolist()
if numerical_cols:
    print("\n--- Correlation Matrix ---")
    correlation_matrix = data[numerical_cols].corr()
    print(correlation_matrix)

    # Visualization of correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.savefig("correlation_matrix.png")
    plt.show()
else:
    print("\nNo numerical columns available for correlation analysis.")

# Step 5: Outlier Detection
if numerical_cols:
    print("\n--- Outlier Detection ---")
    for col in numerical_cols:
        q1 = data[col].quantile(0.25)
        q3 = data[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
        print(f"Outliers in {col}: {outliers.shape[0]} instances")
