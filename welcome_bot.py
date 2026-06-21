import os
import threading
import discord
from discord.ext import commands
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- RENDER DEPLOYMENT FIX (DUMMY SERVER) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"root@rebellion network is online.")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_dummy_server)
server_thread.daemon = True
server_thread.start()

# --- PERSISTENT VERIFICATION VIEW ---
class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Initialize Verification", style=discord.ButtonStyle.green, custom_id="verify_button_root_rebellion")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        verified_role = discord.utils.get(guild.roles, name="Verified")
        unverified_role = discord.utils.get(guild.roles, name="Unverified")
        
        if not verified_role or not unverified_role:
            await interaction.response.send_message("[ERROR] Missing roles.", ephemeral=True)
            return

        member = interaction.user
        try:
            await member.add_roles(verified_role)
            await member.remove_roles(unverified_role)
            await interaction.response.send_message("[SUCCESS] Identity decrypted. Welcome to the network.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("[ERROR] Insufficient permissions.", ephemeral=True)

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.members = True  
intents.message_content = True

class RebellionBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(VerifyView())

bot = RebellionBot()

@bot.event
async def on_ready():
    print(f"[SYSTEM] Logged in as {bot.user.name}")

# --- COMMANDS ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_verify(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="root@rebellion:~# Access Control",
        description="```\nClick the button below to initialize verification.\n
```",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=VerifyView())

@bot.command()
async def ctf(ctx):
    embed = discord.Embed(
        title="CTF Challenge #1: Cryptography",
        description="Decode this string to find the flag:\n```text\nZmxhZ3toZWxsb19mcm9tX2Jhc2U2NH0=\n```",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"[SYSTEM] Wiped {amount} messages from the logs.", delete_after=5)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"[SYSTEM] {member.mention} has been forcefully disconnected. (Kick)")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"[SYSTEM] {member.mention} has been blacklisted from the network. (Ban)")

# --- JOIN / LEAVE HANDLERS ---
@bot.event
async def on_member_join(member):
    guild = member.guild
    unverified_role = discord.utils.get(guild.roles, name="Unverified")
    if unverified_role:
        try:
            await member.add_roles(unverified_role)
        except:
            pass

    joins_channel = discord.utils.get(guild.text_channels, name="joins")
    if joins_channel:
        file = discord.File("welcome_banner.gif", filename="welcome_banner.gif")
        embed = discord.Embed(
            title="Incoming Connection",
            description=f"```\nUser: {member.name}\nID: {member.id}\nStatus: Unverified\n
```",
            color=discord.Color.green()
        )
        embed.set_image(url="attachment://welcome_banner.gif")
        await joins_channel.send(f"{member.mention} breached the firewall.", embed=embed, file=file)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    leaves_channel = discord.utils.get(guild.text_channels, name="leaves")
    if leaves_channel:
        file = discord.File("leave_banner.gif", filename="leave_banner.gif")
        embed = discord.Embed(
            title="Connection Terminated",
            description=f"```\nUser: {member.name}\nID: {member.id}\nStatus: Disconnected\n```",
            color=discord.Color.red()
        )
        embed.set_image(url="attachment://leave_banner.gif")
        await leaves_channel.send(f"**{member.name}** dropped from the network.", embed=embed, file=file)

# --- EXECUTION ---
TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)
