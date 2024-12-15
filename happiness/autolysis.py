import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import plotly.express as px
import openai
import sys
import os
import markdown
from charset_normalizer import detect
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage

if len(sys.argv) < 2:
    print("Usage: uv run autolysis.py <filename.csv>")
    sys.exit(1)
file_path = sys.argv[1]
markdown_content = []

# Function to detect encoding, Load and Prepare Dataset
def load_dataset(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = detect(raw_data)
            encoding = result['encoding']
        print(f"Detected encoding: {encoding}")
        data = pd.read_csv(file_path, encoding=encoding)
        return data
    except Exception as e:
        print(f"Error loading/determining the file encoding: {e}")
        return None

# Perform basic analysis
def basic_analysis(csvdata,numerical_cols):
    try:
        data_datatypes = csvdata.dtypes.to_string()
        if len(csvdata.head(50)) >= 50:
            data_sample = csvdata.head(50).to_string()
        else:
            data_sample = csvdata.to_string()

        data_stat = csvdata.describe(include='all').to_string()
        missing_values = csvdata.isnull().sum()
        missing_summary = missing_values[missing_values > 0]
        correlation_matrix = csvdata[numerical_cols].corr()
        analysis_summary = {
                "shape": csvdata.shape,
                "columns": csvdata.columns.tolist(),
                "missing_values": missing_values.to_dict(),
                "numerical_summary": csvdata.describe(include=[np.number]).to_dict(),
                "correlation_matrix": correlation_matrix.to_dict(),
                "sample_rows": data_sample,
                "file_name": file_path,
                "basic_statistics":data_stat,
        }
        markdown_content.append("# Dataset Analysis Report")
        markdown_content.append(f"## CSV File Name: {file_path}")
        markdown_content.append("## Dataset Overview")
        markdown_content.append(f"- **Shape:** {csvdata.shape[0]} rows and {csvdata.shape[1]} columns")
        markdown_content.append("### Columns and Data Types:")
        markdown_content.append(f"```plaintext\n{data_datatypes}\n```")
        markdown_content.append("### Sample Rows:")
        markdown_content.append(f"```plaintext\n{data_sample}\n```")
        markdown_content.append("## Basic Statistics")
        markdown_content.append(f"```plaintext\n{data_stat}\n```")
        markdown_content.append("## Missing Values")
        if not missing_summary.empty:
            markdown_content.append(f"```plaintext\n{missing_summary.to_string()}\n```")
        else:
            markdown_content.append("No missing values detected.")
        markdown_content.append("## Correlation Matrix")
        if numerical_cols:
            markdown_content.append(f"```plaintext\n{correlation_matrix.to_string()}\n```")
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Matrix")
            plt.savefig("correlation_matrix.png")
            plt.close()
            markdown_content.append("![Correlation Matrix](correlation_matrix.png)")
        else:
            markdown_content.append("No numerical columns available for correlation analysis.")
        return analysis_summary
    except Exception as e:
        print("Error while performing the basic analysis: %s" % e)
        traceback.print_exc()

# Identify Outliers in data
def outlier_analysis(csvdata,numerical_cols):
    try:
       markdown_content.append("## Outlier Detection")
       if numerical_cols:
           outlier_report = []
           for col in numerical_cols:
               quartile_first = csvdata[col].quantile(0.25)
               quartile_third = csvdata[col].quantile(0.75)
               inter_quartile_range = quartile_third - quartile_first
               lower_bound = quartile_first - 1.5 * inter_quartile_range
               upper_bound = quartile_third + 1.5 * inter_quartile_range
               outliers = csvdata[(csvdata[col] < lower_bound) | (csvdata[col] > upper_bound)]
               #cleaned_data = csvdata[(csvdata[col] >= lower_bound) & (csvdata[col] <= upper_bound)]
               outlier_report.append(f"- **{col}:** {outliers.shape[0]} outliers")
           markdown_content.extend(outlier_report)
           return outliers
       else:
           markdown_content.append("No numerical columns available for outlier detection.")
    except Exception as e:
            print("Error while determining outliers:  %s" % e)
            traceback.print_exc()

# Perform Advanced Analysis
def perform_clustering(csvdata,numerical_cols,categorical_cols, n_clusters=3):
    try:
        numerical_cols = numerical_cols.select_dtypes(include=["float64", "int64"]).dropna()
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numerical_cols)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        numerical_cols.loc[numerical_cols.index, 'Cluster'] = clusters
        cluster_counts = numerical_cols['Cluster'].value_counts()
        markdown_content.append("## Clustering Analysis")
        markdown_content.append("Cluster Labels:")
        table = "| Cluster | Count |\n|---------|-------|\n"
        for cluster, count in cluster_counts.items():
            table += f"| {cluster} | {count} |\n"
        markdown_content.append(table)
        markdown_content.append("## Categorical Data Analysis")
        uniq_table = "| Column | Unique Value Count |\n|---------|--------------------|\n"
        for col in categorical_cols:
            value_counts = csvdata[col].nunique()
            uniq_table += f"| {col} | {value_counts} |\n"
        markdown_content.append("### Unique Value Count for All Categorical Columns")
        markdown_content.append(uniq_table)
        hier_clust = hier_clustering(numerical_cols)
        clustering_summary = {
                        "kmeans": kmeans,
                        "hier_clust":hier_clust,
        }
        return clustering_summary
    except Exception as e:
        print("Error while performing advanced analysis: %s" % e)
        traceback.print_exc()


# Visualize Data Distributions and Relationships
def generate_visualizations(numerical_data,categorical_cols):
    try:
        markdown_content.append("## Visualizations")
        sns.pairplot(numerical_data)
        plt.savefig("pairplot.png")
        plt.close()
        markdown_content.append("![Pairplot](pairplot.png)")
#         fig = px.scatter_matrix(numerical_data, dimensions=numerical_data.columns)
#         fig.write_image("scatter_matrix.png", width=800, height=600, scale=2)
#         markdown_content.append("![ScatterMatrix](scatter_matrix.png)")
        for col in numerical_data:
            col_display_name = col.replace(" ", "_")
            num_distinct = numerical_data[col].nunique()
            if num_distinct <= 50:
                if num_distinct <= 10:
                    figsize = (16, 12)
                elif num_distinct <= 30:
                    figsize = (14, 10)
                else:
                    figsize = (12, 8)
                category_counts = numerical_data[col].value_counts(normalize=True) * 100
                min_percentage = category_counts.min()
                if min_percentage < 1:
                    min_percentage = 5
                    plt.figure(figsize=figsize)
                    sns.barplot(x=category_counts.index, y=category_counts.values)
                    plt.title(f"Percentage Distribution of {col}")
                    plt.xticks(rotation=45)
                    plt.ylabel("Percentage")
                    plt.ylim(min_percentage, category_counts.max() + 10)
                    plt.savefig(f"{col_display_name}_percentage_distribution.png")
                    plt.close()
                    markdown_content.append(f"![{col} Percentage Distribution]({col_display_name}_percentage_distribution.png)")
            else:
                # If there are more than 50 distinct values, plot not required.
                markdown_content.append(f"Skipping distribution plot for {col} because it has {num_distinct} distinct values.")
    except Exception as e:
        print("Error while generating visualizations: %s" % e)
        traceback.print_exc()

# to-do Hierarchical Clustering
def hier_clustering(numerical_data):
    try:
        markdown_content.append("## Hierarchical Clustering")
        if not numerical_data.empty:
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numerical_data)
            scaled_data_clean = scaled_data[~np.isnan(scaled_data).any(axis=1)]
            scaled_data_clean = scaled_data_clean[~np.isinf(scaled_data_clean).any(axis=1)]
            linked = linkage(scaled_data_clean, method='ward')
            plt.figure(figsize=(10, 7))
            dendrogram(linked, truncate_mode='lastp', p=12, leaf_rotation=45, leaf_font_size=10)
            plt.title("Hierarchical Clustering Dendrogram")
            plt.savefig("dendrogram.png")
            plt.close()
            markdown_content.append("![Dendrogram](dendrogram.png)")
            return linked
    except Exception as e:
        print("Error while performing Hierarchical Clustering: %s" % e)
        traceback.print_exc()


# Interact with LLM
def get_llm_insights(analysis_summary):
    llm_summary_text = f"""
    The dataset contains {analysis_summary['shape'][0]} rows and {analysis_summary['shape'][1]} columns.
    Key findings include:
    - Missing values: {analysis_summary['missing_values']}
    - Top correlations: {list(analysis_summary['correlation_matrix'])[:5]}
    """
    narrative = generate_narrative(llm_summary_text)
    return narrative

# Compile Report
def compile_report():
    with open("report.md", "w") as f:
        f.write("\n".join(markdown_content))
    print("Report saved to REPORT.md")

# Main Function
def main():
    csvdata = load_dataset(file_path)
    numerical_cols = csvdata.select_dtypes(include=np.number)
    numerical_cols_list = numerical_cols.columns.tolist()
    categorical_cols = csvdata.select_dtypes(include=['object']).columns
    analysis_summary = basic_analysis(csvdata,numerical_cols_list)
    outliers = outlier_analysis(csvdata,numerical_cols_list)
    clustering_summary = perform_clustering(csvdata,numerical_cols,categorical_cols)
    generate_visualizations(numerical_cols,categorical_cols)
    linked = hier_clustering(numerical_cols)
    if csvdata is not None:
        #narrative = get_llm_insights(csvdata)
        compile_report()
        print("Analysis completed successfully.")
    elif csvdata is None:
        print("Error while reading the file. Check the CSV file provided.")

if __name__ == "__main__":
    main()
