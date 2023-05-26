import argparse
import re
from datetime import datetime
from collections import Counter, defaultdict

def parse_juju_debug(log_file, charm=None):
    log_entries = []
    error_types = Counter()
    charms_with_messages = set()
    unique_messages = set()
    duplicate_messages = Counter()
    charm_log_counts = defaultdict(Counter)
    
    with open(log_file, 'r') as f:
        log_lines = f.readlines()
        for line in log_lines:
            match = re.match(r'^([^:]+): (\d{2}:\d{2}:\d{2}) (\S+) (.*)$', line)
            if not match:
                continue
            
            component = match.group(1)
            timestamp = match.group(2)
            error_type = match.group(3)
            message = match.group(4)
            log_entry = {'component': component, 'timestamp': timestamp, 'error_type': error_type, 'message': message}
            log_entries.append(log_entry)
            error_types[error_type] += 1
            
            if error_type == 'WARNING':
                charm = re.match(r'^([^\s]+).*$', component).group(1)
                charms_with_messages.add(charm)
            
            charm_log_counts[component][error_type] += 1
            if message in unique_messages:
                duplicate_messages[message] = True
            else:
                unique_messages.add(message)
    
    if charm:
        print(f'Parsing logs for {charm}:')
        total_logs = sum(charm_log_counts[charm].values())
        print(f'Total log messages for {charm}: {total_logs}')
        print(f'Proportions of log messages for {charm}:')
        for error_type, count in charm_log_counts[charm].items():
            proportion = count / total_logs
            print(f'{error_type}: {proportion * 100:.2f}%')
        print('')
    else:
        print('Parsing logs for all charms:')
        for charm, log_count in charm_log_counts.items():
            total_logs = sum(log_count.values())
            print(f'Total log messages for {charm}: {total_logs}')
            print(f'Proportions of log messages for {charm}:')
            for error_type, count in log_count.items():
                proportion = count / total_logs
                print(f'{error_type}: {proportion * 100:.2f}%')
            print('')
    
    total_logs = len(log_entries)
    print(f'Total log messages: {total_logs}')
    
    print('\nCharms that produced messages:')
    for charm in charms_with_messages:
        print(f'- {charm}')
    
    print('\nNumber of each severity of message:')
    for error_type, count in error_types.items():
        print(f'{error_type}: {count}')
    
    total_duplicates = sum(duplicate_messages.values())
    print(f'\nTotal number of duplicate messages: {total_duplicates}')
    
    return log_entries

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Parse Juju debug log files.')
parser.add_argument('log_file', type=str, help='Path to the Juju debug log file')
parser.add_argument('-c', '--charm', type=str, help='Specify a specific charm to parse')
args = parser.parse_args()

# Usage example
parsed_logs = parse_juju_debug(args.log_file, args.charm)
