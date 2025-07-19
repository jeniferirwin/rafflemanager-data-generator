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
python generate_raffle_data.py <blank_count> <roster_count> <mail_count> <mixed_count> [--filename OUTPUT_FILE]
```

### Arguments

- `blank_count`: Number of blank accounts (only basic settings)
- `roster_count`: Number of roster-only accounts
- `mail_count`: Number of mail-only accounts  
- `mixed_count`: Number of mixed accounts (both roster and mail data)
- `--filename`, `-f`: Optional output filename (default: `RaffleManager_Generated.lua`)

### Examples

Generate a balanced test file:
```bash
python generate_raffle_data.py 5 10 15 20
```

Generate a large file with only blank accounts:
```bash
python generate_raffle_data.py 100 0 0 0 --filename large_blank.lua
```

Generate mail-heavy test data:
```bash
python generate_raffle_data.py 0 0 50 0 --filename mail_only.lua
```

Generate a comprehensive test file:
```bash
python generate_raffle_data.py 25 50 75 100 --filename comprehensive_test.lua
```

**Windows Users**: Use the convenient batch file:
```cmd
generate.bat 5 10 15 20
generate.bat 100 0 0 0 large_blank.lua
```

**More Examples**: See `sample_commands.txt` for additional usage scenarios.

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
   - **Data consistency**: `sales10` ≤ `sales30` and `purchases10` ≤ `purchases30` (10-day totals are subsets of 30-day totals)

3. **Mail Accounts**:
   - Include `mail_data` array with raffle ticket purchase records
   - May include mail templates (`body`, `subject`)
   - Include timestamp for last activity

4. **Mixed Accounts**:
   - Combine both roster and mail data
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
- **Ticket Costs**: 500, 1000, 1500, 2000 gold
- **Mail Amounts**: 5,000 - 1,000,000 gold
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

### Example Validation Output
```
Validating test_file.lua...
Validated 1171 roster entries
✓ All entries are logically consistent!
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
- **`validate.py`**: Validates generated files for logical consistency
- **`sample_commands.txt`**: Collection of common usage examples for quick reference
- **`requirements.txt`**: Python dependency information (no external packages needed)

### Quick Start Commands
```bash
# Generate a small test file
python generate_raffle_data.py 2 3 5 2 --filename quick_test.lua

# Validate the generated file
python validate.py quick_test.lua

# Use batch file (Windows)
generate.bat 2 3 5 2 quick_test.lua
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python generate_raffle_data.py 10 20 30 40` | Generate mixed test data |
| `python generate_raffle_data.py 100 0 0 0 --filename blanks.lua` | 100 blank accounts only |
| `python generate_raffle_data.py 0 0 200 0 --filename mail.lua` | 200 mail accounts only |
| `python validate.py filename.lua` | Validate file consistency |
| `generate.bat 5 5 5 5` | Windows: Generate balanced test file |

## Contributing

This tool is designed to be easily extensible. Key areas for enhancement:
- Additional ESO-specific data fields
- More realistic username generation patterns  
- Extended validation rules
- Additional output formats

## License

This project is provided as-is for ESO addon testing purposes.
