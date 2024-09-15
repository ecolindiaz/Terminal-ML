#!/usr/bin/env python

'''

Every function is self documented and I have provided an example script.
If you still have any questions or suggestions just let me know on the forums - @Isaac
'''

import multiprocessing as mp
import requests
import time
import json
import sys
import concurrent.futures
import os

API_LINK = 'http://terminal.c1games.com/api'



def clean_content(content):
    '''
    Formats string from an HTML webpage from requests api.

        Args:
            * content: A string from requests.get(URL).content

        Returns:
            A string that can be parsed using JSON
    '''
    if isinstance(content, bytes):
        content = content.decode('utf-8')

        # Remove leading newline characters and any extra whitespace
    content = content.lstrip('\n').strip()

    # Additional cleaning if needed
    content = content.replace("\\'", '').replace('\\\\', '\\').replace('\\"', '')

    return content

def get_page(url):
    '''
    Get a web page using the requests library.

        Args:
            * url: A webpage url to get

        Returns:
            A requests response object
    '''
    return requests.get(url)

def get_page_content(path, url=API_LINK):
    '''
    Get the content from a webpage, for the terminal api this is a JSON string.

        Args:
            * path: A path relative to terminal's api link
            * url: The base url, default is terminal's api link

        Returns:
            A string that can be parsed using json.
    '''
    return clean_content(get_page(url+path).content)


def get_algos_matches(algo_id):
    '''
    Get the last matches that an algo has played.

        Args:
            * ID: The id of the algo

        Returns:
            A list of dictionaries, where each dictionary contains a match and it's stats.
    '''
    algo_id = int(algo_id)

    try:
        contents = get_page_content('/game/algo/{}/matches'.format(algo_id))
       # print(f"Response content for ID {ID}: {contents[:500]}")  # Print first 500 chars for debugging
        return json.loads(contents)['data']['matches']
    except json.decoder.JSONDecodeError:
        raise KeyError('"{}" is not a valid ID, must be an integer'.format(algo_id))
    except KeyError:
        raise KeyError('Unexpected response format for ID "{}"'.format(algo_id))


def get_match_ids(ID, in_leaderboard=False, verbose=False):

    return [match['id'] for match in get_algos_matches(ID)]

def get_replay(replay_id):
    url = f'https://terminal.c1games.com/api/game/replayexpanded/{replay_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = clean_content(response.content)

        # Debugging output
       # print("Cleaned content length:", len(content))
       # print("Cleaned content (first 500 chars):", content[:500])

        if not content:
            print(f"Empty content for replay ID {replay_id}")
            return None

        # Extract JSON objects using JSONDecoder
        decoder = json.JSONDecoder()
        pos = 0
        json_objects = []

        while pos < len(content):
            try:
                obj, pos = decoder.raw_decode(content, pos)
                json_objects.append(obj)
                # Move to the next valid character after decoding
                pos = content.find('{', pos)
                if pos == -1:
                    break
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e} at position {pos}")
                # Skip the position where decoding failed
                pos += 1

        if json_objects:
            return json_objects  # Return all extracted JSON objects
        else:
            print(f"No valid JSON found for replay ID {replay_id}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch replay ID {replay_id}: {e}")
    return None


'''
import concurrent.futures

initial_algo_id = 312848
algo_ids = {initial_algo_id}  # Set for faster lookup
unique_matches = set()  # Set to store unique match IDs

import concurrent.futures

import concurrent.futures

import concurrent.futures

def process_algo(algo_id):
    try:
        matches = get_algos_matches(algo_id)  # Get matches for a single algorithm ID
        new_algos = set()  # Local set to store new algos
        local_unique_matches = set()  # Local set for unique matches

        for match in matches:
            match_id = match['id']  # Extract the match ID

            if match_id not in unique_matches:
                local_unique_matches.add(match_id)
                print("match added", match_id)

                # Process winning and losing algorithm IDs
                winning_id = match['winning_algo']['id']
                losing_id = match['losing_algo']['id']

                # Check and add winning and losing algos
                if winning_id not in algo_ids:
                    new_algos.add(winning_id)
                    print("algo added", winning_id)

                if losing_id not in algo_ids:
                    new_algos.add(losing_id)
                    print("algo added", losing_id)

        return local_unique_matches, new_algos  # Correctly placed return statement
    except KeyError as e:
        print(f"Skipping ID {algo_id}: {e}")
        return None

start_time = time.time()
timeout_duration = 30 * 60

# Main loop
while True:


    if time.time() - start_time > timeout_duration:
        print("30 minutes")
        break

    new_algos_found = False
    current_algos = list(algo_ids)  # Convert set to list for iteration


    # Parallelize fetching and processing of matches
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_algo, current_algos)

        for result in results:
            if result:
                local_unique_matches, new_algos = result
                if local_unique_matches:
                    unique_matches.update(local_unique_matches)
                    new_algos_found = True

                if new_algos:
                    algo_ids.update(new_algos)
                    new_algos_found = True

    if not new_algos_found:
        break



#print("Unique matches:", unique_matches)
#print("Final algorithm IDs:", algo_ids)

      # 

#print(algo_ids)

with open('unique_matches.json', 'w') as file:
    json.dump(list(unique_matches), file, indent=4) '''

replays = []
def process_match(match_id, batch_number):
    try:
        replay = get_replay(match_id)
        if replay is not None:
            # Save replay to a file
            filename = f'replay_{match_id}.json'
            with open(os.path.join(f'batch_{batch_number}', filename), 'w') as file:
                json.dump(replay, file, indent=4)
            print(f'Replay {match_id} added to batch {batch_number}')
    except Exception as e:
        print(f"Skipping match {match_id} due to errors: {e}")

def process_matches_in_batches(matches, batch_size):
    num_batches = (len(matches) + batch_size - 1) // batch_size
    for batch_number in range(num_batches):
        batch_matches = matches[batch_number * batch_size:(batch_number + 1) * batch_size]
        os.makedirs(f'batch_{batch_number}', exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(lambda m: process_match(m, batch_number), batch_matches)
        print(f'Batch {batch_number} processed')
        # Optionally, add a delay between batches to reduce strain on your system
        time.sleep(10)  # Adjust as necessary

if __name__ == '__main__':
    with open('unique_matches.json', 'r') as file:
        matches = json.load(file)
        unique_matches = matches[:37000]  # Adjust if you want to process a subset

    batch_size = 1000  # Number of replays per batch
    process_matches_in_batches(unique_matches, batch_size)