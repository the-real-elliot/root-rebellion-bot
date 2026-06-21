import discord
import os
import asyncio
import random
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

# ── CTF CHALLENGES ─────────────────────────────────────────
CTF_CHALLENGES = [
    {
        "id": "c1",
        "category": "🔐 Crypto",
        "title": "Caesar's Secret",
        "description": "Decode this Caesar cipher (ROT13):\n```\nEbby gur qvpr, pbqr gur jbeyq.\n```",
        "hint": "ROT13 shifts each letter by 13 positions.",
        "flag": "flag{roll_the_dice_code_the_world}",
        "points": 50
    },
    {
        "id": "c2",
        "category": "🔐 Crypto",
        "title": "Base Mystery",
        "description": "Decode this:\n```\ZmxhZ3toZWxsb19mcm9tX2Jhc2U2NH0=\n```",
        "hint": "It's encoded in a common web encoding.",
        "flag": "flag{hello_from_base64}",
        "points": 50
    },
    {
        "id": "c3",
        "category": "🔐 Crypto",
        "title": "Hash Cracker",
        "description": "What is the plaintext of this MD5 hash?\n```\n5f4dcc3b5aa765d61d8327deb882cf99\n```",
        "hint": "It's a very common password.",
        "flag": "flag{password}",
        "points": 75
    },
    {
        "id": "c4",
        "category": "🐧 Linux",
        "title": "Command Recon",
        "description": "What command lists all open network connections and their ports on Linux?",
        "hint": "It starts with 'ss' or an older command with 'n' flag.",
        "flag": "flag{ss_or_netstat}",
        "points": 50
    },
    {
        "id": "c5",
        "category": "🐧 Linux",
        "title": "File Secrets",
        "description": "What command searches for the string 'password' recursively in all files under /var/www/?",
        "hint": "Think grep with recursive flag.",
        "flag": "flag{grep_r_password}",
        "points": 50
    },
    {
        "id": "c6",
        "category": "🐧 Linux",
        "title": "SUID Hunt",
        "description": "What command finds all SUID binaries on the system for privilege escalation?",
        "hint": "Use find with -perm flag.",
        "flag": "flag{find_suid_binaries}",
        "points": 100
    },
    {
        "id": "c7",
        "category": "🌐 Web",
        "title": "SQLi Basics",
        "description": "What input in a login form would bypass authentication using SQL injection?",
        "hint": "Think about commenting out the rest of the query.",
        "flag": "flag{admin_or_1_equals_1}",
        "points": 75
    },
    {
        "id": "c8",
        "category": "🌐 Web",
        "title": "XSS Payload",
        "description": "What is the simplest XSS payload to pop an alert box in a browser?",
        "hint": "Uses a script tag.",
        "flag": "flag{script_alert_xss}",
        "points": 75
    },
    {
        "id": "c9",
        "category": "🌐 Web",
        "title": "HTTP Headers",
        "description": "What HTTP response header is used to prevent clickjacking attacks?",
        "hint": "It tells the browser whether the page can be embedded in a frame.",
        "flag": "flag{x_frame_options}",
        "points": 50
    },
    {
        "id": "c10",
        "category": "🕵️ OSINT",
        "title": "WHOIS Recon",
        "description": "What tool do you use to find domain registration info, owner, and nameservers?",
        "hint": "It's a classic recon command available on all Linux systems.",
        "flag": "flag{whois}",
        "points": 50
    },
    {
        "id": "c11",
        "category": "🕵️ OSINT",
        "title": "Google Dork",
        "description": "What Google dork finds exposed login pages on a target site example.com?",
        "hint": "Use site: and inurl: operators.",
        "flag": "flag{site_inurl_login}",
        "points": 75
    },
    {
        "id": "c12",
        "category": "💻 Reverse",
        "title": "Binary Decode",
        "description": "What is the ASCII text of this binary?\n```\n01100110 01101100 01100001 01100111\n```",
        "hint": "Convert each 8-bit group to decimal then to ASCII.",
        "flag": "flag{flag}",
        "points": 75
    },
    {
        "id": "c13",
        "category": "💻 Reverse",
        "title": "Hex Decode",
        "description": "Decode this hex string:\n```\n666c61677b6865785f6d617374657d\n```",
        "hint": "Each pair of hex digits is one ASCII character.",
        "flag": "flag{hex_master}",
        "points": 75
    },
    {
        "id": "c14",
        "category": "🔓 Pentesting",
        "title": "Port Scanner",
        "description": "What nmap command does a fast SYN scan on all 65535 ports of a target?",
        "hint": "Use -sS for SYN scan and -p- for all ports.",
        "flag": "flag{nmap_ss_p_all}",
        "points": 100
    },
    {
        "id": "c15",
        "category": "🔓 Pentesting",
        "title": "Service Detection",
        "description": "What nmap flag detects service versions running on open ports?",
        "hint": "It's a single uppercase letter flag.",
        "flag": "flag{nmap_sv_flag}",
        "points": 50
    },
]

# Track active challenges per user: {user_id: challenge}
active_challenges = {}
# Track scores per user: {user_id: points}
scores = {}

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

# ── ON MESSAGE ─────────────────────────────────────────────
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

    # ── !ctf ──
    if cmd == "!ctf":
        challenge = random.choice(CTF_CHALLENGES)
        active_challenges[invoker.id] = challenge
        embed = discord.Embed(
            title=f"{challenge['category']} | {challenge['title']}",
            description=challenge['description'],
            color=0x00FF41
        )
        embed.add_field(name="🏆 Points", value=f"`{challenge['points']} pts`", inline=True)
        embed.add_field(name="📌 Submit", value="`!submit flag{your_answer}`", inline=True)
        embed.add_field(name="💡 Hint", value="`!hint` for a nudge", inline=True)
        embed.set_footer(text="root@rebellion:~# CTF PRACTICE MODE")
        await message.channel.send(embed=embed)

    # ── !hint ──
    elif cmd == "!hint":
        challenge = active_challenges.get(invoker.id)
        if not challenge:
            await message.channel.send(embed=discord.Embed(description="No active challenge! Use `!ctf` first.", color=0xFF0000))
            return
        await message.channel.send(embed=discord.Embed(
            title="💡 HINT",
            description=challenge['hint'],
            color=0xFFA500
        ))

    # ── !submit ──
    elif cmd == "!submit":
        challenge = active_challenges.get(invoker.id)
        if not challenge:
            await message.channel.send(embed=discord.Embed(description="No active challenge! Use `!ctf` first.", color=0xFF0000))
            return
        if len(parts) < 2:
            await message.channel.send(embed=discord.Embed(description="Usage: `!submit flag{your_answer}`", color=0xFF0000))
            return
        submitted = parts[1].strip().lower()
        correct = challenge['flag'].lower()
        if submitted == correct:
            scores[invoker.id] = scores.get(invoker.id, 0) + challenge['points']
            del active_challenges[invoker.id]
            embed = discord.Embed(
                title="✅ CORRECT FLAG!",
                description=f"**{invoker.mention}** captured the flag!\n+**{challenge['points']} points** added.\nTotal: **{scores[invoker.id]} pts**",
                color=0x00FF41
            )
            embed.set_footer(text="root@rebellion:~# FLAG CAPTURED")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="❌ WRONG FLAG",
                description="That's not right. Keep trying or use `!hint`.",
                color=0xFF0000
            )
            await message.channel.send(embed=embed)

    # ── !score ──
    elif cmd == "!score":
        target = message.mentions[0] if message.mentions else invoker
        pts = scores.get(target.id, 0)
        embed = discord.Embed(
            title="📊 SCORE",
            description=f"{target.mention} has **{pts} points**.",
            color=0x00FF41
        )
        embed.set_footer(text="root@rebellion:~# SCOREBOARD")
        await message.channel.send(embed=embed)

    # ── !leaderboard ──
    elif cmd == "!leaderboard":
        if not scores:
            await message.channel.send(embed=discord.Embed(description="No scores yet! Use `!ctf` to start.", color=0xFF0000))
            return
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        desc = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (uid, pts) in enumerate(sorted_scores):
            medal = medals[i] if i < 3 else f"`{i+1}.`"
            user = message.guild.get_member(uid)
            name = user.mention if user else f"`{uid}`"
            desc += f"{medal} {name} — **{pts} pts**\n"
        embed = discord.Embed(title="🏆 CTF LEADERBOARD", description=desc, color=0x00FF41)
        embed.set_footer(text="root@rebellion:~# TOP HACKERS")
        await message.channel.send(embed=embed)

    # ── !skip ──
    elif cmd == "!skip":
        if invoker.id in active_challenges:
            del active_challenges[invoker.id]
        await message.channel.send(embed=discord.Embed(description="Challenge skipped. Use `!ctf` for a new one.", color=0xFFA500))

    # ── MODERATION ──
    elif cmd == "!kick":
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
        await message.channel.send(embed=mod_embed("❌ NOT FOUND", f"`{username}` not in ban list.", 0xFF0000))

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

    elif cmd == "!unmute":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!unmute @user`", 0xFFA500))
            return
        target = message.mentions[0]
        await target.timeout(None)
        await message.channel.send(embed=mod_embed("🔊 USER UNMUTED", f"`{target}` unmuted.", 0x00FF41))

    elif cmd == "!purge":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        deleted = await message.channel.purge(limit=amount + 1)
        msg = await message.channel.send(embed=mod_embed("🗑️ PURGED", f"Deleted **{len(deleted)-1}** messages.", 0x00FF41))
        await asyncio.sleep(3)
        await msg.delete()

    elif cmd == "!warn":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "You don't have permission.", 0xFF0000))
            return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!warn @user reason`", 0xFFA500))
            return
        target = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason provided"
        await message.channel.send(embed=mod_embed("⚠️ USER WARNED", f"{target.mention} warned.\n**Reason:** {reason}", 0xFFA500))

    elif cmd == "!userinfo":
        target = message.mentions[0] if message.mentions else invoker
        embed = discord.Embed(title=f"👤 {target.name}", color=0x00FF41)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Joined", value=f"<t:{int(target.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Roles", value=" ".join([r.mention for r in target.roles[1:]]) or "None", inline=False)
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text="root@rebellion:~# ./userinfo.sh")
        await message.channel.send(embed=embed)

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

    elif cmd == "!commands":
        embed = discord.Embed(title="🤖 BOT COMMANDS", color=0x00FF41)
        embed.add_field(name="🚩 CTF Practice", value="`!ctf` `!hint` `!submit` `!skip` `!score` `!leaderboard`", inline=False)
        embed.add_field(name="🔨 Moderation", value="`!kick` `!ban` `!unban` `!mute` `!unmute` `!purge` `!warn`", inline=False)
        embed.add_field(name="ℹ️ Info", value="`!userinfo` `!serverinfo` `!commands`", inline=False)
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
