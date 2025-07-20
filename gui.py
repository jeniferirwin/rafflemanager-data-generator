#!/usr/bin/env python3
"""
RaffleManager Data Generator GUI
A sleek, hacker-themed interface for generating ESO addon test data.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import threading
import subprocess
import sys
import time
from typing import Dict, Any
from generate_raffle_data import RaffleDataGenerator, load_config, save_config, DEFAULT_CONFIG

class HackerTheme:
    """Color scheme and styling for the hacker aesthetic"""
    BG_DARK = "#0a0a0a"          # Deep black background
    BG_MEDIUM = "#1a1a1a"        # Medium dark panels
    BG_LIGHT = "#2a2a2a"         # Lighter panels/cards
    FG_PRIMARY = "#00ff41"       # Matrix green primary text
    FG_SECONDARY = "#00cc33"     # Darker green secondary text
    FG_ACCENT = "#66ff66"        # Bright green accents
    FG_WHITE = "#ffffff"         # Pure white for important text
    FG_GRAY = "#888888"          # Gray for disabled/secondary
    BORDER = "#333333"           # Border color
    ERROR = "#ff0040"            # Red for errors
    WARNING = "#ffaa00"          # Orange for warnings
    SUCCESS = "#00ff88"          # Bright green for success

class RaffleManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.config = load_config()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.load_settings()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("⚡ RaffleManager Data Generator ⚡")
        
        # Set minimum window size and make it responsive
        self.root.minsize(700, 500)
        
        # Try to size appropriately for screen, but don't exceed it
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Use 80% of screen size or preferred size, whichever is smaller
        preferred_width = min(800, int(screen_width * 0.8))
        preferred_height = min(700, int(screen_height * 0.8))
        
        # Center the window
        x = (screen_width - preferred_width) // 2
        y = (screen_height - preferred_height) // 2
        
        self.root.geometry(f"{preferred_width}x{preferred_height}+{x}+{y}")
        self.root.configure(bg=HackerTheme.BG_DARK)
        self.root.resizable(True, True)
        
        # Configure grid weights for responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def setup_styles(self):
        """Configure ttk styles for hacker theme"""
        style = ttk.Style()
        
        # Configure checkbutton style
        style.theme_use('clam')
        style.configure('Hacker.TCheckbutton',
                       background=HackerTheme.BG_DARK,
                       foreground=HackerTheme.FG_PRIMARY,
                       focuscolor='none',
                       font=('Consolas', 10))
        style.map('Hacker.TCheckbutton',
                 background=[('active', HackerTheme.BG_MEDIUM)])
        
        # Configure entry style
        style.configure('Hacker.TEntry',
                       fieldbackground=HackerTheme.BG_LIGHT,
                       bordercolor=HackerTheme.BORDER,
                       foreground=HackerTheme.FG_WHITE,
                       insertcolor=HackerTheme.FG_ACCENT,
                       font=('Consolas', 10))
        
        # Configure combobox style
        style.configure('Hacker.TCombobox',
                       fieldbackground=HackerTheme.BG_LIGHT,
                       bordercolor=HackerTheme.BORDER,
                       foreground=HackerTheme.FG_WHITE,
                       font=('Consolas', 10))
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Create a canvas with scrollbar for the main content
        self.canvas = tk.Canvas(self.root, bg=HackerTheme.BG_DARK, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=HackerTheme.BG_DARK)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid the canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(20, 0), pady=20)
        self.scrollbar.grid(row=0, column=1, sticky="ns", pady=20, padx=(0, 20))
        
        # Configure root grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container inside the scrollable frame
        main_frame = tk.Frame(self.scrollable_frame, bg=HackerTheme.BG_DARK)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Account Types Section
        self.create_account_types_section(main_frame)
        
        # Settings Section
        self.create_settings_section(main_frame)
        
        # Output Section
        self.create_output_section(main_frame)
        
        # Preview Section
        self.create_preview_section(main_frame)
        
        # Action Buttons
        self.create_action_buttons(main_frame)
        
        # Output/Log Area (fixed height to prevent excessive growth)
        self.create_output_area(main_frame)
        
        # Bind mousewheel to canvas for scrolling
        self.bind_mousewheel()
        
    def bind_mousewheel(self):
        """Bind mousewheel events for scrolling"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)
        
    def create_header(self, parent):
        """Create the application header"""
        header_frame = tk.Frame(parent, bg=HackerTheme.BG_DARK)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Check if we're in a small window
        is_compact = self.root.winfo_width() < 750 if hasattr(self.root, 'winfo_width') else False
        
        if is_compact:
            # Compact header for small screens
            title_label = tk.Label(header_frame, 
                                  text="⚡ RAFFLEMANAGER ⚡",
                                  font=('Consolas', 14, 'bold'),
                                  fg=HackerTheme.FG_ACCENT,
                                  bg=HackerTheme.BG_DARK)
            title_label.grid(row=0, column=0)
            
            subtitle_label = tk.Label(header_frame,
                                     text="[ DATA GENERATOR ]",
                                     font=('Consolas', 9),
                                     fg=HackerTheme.FG_SECONDARY,
                                     bg=HackerTheme.BG_DARK)
            subtitle_label.grid(row=1, column=0, pady=(2, 0))
        else:
            # Full header for larger screens
            title_label = tk.Label(header_frame, 
                                  text="⚡ RAFFLEMANAGER DATA GENERATOR ⚡",
                                  font=('Consolas', 16, 'bold'),
                                  fg=HackerTheme.FG_ACCENT,
                                  bg=HackerTheme.BG_DARK)
            title_label.grid(row=0, column=0)
            
            subtitle_label = tk.Label(header_frame,
                                     text="[ ESO ADDON TESTING SUITE ]",
                                     font=('Consolas', 10),
                                     fg=HackerTheme.FG_SECONDARY,
                                     bg=HackerTheme.BG_DARK)
            subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
    def create_account_types_section(self, parent):
        """Create account types configuration section"""
        # Section frame with border effect
        section_frame = tk.Frame(parent, bg=HackerTheme.BG_MEDIUM, relief='ridge', bd=1)
        section_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        section_frame.grid_columnconfigure(1, weight=1)
        section_frame.grid_columnconfigure(3, weight=1)
        
        # Section header
        header_label = tk.Label(section_frame,
                               text=">>> ACCOUNT TYPES <<<",
                               font=('Consolas', 12, 'bold'),
                               fg=HackerTheme.FG_PRIMARY,
                               bg=HackerTheme.BG_MEDIUM)
        header_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Account type controls
        self.account_vars = {}
        self.count_vars = {}
        self.count_entries = {}
        
        account_types = [
            ('blank', 'BLANK', 'Minimal accounts (version + ticket_cost only)'),
            ('roster', 'ROSTER', 'Guild roster data only'),
            ('mail', 'MAIL', 'Raffle mail data only'),
            ('mixed', 'MIXED', 'Complete accounts (roster + mail)')
        ]
        
        for i, (key, display_name, description) in enumerate(account_types):
            row = i + 1
            
            # Checkbox
            var = tk.BooleanVar()
            self.account_vars[key] = var
            checkbox = ttk.Checkbutton(section_frame,
                                     text=f"[{display_name}]",
                                     variable=var,
                                     style='Hacker.TCheckbutton',
                                     command=self.update_preview)
            checkbox.grid(row=row, column=0, sticky="w", padx=10, pady=5)
            
            # Count entry
            count_var = tk.StringVar()
            self.count_vars[key] = count_var
            count_entry = ttk.Entry(section_frame,
                                   textvariable=count_var,
                                   width=8,
                                   style='Hacker.TEntry')
            count_entry.grid(row=row, column=1, padx=(10, 20), pady=5)
            count_entry.bind('<KeyRelease>', lambda e: self.update_preview())
            self.count_entries[key] = count_entry
            
            # Description
            desc_label = tk.Label(section_frame,
                                 text=description,
                                 font=('Consolas', 9),
                                 fg=HackerTheme.FG_GRAY,
                                 bg=HackerTheme.BG_MEDIUM,
                                 anchor='w')
            desc_label.grid(row=row, column=2, columnspan=2, sticky="w", padx=10, pady=5)
            
    def create_settings_section(self, parent):
        """Create settings configuration section"""
        section_frame = tk.Frame(parent, bg=HackerTheme.BG_MEDIUM, relief='ridge', bd=1)
        section_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        section_frame.grid_columnconfigure(1, weight=1)
        section_frame.grid_columnconfigure(3, weight=1)
        
        # Section header
        header_label = tk.Label(section_frame,
                               text=">>> CONFIGURATION <<<",
                               font=('Consolas', 12, 'bold'),
                               fg=HackerTheme.FG_PRIMARY,
                               bg=HackerTheme.BG_MEDIUM)
        header_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Ticket Cost
        tk.Label(section_frame, text="[TICKET_COST]", font=('Consolas', 10),
                fg=HackerTheme.FG_SECONDARY, bg=HackerTheme.BG_MEDIUM).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.ticket_cost_var = tk.StringVar()
        ticket_cost_entry = ttk.Entry(section_frame, textvariable=self.ticket_cost_var, width=15, style='Hacker.TEntry')
        ticket_cost_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        ticket_cost_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # Roster Entries
        tk.Label(section_frame, text="[ROSTER_ENTRIES]", font=('Consolas', 10),
                fg=HackerTheme.FG_SECONDARY, bg=HackerTheme.BG_MEDIUM).grid(row=1, column=2, sticky="w", padx=10, pady=5)
        
        self.roster_entries_var = tk.StringVar()
        roster_entries_entry = ttk.Entry(section_frame, textvariable=self.roster_entries_var, width=15, style='Hacker.TEntry')
        roster_entries_entry.grid(row=1, column=3, sticky="w", padx=10, pady=5)
        roster_entries_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # Mail Entries
        tk.Label(section_frame, text="[MAIL_ENTRIES]", font=('Consolas', 10),
                fg=HackerTheme.FG_SECONDARY, bg=HackerTheme.BG_MEDIUM).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        self.mail_entries_var = tk.StringVar()
        mail_entries_entry = ttk.Entry(section_frame, textvariable=self.mail_entries_var, width=15, style='Hacker.TEntry')
        mail_entries_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        mail_entries_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
    def create_output_section(self, parent):
        """Create output file configuration section"""
        section_frame = tk.Frame(parent, bg=HackerTheme.BG_MEDIUM, relief='ridge', bd=1)
        section_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        section_frame.grid_columnconfigure(1, weight=1)
        
        # Section header
        header_label = tk.Label(section_frame,
                               text=">>> OUTPUT FILE <<<",
                               font=('Consolas', 12, 'bold'),
                               fg=HackerTheme.FG_PRIMARY,
                               bg=HackerTheme.BG_MEDIUM)
        header_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Filename
        tk.Label(section_frame, text="[FILENAME]", font=('Consolas', 10),
                fg=HackerTheme.FG_SECONDARY, bg=HackerTheme.BG_MEDIUM).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.filename_var = tk.StringVar()
        filename_entry = ttk.Entry(section_frame, textvariable=self.filename_var, style='Hacker.TEntry')
        filename_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Browse button
        browse_btn = tk.Button(section_frame, text="📁",
                              bg=HackerTheme.BG_LIGHT, fg=HackerTheme.FG_ACCENT,
                              font=('Consolas', 10), relief='ridge', bd=1,
                              command=self.browse_file)
        browse_btn.grid(row=1, column=2, padx=10, pady=5)
        
    def create_preview_section(self, parent):
        """Create data preview section"""
        section_frame = tk.Frame(parent, bg=HackerTheme.BG_MEDIUM, relief='ridge', bd=1)
        section_frame.grid(row=4, column=0, sticky="ew", pady=(0, 15))
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Section header
        header_label = tk.Label(section_frame,
                               text=">>> GENERATION PREVIEW <<<",
                               font=('Consolas', 12, 'bold'),
                               fg=HackerTheme.FG_PRIMARY,
                               bg=HackerTheme.BG_MEDIUM)
        header_label.grid(row=0, column=0, pady=10)
        
        # Preview text
        self.preview_var = tk.StringVar()
        self.preview_label = tk.Label(section_frame,
                                     textvariable=self.preview_var,
                                     font=('Consolas', 9),
                                     fg=HackerTheme.FG_WHITE,
                                     bg=HackerTheme.BG_MEDIUM,
                                     justify='left',
                                     anchor='w')
        self.preview_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg=HackerTheme.BG_DARK)
        button_frame.grid(row=5, column=0, pady=(0, 15))
        
        # Generate button
        self.generate_btn = tk.Button(button_frame, text="⚡ GENERATE DATA ⚡",
                                     font=('Consolas', 12, 'bold'),
                                     bg=HackerTheme.FG_PRIMARY, fg=HackerTheme.BG_DARK,
                                     relief='ridge', bd=2, padx=20, pady=10,
                                     command=self.generate_data)
        self.generate_btn.grid(row=0, column=0, padx=10)
        
        # Validate button
        validate_btn = tk.Button(button_frame, text="🔍 VALIDATE",
                                font=('Consolas', 10),
                                bg=HackerTheme.BG_LIGHT, fg=HackerTheme.FG_ACCENT,
                                relief='ridge', bd=1, padx=15, pady=5,
                                command=self.validate_last_file)
        validate_btn.grid(row=0, column=1, padx=10)
        
        # Reset button
        reset_btn = tk.Button(button_frame, text="🔄 RESET",
                             font=('Consolas', 10),
                             bg=HackerTheme.BG_LIGHT, fg=HackerTheme.WARNING,
                             relief='ridge', bd=1, padx=15, pady=5,
                             command=self.reset_to_defaults)
        reset_btn.grid(row=0, column=2, padx=10)
        
    def create_output_area(self, parent):
        """Create output/log area with fixed height"""
        section_frame = tk.Frame(parent, bg=HackerTheme.BG_MEDIUM, relief='ridge', bd=1)
        section_frame.grid(row=6, column=0, sticky="ew", pady=(15, 0))
        section_frame.grid_rowconfigure(1, weight=0)  # Don't expand
        section_frame.grid_columnconfigure(0, weight=1)
        
        # Section header
        header_label = tk.Label(section_frame,
                               text=">>> SYSTEM OUTPUT <<<",
                               font=('Consolas', 12, 'bold'),
                               fg=HackerTheme.FG_PRIMARY,
                               bg=HackerTheme.BG_MEDIUM)
        header_label.grid(row=0, column=0, pady=10)
        
        # Output text area with scrollbar - FIXED HEIGHT
        output_frame = tk.Frame(section_frame, bg=HackerTheme.BG_MEDIUM)
        output_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        output_frame.grid_rowconfigure(0, weight=0)  # Don't expand
        output_frame.grid_columnconfigure(0, weight=1)
        
        self.output_text = tk.Text(output_frame,
                                  bg=HackerTheme.BG_DARK,
                                  fg=HackerTheme.FG_PRIMARY,
                                  font=('Consolas', 9),
                                  relief='flat',
                                  wrap=tk.WORD,
                                  height=6)  # Fixed height
        self.output_text.grid(row=0, column=0, sticky="ew")
        
        scrollbar = tk.Scrollbar(output_frame, command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.config(yscrollcommand=scrollbar.set)
        
        # Initial message
        self.log_message("⚡ RaffleManager Data Generator initialized")
        self.log_message("📁 Ready to generate ESO addon test data...")
        self.log_message("💡 Tip: Use mouse wheel to scroll, Ctrl+G to generate")
        
        # Add keyboard shortcuts
        self.root.bind('<Control-g>', lambda e: self.generate_data())
        self.root.bind('<Control-r>', lambda e: self.reset_to_defaults())
        self.root.bind('<F5>', lambda e: self.update_preview())
        
        # Make Enter key work in entry fields
        for entry in [self.ticket_cost_var, self.roster_entries_var, self.mail_entries_var]:
            # We'll bind this after the entry widgets are created
            pass
        
    def load_settings(self):
        """Load settings from config into GUI"""
        # Account types and counts
        account_types_enabled = self.config.get('account_types_enabled', {})
        account_counts = self.config.get('account_counts', {})
        
        for account_type in ['blank', 'roster', 'mail', 'mixed']:
            # Set checkbox state
            enabled = account_types_enabled.get(account_type, True)
            self.account_vars[account_type].set(enabled)
            
            # Set count
            count = account_counts.get(account_type, 10)
            self.count_vars[account_type].set(str(count))
            
            # Update entry state
            self.update_entry_state(account_type)
        
        # Other settings
        self.ticket_cost_var.set(str(self.config.get('default_ticket_cost', 1000)))
        self.roster_entries_var.set(str(self.config.get('roster_entries_per_account', 10)))
        self.mail_entries_var.set(str(self.config.get('mail_entries_per_account', 10)))
        self.filename_var.set(self.config.get('default_output_filename', 'RaffleManager_Generated.lua'))
        
        self.update_preview()
        
    def save_settings(self):
        """Save current GUI settings to config"""
        # Account types and counts
        account_types_enabled = {}
        account_counts = {}
        
        for account_type in ['blank', 'roster', 'mail', 'mixed']:
            account_types_enabled[account_type] = self.account_vars[account_type].get()
            try:
                account_counts[account_type] = int(self.count_vars[account_type].get() or "0")
            except ValueError:
                account_counts[account_type] = 0
        
        # Update config
        self.config['account_types_enabled'] = account_types_enabled
        self.config['account_counts'] = account_counts
        
        try:
            self.config['default_ticket_cost'] = int(self.ticket_cost_var.get() or "1000")
        except ValueError:
            self.config['default_ticket_cost'] = 1000
            
        try:
            self.config['roster_entries_per_account'] = int(self.roster_entries_var.get() or "10")
        except ValueError:
            self.config['roster_entries_per_account'] = 10
            
        try:
            self.config['mail_entries_per_account'] = int(self.mail_entries_var.get() or "10")
        except ValueError:
            self.config['mail_entries_per_account'] = 10
        
        self.config['default_output_filename'] = self.filename_var.get() or 'RaffleManager_Generated.lua'
        
        save_config(self.config)
        
    def update_entry_state(self, account_type):
        """Update entry field state based on checkbox"""
        enabled = self.account_vars[account_type].get()
        entry = self.count_entries[account_type]
        
        if enabled:
            entry.configure(state='normal')
        else:
            entry.configure(state='disabled')
            
    def update_preview(self):
        """Update the generation preview"""
        try:
            total_accounts = 0
            account_details = []
            
            for account_type in ['blank', 'roster', 'mail', 'mixed']:
                if self.account_vars[account_type].get():
                    count = int(self.count_vars[account_type].get() or "0")
                    if count > 0:
                        total_accounts += count
                        
                        if account_type == 'roster':
                            roster_entries = int(self.roster_entries_var.get() or "10")
                            account_details.append(f"• {count} {account_type.upper()} accounts ({roster_entries} entries each)")
                        elif account_type == 'mail':
                            mail_entries = int(self.mail_entries_var.get() or "10")
                            account_details.append(f"• {count} {account_type.upper()} accounts ({mail_entries} entries each)")
                        elif account_type == 'mixed':
                            roster_entries = int(self.roster_entries_var.get() or "10")
                            mail_entries = int(self.mail_entries_var.get() or "10")
                            account_details.append(f"• {count} {account_type.upper()} accounts ({roster_entries} roster + {mail_entries} mail)")
                        else:
                            account_details.append(f"• {count} {account_type.upper()} accounts")
                
                # Update entry state
                self.update_entry_state(account_type)
            
            ticket_cost = int(self.ticket_cost_var.get() or "1000")
            filename = self.filename_var.get() or "RaffleManager_Generated.lua"
            
            preview_text = f"TOTAL: {total_accounts} accounts | TICKET_COST: {ticket_cost}\n"
            preview_text += f"OUTPUT: {filename}\n\n"
            preview_text += "\n".join(account_details) if account_details else "⚠ No accounts selected"
            
            self.preview_var.set(preview_text)
            
            # Enable/disable generate button
            self.generate_btn.configure(state='normal' if total_accounts > 0 else 'disabled')
            
        except ValueError:
            self.preview_var.set("⚠ Invalid input - please check your values")
            self.generate_btn.configure(state='disabled')
            
    def browse_file(self):
        """Open file dialog for output filename"""
        filename = filedialog.asksaveasfilename(
            title="Save RaffleManager Data As",
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua"), ("All files", "*.*")]
        )
        if filename:
            self.filename_var.set(os.path.basename(filename))
            
    def log_message(self, message: str, level: str = "info"):
        """Add a message to the output log"""
        timestamp = time.strftime("%H:%M:%S")
        
        if level == "error":
            color_tag = "error"
            prefix = "❌"
        elif level == "warning":
            color_tag = "warning"
            prefix = "⚠️"
        elif level == "success":
            color_tag = "success"
            prefix = "✅"
        else:
            color_tag = "info"
            prefix = "ℹ️"
            
        formatted_message = f"[{timestamp}] {prefix} {message}\n"
        
        # Configure color tags
        self.output_text.tag_configure("error", foreground=HackerTheme.ERROR)
        self.output_text.tag_configure("warning", foreground=HackerTheme.WARNING)
        self.output_text.tag_configure("success", foreground=HackerTheme.SUCCESS)
        self.output_text.tag_configure("info", foreground=HackerTheme.FG_PRIMARY)
        
        # Insert message
        self.output_text.insert(tk.END, formatted_message, color_tag)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
        
    def generate_data(self):
        """Generate the data file"""
        try:
            self.save_settings()
            
            # Get parameters
            blank_count = int(self.count_vars['blank'].get() or "0") if self.account_vars['blank'].get() else 0
            roster_count = int(self.count_vars['roster'].get() or "0") if self.account_vars['roster'].get() else 0
            mail_count = int(self.count_vars['mail'].get() or "0") if self.account_vars['mail'].get() else 0
            mixed_count = int(self.count_vars['mixed'].get() or "0") if self.account_vars['mixed'].get() else 0
            
            ticket_cost = int(self.ticket_cost_var.get() or "1000")
            roster_entries = int(self.roster_entries_var.get() or "10")
            mail_entries = int(self.mail_entries_var.get() or "10")
            filename = self.filename_var.get() or "RaffleManager_Generated.lua"
            
            if blank_count + roster_count + mail_count + mixed_count == 0:
                self.log_message("No accounts selected for generation", "error")
                return
                
            self.log_message(f"Starting generation of {filename}...")
            self.generate_btn.configure(state='disabled', text="⚡ GENERATING...")
            
            # Run generation in thread to prevent GUI freeze
            def generate_thread():
                try:
                    generator = RaffleDataGenerator()
                    generator.generate_file(
                        blank_count, roster_count, mail_count, mixed_count,
                        filename, ticket_cost, roster_entries, mail_entries
                    )
                    
                    total_accounts = blank_count + roster_count + mail_count + mixed_count
                    self.root.after(0, lambda: self.log_message(
                        f"Successfully generated {filename} with {total_accounts} accounts", "success"))
                    
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Generation failed: {str(e)}", "error"))
                finally:
                    self.root.after(0, lambda: self.generate_btn.configure(
                        state='normal', text="⚡ GENERATE DATA ⚡"))
            
            threading.Thread(target=generate_thread, daemon=True).start()
            
        except ValueError as e:
            self.log_message(f"Invalid input: {str(e)}", "error")
        except Exception as e:
            self.log_message(f"Error: {str(e)}", "error")
            
    def validate_last_file(self):
        """Validate the last generated file"""
        filename = self.filename_var.get() or "RaffleManager_Generated.lua"
        
        if not os.path.exists(filename):
            self.log_message(f"File {filename} not found", "error")
            return
            
        self.log_message(f"Validating {filename}...")
        
        try:
            # Run validation scripts
            def validate_thread():
                try:
                    # Validate roster data
                    result = subprocess.run([sys.executable, "validate.py", filename], 
                                          capture_output=True, text=True, encoding='utf-8')
                    if result.returncode == 0:
                        self.root.after(0, lambda: self.log_message("Roster validation passed", "success"))
                        if result.stdout.strip():
                            self.root.after(0, lambda: self.log_message(result.stdout.strip(), "info"))
                    else:
                        error_msg = result.stderr.strip() if result.stderr else "Unknown validation error"
                        self.root.after(0, lambda: self.log_message(f"Roster validation failed: {error_msg}", "error"))
                    
                    # Check mail amounts if applicable
                    if os.path.exists("check_amounts.py"):
                        result = subprocess.run([sys.executable, "check_amounts.py", filename], 
                                              capture_output=True, text=True, encoding='utf-8')
                        if result.returncode == 0:
                            self.root.after(0, lambda: self.log_message("Mail amount validation passed", "success"))
                            if result.stdout.strip():
                                # Log the amount validation details
                                lines = result.stdout.strip().split('\n')
                                for line in lines[:3]:  # Show first 3 lines of output
                                    self.root.after(0, lambda l=line: self.log_message(l, "info"))
                        else:
                            error_msg = result.stderr.strip() if result.stderr else "Unknown validation error"
                            self.root.after(0, lambda: self.log_message(f"Mail validation failed: {error_msg}", "error"))
                            
                except Exception as e:
                    self.root.after(0, lambda: self.log_message(f"Validation error: {str(e)}", "error"))
            
            threading.Thread(target=validate_thread, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"Validation error: {str(e)}", "error")
            
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        result = messagebox.askyesno("Reset Settings", 
                                    "Reset all settings to program defaults?\n\nThis cannot be undone.")
        if result:
            # Update config with defaults
            self.config.update(DEFAULT_CONFIG)
            self.config['account_types_enabled'] = {
                'blank': True, 'roster': True, 'mail': True, 'mixed': True
            }
            self.config['account_counts'] = {
                'blank': 5, 'roster': 10, 'mail': 15, 'mixed': 20
            }
            save_config(self.config)
            
            # Reload GUI
            self.load_settings()
            self.log_message("Settings reset to defaults", "success")
            
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = RaffleManagerGUI()
    app.run()
