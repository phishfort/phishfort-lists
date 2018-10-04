import requests
import json
import os
from shutil import copyfile
import argparse
import sys
from settings import urlscanapikey
import time
from pprint import pformat
from tldextract import tldextract
from datetime import datetime

def urlscan_screenshot(url):
    #First, let's see if it's been indexed already.
    domain = tldextract.extract(url).fqdn
    print("\t\t[-] Looking up domain screenshot {}".format(domain))
    if lookup_screenshot(url):
        print ("\t\t[-] Already screenshotted...")
        return
    else:
        print ("\t\t[-] No screenshot yet, sending to urlscan...")
        urlscanio = "https://urlscan.io/api/v1/scan/"
        key = urlscanapikey
        headers  = {
            "Content-Type" : "application/json",
            "API-Key" : key
        }
        data = {
            "url" : url,
            "public" : "on"
        }
        try:
            r = requests.post(urlscanio, headers=headers, json=data)
            save_screenshot(url, r.json()['result'])
        except Exception as e:
            print (e)
            pass
        time.sleep(2)

def fetch_screenshots():
    if os.path.exists("screenshots/mapping.json"):
        f = open("screenshots/mapping.json", 'r')
        current = f.read()
        f.close()
        current = json.loads(current)
        return current
    else:
        return False

def lookup_screenshot(url):
    domain = tldextract.extract(url).fqdn
    if os.path.exists("screenshots/mapping.json"):
        f = open("screenshots/mapping.json", 'r')
        current = f.read()
        f.close()
        current = json.loads(current)
        return current.get(domain, False)
    else:
        return False

def save_screenshot(url, urlscanurl):
    domain = tldextract.extract(url).fqdn
    if os.path.exists("screenshots/mapping.json"):
        f = open("screenshots/mapping.json", 'r')
        current = f.read()
        f.close()
        current = json.loads(current)
        current[domain] = urlscanurl
        f = open("screenshots/mapping.json", 'w')
        current = f.write(json.dumps(current))
        f.close()
    else:
        current = {domain : urlscanurl}
        f = open("screenshots/mapping.json", 'w')
        current = f.write(json.dumps(current))
        f.close()

def ensure_that_domain_file_exists_and_is_valid_json():
    '''
    Make sure that we pass EAL nicely formatted data and that the file exists.
    '''
    file_exists = os.path.exists("blacklists/domains.json")
    if not file_exists:
        create_file = open("blacklists/domains.json", 'w')
        create_file.close()
    try:
        domains = open("blacklists/domains.json", 'r')
        contents = domains.read()
        domains.close()
        json_contents = json.loads(contents)
        return json_contents
    except:
        #Create a backup of the current domains file, then place and empty
        #json file there.
        print ('''
        The domains file was not json compliant, making a backup and then
        replacing the domain file with empty json array.
        ''')
        copyfile("blacklists/domains.json", "blacklists/domains.json.bak")
        create_file = open("blacklists/domains.json", 'w')
        create_file.write("[]\n")
        create_file.close()
        return False

def preprocess_domain(domain):
    '''
    Tidy up the domain for processing.

    :param domain: domain to clean
    :return: cleaned up domain
    '''
    #Lets ensure that it's in an nice string format for idna

    try:
        domain = domain.strip("*.").strip(".").strip().lower()
        if domain.startswith("www."):
            domain = domain[4:]
        domain = domain.encode("idna").decode("utf-8")
    except Exception as e:
        print (e)
        print ("[x] Error converting domain {} to idna, skipping adding...".format(domain))
        return False

    return domain

def push_changes_to_eal():
    os.system("git add blacklists/domains.json ")
    os.system("git add screenshots/mapping.json ")
    os.system("git commit -m \"updated blacklist\"")
    os.system("git push")

def prepare_pull_metamask(phishfort_blacklist):
    blacklist = []
    whitelist = get_existing_whitelist()
    try:
        r3 = requests.get("https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json")
        blacklist = blacklist + r3.json()['blacklist']
    except Exception as e:
        print (e)
        print ("Error parsing metamask blacklist")
        return False
    final = []
    description = ""
    screenshots = fetch_screenshots()
    for entry in phishfort_blacklist:
        if entry in blacklist or entry in whitelist:
            continue
        final.append(entry)
        description+="{}: {} added on {}\n".format(entry, screenshots.get(entry, "*not available*"), str(datetime.now()))
    if len(final) > 0:
        final.sort()
        f = open("metamask_pull.txt", 'w')
        f.write(pformat(final).replace("'", '"'))
        f.write("\n**********\n")
        f.write(description)
        f.close()
        print("[+] Wrote metamask pr to metamask_pull.txt")

def get_existing_blacklists():
    '''
    Fetch the existing EAL blacklist and ensure that we do not duplicate entries.
    '''
    blacklist = []
    try:
        r = requests.get("https://api.infura.io/v2/blacklist")
        blacklist = r.json()['blacklist']
    except:
        print ("[x] Error fetching blacklist, please ensure that you are able to reach the EAL endpoint.")
        return False
    try:
        r2 = requests.get("https://etherscamdb.info/api/blacklist/")
        blacklist = blacklist + r2.json()
    except:
        print ("[x] Error fetching blacklist, please ensure that you are able to reach the Etherscam endpoint.")
        return False

    try:
        r3 = requests.get("https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json")
        blacklist = blacklist + r3.json()['blacklist']
    except Exception as e:
        print (e)
        print ("Error parsing metamask blacklist")
        False
    
    return set(blacklist)

def extend_json_array_file(filename, contents):
    f = open(filename, 'r')
    old_contents = f.read()
    f.close()
    array = set(json.loads(old_contents) + list(contents))
    f = open(filename, 'w')
    f.write(json.dumps(list(array), indent=4, sort_keys=True))
    f.close()

def extend_json_dict_file(filename, contents):
    try:
        f = open(filename, 'r')
        old_contents = f.read()
        f.close()
    except:
        old_contents = "{}"
    combined_dict = {**json.loads(old_contents), **contents}
    f = open(filename, 'w')
    f.write(json.dumps(combined_dict,indent=4, sort_keys=True))
    f.close()

def get_existing_whitelist():
    r = requests.get("https://etherscamdb.info/api/whitelist/")
    whitelist = r.json()
    r3 = requests.get("https://raw.githubusercontent.com/MetaMask/eth-phishing-detect/master/src/config.json")
    whitelist = whitelist + r3.json()['whitelist']
    return whitelist

def load_file():
    ensure_that_domain_file_exists_and_is_valid_json()
    f = open(args.blacklist_file, 'r')
    contents = f.readlines()
    f.close()
    if len(contents) == 0:
        print ("[x] Error - the blacklist file provided is empty")
        sys.exit()


    blacklist = get_existing_blacklists()
    print ("[+] Currently {} entries in EAL blacklist...".format(len(blacklist)))
    if not blacklist:
        sys.exit()

    #New entries set
    new_entries = set()

    #Let's store an internal record of when we reported this. We can also used
    #this date to clean out old domains from the blacklist.
    internal_record = {}

    #Unfiltered....
    unfiltered_blacklist = set()

    whitelist = set(get_existing_whitelist())
    #Loop through each of the entries
    for entry in contents:
        clean_entry = preprocess_domain(entry)
        if not clean_entry:
            continue
        if entry in whitelist:
            print ("\t[-] Found {} but it is whitelisted.")
            continue
        unfiltered_blacklist.add(clean_entry)
        if entry in blacklist:
            print ("\t[-] Found {} but it is already present in the blacklist.")
            continue
        print ("\t[+] Added {}".format(clean_entry))
        new_entries.add(clean_entry)
        urlscan_screenshot(clean_entry)
        internal_record[clean_entry] = str(time.time())
    print ("[+] Found {} new entries...".format(len(new_entries)))

    extend_json_array_file("blacklists/domains.json", new_entries)
    
    extend_json_dict_file("internal_domain_tracking.json", internal_record)

    ensure_that_domain_file_exists_and_is_valid_json()
    prepare_pull_metamask(unfiltered_blacklist)

parser = argparse.ArgumentParser(description='Tool for storing and commiting blacklist to git.')
parser.add_argument('--blacklist-file', metavar='N',type=str,nargs="?", const="blacklist", required=True,
                    help='The new blacklist file to add')
args = parser.parse_args()

if __name__ == "__main__":
    load_file()
    push_changes_to_eal()
