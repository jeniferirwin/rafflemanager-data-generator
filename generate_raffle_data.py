#!/usr/bin/env python3
"""
RaffleManager Data Generator
A CLI tool to generate .lua data files for RaffleManager ESO addon testing.
"""

import argparse
import random
import time
import os
from typing import List, Dict, Any

# Word lists for generating realistic but generic usernames (similar to Docker container names)
ADJECTIVES = [
    "active", "ancient", "bold", "brave", "calm", "clever", "cool", "curious",
    "daring", "eager", "epic", "fast", "gentle", "happy", "keen", "lucky",
    "mighty", "noble", "proud", "quick", "royal", "silent", "swift", "wise",
    "young", "zealous", "bright", "cosmic", "divine", "fierce", "golden",
    "humble", "iron", "jovial", "kind", "lunar", "magic", "nimble", "ocean",
    "plasma", "quantum", "radiant", "stellar", "thunder", "ultra", "vibrant",
    "wild", "xenial", "yellow", "zesty"
]

NOUNS = [
    "archer", "baker", "crafter", "dancer", "explorer", "fighter", "guardian",
    "hunter", "knight", "mage", "navigator", "oracle", "paladin", "ranger",
    "scholar", "trader", "warrior", "wizard", "alchemist", "bard", "cleric",
    "druid", "engineer", "forger", "gladiator", "herbalist", "inventor",
    "jeweler", "keeper", "librarian", "merchant", "nomad", "observer",
    "protector", "questor", "runner", "seeker", "templar", "voyager", "weaver",
    "crystal", "phoenix", "dragon", "storm", "shadow", "flame", "frost",
    "thunder", "lightning", "mystic"
]

RANKS = ["Recruit", "Member", "Veteran", "Officer", "Guild Master"]

MAIL_SUBJECTS = [
    "tix", "tickets", "raffle", "raffle tickets", "weekly raffle",
    "raffle entry", "BBC raffle", "guild raffle", "raffle tix",
    "tickets please", "raffle please", "", "Gold", "entry fee"
]

MAIL_BODY_TEMPLATES = [
    "Hello, <<1>>!\r\n\r\nConfirming your purchase for the Guild Raffle!\r \n\r\nNumber of Tickets Purchased:|cFFD000    <<2>>|r\r\n\r\nAdditional tickets can be purchased until Tuesday Night.\r\n\r\nDrawings are held weekly.",
    "Welcome to the raffle, <<1>>!\r\n\r\nTickets purchased: <<2>>\r\n\r\nGood luck in this week's drawing!",
    "Raffle confirmation for <<1>>\r\n\r\nTickets: <<2>>\r\n\r\nThank you for participating!"
]

MAIL_SUBJECTS_TEMPLATES = [
    ":: |cF5FC24Guild Raffle Receipt|r ::",
    "Raffle Ticket Confirmation",
    "Weekly Raffle Entry Confirmed"
]

class RaffleDataGenerator:
    def __init__(self):
        self.used_usernames = set()
        self.used_mail_ids = set()
        
    def generate_username(self) -> str:
        """Generate a unique username using adjective + noun pattern"""
        attempts = 0
        while attempts < 100:
            adjective = random.choice(ADJECTIVES)
            noun = random.choice(NOUNS)
            
            # Add some variation
            if random.random() < 0.3:
                number = random.randint(1, 999)
                username = f"@{adjective.title()}{noun.title()}{number}"
            else:
                username = f"@{adjective.title()}{noun.title()}"
            
            if username not in self.used_usernames:
                self.used_usernames.add(username)
                return username
            attempts += 1
        
        # Fallback with timestamp if we can't find unique name
        timestamp = str(int(time.time()))[-6:]
        username = f"@{random.choice(ADJECTIVES).title()}{timestamp}"
        self.used_usernames.add(username)
        return username
    
    def generate_mail_id(self) -> str:
        """Generate a unique mail ID"""
        while True:
            mail_id = str(random.randint(2700000000, 2999999999))
            if mail_id not in self.used_mail_ids:
                self.used_mail_ids.add(mail_id)
                return mail_id
    
    def generate_blank_account(self) -> Dict[str, Any]:
        """Generate a blank account with minimal data"""
        ticket_cost = random.choice([500, 1000, 1500, 2000])
        return {
            "$AccountWide": {
                "version": 1,
                "ticket_cost": ticket_cost
            }
        }
    
    def generate_roster_data(self, num_entries: int) -> List[Dict[str, Any]]:
        """Generate roster data entries"""
        roster_data = []
        for i in range(num_entries):
            # Generate 30-day totals first, then 10-day totals as subset
            sales30 = random.randint(0, 5000000)
            purchases30 = random.randint(0, 100000)
            
            # 10-day totals should be <= 30-day totals
            # Handle edge case where 30-day total is 0
            if sales30 == 0:
                sales10 = 0
            else:
                sales10 = random.randint(0, sales30)
                
            if purchases30 == 0:
                purchases10 = 0
            else:
                purchases10 = random.randint(0, purchases30)
            
            entry = {
                "account": self.generate_username(),
                "joined": random.randint(0, int(time.time())),
                "sales10": sales10,
                "purchases30": purchases30,
                "sales30": sales30,
                "rank": random.choice(RANKS),
                "purchases10": purchases10
            }
            roster_data.append(entry)
        return roster_data
    
    def generate_mail_data(self, num_entries: int) -> List[Dict[str, Any]]:
        """Generate mail data entries"""
        mail_data = []
        for i in range(num_entries):
            entry = {
                "subject": random.choice(MAIL_SUBJECTS),
                "id": self.generate_mail_id(),
                "amount": random.randint(5000, 1000000),
                "user": self.generate_username()
            }
            mail_data.append(entry)
        return mail_data
    
    def generate_roster_account(self) -> Dict[str, Any]:
        """Generate an account with only roster data"""
        num_roster_entries = random.randint(5, 50)
        ticket_cost = random.choice([500, 1000, 1500, 2000])
        
        return {
            "$AccountWide": {
                "version": 1,
                "ticket_cost": ticket_cost,
                "roster_data": self.generate_roster_data(num_roster_entries)
            }
        }
    
    def generate_mail_account(self) -> Dict[str, Any]:
        """Generate an account with only mail data"""
        num_mail_entries = random.randint(3, 30)
        ticket_cost = random.choice([500, 1000, 1500, 2000])
        
        account_data = {
            "version": 1,
            "ticket_cost": ticket_cost,
            "mail_data": self.generate_mail_data(num_mail_entries),
            "timestamp": random.randint(1600000000, int(time.time()))
        }
        
        # Sometimes add body and subject templates
        if random.random() < 0.7:
            account_data["body"] = random.choice(MAIL_BODY_TEMPLATES)
            account_data["subject"] = random.choice(MAIL_SUBJECTS_TEMPLATES)
        
        return {"$AccountWide": account_data}
    
    def generate_mixed_account(self) -> Dict[str, Any]:
        """Generate an account with both roster and mail data"""
        num_roster_entries = random.randint(5, 50)
        num_mail_entries = random.randint(3, 30)
        ticket_cost = random.choice([500, 1000, 1500, 2000])
        
        account_data = {
            "version": 1,
            "ticket_cost": ticket_cost,
            "mail_data": self.generate_mail_data(num_mail_entries),
            "timestamp": random.randint(1600000000, int(time.time())),
            "roster_data": self.generate_roster_data(num_roster_entries)
        }
        
        # Sometimes add body and subject templates
        if random.random() < 0.7:
            account_data["body"] = random.choice(MAIL_BODY_TEMPLATES)
            account_data["subject"] = random.choice(MAIL_SUBJECTS_TEMPLATES)
        
        return {"$AccountWide": account_data}
    
    def format_lua_value(self, value: Any, indent: int = 0) -> str:
        """Format a Python value as Lua syntax"""
        spaces = "    " * indent
        
        if isinstance(value, dict):
            if not value:
                return "{}"
            
            lines = ["{"]
            for key, val in value.items():
                if isinstance(key, str):
                    key_str = f'["{key}"]'
                else:
                    key_str = f"[{key}]"
                
                val_str = self.format_lua_value(val, indent + 1)
                lines.append(f"{spaces}    {key_str} = {val_str},")
            lines.append(f"{spaces}}}")
            return "\n".join(lines)
        
        elif isinstance(value, list):
            if not value:
                return "{}"
            
            lines = ["{"]
            for i, item in enumerate(value, 1):
                item_str = self.format_lua_value(item, indent + 1)
                lines.append(f"{spaces}    [{i}] = {item_str},")
            lines.append(f"{spaces}}}")
            return "\n".join(lines)
        
        elif isinstance(value, str):
            # Escape quotes and return as quoted string
            escaped = value.replace('"', '\\"')
            return f'"{escaped}"'
        
        elif isinstance(value, (int, float)):
            return str(value)
        
        elif isinstance(value, bool):
            return "true" if value else "false"
        
        else:
            return str(value)
    
    def generate_file(self, blank_count: int, roster_count: int, 
                     mail_count: int, mixed_count: int, filename: str):
        """Generate a complete .lua file with specified account types"""
        accounts = {}
        
        # Generate blank accounts
        for _ in range(blank_count):
            username = self.generate_username()
            accounts[username] = self.generate_blank_account()
        
        # Generate roster accounts
        for _ in range(roster_count):
            username = self.generate_username()
            accounts[username] = self.generate_roster_account()
        
        # Generate mail accounts
        for _ in range(mail_count):
            username = self.generate_username()
            accounts[username] = self.generate_mail_account()
        
        # Generate mixed accounts
        for _ in range(mixed_count):
            username = self.generate_username()
            accounts[username] = self.generate_mixed_account()
        
        # Create the full data structure
        data = {
            "RaffleManager_SavedVariables": {
                "Default": accounts
            }
        }
        
        # Format as Lua
        lua_content = f"RaffleManager_SavedVariables =\n{self.format_lua_value(data['RaffleManager_SavedVariables'])}\n"
        
        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(lua_content)
        
        total_accounts = blank_count + roster_count + mail_count + mixed_count
        print(f"Generated {filename} with {total_accounts} accounts:")
        print(f"  - {blank_count} blank accounts")
        print(f"  - {roster_count} roster accounts") 
        print(f"  - {mail_count} mail accounts")
        print(f"  - {mixed_count} mixed accounts")

def get_unique_filename(base_name: str) -> str:
    """Generate a unique filename by appending a number if needed"""
    if not os.path.exists(base_name):
        return base_name
    
    name, ext = os.path.splitext(base_name)
    counter = 1
    
    while True:
        new_name = f"{name}_{counter}{ext}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

def main():
    parser = argparse.ArgumentParser(
        description="Generate .lua data files for RaffleManager ESO addon testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_raffle_data.py 5 10 15 20
    Generates a file with 5 blank, 10 roster, 15 mail, and 20 mixed accounts

  python generate_raffle_data.py 100 0 0 0 --filename large_blank.lua
    Generates a file with 100 blank accounts only

  python generate_raffle_data.py 0 0 50 0 --filename mail_only.lua
    Generates a file with 50 mail accounts only
        """
    )
    
    parser.add_argument('blank_count', type=int, 
                       help='Number of blank accounts (only basic settings)')
    parser.add_argument('roster_count', type=int,
                       help='Number of roster-only accounts')
    parser.add_argument('mail_count', type=int,
                       help='Number of mail-only accounts')
    parser.add_argument('mixed_count', type=int,
                       help='Number of mixed accounts (both roster and mail)')
    parser.add_argument('--filename', '-f', type=str,
                       help='Output filename (default: RaffleManager_Generated.lua)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.blank_count < 0 or args.roster_count < 0 or args.mail_count < 0 or args.mixed_count < 0:
        print("Error: All account counts must be non-negative")
        return 1
    
    total_accounts = args.blank_count + args.roster_count + args.mail_count + args.mixed_count
    if total_accounts == 0:
        print("Error: At least one account must be specified")
        return 1
    
    # Determine filename
    if args.filename:
        filename = args.filename
    else:
        filename = "RaffleManager_Generated.lua"
    
    # Ensure unique filename
    filename = get_unique_filename(filename)
    
    # Generate the file
    generator = RaffleDataGenerator()
    generator.generate_file(args.blank_count, args.roster_count, 
                           args.mail_count, args.mixed_count, filename)
    
    return 0

if __name__ == "__main__":
    exit(main())
