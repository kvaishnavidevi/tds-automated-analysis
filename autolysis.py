# /// script
# dependencies = [
#   "pandas",
#   "numpy",
#   "matplotlib",
#   "seaborn",
#   "charset_normalizer",
#   "pathlib",
#   "scikit-learn",
#   "scipy",
#   "plotly",
#   "markdown",
#   "openai==0.28",
# ]
# ///

import time
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

if len(sys.argv) < 2:
    print("Usage: uv run autolysis.py <filename.csv>")
    sys.exit(1)
file_path = sys.argv[1]
markdown_content = []
final_md_content = []
openai.api_key = os.environ["AIPROXY_TOKEN"]
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"

# Function to detect encoding, Load and Prepare Dataset
def load_dataset(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = detect(raw_data)
            encoding = result['encoding']
        print(f"Detected encoding: {encoding}")
        data = pd.read_csv(file_path, encoding=encoding)
        print(f"Data read successfully from: {file_path}")
        return data
    except Exception as e:
        print(f"Error loading/determining the file encoding: {e}")
        return None

# Remove un-necssary data before sending LLM/analysis
def filtered_dataset(csvdata):
    try:
        column_name_keywords = {"url", "image", "website", "link", "rawdata","site","web"}
        filtered_data = csvdata.loc[:, ~csvdata.columns.str.contains('|'.join(column_name_keywords), case=False)]
        print("Filtered un-necessary columns")
        return filtered_data
    except Exception as e:
        print(f"Error while filtering columns: {e}")
        return None

# Fetch sample records
def sample_dataset(csvdata):
    try:
        if len(csvdata.head(50)) >= 50:
            csvdata_sample = csvdata.sample(50).to_string()
        else:
            csvdata_sample = csvdata.to_string()
        print("Sample records fetch successful")
        return csvdata_sample
    except Exception as e:
        print(f"Error while getting sample records: {e}")
        return None

# Perform basic analysis
def basic_analysis(csvdata,numerical_cols):
    try:
        data_datatypes = csvdata.dtypes.to_string()
        data_sample = sample_dataset(csvdata)
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
        markdown_content.append("### Exploratory Data Analysis")
        markdown_content.append(f"### CSV File Name: {file_path}")
        markdown_content.append("### Dataset Overview")
        markdown_content.append(f"- **Shape:** {csvdata.shape[0]} rows and {csvdata.shape[1]} columns")
        markdown_content.append("### Columns and Data Types:")
        markdown_content.append(f"```plaintext\n{data_datatypes}\n```")
        markdown_content.append("### Sample Rows:")
        markdown_content.append(f"```plaintext\n{data_sample}\n```")
        markdown_content.append("### Basic Statistics")
        markdown_content.append(f"```plaintext\n{data_stat}\n```")
        markdown_content.append("### Missing Values")
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
        print("Completed Basic Analysis")
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
           print("Completed Outlier Analysis")
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
                        "hierarchical_clustering":hier_clust,
        }
        print("Completed Advanced Analysis")
        return clustering_summary
    except Exception as e:
        print("Error while performing advanced analysis: %s" % e)
        traceback.print_exc()


# Visualize Data Distributions and Relationships
def generate_visualizations(numerical_data,categorical_cols):
    try:
        markdown_content.append("## Visualizations")
        if(numerical_data.shape[1]>10):
            numerical_data_filtered = numerical_data[numerical_data.columns[:10]]
        else:
            numerical_data_filtered = numerical_data
        sns.pairplot(numerical_data_filtered)
        plt.savefig("pairplot.png")
        plt.close()
        markdown_content.append("![Pairplot](pairplot.png)")
        print("Completed Visualizations")
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
            print("Completed Hierarchical Clustering")
            return linked
    except Exception as e:
        print("Error while performing Hierarchical Clustering: %s" % e)
        traceback.print_exc()

# Limit 2000 words only.
def llm_request_shorten(llm_summary):
    word_split = llm_summary.split()
    llm_shorten_request = llm_summary
    if len(word_split)>2000:
        llm_shorten_request = " ".join(word_split[:2000])
    # construct as a conv to llm
    conversation = [
                {"role": "system", "content": "assume you are a data storyteller based csvfile for data analysis"},
                {"role": "user", "content": llm_shorten_request},
    ]

    return conversation

# Interact with LLM
def prepare_llm_request(analysis_summary,adv_analysis_summary):
    llm_summary_text = f"""
    Assume that you are data storyteller. Based on the following, write an insightful and engaging narrative:
    The dataset contains {analysis_summary['shape'][0]} rows and {analysis_summary['shape'][1]} columns.
    Columns: {analysis_summary['columns']}
    File Name: {analysis_summary['file_name']}
    Key findings include:
    - Missing values: {analysis_summary['missing_values']}
    - Top correlations: {list(analysis_summary['correlation_matrix'])[:5]}
    - Numerical data summary: {analysis_summary['numerical_summary']}
    - Basic Statistics: {analysis_summary['basic_statistics']}
    - Advance Analysis:
        Kmeans : {adv_analysis_summary['kmeans']}
        Hierarchical Clustering : {adv_analysis_summary['hierarchical_clustering']}
    - Outliers: {adv_analysis_summary['outliers']}
    - Sample Rows:
        {analysis_summary['sample_rows']}
    """
    return llm_summary_text

# LLM Call
def call_llm_for_insights(llm_request, context="csvfile data analysis", max_tokens=2000):
    try:
        response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=llm_request,
        temperature=0.7,
        max_tokens=max_tokens,
        )
        print(f"LLM Response {response}")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error occurred while fetching insights from LLM: {e}")
        traceback.print_exc()

# Compile Final Report
def compile_report(llm_response):
    try:
        final_md_content.append(llm_response)
        final_md_content.append(markdown_content)
        flat_list = []
        for item in final_md_content:
            if isinstance(item, list):
                flat_list.append("\n".join(item))
            else:
                flat_list.append(str(item))
        with open("README.md", "w") as f:
            f.write("\n".join(flat_list))
        print("Report saved to README.md")
    except Exception as e:
        print(f"Error occurred while writing final README.md file: {e}")
        traceback.print_exc()

# Main Function
def main():
    start_time = time.time()
    csvdata = load_dataset(file_path)
    if csvdata is not None:
        csvdata = filtered_dataset(csvdata)
        numerical_cols = csvdata.select_dtypes(include=np.number)
        numerical_cols_list = numerical_cols.columns.tolist()
        categorical_cols = csvdata.select_dtypes(include=['object']).columns
        analysis_summary = basic_analysis(csvdata,numerical_cols_list)
        outliers = outlier_analysis(csvdata,numerical_cols_list)
        clustering_summary = perform_clustering(csvdata,numerical_cols,categorical_cols)
        generate_visualizations(numerical_cols,categorical_cols)
        adv_analysis_summary = {
                        "outliers": outliers,
                        "kmeans": clustering_summary['kmeans'],
                        "hierarchical_clustering": clustering_summary['hierarchical_clustering'],
                }
        llm_request = prepare_llm_request(analysis_summary,adv_analysis_summary)
        final_llm_request = llm_request_shorten(llm_request)
        llm_response = call_llm_for_insights(final_llm_request)
        compile_report(llm_response)
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Analysis completed successfully in {runtime} seconds")
    elif csvdata is None:
        print("Error while reading the file. Check the CSV file provided.")

if __name__ == "__main__":
    main()
