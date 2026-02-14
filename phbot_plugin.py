"""
Silkroad phBot Plugin Template
This is a base structure for creating phBot plugins
"""

import phBot
from phBot import *

# phBot API functions used in this plugin (imported via wildcard import above):
# - log(message): Logs messages to the bot console
# - get_character_data(): Returns dictionary with character information (HP, MP, etc.)

# ====================================================================================================
# Plugin Information (Required)
# ====================================================================================================

pName = "MyPlugin"  # Plugin name that will be displayed in the bot
pVersion = "1.0.0"  # Plugin version
# WARNING: Generate a unique GUID for your plugin! Use an online GUID generator.
# Never use this default GUID in production - it MUST be unique for each plugin.
pGuid = "00000000-0000-0000-0000-000000000000"  # Unique identifier (generate a new GUID for your plugin)


# ====================================================================================================
# Plugin Functions
# ====================================================================================================

def event_loop():
    """
    This function is called repeatedly by the bot (every ~500ms)
    Use this for continuous checks or actions that need to run periodically
    """
    # Example: Check character status periodically
    # character = get_character_data()
    # if character:
    #     log("Character is alive and running")
    pass


def handle_event(event_type, data):
    """
    This function handles various events triggered by the bot
    
    Args:
        event_type (int): The type of event that occurred
        data: Event-specific data (format varies by event type)
    
    Common event types:
        0 - Bot started
        1 - Bot stopped
        2 - Connected to server
        3 - Disconnected from server
        4 - Character spawned/loaded
        5 - Character died
    """
    if event_type == 0:
        log("Plugin: Bot started")
    elif event_type == 1:
        log("Plugin: Bot stopped")
    elif event_type == 2:
        log("Plugin: Connected to server")
    elif event_type == 3:
        log("Plugin: Disconnected from server")
    elif event_type == 4:
        log("Plugin: Character spawned")
    elif event_type == 5:
        log("Plugin: Character died")


# ====================================================================================================
# Logging Functions
# ====================================================================================================

def log_to_console(message):
    """
    Helper function to log messages to the bot's console
    
    Usage:
        log_to_console("This is a test message")
    
    You can also use phBot's built-in log function directly:
        log("Your message here")
    """
    log(f"[{pName}] {message}")


# ====================================================================================================
# Character Data Functions
# ====================================================================================================

def get_character_info():
    """
    Reads and returns character data (HP, MP, etc.)
    
    Returns:
        dict: Character information including HP, MP, and other stats
    
    Example usage:
        char_data = get_character_info()
        if char_data:
            log_to_console(f"HP: {char_data['hp']}/{char_data['max_hp']}")
            log_to_console(f"MP: {char_data['mp']}/{char_data['max_mp']}")
    """
    # Get character data from phBot
    character = get_character_data()
    
    if character:
        char_info = {
            'name': character['name'],
            'hp': character['hp'],
            'max_hp': character['max_hp'],
            'mp': character['mp'],
            'max_mp': character['max_mp'],
            'hp_percent': (character['hp'] / character['max_hp'] * 100) if character['max_hp'] > 0 else 0,
            'mp_percent': (character['mp'] / character['max_mp'] * 100) if character['max_mp'] > 0 else 0,
            'level': character.get('level', 0),
            'exp': character.get('exp', 0),
            'gold': character.get('gold', 0)
        }
        return char_info
    
    return None


# ====================================================================================================
# Additional Event Handlers (Optional but commonly used)
# ====================================================================================================

def joined_game():
    """
    Called when character successfully joins the game world
    """
    log_to_console("Character joined the game")
    
    # Example: Get and display character info when joining
    char_info = get_character_info()
    if char_info:
        log_to_console(f"Character: {char_info['name']}")
        log_to_console(f"Level: {char_info['level']}")
        log_to_console(f"HP: {char_info['hp']}/{char_info['max_hp']} ({char_info['hp_percent']:.1f}%)")
        log_to_console(f"MP: {char_info['mp']}/{char_info['max_mp']} ({char_info['mp_percent']:.1f}%)")


def handle_chat(message_type, player_name, message):
    """
    Called when a chat message is received
    
    Args:
        message_type (int): Type of message (1=All, 2=Private, 3=Party, 4=Guild, etc.)
        player_name (str): Name of the player who sent the message
        message (str): The actual message content
    """
    # Example: Log all chat messages
    # log_to_console(f"[Chat] {player_name}: {message}")
    pass


def handle_silkroad_response(opcode, data):
    """
    Called when the bot receives a packet from the server
    
    Args:
        opcode (int): The packet opcode
        data (bytes): The raw packet data
    
    Use this for advanced packet handling
    """
    pass


def handle_joymax_message(opcode, data):
    """
    Called when sending packets to the server
    
    Args:
        opcode (int): The packet opcode
        data (bytes): The raw packet data
    
    Return False to block the packet, True to allow it
    """
    return True


# ====================================================================================================
# Plugin Initialization
# ====================================================================================================

# This code runs when the plugin is loaded
log_to_console(f"Plugin loaded successfully - Version {pVersion}")

# Validate that the GUID has been changed from the default template value
if pGuid == "00000000-0000-0000-0000-000000000000":
    log_to_console("WARNING: You are using the default GUID!")
    log_to_console("WARNING: Please generate a unique GUID for your plugin to avoid conflicts!")
else:
    log_to_console("Plugin is ready to use")

# ====================================================================================================
# Usage Examples and Notes
# ====================================================================================================
"""
HOW TO USE THIS PLUGIN:

1. LOGGING MESSAGES:
   - Use log("message") to log directly to console
   - Use log_to_console("message") to log with plugin name prefix
   
   Example:
       log("Simple message")
       log_to_console("Message with plugin name")

2. READING CHARACTER DATA (HP/MP):
   - Call get_character_info() to get current character stats
   
   Example:
       char = get_character_info()
       if char:
           current_hp = char['hp']
           max_hp = char['max_hp']
           hp_percentage = char['hp_percent']
           
           # Check if HP is low
           if hp_percentage < 30:
               log_to_console("Warning: HP is low!")

3. EVENT LOOP:
   - event_loop() runs continuously (every ~500ms)
   - Use for periodic checks or actions
   
   Example:
       def event_loop():
           char = get_character_info()
           if char and char['hp_percent'] < 50:
               # Use HP potion or take action
               pass

4. HANDLING EVENTS:
   - handle_event() is called when specific game events occur
   - Useful for responding to bot state changes
   
   Example:
       def handle_event(event_type, data):
           if event_type == 5:  # Character died
               log_to_console("Character died! Respawning...")

IMPORTANT NOTES:
- Always generate a unique GUID for pGuid (you can use online GUID generators)
- The plugin must be placed in the phBot/Plugins folder
- Restart the bot or use the reload plugins command after making changes
- Test your plugin thoroughly before using it in production
"""
