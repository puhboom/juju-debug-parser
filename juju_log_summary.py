import re
import argparse
from collections import Counter, defaultdict

def juju_log_summary(log_file, charm=None):
    charm_counts = defaultdict(Counter)
    unique_messages = set()
    duplicate_messages = Counter()
    error_types = Counter()
    machines_with_warnings = set()
    log_totalizer = int(0)

    with open(log_file, 'r') as f:
        log_lines = f.readlines()
        for line in log_lines:
            # |||--- STEP 1 ---||| 
            # use regex to screen for the log string format of interest
            # machine: HH:MM:SS ERRORTYPE module.some.where error message...
            match = re.match(r'^([^:]+): (\d{2}:\d{2}:\d{2}) (\S+) (.*)$', line)
            if not match:
                continue # bail on non-matching strings
            
            # |||--- STEP 2 ---||| 
            # map the segments of the message to their fields
            log_totalizer += 1
            machine = match.group(1)
            # timestamp = match.group(2)            
            error_type = match.group(3)
            message = match.group(4)
            
            # |||--- STEP 3 ---||| 
            error_types[error_type] += 1            # increment error type counters
            charm_counts[machine][error_type] += 1  # increment per machine & type counters
            
            if message in unique_messages:          # check if message seen before
                duplicate_messages[message] += 1    # increment duplicate message counter if pre-existing
            else:
                unique_messages.add(message)        # else, add to unique message set

            if error_type == 'WARNING':             # if it's a WARNING
                machines_with_warnings.add(machine) # make sure machine is in set of machines with warnings
    
    # |||--- STEP 4 ---|||
    if charm:                                                       # separate print section for charm specific
        print(f'Parsing logs for {charm}:')
        total_logs = sum(charm_counts[charm].values())
        print(f'Total log messages for {charm}: {total_logs}')
        duplicate_logs = [log for log, count in duplicate_messages.items() if count > 1]
        
        print('\nDuplicate messages:')
        for log in duplicate_logs:
            duplicate_count = duplicate_messages[log]
            print(f'Type: {error_type} Count: {duplicate_count} Message: {log[0:128]}')   # truncate message for ease of use
        
        print(f'Proportions of log messages for {charm}:')
        for error_type, count in charm_counts[charm].items():
            proportion = count / total_logs
            print(f'{error_type}: {proportion * 100:.2f}%')
        print('')

    else:    
        print('Parsing all charms.')
        if len(machines_with_warnings) > 0:
            print('\nCharms that produced a WARNING:')
            for machine in machines_with_warnings:
                print(f'- {machine}')
        else:
            print('\nNo charms produced WARNINGs.')

        print('\nNumber of each severity of message:')
        for error_type, count in error_types.items():
            print(f'{error_type}: {count}')
        
        duplicate_logs = [log for log, count in duplicate_messages.items() if count > 1]
        print('\nDuplicate messages:')
        for log in duplicate_logs:
            duplicate_count = duplicate_messages[log]
            print(f'Type: {error_type} Count: {duplicate_count} Message: {log[0:128]}')   # truncate message for ease of use

        for machine, log_count in charm_counts.items():
            machine_total_logs = sum(log_count.values())
            print(f'\nTotal log messages for {machine}: {machine_total_logs}')
            # print(f'Proportions of log messages for {machine}:')
            for error_type, count in log_count.items():
                proportion = count / machine_total_logs
                print(f'{count} were {error_type}: {proportion * 100:.2f}%')

        print(f'\nTotal number of log messages: {log_totalizer}')
    return charm_counts

# |||--- STEP 5 ---|||
# Parse command-line arguments
parser = argparse.ArgumentParser(description='Parse Juju debug log files.')
parser.add_argument('log_file', type=str, help='Path to the Juju debug log file')
parser.add_argument('-c', '--charm', type=str, help='Specify a specific charm to parse')
args = parser.parse_args()

# Usage example
log_summary = juju_log_summary(args.log_file,args.charm)