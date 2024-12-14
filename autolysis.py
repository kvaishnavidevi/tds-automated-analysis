import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import openai
import sys
import os
import markdown
from charset_normalizer import detect
from pathlib import Path

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

if len(sys.argv) < 2:
    print("Usage: uv run autolysis.py <filename.csv>")
    sys.exit(1)

# Get the file name from the command-line arguments
file_path = sys.argv[1]

# Detect encoding
with open(file_path, 'rb') as file:
    raw_data = file.read()
    result = detect(raw_data)
    encoding = result['encoding']

print(f"Detected encoding: {encoding}")

# Step 1: Load the dataset
#file_path = input("Enter the path to your dataset (CSV file): ")
try:
    data = pd.read_csv(file_path, encoding=encoding)
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Prepare README content
markdown_content = []

# Dataset Overview
markdown_content.append("# Dataset Analysis Report")
markdown_content.append(f"## CSV File Name: {file_path}")
markdown_content.append("## Dataset Overview")
markdown_content.append(f"- **Shape:** {data.shape[0]} rows and {data.shape[1]} columns")
markdown_content.append("### Columns and Data Types:")
markdown_content.append(f"```plaintext\n{data.dtypes.to_string()}\n```")
markdown_content.append("### Sample Rows:")
markdown_content.append(f"```plaintext\n{data.head().to_string()}\n```")

# Basic Statistics
markdown_content.append("## Basic Statistics")
markdown_content.append(f"```plaintext\n{data.describe(include='all').to_string()}\n```")

# Missing Values
missing_values = data.isnull().sum()
missing_summary = missing_values[missing_values > 0]
if not missing_summary.empty:
    markdown_content.append("## Missing Values")
    markdown_content.append(f"```plaintext\n{missing_summary.to_string()}\n```")
else:
    markdown_content.append("## Missing Values")
    markdown_content.append("No missing values detected.")

# Correlation Matrix
numerical_cols = data.select_dtypes(include=np.number).columns.tolist()
if numerical_cols:
    correlation_matrix = data[numerical_cols].corr()
    markdown_content.append("## Correlation Matrix")
    markdown_content.append(f"```plaintext\n{correlation_matrix.to_string()}\n```")

    # Save correlation matrix plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.savefig("correlation_matrix.png")
    markdown_content.append("![Correlation Matrix](correlation_matrix.png)")
else:
    markdown_content.append("## Correlation Matrix")
    markdown_content.append("No numerical columns available for correlation analysis.")

# Outlier Detection
if numerical_cols:
    markdown_content.append("## Outlier Detection")
    outlier_report = []
    for col in numerical_cols:
        q1 = data[col].quantile(0.25)
        q3 = data[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]
        outlier_report.append(f"- **{col}:** {outliers.shape[0]} outliers")
    markdown_content.extend(outlier_report)
else:
    markdown_content.append("## Outlier Detection")
    markdown_content.append("No numerical columns available for outlier detection.")

# Generate Narrative
if len(numerical_cols) > 0:
    summary = f"The dataset has {data.shape[0]} rows and {data.shape[1]} columns. "\
              f"Missing values were identified in {len(missing_summary)} columns. "\
              f"Numerical columns include {', '.join(numerical_cols)}."
    #narrative = generate_narrative(summary)
    markdown_content.append("## Generated Narrative")
    #markdown_content.append(f"{narrative}")
else:
    markdown_content.append("## Generated Narrative")
    markdown_content.append("No numerical columns for narrative generation.")

# Save to README.md
readme_path = "README.md"
with open(readme_path, "w") as f:
    f.write("\n\n".join(markdown_content))

print(f"Analysis results of {file_path} saved to {readme_path}.")
"""
file_name = Path(readme_path).stem
print(file_name)

# Open and read the file
with open(readme_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Convert markdown to HTML
html_content = markdown.markdown(content)

# Display the HTML content
print(html_content) """
