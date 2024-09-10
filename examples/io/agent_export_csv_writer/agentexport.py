#!/usr/bin/env python
from tenable.io import TenableIO
from csv import DictWriter
import click, logging

# Function to format agent groups into a single string
def agent_groups(groups):
    # If no groups is None return None
    if groups is None:
        return None
    else:
        # Otherwise, create a list to store formatted group strings
        output = []
        for group in groups:
            # Format each group as "name (id)"
            output.append(f"{group['name']} ({group['id']})")
        # Join all formatted group strings with a '|' delimiter
        output = '|'.join(output)
        return output

# Function to handle agent health status
def agent_health(health):
    # If health status is not provided, return "UNKNOWN"
    if health is None:
        return "UNKNOWN"
    else:
        # Otherwise, return the provided health status
        return health

# Define a Click command-line interface
@click.command()
@click.argument('output', type=click.File('w'))  # Output file for the CSV
@click.option('--access-key', '-s', help='Tenable.io API Access Key')  # API Access Key option
@click.option('--secret-key', '-a', help='Tenable.io API Secret Key')  # API Secret Key option
@click.option('--health', '-e', default=None, type=click.STRING, help='Comma separated list of agent Health')
@click.option('--debug', '-d', is_flag=True, default=False, help='Enable debugging')  # Debug flag
def cli(output, access_key, secret_key, health, debug):
    '''
    Agent -> CSV Writer

    Exports agents to a CSV in the current directory.
    '''
    # Enable logging, with different levels based on the debug flag
    if debug:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', handlers=[logging.StreamHandler()])
        
    # Initialize TenableIO API client
    tvm = TenableIO(access_key, secret_key)

    # If 'health' is not None, split it by commas, convert each item to uppercase, and log the specific agents being exported
    if health: 
        logging.info(f'Exporting {health} agents') 
        health = [item.upper() for item in health.replace(" ", "").split(',')]
        
    else:
        # Log that all agents are being exported since 'health' is None or empty
        logging.info(f'Exporting all agents') 

    # Define the fields/columns for the CSV
    fields = [
        'id', 
        'uuid', 
        'name', 
        'platform', 
        'distro', 
        'ip', 
        'core_build', 
        'core_version', 
        'linked_on', 
        'last_connect', 
        'status', 
        'health',
        'supports_remote_logs', 
        'network_uuid', 
        'network_name', 
        'profile_uuid', 
        'profile_name', 
        'supports_remote_settings', 
        'groups'
    ]
    
    # Create a CSV writer object
    writer = DictWriter(output, fields, extrasaction='ignore')
    writer.writeheader()  # Write the header row to the CSV

    # Iterate over agents from TenableIO API with a limit of 200 per request
    # and count the number of agents with the count variable
    counter = 0
    for agent in tvm.agents.list(limit=200):
        # Format the agent's groups and set the health status
        agent['groups'] = agent_groups(agent.get('groups'))
        agent['health'] = agent_health(agent.get('health_state_name'))
        # Write the agent data to the CSV based on the specified health status
        if health:
            if agent['health'] in health:
                writer.writerow(agent)
                counter += 1
        else:
            writer.writerow(agent)
            counter += 1

    logging.info(f'Finished writing {counter} agents to {output.name}')

# Entry point for the script
if __name__ == '__main__':
    cli()
