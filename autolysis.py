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
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage

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
# Clustering Analysis

# Select numerical columns for clustering
numerical_data = data.select_dtypes(include=["float64", "int64"]).dropna()

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numerical_data)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(scaled_data)
markdown_content.append("## Clustering Analysis")
markdown_content.append("Cluster Labels:")

# Add cluster labels to the dataset
#data['Cluster'] = pd.NA  # Initialize with missing values
data.loc[numerical_data.index, 'Cluster'] = clusters
cluster_counts = data['Cluster'].value_counts()
table = "| Cluster | Count |\n|---------|-------|\n"
for cluster, count in cluster_counts.items():
    table += f"| {cluster} | {count} |\n"
markdown_content.append(table)

# Analyze Categorical Data
categorical_columns = data.select_dtypes(include=['object']).columns
markdown_content.append("## Categorical Data Analysis")

# Prepare table headers
uniq_table = "| Column | Unique Value Count |\n|---------|--------------------|\n"

# Loop through categorical columns and collect unique value counts
for col in categorical_columns:
    value_counts = data[col].nunique()
    uniq_table += f"| {col} | {value_counts} |\n"

# Append the table to markdown content
markdown_content.append("### Unique Value Count for All Categorical Columns")
markdown_content.append(uniq_table)

# Visualize Data Distributions and Relationships
markdown_content.append("## Visualizations")

# Pairplot for relationships
numerical_data = data.select_dtypes(include=['float64', 'int64']).dropna()
sns.pairplot(numerical_data)
plt.savefig("pairplot.png")
plt.close()
markdown_content.append("![Pairplot](pairplot.png)")

# Countplots for categorical variables
""" for col in categorical_columns:
    col_display_name = col.replace(" ", "_")
    plt.figure(figsize=(16, 12))
    sns.countplot(x=col, data=data)
    plt.title(f"Distribution of {col}")
    plt.xticks(rotation=45)
    plt.savefig(f"{col_display_name}_countplot.png")
    plt.close()
    markdown_content.append(f"![{col} Distribution]({col_display_name}_countplot.png)") """
for col in categorical_columns:
    col_display_name = col.replace(" ", "_")

    # Check the number of distinct values in the column
    num_distinct = data[col].nunique()

    # Only generate a plot if the column has 50 or fewer distinct values
    if num_distinct <= 50:
        # Determine figure size based on number of distinct values
        if num_distinct <= 10:
            figsize = (16, 12)  # Larger figure for fewer categories
        elif num_distinct <= 30:
            figsize = (14, 10)  # Medium figure for more categories
        else:
            figsize = (12, 8)   # Smaller figure for many categories

        # Calculate the percentage distribution of categories
        category_counts = data[col].value_counts(normalize=True) * 100

        # Adjust the y-axis limits to ensure small values are visible
        min_percentage = category_counts.min()
        if min_percentage < 1:
            min_percentage = 1  # Set a minimum threshold for visibility

        # Plot the count plot for categorical data with normalized values
        plt.figure(figsize=figsize)
        sns.barplot(x=category_counts.index, y=category_counts.values)
        plt.title(f"Percentage Distribution of {col}")
        plt.xticks(rotation=45)
        plt.ylabel("Percentage")

        # Ensure small bars are visible
        plt.ylim(min_percentage, category_counts.max() + 5)  # Adjust y-axis range

        # Save the plot and append to markdown content
        plt.savefig(f"{col_display_name}_percentage_distribution.png")
        plt.close()
        markdown_content.append(f"![{col} Percentage Distribution]({col_display_name}_percentage_distribution.png)")
    else:
        # If there are more than 50 distinct values, don't create the plot
        markdown_content.append(f"Skipping distribution plot for {col} because it has {num_distinct} distinct values.")

# Hierarchical Clustering
markdown_content.append("## Hierarchical Clustering")

if not numerical_data.empty:
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numerical_data)

    # Compute linkage matrix
    linked = linkage(scaled_data, method='ward')

    # Plot dendrogram
    plt.figure(figsize=(10, 7))
    dendrogram(linked, truncate_mode='lastp', p=12, leaf_rotation=45, leaf_font_size=10)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.savefig("dendrogram.png")
    plt.close()

    markdown_content.append("![Dendrogram](dendrogram.png)")

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
