# Version 4: Fix column names problem by using the set intersections

import sys
import time

class H1BCounts:
    def __init__(self, input_file, output_top10_job, output_top10_state):
        self.total_certified = 0
        self.input_file = input_file
        self.output_top10_job = output_top10_job
        self.output_top10_state = output_top10_state
        self.job_dict = {}
        self.state_dict = {}
        self.sort_job = []
        self.sort_state = []
        
        # Create both two headers for writing files afterward
        self.job_header = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
        self.state_header = "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
    
    

    def read_data(self, input_file):
        
        with open(self.input_file, "r") as f:
            headers = f.readline().split(";")
            
            # Yearly column names for filtering the column names we need
            colnames = {'status_col': ['CASE_STATUS', 'STATUS', 'Approval Status'],
            'job_col': ['SOC_NAME', 'LCA_CASE_SOC_NAME', 'Occupational_Title'],
            'state_col': ['WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE', 'State_1']}
            
            status_header = list(set(colnames['status_col']) & set(headers))[0]
            job_header = list(set(colnames['job_col']) & set(headers))[0]
            state_header = list(set(colnames['state_col']) & set(headers))[0]
            
            for line in f:
                values = line.split(";")
                raw_data = dict(zip(headers, values))
                
                # Filter the "CERTIFIED" case
                if raw_data[status_header] != "CERTIFIED":
                    continue
                
                # Use two dictionary to save the specific term frequency
                self.job_dict[raw_data[job_header]] = self.job_dict.get(raw_data[job_header], 0) + 1
                self.state_dict[raw_data[state_header]] = self.state_dict.get(raw_data[state_header], 0) + 1
                self.total_certified += 1


    # Sort top 10 job counts and state counts in a descending order
    def sort_top10(self):
        self.sort_job = sorted(self.job_dict.items(), key = lambda s: (-s[1], s[0]))[:10]
        self.sort_job = [list(elem) for elem in self.sort_job]
        
        self.sort_state = sorted(self.state_dict.items(), key = lambda s: (-s[1], s[0]))[:10]
        self.sort_state = [list(elem) for elem in self.sort_state]


    # Calculate the percentage rounding to 1st digit: (Numbers of specific counts / Total "CERTIFIED" case) * 100
    def percentage(self):
        for i in range(len(self.sort_job)):
            self.sort_job[i].append(round(self.sort_job[i][1] / self.total_certified * 100, 1))
        
        for i in range(len(self.sort_state)):
            self.sort_state[i].append(round(self.sort_state[i][1] / self.total_certified * 100, 1))


    # Output files
    def write_output_job(self):
        with open(self.output_top10_job, 'w') as f:
            f.write(self.job_header + '\n')
            for row in self.sort_job:
                output = row[0] + ';' + str(row[1]) + ';' + str(row[2]) + '%'
                f.write(output + '\n')

    def write_output_state(self):
        with open(self.output_top10_state, 'w') as f:
            f.write(self.state_header + '\n')
            for row in self.sort_state:
                output = row[0] + ';' + str(row[1]) + ';' + str(row[2]) + '%'
                f.write(output + '\n')

# Our main function
def H1BCount(input_file, output_top10_job, output_top10_state):
    t1 = time.time()
    print("Start processing the data...")
    result = H1BCounts(input_file, output_top10_job, output_top10_state)
    
    # Load the csv file and generate two dictionary to record the individual counts for both the occupations and states
    result.read_data(input_file)
    
    t2 = time.time()
    print("It takes {} seconds to clean the data".format(round(t2 - t1, 2)))
    
    # Sort top 10 occupations and states based on the number of individual counts (descending order) and the names (alphabetical order)
    result.sort_top10()
    
    # Use "percentage" function to calculate: (Numbers of specific counts / Total "CERTIFIED" case) * 100
    result.percentage()
    
    # Output two txt files: top_10_occupations.txt and top_10_states.txt
    result.write_output_job()
    result.write_output_state()
    print("Congratulation! Two txt files have been generated!")

# If this py file is called, all the codes will be executed; if this py file is imported to other py files, then the codes below this if statement will not be executed.
if __name__ == '__main__':
    # List of my command line arguments
    H1BCount(sys.argv[1], sys.argv[2], sys.argv[3])



