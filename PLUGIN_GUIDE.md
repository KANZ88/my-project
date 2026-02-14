# Silkroad phBot Plugin Guide

This repository contains a base structure for creating Silkroad phBot plugins using Python.

## Overview

The `phbot_plugin.py` file provides a complete template that follows the standard phBot API format, including all required components and helpful examples.

## Plugin Structure

### Required Components

1. **Plugin Information Variables** (Required)
   - `pName`: Plugin name displayed in the bot
   - `pVersion`: Plugin version
   - `pGuid`: Unique identifier (GUID)

2. **Mandatory Functions**
   - `event_loop()`: Called repeatedly by the bot (~500ms interval)
   - `handle_event(event_type, data)`: Handles various game events

### Optional Components

The template includes several optional but commonly used event handlers:
- `joined_game()`: Called when character joins the game world
- `handle_chat()`: Processes chat messages
- `handle_silkroad_response()`: Advanced packet handling (incoming)
- `handle_joymax_message()`: Advanced packet handling (outgoing)

## Key Features

### 1. Console Logging

Two methods for logging messages:

```python
# Direct logging
log("Simple message")

# Logging with plugin name prefix
log_to_console("Message with plugin name")
```

### 2. Reading Character Data (HP/MP)

Get character information including HP, MP, and other stats:

```python
char_info = get_character_info()
if char_info:
    print(f"HP: {char_info['hp']}/{char_info['max_hp']}")
    print(f"MP: {char_info['mp']}/{char_info['max_mp']}")
    print(f"HP%: {char_info['hp_percent']:.1f}%")
    print(f"MP%: {char_info['mp_percent']:.1f}%")
```

Available character data fields:
- `name`: Character name
- `hp`: Current HP
- `max_hp`: Maximum HP
- `mp`: Current MP
- `max_mp`: Maximum MP
- `hp_percent`: HP percentage (0-100)
- `mp_percent`: MP percentage (0-100)
- `level`: Character level
- `exp`: Experience points
- `gold`: Current gold amount

### 3. Event Loop

Use for periodic checks or continuous actions:

```python
def event_loop():
    char = get_character_info()
    if char and char['hp_percent'] < 50:
        log_to_console("Warning: HP is below 50%!")
        # Take action (use potion, etc.)
```

### 4. Event Handling

Respond to specific game events:

```python
def handle_event(event_type, data):
    if event_type == 5:  # Character died
        log_to_console("Character died!")
        # Handle death event
```

Common event types:
- `0`: Bot started
- `1`: Bot stopped
- `2`: Connected to server
- `3`: Disconnected from server
- `4`: Character spawned/loaded
- `5`: Character died

## Installation

1. Generate a unique GUID for your plugin (use an online GUID generator)
2. Update the `pGuid` variable in `phbot_plugin.py`
3. Customize `pName` and `pVersion` as needed
4. Place the plugin file in the `phBot/Plugins` folder
5. Restart the bot or use the reload plugins command

## Customization

To create your own plugin:

1. Copy `phbot_plugin.py` and rename it
2. Update plugin information (pName, pVersion, pGuid)
3. Implement your custom logic in:
   - `event_loop()` for continuous actions
   - `handle_event()` for event responses
   - Add new functions as needed
4. Use the provided helper functions for logging and data access

## Example Use Cases

### Monitor HP and Use Potions

```python
def event_loop():
    char = get_character_info()
    if char and char['hp_percent'] < 30:
        log_to_console(f"HP critical: {char['hp_percent']:.1f}%")
        # Use HP potion command here
```

### Log Character Status on Join

```python
def joined_game():
    char_info = get_character_info()
    if char_info:
        log_to_console(f"Character: {char_info['name']}")
        log_to_console(f"Level: {char_info['level']}")
        log_to_console(f"HP: {char_info['hp']}/{char_info['max_hp']}")
```

### Respond to Death

```python
def handle_event(event_type, data):
    if event_type == 5:  # Character died
        log_to_console("Character died! Preparing to respawn...")
        # Add respawn logic
```

## Best Practices

1. **Always generate a unique GUID** - Never use the default GUID in production
2. **Test thoroughly** - Test your plugin in a safe environment first
3. **Handle errors gracefully** - Use try-except blocks for critical sections
4. **Don't block event_loop()** - Keep operations fast to avoid slowing down the bot
5. **Comment your code** - Document custom logic for future reference

## Notes

- The plugin runs within the phBot environment
- Access to game data depends on phBot's API capabilities
- Some advanced features may require additional phBot modules
- Always check phBot documentation for the latest API changes

## Support

For more information about phBot API and plugin development:
- Visit the official phBot forums
- Check phBot documentation
- Review other plugin examples in the community

## License

This template is provided as-is for educational and development purposes.
