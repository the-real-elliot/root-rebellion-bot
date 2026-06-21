import discord
import os
import asyncio
from discord.ui import Button, View

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = 1515008902821838948
MOD_ROLES = ["OWNER", "ADMINISTRATOR", "TheRealElliot", "HEAD MOD", "MODERATOR"]

WELCOME_GIF = "https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/welcome_banner.gif"
LEAVE_GIF   = "https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/leave_banner.gif"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

def has_mod_role(member):
    return any(r.name in MOD_ROLES for r in member.roles)

def mod_embed(title, desc, color=0x00FF41):
    e = discord.Embed(title=title, description=desc, color=color)
    e.set_footer(text="root@rebellion:~# MOD ACTION")
    return e

# ── VERIFY VIEW ────────────────────────────────────────────
class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verify Me", style=discord.ButtonStyle.green, custom_id="verify_btn")
    async def verify(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        verified = discord.utils.get(guild.roles, name="Verified")
        unverified = discord.utils.get(guild.roles, name="Unverified")
        if verified in member.roles:
            await interaction.response.send_message("Already verified!", ephemeral=True)
            return
        await member.add_roles(verified)
        if unverified in member.roles:
            await member.remove_roles(unverified)
        await interaction.response.send_message("✅ Access granted! Go to **#self-roles** and pick your roles!", ephemeral=True)

# ── SELF ROLES ─────────────────────────────────────────────
class AgeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="18+", style=discord.ButtonStyle.blurple, custom_id="age_18plus")
    async def age_18plus(self, interaction, button):
        await toggle_role(interaction, "18+")

    @discord.ui.button(label="18-", style=discord.ButtonStyle.gray, custom_id="age_18minus")
    async def age_18minus(self, interaction, button):
        await toggle_role(interaction, "18-")

class RegionView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🇮🇳 India", style=discord.ButtonStyle.blurple, custom_id="region_india")
    async def india(self, interaction, button):
        await toggle_role(interaction, "India")

    @discord.ui.button(label="🌏 Asia", style=discord.ButtonStyle.blurple, custom_id="region_asia")
    async def asia(self, interaction, button):
        await toggle_role(interaction, "Asia")

    @discord.ui.button(label="🇺🇸 USA", style=discord.ButtonStyle.blurple, custom_id="region_usa")
    async def usa(self, interaction, button):
        await toggle_role(interaction, "USA")

    @discord.ui.button(label="🌍 Europe", style=discord.ButtonStyle.blurple, custom_id="region_europe")
    async def europe(self, interaction, button):
        await toggle_role(interaction, "Europe")

    @discord.ui.button(label="🌎 Other", style=discord.ButtonStyle.gray, custom_id="region_other")
    async def other(self, interaction, button):
        await toggle_role(interaction, "Other")

class GenderView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="He/Him", style=discord.ButtonStyle.blurple, custom_id="gender_he")
    async def he(self, interaction, button):
        await toggle_role(interaction, "He/Him")

    @discord.ui.button(label="She/Her", style=discord.ButtonStyle.blurple, custom_id="gender_she")
    async def she(self, interaction, button):
        await toggle_role(interaction, "She/Her")

    @discord.ui.button(label="They/Them", style=discord.ButtonStyle.gray, custom_id="gender_they")
    async def they(self, interaction, button):
        await toggle_role(interaction, "They/Them")

class HackerView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔓 Pentester", style=discord.ButtonStyle.green, custom_id="rank_pentester")
    async def pentester(self, interaction, button):
        await toggle_role(interaction, "Pentester")

    @discord.ui.button(label="🐛 Bug Bounty Hunter", style=discord.ButtonStyle.green, custom_id="rank_bbh")
    async def bbh(self, interaction, button):
        await toggle_role(interaction, "Bug Bounty Hunter")

    @discord.ui.button(label="💻 Developer", style=discord.ButtonStyle.green, custom_id="rank_dev")
    async def dev(self, interaction, button):
        await toggle_role(interaction, "Developer")

    @discord.ui.button(label="🎯 CTF Player", style=discord.ButtonStyle.green, custom_id="rank_ctf")
    async def ctf(self, interaction, button):
        await toggle_role(interaction, "CTF Player")

    @discord.ui.button(label="🔧 OSINT Analyst", style=discord.ButtonStyle.green, custom_id="rank_osint")
    async def osint(self, interaction, button):
        await toggle_role(interaction, "OSINT Analyst")

class HackerView2(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="💉 Exploit Dev", style=discord.ButtonStyle.red, custom_id="rank_exploit")
    async def exploit(self, interaction, button):
        await toggle_role(interaction, "Exploit Dev")

    @discord.ui.button(label="🌐 Web App Tester", style=discord.ButtonStyle.blurple, custom_id="rank_wat")
    async def wat(self, interaction, button):
        await toggle_role(interaction, "Web App Tester")

    @discord.ui.button(label="👶 Script Kiddie", style=discord.ButtonStyle.gray, custom_id="rank_sk")
    async def sk(self, interaction, button):
        await toggle_role(interaction, "Script Kiddie")

async def toggle_role(interaction, role_name):
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

# ── ON READY ───────────────────────────────────────────────
@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    print(f"✅ root@rebellion:~# bot online as {client.user}")

    client.add_view(VerifyView())
    client.add_view(AgeView())
    client.add_view(RegionView())
    client.add_view(GenderView())
    client.add_view(HackerView())
    client.add_view(HackerView2())

    verify_ch = next((c for c in guild.text_channels if "verify" in c.name), None)
    if verify_ch:
        async for msg in verify_ch.history(limit=10):
            if msg.author == client.user:
                await msg.delete()
        embed = discord.Embed(
            title="🔐 SYSTEM VERIFICATION",
            description="> `Scanning identity...`\n> `Checking credentials...`\n> `Press button to authenticate.`\n\nClick below to gain access to **Root Rebellion**.",
            color=0x00FF41
        )
        embed.set_footer(text="root@rebellion:~# ./verify.sh")
        await verify_ch.send(embed=embed, view=VerifyView())
        print("✅ Verify button posted")

    roles_ch = next((c for c in guild.text_channels if "self-roles" in c.name), None)
    if roles_ch:
        async for msg in roles_ch.history(limit=20):
            if msg.author == client.user:
                await msg.delete()
        await roles_ch.send(embed=discord.Embed(title="🔞 Age", description="Pick your age group.", color=0x9B59B6), view=AgeView())
        await roles_ch.send(embed=discord.Embed(title="🌍 Region", description="Pick your region.", color=0x3498DB), view=RegionView())
        await roles_ch.send(embed=discord.Embed(title="⚧ Gender", description="Pick your pronouns.", color=0xE91E63), view=GenderView())
        await roles_ch.send(embed=discord.Embed(title="💀 Hacker Rank", description="Pick your specialization.", color=0x00FF41), view=HackerView())
        await roles_ch.send(view=HackerView2())
        print("✅ Self-roles posted")

# ── MODERATION ─────────────────────────────────────────────
@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    parts = content.split()
    if not parts:
        return

    cmd = parts[0].lower()
    invoker = message.author

    # ── !kick ──
    if cmd == "!kick":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!kick @user reason`", 0xFFA500))
            return
        target = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason provided"
        await target.kick(reason=reason)
        await message.channel.send(embed=mod_embed("👢 USER KICKED", f"`{target}` was kicked.\n**Reason:** {reason}", 0xFFA500))

    # ── !ban ──
    elif cmd == "!ban":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!ban @user reason`", 0xFFA500))
            return
        target = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason provided"
        await target.ban(reason=reason)
        await message.channel.send(embed=mod_embed("🔨 USER BANNED", f"`{target}` was banned.\n**Reason:** {reason}", 0xFF0000))

    # ── !unban ──
    elif cmd == "!unban":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if len(parts) < 2:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!unban username#0000`", 0xFFA500))
            return
        username = parts[1]
        bans = [entry async for entry in message.guild.bans()]
        for entry in bans:
            if str(entry.user) == username:
                await message.guild.unban(entry.user)
                await message.channel.send(embed=mod_embed("✅ USER UNBANNED", f"`{entry.user}` was unbanned.", 0x00FF41))
                return
        await message.channel.send(embed=mod_embed("❌ NOT FOUND", f"`{username}` not found in ban list.", 0xFF0000))

    # ── !mute ──
    elif cmd == "!mute":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!mute @user minutes reason`", 0xFFA500))
            return
        target = message.mentions[0]
        minutes = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10
        reason = " ".join(parts[3:]) if len(parts) > 3 else "No reason provided"
        await target.timeout(discord.utils.utcnow() + __import__('datetime').timedelta(minutes=minutes), reason=reason)
        await message.channel.send(embed=mod_embed("🔇 USER MUTED", f"`{target}` muted for **{minutes} min**.\n**Reason:** {reason}", 0xFFA500))

    # ── !unmute ──
    elif cmd == "!unmute":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!unmute @user`", 0xFFA500))
            return
        target = message.mentions[0]
        await target.timeout(None)
        await message.channel.send(embed=mod_embed("🔊 USER UNMUTED", f"`{target}` has been unmuted.", 0x00FF41))

    # ── !purge ──
    elif cmd == "!purge":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        deleted = await message.channel.purge(limit=amount + 1)
        msg = await message.channel.send(embed=mod_embed("🗑️ PURGED", f"Deleted **{len(deleted)-1}** messages.", 0x00FF41))
        await asyncio.sleep(3)
        await msg.delete()

    # ── !warn ──
    elif cmd == "!warn":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!warn @user reason`", 0xFFA500))
            return
        target = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason provided"
        await message.channel.send(embed=mod_embed("⚠️ USER WARNED", f"{target.mention} has been warned.\n**Reason:** {reason}", 0xFFA500))

    # ── !userinfo ──
    elif cmd == "!userinfo":
        target = message.mentions[0] if message.mentions else message.author
        embed = discord.Embed(title=f"👤 {target.name}", color=0x00FF41)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Roles", value=" ".join([r.mention for r in target.roles[1:]]) or "None", inline=False)
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text="root@rebellion:~# ./userinfo.sh")
        await message.channel.send(embed=embed)

    # ── !serverinfo ──
    elif cmd == "!serverinfo":
        guild = message.guild
        embed = discord.Embed(title=f"🖥️ {guild.name}", color=0x00FF41)
        embed.add_field(name="Members", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Channels", value=f"`{len(guild.text_channels)}`", inline=True)
        embed.add_field(name="Roles", value=f"`{len(guild.roles)}`", inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created", value=f"<t:{int(guild.created_at.timestamp())}:R>", inline=True)
        embed.set_footer(text="root@rebellion:~# ./serverinfo.sh")
        await message.channel.send(embed=embed)

    # ── !commands ──
    elif cmd == "!commands":
        embed = discord.Embed(title="🤖 BOT COMMANDS", color=0x00FF41)
        embed.add_field(name="Moderation", value="`!kick` `!ban` `!unban` `!mute` `!unmute` `!purge` `!warn`", inline=False)
        embed.add_field(name="Info", value="`!userinfo` `!serverinfo`", inline=False)
        embed.set_footer(text="root@rebellion:~# ./help.sh")
        await message.channel.send(embed=embed)

# ── WELCOME / LEAVE ────────────────────────────────────────
@client.event
async def on_member_join(member):
    guild = member.guild
    if member.bot:
        bot_role = discord.utils.get(guild.roles, name="BOT")
        if bot_role:
            await member.add_roles(bot_role)
        return
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

@client.event
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

client.run(TOKEN)
