#!/usr/bin/env python3
"""
Check mail amounts for divisibility by ticket cost
"""

import re
import sys

def check_amounts(filename):
    """Check what percentage of mail amounts are divisible by ticket cost"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract ticket cost (assuming it's consistent)
    ticket_cost_match = re.search(r'\["ticket_cost"\]\s*=\s*(\d+)', content)
    if not ticket_cost_match:
        print("Could not find ticket_cost in file")
        return
    
    ticket_cost = int(ticket_cost_match.group(1))
    print(f"Ticket cost: {ticket_cost}")
    
    # Find all mail amounts
    amount_pattern = r'\["amount"\]\s*=\s*(\d+)'
    amounts = [int(match) for match in re.findall(amount_pattern, content)]
    
    if not amounts:
        print("No mail amounts found")
        return
    
    valid_amounts = [amount for amount in amounts if amount % ticket_cost == 0]
    invalid_amounts = [amount for amount in amounts if amount % ticket_cost != 0]
    
    total = len(amounts)
    valid_count = len(valid_amounts)
    invalid_count = len(invalid_amounts)
    
    print(f"\nTotal mail entries: {total}")
    print(f"Valid amounts (divisible by {ticket_cost}): {valid_count} ({valid_count/total*100:.1f}%)")
    print(f"Invalid amounts: {invalid_count} ({invalid_count/total*100:.1f}%)")
    
    if invalid_count > 0:
        print(f"\nSample invalid amounts:")
        for amount in invalid_amounts[:5]:
            remainder = amount % ticket_cost
            print(f"  {amount} (remainder: {remainder})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_amounts.py <filename.lua>")
        sys.exit(1)
    
    check_amounts(sys.argv[1])
