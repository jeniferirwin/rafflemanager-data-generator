#!/usr/bin/env python3
"""
RaffleManager Data Generator
A CLI tool to generate .lua data files for RaffleManager ESO addon testing.
"""

import argparse
import random
import time
import os
import json
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

# Default configuration
DEFAULT_CONFIG = {
    "mail_entries_per_account": 10,
    "roster_entries_per_account": 10,
    "default_ticket_cost": 1000,
    "default_output_filename": "RaffleManager_Generated.lua",
    "account_types_enabled": {
        "blank": True,
        "roster": True,
        "mail": True,
        "mixed": True
    },
    "account_counts": {
        "blank": 5,
        "roster": 10,
        "mail": 15,
        "mixed": 20
    }
}

CONFIG_FILE = "config.json"

def load_config() -> Dict[str, Any]:
    """Load configuration from file, create with defaults if not exists"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Ensure all required keys exist
                for key, default_value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = default_value
                return config
        else:
            # Create default config file
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load config file ({e}). Using defaults.")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save config file ({e})")

def reset_config_to_defaults() -> Dict[str, Any]:
    """Reset configuration to defaults and save"""
    config = DEFAULT_CONFIG.copy()
    save_config(config)
    return config

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
    
    def generate_blank_account(self, ticket_cost: int = 1000) -> Dict[str, Any]:
        """Generate a blank account with minimal data"""
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
    
    def generate_mail_data(self, num_entries: int, ticket_cost: int = 1000) -> List[Dict[str, Any]]:
        """Generate mail data entries with amounts mostly divisible by ticket_cost"""
        mail_data = []
        for i in range(num_entries):
            # 90% of users send correct amounts (divisible by ticket_cost)
            # 10% send incorrect amounts
            if random.random() < 0.9:
                # Generate a valid amount (multiple of ticket_cost)
                num_tickets = random.randint(1, 1000)  # 1 to 1000 tickets
                amount = num_tickets * ticket_cost
            else:
                # Generate an invalid amount (not divisible by ticket_cost)
                base_amount = random.randint(1, 1000) * ticket_cost
                # Add a random offset that makes it invalid
                offset = random.randint(1, ticket_cost - 1)
                amount = base_amount + offset
            
            entry = {
                "subject": random.choice(MAIL_SUBJECTS),
                "id": self.generate_mail_id(),
                "amount": amount,
                "user": self.generate_username()
            }
            mail_data.append(entry)
        return mail_data
    
    def generate_roster_account(self, ticket_cost: int = 1000, roster_entries: int = 10) -> Dict[str, Any]:
        """Generate an account with only roster data"""
        
        return {
            "$AccountWide": {
                "version": 1,
                "ticket_cost": ticket_cost,
                "roster_data": self.generate_roster_data(roster_entries),
                "roster_timestamp": random.randint(1600000000, int(time.time()))
            }
        }
    
    def generate_mail_account(self, ticket_cost: int = 1000, mail_entries: int = 10) -> Dict[str, Any]:
        """Generate an account with only mail data"""
        
        account_data = {
            "version": 1,
            "ticket_cost": ticket_cost,
            "mail_data": self.generate_mail_data(mail_entries, ticket_cost),
            "timestamp": random.randint(1600000000, int(time.time()))
        }
        
        # Sometimes add body and subject templates
        if random.random() < 0.7:
            account_data["body"] = random.choice(MAIL_BODY_TEMPLATES)
            account_data["subject"] = random.choice(MAIL_SUBJECTS_TEMPLATES)
        
        return {"$AccountWide": account_data}
    
    def generate_mixed_account(self, ticket_cost: int = 1000, roster_entries: int = 10, mail_entries: int = 10) -> Dict[str, Any]:
        """Generate an account with both roster and mail data"""
        
        account_data = {
            "version": 1,
            "ticket_cost": ticket_cost,
            "mail_data": self.generate_mail_data(mail_entries, ticket_cost),
            "timestamp": random.randint(1600000000, int(time.time())),
            "roster_data": self.generate_roster_data(roster_entries),
            "roster_timestamp": random.randint(1600000000, int(time.time()))
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
                     mail_count: int, mixed_count: int, filename: str, 
                     ticket_cost: int = 1000, roster_entries: int = 10, mail_entries: int = 10):
        """Generate a complete .lua file with specified account types"""
        accounts = {}
        
        # Generate blank accounts
        for _ in range(blank_count):
            username = self.generate_username()
            accounts[username] = self.generate_blank_account(ticket_cost)
        
        # Generate roster accounts
        for _ in range(roster_count):
            username = self.generate_username()
            accounts[username] = self.generate_roster_account(ticket_cost, roster_entries)
        
        # Generate mail accounts
        for _ in range(mail_count):
            username = self.generate_username()
            accounts[username] = self.generate_mail_account(ticket_cost, mail_entries)
        
        # Generate mixed accounts
        for _ in range(mixed_count):
            username = self.generate_username()
            accounts[username] = self.generate_mixed_account(ticket_cost, roster_entries, mail_entries)
        
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
        print(f"  - {roster_count} roster accounts ({roster_entries} entries each)")
        print(f"  - {mail_count} mail accounts ({mail_entries} entries each)")
        print(f"  - {mixed_count} mixed accounts ({roster_entries} roster + {mail_entries} mail entries each)")

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
    # Load configuration
    config = load_config()
    
    parser = argparse.ArgumentParser(
        description="Generate .lua data files for RaffleManager ESO addon testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_raffle_data.py 5 10 15 20
    Generates a file with 5 blank, 10 roster, 15 mail, and 20 mixed accounts (uses saved settings)

  python generate_raffle_data.py 100 0 0 0 --filename large_blank.lua --ticket-cost 500
    Generates a file with 100 blank accounts only, with 500 gold ticket cost

  python generate_raffle_data.py 0 0 50 0 --filename mail_only.lua -t 2000 --mail-entries 25
    Generates a file with 50 mail accounts, each with 25 mail entries, 2000 gold ticket cost

  python generate_raffle_data.py 0 10 0 0 --roster-entries 100
    Generates 10 roster accounts, each with 100 roster entries (large guild test)
        """
    )
    
    parser.add_argument('blank_count', type=int, nargs='?', default=0,
                       help='Number of blank accounts (only basic settings)')
    parser.add_argument('roster_count', type=int, nargs='?', default=0,
                       help='Number of roster-only accounts')
    parser.add_argument('mail_count', type=int, nargs='?', default=0,
                       help='Number of mail-only accounts')
    parser.add_argument('mixed_count', type=int, nargs='?', default=0,
                       help='Number of mixed accounts (both roster and mail)')
    parser.add_argument('--ticket-cost', '-t', type=int, default=config['default_ticket_cost'],
                       help=f'Ticket cost for all accounts (default: {config["default_ticket_cost"]})')
    parser.add_argument('--filename', '-f', type=str,
                       help=f'Output filename (default: {config["default_output_filename"]})')
    parser.add_argument('--roster-entries', '-r', type=int, default=config['roster_entries_per_account'],
                       help=f'Number of roster entries per account (default: {config["roster_entries_per_account"]})')
    parser.add_argument('--mail-entries', '-m', type=int, default=config['mail_entries_per_account'],
                       help=f'Number of mail entries per account (default: {config["mail_entries_per_account"]})')
    parser.add_argument('--reset-config', action='store_true',
                       help='Reset all settings to program defaults and exit')
    
    args = parser.parse_args()
    
    # Handle config reset
    if args.reset_config:
        reset_config_to_defaults()
        print("Configuration reset to defaults:")
        for key, value in DEFAULT_CONFIG.items():
            print(f"  {key}: {value}")
        return 0
    
    # Validate arguments
    if args.blank_count < 0 or args.roster_count < 0 or args.mail_count < 0 or args.mixed_count < 0:
        print("Error: All account counts must be non-negative")
        return 1
    
    if args.ticket_cost <= 0:
        print("Error: Ticket cost must be positive")
        return 1
        
    if args.roster_entries <= 0:
        print("Error: Roster entries per account must be positive")
        return 1
        
    if args.mail_entries <= 0:
        print("Error: Mail entries per account must be positive")
        return 1
    
    total_accounts = args.blank_count + args.roster_count + args.mail_count + args.mixed_count
    if total_accounts == 0:
        print("Error: At least one account must be specified")
        return 1
    
    # Update and save configuration with new values
    config['default_ticket_cost'] = args.ticket_cost
    config['roster_entries_per_account'] = args.roster_entries
    config['mail_entries_per_account'] = args.mail_entries
    if args.filename:
        config['default_output_filename'] = args.filename
    save_config(config)
    
    # Determine filename
    if args.filename:
        filename = args.filename
    else:
        filename = config['default_output_filename']
    
    # Ensure unique filename
    filename = get_unique_filename(filename)
    
    # Generate the file
    generator = RaffleDataGenerator()
    generator.generate_file(args.blank_count, args.roster_count, 
                           args.mail_count, args.mixed_count, filename, 
                           args.ticket_cost, args.roster_entries, args.mail_entries)
    
    return 0

if __name__ == "__main__":
    exit(main())
