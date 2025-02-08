import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import matplotlib.font_manager as fm  # Import font manager

# Set a font that supports special characters
plt.rcParams["font.family"] = "Arial"

def analyze_json_data(file_path):
    """Reads and extracts job data from JSON files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error processing {file_path}: {e}")
        return None

    if not isinstance(data, list):
        print(f"Warning: JSON in {file_path} is not a list. Skipping file.")
        return None

    all_jobs = []
    for item in data:
        if isinstance(item, dict) and 'jobs' in item:
            all_jobs.extend(item['jobs'])
        elif isinstance(item, dict):
            all_jobs.append(item)
    
    return pd.DataFrame(all_jobs)

def generate_analytics(df, file_name):
    """Generates analytics and plots from the DataFrame."""
    
    if df.empty:
        return "No job data found for analysis.", None, None

    analytics_text = f"## Job Market Analytics for {file_name}\n\n"

    total_jobs = len(df)
    analytics_text += f"Total Jobs: {total_jobs}\n\n"

    salary_plot_filename = None
    skills_plot_filename = None

    for column in df.columns:
        analytics_text += f"### Analysis of {column}\n\n"

        if pd.api.types.is_numeric_dtype(df[column]):
            desc = df[column].describe()
            analytics_text += f"{desc.to_string()}\n\n"

            fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
            df[column].hist(bins=20, ax=ax)
            ax.set_title(f"Distribution of {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Count")
            plot_filename = f"{os.path.splitext(os.path.basename(file_name))[0]}_{column}_distribution.png"
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.close(fig)

            if column == 'salary':
                salary_plot_filename = plot_filename
            elif column == 'experience_required':
                skills_plot_filename = plot_filename

        elif pd.api.types.is_object_dtype(df[column]):  
            value_counts = df[column].value_counts().head(10)
            analytics_text += f"Top 10 {column}:\n"
            for value, count in value_counts.items():
                analytics_text += f"- {value}: {count}\n"

            fig, ax = plt.subplots(figsize=(12, 8), constrained_layout=True)
            value_counts.plot(kind='bar', ax=ax)
            ax.set_title(f"Top 10 {column} Distribution")
            ax.set_xlabel(column)
            ax.set_ylabel("Count")
            plt.xticks(rotation=45, ha='right')
            plot_filename = f"{os.path.splitext(os.path.basename(file_name))[0]}_{column}_distribution.png"
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.close(fig)

            if column == 'skillset':
                skills_plot_filename = plot_filename
            elif column == 'title':
                salary_plot_filename = plot_filename

        else:
            analytics_text += f"No specific analysis implemented for {column} (data type: {df[column].dtype})\n\n"

    return analytics_text, salary_plot_filename, skills_plot_filename

def add_text_page(pdf, text, fontsize=10):
    """Adds formatted text to the PDF report."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')
    ax.text(0.1, 0.9, text, ha='left', va='top', wrap=True, fontsize=fontsize)
    pdf.savefig(fig)
    plt.close(fig)

def create_pdf_report(file_path, analytics_text, salary_plot_filename=None, skills_plot_filename=None):
    """Generates a PDF report with analytics and plots."""
    
    pdf_file_name = os.path.splitext(os.path.basename(file_path))[0] + ".pdf"
    with PdfPages(pdf_file_name) as pdf:

        # Add text analytics to PDF
        add_text_page(pdf, analytics_text)

        # Add plots if they exist
        for plot_filename in [salary_plot_filename, skills_plot_filename]:
            if plot_filename and os.path.exists(plot_filename):
                fig = plt.figure()
                plt.imshow(plt.imread(plot_filename))
                plt.axis('off')
                pdf.savefig(fig)
                plt.close(fig)
            else:
                print(f"Warning: {plot_filename} not found, skipping.")

# Example usage:
json_files_path = "D:\Prasun\Dump\jobs\jobs\json"  # Current directory
for filename in os.listdir(json_files_path):
    if filename.endswith(".json"):
        file_path = os.path.join(json_files_path, filename)
        df = analyze_json_data(file_path)
        if df is not None:
            analytics, salary_plot, skills_plot = generate_analytics(df, filename)
            if analytics:
                create_pdf_report(file_path, analytics, salary_plot, skills_plot)
                print(f"Report generated for {filename}")
        else:
            print(f"Skipping {filename} due to errors.")
