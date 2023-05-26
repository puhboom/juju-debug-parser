import re
import argparse
from collections import Counter

def count_error_types(log_file, charme=None):
    severityCounter = Counter()
    charmsCount = Counter()


    with open(log_file, 'r') as f:
        log_lines = f.readlines()
        for line in log_lines:
            # use regex to screen for the log string format of interest
            match = re.match(r'^([^:]+): (\d{2}:\d{2}:\d{2}) (\S+) (.*)$', line)
            if match:
                # here's where we map the segments of the message to their fields
                charm = match.group(1)

                error_type = match.group(3)
                severityCounter[error_type] += 1
    
    return severityCounter

# Parse command-line arguments
# parser = argparse.ArgumentParser(description='Parse Juju debug log files.')
# parser.add_argument('log_file', type=str, help='Path to the Juju debug log file')
# parser.add_argument('-c', '--charm', type=str, help='Specify a specific charm to parse')
# args = parser.parse_args()

# Usage example
log_file_path = 'juju-debug.txt'
error_counts = count_error_types(log_file_path)
print(error_counts)
