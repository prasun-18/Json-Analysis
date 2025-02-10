# Job Data Analysis Script

## Overview

This Python script processes job listings from JSON files, extracts relevant job details, and performs data analysis to provide insights into salary distributions and job demand. The script reads JSON files, processes salary information, categorizes job skillsets, and generates analytical reports and visualizations.

## Features

- **Reads JSON job data:** Extracts job details such as title, salary, skillset, and URL.
- **Handles missing data:** Defaults missing fields to predefined values.
- **Salary extraction:** Parses salary data from text and converts it to numeric format.
- **Data visualization:** Generates a bar chart of total salary distribution across different skillsets.
- **Job analysis:** Identifies the highest-paying jobs and the most in-demand job titles.
- **Output files:** Saves analysis results in text and image formats.

## Prerequisites

Ensure the following Python packages are installed before running the script:

```sh
pip install pandas matplotlib
```

## Folder Structure

```
D:\Prasun\Dump\Gig\json\  # Folder containing JSON job data files
salary_vs_skillset.png        # Output visualization file
job_analysis_report.txt       # Text file containing job analysis results
```

## Script Details

### 1. Extract Numeric Salary

```python
def extract_numeric_salary(salary):
```

- Extracts numeric values from salary strings.
- Returns the first found numeric value or defaults to `0` if none found.

### 2. Load JSON Files

```python
def load_json_files(folder_path):
```

- Reads all JSON files from the specified folder.
- Extracts job data and handles nested structures.
- Skips invalid JSON files and logs warnings.

### 3. Process Job Data

```python
def process_data(jobs):
```

- Converts job data into a structured Pandas DataFrame.
- Handles missing fields and defaults values.
- Extracts and stores title, salary, skillset, and URL.

### 4. Plot Salary vs. Skillset

```python
def plot_salary_vs_skillset(df):
```

- Groups data by skillset and computes total salary.
- Plots a bar chart for the top 10 skillsets.
- Saves the visualization as `salary_vs_skillset.png`.

### 5. Analyze Jobs

```python
def analyze_jobs(df):
```

- Identifies the top 10 highest-paying jobs.
- Finds the most in-demand job title.
- Saves the analysis results in `job_analysis_report.txt`.

### 6. Main Function

```python
def main():
```

- Orchestrates the entire workflow.
- Loads JSON job data.
- Processes job listings into a DataFrame.
- Generates analysis and visualization outputs.
- Prints execution status messages.

## Running the Script

Run the script from the command line:

```sh
python job_analysis.py
```

The output files `salary_vs_skillset.png` and `job_analysis_report.txt` will be generated in the script directory.

## Output Files

- **salary\_vs\_skillset.png:** A bar chart visualizing total salary by skillset.
- **job\_analysis\_report.txt:** A text file containing insights on high-paying jobs and job demand.

## Error Handling

- Invalid JSON files are skipped with a warning message.
- Missing salary fields default to `0`.
- Missing job details default to predefined values.

## Author

Prasun Kumar

