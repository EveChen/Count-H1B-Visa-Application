# Insight Data Engineer Challenge
### Problem
The original description about this challenge is [here](https://github.com/InsightDataScience/h1b_statistics)


1. Get "CERTIFIED" cases
2. Get **Occupation counts** and **State counts** (*Be aware of the yearly column names)
3. Get the percentage, which is (Numbers of Occupation or State counts / Total Certified Case) * 100%
4. Sort the counts and select top 10 items
5. Output the results to ```top_10_occupations.txt``` and ```top_10_states.txt```

---

### My Approach
1. Open the file, read the data line by line, filter the "CERTIFIED" data and count the numbers of *Occupations* & *States*.

    * ###### **Key point:** I did not save the raw data to a list but only save the term frequencies to two dictionaries, which represent the numbers of *Occupations* and *States*. Also, I'm aware of the column names which vary for different year ranges. I used either `if` conditions or `set` intersections to deal with this problem. 

2. Sort two ditionaries by the built-in function and set two orders as the question requested.

    * ###### **Key point:** Sorted by **NUMBER_CERTIFIED_APPLICATIONS**. Also, in case of a tie, alphabetically sorted by **TOP_OCCUPATIONS** or **TOP_STATES**.

3. Calculate percentages and add the results to the sorting lists.

    * ###### **Key point:** Because tuples are immunicable, I change the original sort tuples to lists that we can further calculate percentages.

4. Write output files ```top_10_occupations.txt``` and ```top_10_states.txt```.

    * ###### **Key point:** Use OOP to make codes more scalable, reusable and understandable.

*Note: I did not use packages like pandas, csv, numpy etc*

---


### Results Comparison (Four versions)
* Version 1: Save the data line by line and then creates two dictionary to store **Occupation counts** and **State counts**.
* Version 2: Directly save **Occupation counts** and **State counts** to dictionary without saving the original data. 
* Version 3: Because column names vary by years, I decide to use `if` conditions to filter the columns we want. e.g. `if "soc_name" in header.lower() or "occupational_title" in header.lower()...`
* Version 4: Same as the above problem, I use `set` to find the intersected column names.


| Version  | Speed | Data Structure | OOP | Column Names (by year) |
| -------- | -------- | --------- | --------- | --------- | 
| Version 1 | 20 seconds | list | No | Fixed column names |
| Version 2 | 6 seconds | dictionary | Yes | Fixed column names |
| Version 3 | 4 ~ 5 seconds | dictionary | Yes | Filtered (with **if** statements) |
| Version 4 | 4 ~ 5 seconds | dictionary | Yes | Filtered (with **set** intersections) |


---

### Challenge - Column Names
One of the challenges in this task is that the column names vary for different year ranges. Here's the table I organized from **File Structure** pdf files. I use the following column names to filter our data by year.

* To filter **Status Column**: Use *status* as a keyword
* To filter **Occupation Column**: Use *soc_name* or *occupational_title* as keywords
* To filter **State Column**: Use *workloc1* or *worksite_state* or *state_1* as keywords


| Year  | Status Column | Occupation Column | State Column | Link |
| -------- | -------- | --------- | --------- | -------- |
| 2017 | CASE_STATUS | SOC_NAME | WORKSITE_STATE | [link](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_FY17_Record_Layout.pdf)
| 2016 | CASE_STATUS | SOC_NAME | WORKSITE_STATE | [link](https://www.foreignlaborcert.doleta.gov/docs/Performance_Data/Disclosure/FY15-FY16/H-1B_FY16_Record_Layout.pdf)  |
| 2015 | CASE_STATUS | SOC_NAME | WORKSITE_STATE | [link](https://www.foreignlaborcert.doleta.gov/docs/py2015q4/H-1B_FY15_Record_Layout.docx)  |
| 2014 | STATUS | LCA_CASE_SOC_NAME | LCA_CASE_WORKLOC1_STATE | [link](https://www.foreignlaborcert.doleta.gov/docs/py2014q4/H1B_FY14_Record_Layout.doc)  |
| 2013 | STATUS | LCA_CASE_SOC_NAME | LCA_CASE_WORKLOC1_STATE | [link](https://www.foreignlaborcert.doleta.gov/docs/lca/LCA_Record_Layout_FY13.doc)  |
| 2012 | STATUS | LCA_CASE_SOC_NAME | LCA_CASE_WORKLOC1_STATE | [link](https://www.foreignlaborcert.doleta.gov/docs/py2012_q4/LCA_Record_Layout_FY12.doc)  |
| 2011 | STATUS | LCA_CASE_SOC_NAME | LCA_CASE_WORKLOC1_STATE | [link](https://www.foreignlaborcert.doleta.gov/pdf/quarter_4_2011/H-1B_Record_Layout_FY11_Q4.doc)  |
| 2010 | STATUS | LCA_CASE_SOC_NAME | LCA_CASE_WORKLOC1_STATE | [link](https://www.foreignlaborcert.doleta.gov/pdf/H-1B_Record_Layout_FY10.doc)  |
| 2009 | STATUS | LCA_CASE_SOC_NAME | LCA_CASE_WORKLOC1_STATE | [link](https://www.foreignlaborcert.doleta.gov/pdf/H1B_Layout_FY09.doc)  |
| 2008 | Approval_Status | Occupational_Title | State_1 | [link](https://www.foreignlaborcert.doleta.gov/pdf/H-1B_Record_Layout_FY08.doc)  |

Note: There are two similar column names for filtering the State: *LCA_CASE_WORKLOC1_STATE* and *LCA_CASE_WORKLOC2_STATE*. Because *LCA_CASE_WORKLOC2_STATE* has more missing values, I decide to use *LCA_CASE_WORKLOC1_STATE* to filter our State column name.



---

### How to Execute
Please run ```./run.sh``` and you will see two output files in the output folder. Please note that the default version is **version 4**, which is the fastest version. If you want to run other versions, please change the code `./src/H1BCounts_version4.py` in file `run.sh`.

---

### Plan for the Future
#### **Question: Find the average certified amount for each occupations**
1. Example
  * year 2016: ("job1", 150), ("job2", 100), ("job3", 50)
  * year 2015: ("job1", 200), ("job2", 80)

2. Record frequency - **mapValues**
  * year 2016: ("job1", (150, 1)), ("job2", (100, 1)), ("job3", (50, 1))
  * year 2015: ("job1", (200, 1)), ("job2", (80, 1))
  

3. Sum the values by key - **reduceByKey**
("job1", (350, 2)), ("job2", (180, 2)), ("job3", (50, 1))

4. Calculate the average certified amount - **mapValues & collect**
("job1", 175), ("job2", 90), ("job3", 50)

---

### Note
Because I'm really interested in how to efficiently tackle this problem, I add more details about how to decrease the time/space complexity and even think about a future case after the submission deadline. Also, I would like to express my appreciation about giving me this opportunity to tackle this interesting challenge. I do enjoy it very much and thanks for reading this readme file!
