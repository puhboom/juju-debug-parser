import re
from datetime import datetime
from collections import Counter, defaultdict

def parse_juju_debug_log(log_file):
    log_entries = []
    error_types = Counter()
    charms_with_messages = set()
    duplicate_messages = Counter()
    charm_log_counts = defaultdict(Counter)
    
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
                
                if error_type == 'WARNING':
                    charm = re.match(r'^([^\s]+).*$', component).group(1)
                    charms_with_messages.add(charm)
                
                charm_log_counts[component][error_type] += 1
        
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
    
    duplicate_logs = [log for log, count in error_types.items() if count > 1]
    print('\nNumber of duplicate messages (and their severity):')
    for log in duplicate_logs:
        duplicate_count = error_types[log]
        print(f'{log} (Severity: {duplicate_count})')
        
    return log_entries

# Usage example
log_file_path = 'juju-debug.txt'
parsed_logs = parse_juju_debug_log(log_file_path)
