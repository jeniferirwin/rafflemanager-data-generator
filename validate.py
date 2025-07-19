#!/usr/bin/env python3
"""
Validate RaffleManager .lua files for logical consistency
"""

import re
import sys

def validate_roster_data(filename):
    """Validate that roster data has consistent 10-day vs 30-day values"""
    print(f"Validating {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all roster entries
    roster_pattern = r'\["sales10"\]\s*=\s*(\d+),.*?\["purchases30"\]\s*=\s*(\d+),.*?\["sales30"\]\s*=\s*(\d+),.*?\["purchases10"\]\s*=\s*(\d+)'
    matches = re.findall(roster_pattern, content, re.DOTALL)
    
    issues = []
    total_entries = 0
    
    for i, match in enumerate(matches):
        sales10, purchases30, sales30, purchases10 = map(int, match)
        total_entries += 1
        
        # Check sales consistency
        if sales10 > sales30:
            issues.append(f"Entry {i+1}: sales10 ({sales10}) > sales30 ({sales30})")
        
        # Check purchases consistency  
        if purchases10 > purchases30:
            issues.append(f"Entry {i+1}: purchases10 ({purchases10}) > purchases30 ({purchases30})")
    
    print(f"Validated {total_entries} roster entries")
    
    if issues:
        print(f"Found {len(issues)} logical inconsistencies:")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
        return False
    else:
        print("✓ All entries are logically consistent!")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate.py <filename.lua>")
        sys.exit(1)
    
    filename = sys.argv[1]
    if validate_roster_data(filename):
        sys.exit(0)
    else:
        sys.exit(1)
