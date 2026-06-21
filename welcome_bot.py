import os
import discord
from discord.ext import commands

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
            await interaction.response.send_message("[ERROR] Missing 'Verified' or 'Unverified' roles.", ephemeral=True)
            return

        member = interaction.user
        
        try:
            await member.add_roles(verified_role)
            await member.remove_roles(unverified_role)
            await interaction.response.send_message("[SUCCESS] Identity decrypted. Welcome to the network, operative.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("[ERROR] Insufficient permissions. Check role hierarchy.", ephemeral=True)

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
    print(f"[SYSTEM] Logged in as {bot.user.name} ({bot.user.id})")
    print("[SYSTEM] Persistent verification listener active.")

# --- VERIFY SETUP COMMAND ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_verify(ctx):
    await ctx.message.delete()
    
    embed = discord.Embed(
        title="root@rebellion:~# Access Control Protocol",
        description=(
            "```\n"
            "============= SECURITY GATEWAY =============\n"
            "Unauthorized access detected.\n"
            "To unlock the community channels and complete your \n"
            "onboarding, you must initialize verification.\n\n"
            "By clicking the button below, you agree to follow \n"
            "the server directives and respect the network rules.\n"
            "============================================\n"
            "
```"
        ),
        color=discord.Color.from_rgb(0, 255, 0)
    )
    await ctx.send(embed=embed, view=VerifyView())

# --- JOIN HANDLER ---
@bot.event
async def on_member_join(member):
    guild = member.guild
    unverified_role = discord.utils.get(guild.roles, name="Unverified")
    if unverified_role:
        try:
            await member.add_roles(unverified_role)
        except discord.Forbidden:
            print("[ERROR] Cannot assign Unverified role.")

    joins_channel = discord.utils.get(guild.text_channels, name="joins")
    if joins_channel:
        embed = discord.Embed(
            title="Incoming Connection Detected",
            description=f"```\nUser: {member.name}\nID: {member.id}\nStatus: Unverified\nMember Count: {guild.member_count}\n```",
            color=discord.Color.from_rgb(0, 255, 0)
        )
        embed.set_image(url="https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/welcome_banner.gif")
        await joins_channel.send(f"{member.mention} has breached the firewall.", embed=embed)

# --- LEAVE HANDLER ---
@bot.event
async def on_member_remove(member):
    guild = member.guild
    leaves_channel = discord.utils.get(guild.text_channels, name="leaves")
    
    if leaves_channel:
        embed = discord.Embed(
            title="Connection Terminated",
            description=f"```\nUser: {member.name}\nID: {member.id}\nStatus: Disconnected\nRemaining Operatives: {guild.member_count}\n
```",
            color=discord.Color.from_rgb(255, 0, 0)
        )
        embed.set_image(url="https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/leave_banner.gif")
        await leaves_channel.send(f"**{member.name}** has dropped from the network.", embed=embed)

# --- EXECUTION ---
TOKEN = os.environ.get("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("[FATAL] DISCORD_TOKEN variable missing from environment.")
