import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import re

# Define the folder path
FOLDER_PATH = "D:\Prasun\Dump\Gig\json"

def extract_numeric_salary(salary):
    """Extract numeric salary from text, handling different formats"""
    numbers = re.findall(r"\d+", salary.replace(",", ""))
    return int(numbers[0]) if numbers else 0  # Default to 0 if no number is found

def load_json_files(folder_path):
    """Reads all JSON files in a folder and extracts job data"""
    all_jobs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for job_data in data:
                        all_jobs.extend(job_data.get("jobs", []))  # Handle nested structure
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
    return all_jobs

def process_data(jobs):
    """Extracts relevant job details and handles missing data"""
    job_list = []
    for job in jobs:
        salary_numeric = extract_numeric_salary(job.get("salary", "0"))
        job_list.append({
            "title": job.get("title", "Unknown Title"),
            "salary": salary_numeric,
            "skillset": job.get("skillset", "Not Specified"),
            "url": job.get("url", "No URL")
        })
    return pd.DataFrame(job_list)

def plot_salary_vs_skillset(df):
    """Plots a bar chart of total salary by skillset"""
    skillset_salary = df.groupby("skillset")["salary"].sum().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    skillset_salary.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Total Salary by Skillset (Top 10)", fontsize=14)
    plt.xlabel("Skillset", fontsize=12)
    plt.ylabel("Total Salary ($)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Save the figure
    plt.savefig("salary_vs_skillset.png")
    plt.show()

def analyze_jobs(df):
    """Finds highest-paying jobs and most demanding titles"""
    # Get top 10 highest-paying jobs
    top_10_jobs = df.sort_values(by="salary", ascending=False).head(10)
    
    # Identify the most in-demand job title
    most_common_title = df["title"].value_counts().idxmax()
    
    # Save results to a text file
    with open("job_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write("Top 10 Highest-Paying Jobs:\n")
        for idx, row in top_10_jobs.iterrows():
            f.write(f"\n{idx+1}. {row['title']} - ${row['salary']}\n   Skillset: {row['skillset']}\n   URL: {row['url']}\n")
        
        f.write("\nMost Demanding Job Title: " + most_common_title + "\n")

def main():
    """Main function to execute the workflow"""
    print("Loading job data from JSON files...")
    jobs = load_json_files(FOLDER_PATH)
    
    print(f"Total jobs found: {len(jobs)}")
    
    if not jobs:
        print("No jobs found. Exiting...")
        return

    df = process_data(jobs)
    
    print("Generating analytics...")
    plot_salary_vs_skillset(df)
    analyze_jobs(df)
    
    print("Analysis completed. Check 'salary_vs_skillset.png' and 'job_analysis_report.txt'!")

if __name__ == "__main__":
    main()
