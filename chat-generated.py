import re
from datetime import datetime
from collections import Counter

def parse_juju_debug_log(log_file):
    log_entries = []
    error_types = Counter()
    timestamps = []
    with open(log_file, 'r') as f:
        log_lines = f.readlines()
        for line in log_lines:
            match = re.match(r'^([^:]+): (\d{2}:\d{2}:\d{2}) (\S+) (.*)$', line)
            if match:
                component = match.group(1)
                timestamp = match.group(2)
                error_type = match.group(3)
                message = match.group(4)
                log_entry = {'component': component, 'timestamp': timestamp, 'error_type': error_type, 'message': message}
                log_entries.append(log_entry)
                error_types[error_type] += 1
                timestamps.append(datetime.strptime(timestamp, '%H:%M:%S'))
    
    return log_entries, error_types, timestamps

# Usage example
log_file_path = 'juju-debug.txt'
parsed_logs, error_types, timestamps = parse_juju_debug_log(log_file_path)

# Print the number of error message types
print('Error Message Types:')
for error_type, count in error_types.items():
    print(f'{error_type}: {count}')

# Print other summarizing statistics
total_entries = len(parsed_logs)
total_errors = sum(error_types.values())
earliest_timestamp = min(timestamps)
latest_timestamp = max(timestamps)

print(f'Total log entries: {total_entries}')
print(f'Total error entries: {total_errors}')
print(f'Earliest timestamp: {earliest_timestamp}')
print(f'Latest timestamp: {latest_timestamp}')
