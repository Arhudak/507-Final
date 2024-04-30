Scientific Journals Network Project: Data Sources README

Data Source: 
Journal Dataset
Origin: 
This data was originally accessed through:
https://www.kaggle.com/datasets/alijalali4ai/scimagojr-scientific-journals-dataset
This data was originally named ScimagoJR 2022.csv.
While there is data from the years 1999-2022, this project used the most recent year available (2022).

Format: The dataset is in CSV (Comma-Separated Values) format.

Access: Data was accessed using the pandas library in Python with the read_csv function. 
The top 1000 rows were selected for analysis as the full dataset (about 25,000 rows) created long wait times. 
Here is the relevant code snippet for accessing the data:

journal = pd.read_csv('journal2022.csv').head(1000)

Summary of Data:

The dataset contains journal information across various fields. Specifically, the following 21 variables are included in the dataset:
Rank
Sourceid
Title
Type
Issn
SJR (Scientific Journal Rankings)
SJR Best Quartile
H index
Total Docs. (2022)
Total Docs. (3 years)
Total Refs.
Total Cites (3 years)
Citable Docs. (3 years)
Cites / Doc. (2 years)
Ref. / Doc.
Country
Region
Publisher
Coverage
Categories
Areas

Brief Description of Data: The dataset is a list of journals with various metrics relevant to journal quality and productivity, such as the SJR ranking, H-index, and citation counts. 
It includes metadata like ISSNs, publisher information, and subject categories. 
The entries represent aggregate data to help understand publishing patterns across different regions and categories.

General Usage Notes
The dataset should be located in the same directory as your Python script or explicitly referenced with the correct filepath in the pd.read_csv() function.
Given the nature of the data, confirming the dataset's currency and updating it periodically will be necessary for long-term projects.
