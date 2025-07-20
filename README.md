# RaffleManager Data Generator

A CLI tool to generate `.lua` data files for RaffleManager ESO addon testing. This tool creates realistic but generic test data with customizable account types and counts.

## Features

- **Generic Username Generation**: Uses Docker-style naming (adjective + noun combinations) to avoid real player names
- **Four Account Types**:
  - **Blank**: Basic accounts with only version and ticket_cost settings
  - **Roster**: Accounts with guild roster data only
  - **Mail**: Accounts with raffle mail data only  
  - **Mixed**: Accounts with both roster and mail data
- **Automatic File Naming**: Prevents overwriting existing files by appending numbers
- **Realistic Data**: Generates believable timestamps, amounts, ranks, and other ESO-specific data
- **Data Validation**: Built-in logical consistency checks for roster data
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Batch File Support**: Convenient Windows batch file for easy execution

## Installation

No installation required - just run the Python script directly.

**Requirements**: Python 3.6+

## Project Structure

```
rafflemanager-data-generator/
├── generate_raffle_data.py    # Main CLI generator script
├── generate.bat               # Windows batch file for convenience
├── validate.py                # Validation tool for generated files
├── sample_commands.txt        # Common usage examples
├── requirements.txt           # Python dependencies (none required)
└── README.md                  # This documentation
```

## Usage

```bash
python generate_raffle_data.py <blank_count> <roster_count> <mail_count> <mixed_count> [--filename OUTPUT_FILE] [--ticket-cost COST]
```

### Arguments

- `blank_count`: Number of blank accounts (only basic settings)
- `roster_count`: Number of roster-only accounts
- `mail_count`: Number of mail-only accounts  
- `mixed_count`: Number of mixed accounts (both roster and mail data)
- `--filename`, `-f`: Optional output filename (default: `RaffleManager_Generated.lua`)
- `--output-folder`, `-o`: Optional output folder path (default: current directory)
- `--ticket-cost`, `-t`: Optional ticket cost for all accounts (default: 1000)
- `--timestamp-date`: Base timestamp date in MM/DD/YYYY format (default: 07/20/2025)
- `--timestamp-time`: Base timestamp time in HH:MM:SS format (default: 00:00:00)

### Examples

Generate a balanced test file with default 1000 gold ticket cost:
```bash
python generate_raffle_data.py 5 10 15 20
```

Generate a large file with only blank accounts and custom ticket cost:
```bash
python generate_raffle_data.py 100 0 0 0 --filename large_blank.lua --ticket-cost 500
```

Generate mail-heavy test data with expensive tickets:
```bash
python generate_raffle_data.py 0 0 50 0 --filename mail_only.lua -t 2000
```

Generate a comprehensive test file with custom ticket cost:
```bash
python generate_raffle_data.py 25 50 75 100 --filename comprehensive_test.lua --ticket-cost 1500
```

Generate files in a specific output folder:
```bash
python generate_raffle_data.py 10 10 10 10 --output-folder "test_data" --filename weekly_test.lua
```

Generate with custom timestamp (Christmas 2024 data):
```bash
python generate_raffle_data.py 5 5 5 5 --timestamp-date "12/25/2024" --timestamp-time "09:00:00"
```

**Windows Users**: Use the convenient batch file:
```cmd
generate.bat 5 10 15 20
generate.bat 100 0 0 0 large_blank.lua 500
generate.bat 10 20 30 40 custom.lua 1500
```

**More Examples**: See `sample_commands.txt` for additional usage scenarios.

## Timestamp Configuration

The tool allows you to control the base timestamp for all generated data:

- **Base Timestamp**: Set via CLI arguments or GUI fields (MM/DD/YYYY HH:MM:SS)
- **Realistic Variation**: Generated timestamps vary within ±30 days of the base timestamp
- **Data Consistency**: Mail and roster timestamps are within ±7 days of the base timestamp
- **Default Setting**: July 20, 2025 at 00:00:00

### CLI Timestamp Examples
```bash
# Generate data for a specific historical date
python generate_raffle_data.py 10 10 10 10 --timestamp-date "03/15/2023" --timestamp-time "14:30:00"

# Generate current date data (default behavior if no timestamp specified)
python generate_raffle_data.py 5 5 5 5
```

### GUI Timestamp Fields
The GUI provides six input boxes for easy timestamp configuration:
- **MM DD YYYY**: Month, Day, Year (e.g., 07 20 2025)
- **HH MM SS**: Hour, Minute, Second in 24-hour format (e.g., 00 00 00)

## Generated Data Structure

The tool generates `.lua` files matching the RaffleManager SavedVariables format:

```lua
RaffleManager_SavedVariables =
{
    ["Default"] = 
    {
        ["@GeneratedUsername"] = 
        {
            ["$AccountWide"] = 
            {
                -- Account data based on type
            },
        },
        -- ... more accounts
    },
}
```

### Account Types

1. **Blank Accounts**:
   ```lua
   ["$AccountWide"] = 
   {
       ["version"] = 1,
       ["ticket_cost"] = 1000,
   },
   ```

2. **Roster Accounts**:
   - Include `roster_data` array with guild member information
   - Each entry contains account, join date, sales/purchase data, rank
   - Include `roster_timestamp` for roster data last update
   - **Data consistency**: `sales10` ≤ `sales30` and `purchases10` ≤ `purchases30` (10-day totals are subsets of 30-day totals)

3. **Mail Accounts**:
   - Include `mail_data` array with raffle ticket purchase records
   - May include mail templates (`body`, `subject`)
   - Include timestamp for last activity
   - **Realistic Amounts**: 90% of mail amounts are divisible by the ticket cost (valid ticket purchases), 10% contain "user errors" with invalid amounts

4. **Mixed Accounts**:
   - Combine both roster and mail data
   - Include both `timestamp` (mail data) and `roster_timestamp` (roster data)
   - Most comprehensive account type for testing

## Generated Username Format

Usernames follow the pattern `@AdjactiveNoun` or `@AdjectiveNoun123`:
- Examples: `@BraveKnight`, `@SwiftMage42`, `@NobleTrader`
- No real ESO player names are used
- All usernames are unique within each generated file

## File Output

- Files are saved in the current directory
- If the specified filename exists, a number is appended (e.g., `RaffleManager_Generated_1.lua`)
- Output includes a summary of generated accounts by type

## Sample Output

```
Generated RaffleManager_Generated.lua with 50 accounts:
  - 5 blank accounts
  - 10 roster accounts
  - 15 mail accounts
  - 20 mixed accounts
```

## Use Cases

- **Performance Testing**: Generate large files to test addon performance
- **Edge Case Testing**: Create specific combinations of account types
- **Development**: Quick generation of test data during addon development  
- **QA Testing**: Consistent, reproducible test datasets

## Data Ranges

The generator uses realistic ranges for ESO data:
- **Ticket Costs**: User-specified (default: 1000 gold) - can be any positive integer
- **Mail Entries**: 10-30 mail entries per account with mail data
- **Mail Amounts**: 5,000 - 1,000,000 gold (90% divisible by ticket cost, 10% with random remainders to simulate user errors)
- **Sales Data**: 0 - 5,000,000 gold
- **Purchase Data**: 0 - 100,000 gold
- **Timestamps**: Unix timestamps from 2020 to present
- **Guild Ranks**: Recruit, Member, Veteran, Officer, Guild Master

## Data Validation

The tool includes built-in validation to ensure logical consistency:

### Validate Generated Files
```bash
python validate.py <filename.lua>
```

The validator checks:
- **Roster Data Consistency**: Ensures `sales10 ≤ sales30` and `purchases10 ≤ purchases30`
- **Data Integrity**: Verifies proper formatting and structure

**Note**: The GUI validation buttons automatically find and validate the most recently generated file, even if it's in a custom output folder.

### Example Validation Output
```
Validating test_file.lua...
Validated 1171 roster entries
✓ All entries are logically consistent!
```

### Validate Mail Amount Distribution
```bash
python check_amounts.py <filename.lua>
```

This tool verifies that mail amounts follow the realistic distribution:
- Shows percentage of amounts divisible by the ticket cost (should be ~90%)
- Lists sample invalid amounts with their remainders
- Helps verify the realism of generated raffle data

#### Example Amount Validation Output
```
Ticket cost: 750
Total mail entries: 833
Valid amounts (divisible by 750): 746 (89.6%)
Invalid amounts: 87 (10.4%)
Sample invalid amounts:
  632568 (remainder: 318)
  404426 (remainder: 176)
  424206 (remainder: 456)
```

## Troubleshooting

**Common Issues:**
- **Permission Errors**: Ensure you have write permissions in the output directory
- **File Exists**: The tool automatically appends numbers to avoid overwriting (e.g., `file_1.lua`)
- **Large Files**: For files with >1000 accounts, generation may take a few seconds

**Performance Tips:**
- Use smaller batch sizes for initial testing
- Large files (10,000+ accounts) are suitable for stress testing

## Tools Included

### Primary Tools
- **`generate_raffle_data.py`**: Main CLI generator with full customization options
- **`generate.bat`**: Windows batch file for quick generation without typing full commands

### Utility Tools  
- **`validate.py`**: Validates generated files for logical consistency (roster data)
- **`check_amounts.py`**: Validates mail amount distribution and realism
- **`sample_commands.txt`**: Collection of common usage examples for quick reference
- **`requirements.txt`**: Python dependency information (no external packages needed)

### Quick Start Commands
```bash
# Generate a small test file with default ticket cost (1000)
python generate_raffle_data.py 2 3 5 2 --filename quick_test.lua

# Generate with custom ticket cost
python generate_raffle_data.py 2 3 5 2 --filename custom_test.lua --ticket-cost 500

# Validate the generated file's roster data consistency
python validate.py quick_test.lua

# Check mail amount distribution and realism
python check_amounts.py quick_test.lua

# Use batch file (Windows)
generate.bat 2 3 5 2 quick_test.lua 500
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python generate_raffle_data.py 10 20 30 40` | Generate mixed test data (default 1000 ticket cost) |
| `python generate_raffle_data.py 100 0 0 0 --filename blanks.lua --ticket-cost 500` | 100 blank accounts with 500 gold tickets |
| `python generate_raffle_data.py 0 0 200 0 --filename mail.lua -t 2000` | 200 mail accounts with expensive tickets |
| `python validate.py filename.lua` | Validate roster data consistency |
| `python check_amounts.py filename.lua` | Check mail amount distribution (90% valid, 10% invalid) |
| `generate.bat 5 5 5 5 custom.lua 1500` | Windows: Generate with custom filename and ticket cost |

## Contributing

This tool is designed to be easily extensible. Key areas for enhancement:
- Additional ESO-specific data fields
- More realistic username generation patterns  
- Extended validation rules
- Additional output formats

## License

This project is provided as-is for ESO addon testing purposes.
