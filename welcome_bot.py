import discord
import os
import threading
from discord.ext import commands
from discord.ui import Button, View
from http.server import BaseHTTPRequestHandler, HTTPServer

# ── RENDER DEPLOYMENT FIX ──────────────────────────────────
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

# ── BOT SETUP ──────────────────────────────────────────────
TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD_ID = 1515008902821838948

WELCOME_GIF = "https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/welcome_banner.gif"
LEAVE_GIF   = "https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/leave_banner.gif"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class RebellionBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Register persistent views so buttons work after restarts
        self.add_view(VerifyView())
        self.add_view(AgeView())
        self.add_view(RegionView())
        self.add_view(GenderView())
        self.add_view(HackerView())
        self.add_view(HackerView2())

bot = RebellionBot()

# ── TOGGLE ROLE HELPER ─────────────────────────────────────
async def toggle_role(interaction: discord.Interaction, role_name: str):
    guild = interaction.guild
    member = interaction.user
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        await interaction.response.send_message(f"Role `{role_name}` not found!", ephemeral=True)
        return
    if role in member.roles:
        await member.remove_roles(role)
        await interaction.response.send_message(f"❌ Removed: **{role_name}**", ephemeral=True)
    else:
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ Added: **{role_name}**", ephemeral=True)

# ── VIEWS ──────────────────────────────────────────────────
class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verify Me", style=discord.ButtonStyle.green, custom_id="verify_btn")
    async def verify(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        verified = discord.utils.get(guild.roles, name="Verified")
        unverified = discord.utils.get(guild.roles, name="Unverified")
        
        if verified and verified in member.roles:
            await interaction.response.send_message("Already verified!", ephemeral=True)
            return
            
        if verified:
            await member.add_roles(verified)
        if unverified and unverified in member.roles:
            await member.remove_roles(unverified)
            
        await interaction.response.send_message(
            "✅ Access granted! Go to **#self-roles** and pick your roles!", 
            ephemeral=True
        )

class AgeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="18+", style=discord.ButtonStyle.blurple, custom_id="age_18plus")
    async def age_18plus(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "18+")

    @discord.ui.button(label="18-", style=discord.ButtonStyle.gray, custom_id="age_18minus")
    async def age_18minus(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "18-")

class RegionView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🇮🇳 India", style=discord.ButtonStyle.blurple, custom_id="region_india")
    async def india(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "India")

    @discord.ui.button(label="🌏 Asia", style=discord.ButtonStyle.blurple, custom_id="region_asia")
    async def asia(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Asia")

    @discord.ui.button(label="🇺🇸 USA", style=discord.ButtonStyle.blurple, custom_id="region_usa")
    async def usa(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "USA")

    @discord.ui.button(label="🌍 Europe", style=discord.ButtonStyle.blurple, custom_id="region_europe")
    async def europe(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Europe")

    @discord.ui.button(label="🌎 Other", style=discord.ButtonStyle.gray, custom_id="region_other")
    async def other(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Other")

class GenderView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="He/Him", style=discord.ButtonStyle.blurple, custom_id="gender_he")
    async def he(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "He/Him")

    @discord.ui.button(label="She/Her", style=discord.ButtonStyle.blurple, custom_id="gender_she")
    async def she(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "She/Her")

    @discord.ui.button(label="They/Them", style=discord.ButtonStyle.gray, custom_id="gender_they")
    async def they(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "They/Them")

class HackerView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔓 Pentester", style=discord.ButtonStyle.green, custom_id="rank_pentester")
    async def pentester(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Pentester")

    @discord.ui.button(label="🐛 Bug Bounty Hunter", style=discord.ButtonStyle.green, custom_id="rank_bbh")
    async def bbh(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Bug Bounty Hunter")

    @discord.ui.button(label="💻 Developer", style=discord.ButtonStyle.green, custom_id="rank_dev")
    async def dev(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Developer")

    @discord.ui.button(label="🎯 CTF Player", style=discord.ButtonStyle.green, custom_id="rank_ctf")
    async def ctf(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "CTF Player")

    @discord.ui.button(label="🔧 OSINT Analyst", style=discord.ButtonStyle.green, custom_id="rank_osint")
    async def osint(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "OSINT Analyst")

class HackerView2(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💉 Exploit Dev", style=discord.ButtonStyle.red, custom_id="rank_exploit")
    async def exploit(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Exploit Dev")

    @discord.ui.button(label="🌐 Web App Tester", style=discord.ButtonStyle.blurple, custom_id="rank_wat")
    async def wat(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Web App Tester")

    @discord.ui.button(label="🕵️ OSINT", style=discord.ButtonStyle.blurple, custom_id="rank_osint2")
    async def osint2(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "OSINT Analyst")

    @discord.ui.button(label="👶 Script Kiddie", style=discord.ButtonStyle.gray, custom_id="rank_sk")
    async def sk(self, interaction: discord.Interaction, button: Button):
        await toggle_role(interaction, "Script Kiddie")

# ── ON READY ───────────────────────────────────────────────
@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
    print(f"✅ root@rebellion:~# bot online as {bot.user}")

    if not guild:
        return

    # Post verify button
    verify_ch = next((c for c in guild.text_channels if "verify" in c.name), None)
    if verify_ch:
        async for msg in verify_ch.history(limit=10):
            if msg.author == bot.user:
                await msg.delete()
        embed = discord.Embed(
            title="🔐 SYSTEM VERIFICATION",
            description="> `Scanning identity...`\n> `Checking credentials...`\n> `Press button to authenticate.`\n\nClick below to gain access to **Root Rebellion**.",
            color=0x00FF41
        )
        embed.set_footer(text="root@rebellion:~# ./verify.sh")
        await verify_ch.send(embed=embed, view=VerifyView())
        print("✅ Verify button posted")

    # Post self-roles buttons
    roles_ch = next((c for c in guild.text_channels if "self-roles" in c.name), None)
    if roles_ch:
        async for msg in roles_ch.history(limit=20):
            if msg.author == bot.user:
                await msg.delete()

        embed1 = discord.Embed(title="🔞 Age", description="Pick your age group.", color=0x9B59B6)
        await roles_ch.send(embed=embed1, view=AgeView())

        embed2 = discord.Embed(title="🌍 Region", description="Pick your region.", color=0x3498DB)
        await roles_ch.send(embed=embed2, view=RegionView())

        embed3 = discord.Embed(title="⚧ Gender", description="Pick your pronouns.", color=0xE91E63)
        await roles_ch.send(embed=embed3, view=GenderView())

        embed4 = discord.Embed(title="💀 Hacker Rank", description="Pick your specialization — multiple allowed.", color=0x00FF41)
        await roles_ch.send(embed=embed4, view=HackerView())
        await roles_ch.send(view=HackerView2())

        print("✅ Self-roles posted")

# ── WELCOME / LEAVE ────────────────────────────────────────
@bot.event
async def on_member_join(member):
    guild = member.guild
    unverified = discord.utils.get(guild.roles, name="Unverified")
    if unverified:
        await member.add_roles(unverified)
    
    channel = next((c for c in guild.text_channels if "joins" in c.name), None)
    if not channel:
        return
        
    embed = discord.Embed(
        description=f"> `Initializing new connection...`\n> `Scanning user profile...`\n> `Access point detected.`\n> `root@rebellion:~# ./welcome.sh`\n\n# 👾 {member.mention} has entered the grid.\n\n**Read the rules. Verify yourself. Own the system.**",
        color=0x00FF41
    )
    embed.set_image(url=WELCOME_GIF)
    embed.add_field(name="👤 User", value=member.mention, inline=True)
    embed.add_field(name="🪪 ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="👥 Member #", value=f"`{guild.member_count}`", inline=True)
    embed.add_field(name="📅 Account Age", value=f"<t:{int(member.created_at.timestamp())}:R>", inline=True)
    embed.set_footer(text="root@rebellion:~# WE EXPLOIT. WE LEARN. WE OWN.")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = next((c for c in guild.text_channels if "leaves" in c.name), None)
    if not channel:
        return
        
    embed = discord.Embed(
        description=f"> `Closing session...`\n> `Clearing traces...`\n> `Connection terminated.`\n> `root@rebellion:~# ./goodbye.sh`\n\n# 💀 **{member.name}** has left the grid.\n\n**You left. The impact stays. Good luck.**",
        color=0xFF0000
    )
    embed.set_image(url=LEAVE_GIF)
    embed.add_field(name="👤 User", value=f"`{member.name}`", inline=True)
    embed.add_field(name="🪪 ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="👥 Members Left", value=f"`{guild.member_count}`", inline=True)
    embed.set_footer(text="root@rebellion:~# SESSION CLOSED.")
    await channel.send(embed=embed)

# ── COMMANDS ───────────────────────────────────────────────
@bot.command()
async def ctf(ctx):
    embed = discord.Embed(
        title="CTF Challenge #1: Cryptography",
        description="Decode this string to find the flag:\n```text\nZmxhZ3toZWxsb19mcm9tX2Jhc2U2NH0=\n
```",
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

if TOKEN:
    bot.run(TOKEN)
else:
    print("[FATAL] DISCORD_TOKEN variable missing from environment.")
