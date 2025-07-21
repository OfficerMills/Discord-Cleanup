# Discord Remote Administration Bot
> **[FiveO Development](https://discord.gg/rc3FXthyzD)**
> **Last Updated:** July 21, 2025

⚠️ **CRITICAL WARNING: This is a powerful administrative tool that can cause irreversible damage to Discord servers. Use with extreme caution and only for legitimate purposes.**

## LEGAL DISCLAIMER AND TERMS OF USE

### IMPORTANT NOTICE - READ BEFORE USE

This Discord bot software ("the Software") is provided for **legitimate administrative purposes only**. By downloading, installing, or using this Software, you agree to the following terms and conditions:

### PROHIBITED USES

**This Software is STRICTLY PROHIBITED from being used for:**

- Server raiding or griefing
- Harassment, abuse, or targeting of individuals or communities
- Circumventing Discord's Terms of Service or Community Guidelines
- Unauthorized access to Discord servers or accounts
- Creating disruption, chaos, or harm to Discord communities
- Any illegal activities under local, state, federal, or international law
- Mass deletion of content without proper authorization
- Any form of cyberbullying, doxxing, or malicious behavior

### USER RESPONSIBILITIES

By using this Software, you acknowledge and agree that:

1. **You are solely responsible** for all actions performed using this Software
2. **You will only use this Software on servers where you have explicit permission** from the server owner
3. **You will comply with all applicable laws** and Discord's Terms of Service
4. **You understand the destructive nature** of the commands and will exercise extreme caution
5. **You will not distribute or share** this Software with individuals who may misuse it

**THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. THE DEVELOPER(S) DISCLAIM ALL LIABILITY for any damages, losses, or consequences resulting from the use or misuse of this Software.**

---

## Overview

This Discord bot provides remote administrative capabilities across multiple servers simultaneously. It's designed for authorized administrators who need to manage multiple Discord servers from a centralized control location.

### Key Features

- **Remote Channel Management**: Delete all channels or create multiple channels in target servers
- **Remote Member Management**: Mass kick members from target servers  
- **Multi-server Support**: Manage multiple Discord servers from one control location
- **Authorization System**: Restricts access to pre-approved user IDs
- **Permission Verification**: Checks bot permissions before executing commands
- **Audit Logging**: Creates logs of operations performed

## Commands

### `/remote-clean`
**⚠️ EXTREMELY DESTRUCTIVE COMMAND**

Remotely deletes ALL channels (text, voice, and categories) from a specified server.

**Parameters:**
- `guild_id` - The Discord server ID where channels should be deleted
- `confirm` - Must type "CONFIRM" to proceed

**Requirements:**
- User must be in `AUTHORIZED_USERS` list
- Bot must have "Manage Channels" permission in target server
- Command must be run from authorized control server (if configured)

### `/remote-purge`
**⚠️ EXTREMELY DESTRUCTIVE COMMAND**

Remotely kicks ALL members from a specified server (except bots and server owner).

**Parameters:**
- `guild_id` - The Discord server ID where members should be kicked
- `confirm` - Must type "CONFIRM" to proceed

**Requirements:**
- User must be in `AUTHORIZED_USERS` list
- Bot must have "Kick Members" permission in target server
- Command must be run from authorized control server (if configured)

### `/remote-create`

Remotely creates multiple channels in a specified server.

**Parameters:**
- `guild_id` - The Discord server ID where channels should be created
- `amount` - Number of channels to create (1-50)
- `channel_type` - Type of channels ("Text" or "Voice")
- `name_prefix` - Optional prefix for channel names

**Requirements:**
- User must be in `AUTHORIZED_USERS` list
- Bot must have "Manage Channels" permission in target server
- Target server must not exceed Discord's 500 channel limit

### `/list-servers`

Lists all servers the bot is currently in, showing server names, IDs, member counts, and bot permissions.

**Requirements:**
- User must be in `AUTHORIZED_USERS` list
- Command must be run from authorized control server (if configured)

## Setup and Configuration

### Prerequisites

- Python 3.8 or higher
- discord.py library (`pip install discord.py`)
- Discord bot token
- Discord application with bot permissions

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install discord.py
   ```

3. Configure the bot by editing these variables in the code:

   ```python
   # Add authorized user Discord IDs
   AUTHORIZED_USERS = [
       1039776738508537907,  # Replace with your Discord User ID
       # Add more user IDs as needed
   ]

   # Optional: Set control server for extra security
   CONTROL_SERVER_ID = 1387814650959364266  # Replace with your control server ID
   ```

4. Replace the bot token:
   ```python
   bot.run('YOUR_BOT_TOKEN_HERE')
   ```

### Required Bot Permissions

The bot needs the following permissions in target servers:
- **Manage Channels** (for channel operations)
- **Kick Members** (for member operations)
- **Send Messages** (for logging)
- **View Channels** (basic functionality)

### Discord Developer Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Under "Privileged Gateway Intents", enable:
   - Server Members Intent
   - Message Content Intent

## Security Features

### Authorization System
- Commands are restricted to users listed in `AUTHORIZED_USERS`
- Optional control server restriction prevents commands from unauthorized servers
- All commands require explicit confirmation for destructive operations

### Permission Verification
- Bot checks its permissions before executing commands
- Operations fail safely if insufficient permissions
- Role hierarchy respected (can't kick members with higher roles)

### Rate Limiting
- Built-in delays prevent Discord API rate limits
- Commands process items sequentially to avoid overwhelming servers

### Logging
- Console logging for all operations
- Attempts to create audit logs in target servers
- Detailed success/failure reporting

## Getting User and Server IDs

### Finding Your Discord User ID
1. Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
2. Right-click your username and select "Copy User ID"

### Finding Server IDs
1. Right-click on server name in Discord server list
2. Select "Copy Server ID"

## Warnings and Best Practices

### ⚠️ CRITICAL WARNINGS

1. **These commands are IRREVERSIBLE** - Deleted channels and kicked members cannot be automatically restored
2. **Test on development servers first** - Never test on production servers
3. **Verify server IDs carefully** - Double-check you're targeting the correct server
4. **Keep bot token secure** - Never share or commit your bot token to public repositories
5. **Limit authorized users** - Only add trusted administrators to the authorized users list

### Best Practices

- **Always backup server configurations** before running destructive commands
- **Communicate with server members** before performing mass operations
- **Use a dedicated control server** for running these commands
- **Monitor bot permissions** regularly across all servers
- **Keep logs** of all operations performed
- **Update authorization lists** as team membership changes

## Error Handling

The bot includes comprehensive error handling:
- Permission checks before command execution
- Graceful handling of rate limits
- Detailed error reporting for failed operations
- Safe fallbacks when operations cannot complete

## Legal and Ethical Considerations

### Legitimate Uses
- Emergency server cleanup after raids or spam attacks
- Server restructuring with proper authorization
- Educational purposes in controlled environments
- Authorized administrative tasks

### Prohibited Uses
- Server raiding or griefing
- Unauthorized access to servers
- Harassment or abuse of communities
- Any illegal activities

### Liability
Users are solely responsible for their use of this software. The developers disclaim all liability for misuse or damages caused by this software.

## Support and Reporting

If you encounter issues or need to report misuse:
- Create an issue in this repository for technical problems
- Report malicious use to Discord Trust & Safety
- Contact local authorities if illegal activity is suspected

## License

This project is provided for educational and legitimate administrative purposes only. Users must comply with all applicable laws and Discord's Terms of Service.

---

**Remember: With great power comes great responsibility. Use this tool wisely and ethically.**