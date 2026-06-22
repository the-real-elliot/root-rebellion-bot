import discord
import os
import asyncio
import random
import time
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

# ── CHALLENGE BANKS ────────────────────────────────────────
CHALLENGES = {
    "easy": [
        {"id":"e1","category":"🔐 Crypto","title":"ROT13 Decode","desc":"Decode this:\n```\nEbby gur qvpr, pbqr gur jbeyq.\n```","hint":"ROT13 shifts letters by 13.","flag":"flag{roll_the_dice_code_the_world}","points":50},
        {"id":"e2","category":"🔐 Crypto","title":"Base64","desc":"Decode:\n```\nZmxhZ3toZWxsb19oYWNrZXJ9\n```","hint":"Common web encoding.","flag":"flag{hello_hacker}","points":50},
        {"id":"e3","category":"🐧 Linux","title":"Find Files","desc":"What command finds all files named 'passwd' on the system?","hint":"Use find with -name flag.","flag":"flag{find_slash_name_passwd}","points":50},
        {"id":"e4","category":"🐧 Linux","title":"Permissions","desc":"What chmod value gives owner read+write+execute, group read, others nothing?","hint":"Think octal numbers.","flag":"flag{chmod_740}","points":50},
        {"id":"e5","category":"🌐 Web","title":"HTTP Methods","desc":"What HTTP method is used to send data to a server to create a resource?","hint":"Not GET.","flag":"flag{post_method}","points":50},
        {"id":"e6","category":"🌐 Web","title":"Status Codes","desc":"What HTTP status code means 'Unauthorized'?","hint":"4xx range.","flag":"flag{401_unauthorized}","points":50},
        {"id":"e7","category":"💻 Binary","title":"Binary to ASCII","desc":"Convert:\n```\n01100110 01101100 01100001 01100111\n```","hint":"8 bits per character.","flag":"flag{flag}","points":50},
        {"id":"e8","category":"🕵️ OSINT","title":"WHOIS Tool","desc":"What command line tool queries domain registration info?","hint":"Classic recon tool on all Linux systems.","flag":"flag{whois}","points":50},
        {"id":"e9","category":"🔓 Pentest","title":"Ping Scan","desc":"What nmap flag performs a ping scan to find live hosts?","hint":"Single letter flag, -s something.","flag":"flag{nmap_sn_flag}","points":50},
        {"id":"e10","category":"🔐 Crypto","title":"Hex Decode","desc":"Decode:\n```\n666c61677b6865785f69735f656173797d\n```","hint":"Each hex pair = one ASCII char.","flag":"flag{hex_is_easy}","points":50},
    ],
    "medium": [
        {"id":"m1","category":"🔐 Crypto","title":"MD5 Crack","desc":"What is the plaintext of:\n```\n5f4dcc3b5aa765d61d8327deb882cf99\n```","hint":"Very common password.","flag":"flag{password}","points":100},
        {"id":"m2","category":"🌐 Web","title":"SQLi Bypass","desc":"What SQL injection payload bypasses a basic login form?","hint":"Comment out the rest of the query.","flag":"flag{admin_or_1_equals_1}","points":100},
        {"id":"m3","category":"🌐 Web","title":"XSS Payload","desc":"What is the simplest XSS payload to trigger an alert box?","hint":"Uses a script tag.","flag":"flag{script_alert_xss}","points":100},
        {"id":"m4","category":"🐧 Linux","title":"SUID Binaries","desc":"What command finds all SUID binaries for privilege escalation?","hint":"Use find with -perm flag.","flag":"flag{find_suid_binaries}","points":100},
        {"id":"m5","category":"🌐 Web","title":"Clickjacking Header","desc":"What HTTP header prevents clickjacking attacks?","hint":"Tells browser if page can be framed.","flag":"flag{x_frame_options}","points":100},
        {"id":"m6","category":"🔓 Pentest","title":"Service Version","desc":"What nmap flag detects service versions on open ports?","hint":"Single uppercase letter.","flag":"flag{nmap_sv_flag}","points":100},
        {"id":"m7","category":"💻 Reverse","title":"Hex to Text","desc":"Decode:\n```\n666c61677b72657665727365645f697d\n```","hint":"hex → ASCII.","flag":"flag{reversed_i}","points":100},
        {"id":"m8","category":"🕵️ OSINT","title":"Google Dork","desc":"What Google dork finds login pages on example.com?","hint":"Use site: and inurl: operators.","flag":"flag{site_inurl_login}","points":100},
        {"id":"m9","category":"🔐 Crypto","title":"Caesar +13","desc":"Decode (ROT13):\n```\nPbqr vf cbrgel sbe unpxref\n```","hint":"ROT13 again.","flag":"flag{code_is_poetry_for_hackers}","points":100},
        {"id":"m10","category":"🐧 Linux","title":"Network Ports","desc":"What command lists all open ports and listening services on Linux?","hint":"Starts with ss or netstat.","flag":"flag{ss_or_netstat}","points":100},
    ],
    "hard": [
        {"id":"h1","category":"💉 Exploit","title":"Buffer Overflow","desc":"What is the main goal of a stack buffer overflow attack?","hint":"Think return address overwrite.","flag":"flag{overwrite_return_address}","points":200},
        {"id":"h2","category":"🌐 Web","title":"SSRF Attack","desc":"What vulnerability allows attackers to make the server fetch internal resources?","hint":"Server-Side something.","flag":"flag{server_side_request_forgery}","points":200},
        {"id":"h3","category":"🔐 Crypto","title":"Hash Length Extension","desc":"What attack works against MD5/SHA1 MACs where the key is prepended to the message?","hint":"Extends the hash without knowing the key.","flag":"flag{hash_length_extension}","points":200},
        {"id":"h4","category":"💻 Reverse","title":"Assembly","desc":"What does this x86 assembly do?\n```\nxor eax, eax\n```","hint":"Think XOR with itself.","flag":"flag{sets_eax_to_zero}","points":200},
        {"id":"h5","category":"🌐 Web","title":"XXE Attack","desc":"What vulnerability in XML parsers allows reading internal files?","hint":"XML eXternal Entity.","flag":"flag{xml_external_entity}","points":200},
        {"id":"h6","category":"🔓 Pentest","title":"Pass the Hash","desc":"What attack reuses NTLM hashes without cracking them?","hint":"Windows authentication bypass.","flag":"flag{pass_the_hash}","points":200},
        {"id":"h7","category":"🐧 Linux","title":"Cron PrivEsc","desc":"What file would you check for misconfigured cron jobs for privilege escalation?","hint":"System-wide cron table.","flag":"flag{slash_etc_slash_crontab}","points":200},
        {"id":"h8","category":"💉 Exploit","title":"Format String","desc":"What vulnerability occurs when user input is passed directly as the format string to printf()?","hint":"printf(user_input) not printf(\"%s\", user_input).","flag":"flag{format_string_vulnerability}","points":200},
        {"id":"h9","category":"🔐 Crypto","title":"Padding Oracle","desc":"What attack exploits CBC mode decryption error messages to decrypt ciphertext?","hint":"Oracle tells you if padding is valid.","flag":"flag{padding_oracle_attack}","points":200},
        {"id":"h10","category":"🌐 Web","title":"IDOR","desc":"What vulnerability allows accessing other users' data by changing an ID in the URL?","hint":"Insecure Direct Object Reference.","flag":"flag{insecure_direct_object_reference}","points":200},
    ],
    "speedrun": [
        {"id":"s1","category":"⚡ Speed","title":"Quick Fire: Linux","desc":"What command shows current logged in users?","hint":"Short command, starts with w.","flag":"flag{who_or_w}","points":150,"time_limit":30},
        {"id":"s2","category":"⚡ Speed","title":"Quick Fire: Crypto","desc":"What encoding uses A-Z, a-z, 0-9, +, / characters?","hint":"Common in web.","flag":"flag{base64}","points":150,"time_limit":30},
        {"id":"s3","category":"⚡ Speed","title":"Quick Fire: Web","desc":"What does XSS stand for?","hint":"Cross-Site something.","flag":"flag{cross_site_scripting}","points":150,"time_limit":30},
        {"id":"s4","category":"⚡ Speed","title":"Quick Fire: Tools","desc":"What tool is used for web app proxy interception?","hint":"Common Portswigger tool.","flag":"flag{burp_suite}","points":150,"time_limit":30},
        {"id":"s5","category":"⚡ Speed","title":"Quick Fire: Pentest","desc":"What does CVE stand for?","hint":"Common Vulnerabilities and...","flag":"flag{common_vulnerabilities_exposures}","points":150,"time_limit":30},
    ]
}

# State tracking
active_challenges = {}   # user_id → challenge
active_duels = {}        # duel_id → {challenger, challenged, challenge, start_time}
active_speedruns = {}    # user_id → {challenge, start_time}
active_tournaments = {}  # guild_id → tournament data
scores = {}              # user_id → points

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
    async def age_18plus(self, interaction, button): await toggle_role(interaction, "18+")
    @discord.ui.button(label="18-", style=discord.ButtonStyle.gray, custom_id="age_18minus")
    async def age_18minus(self, interaction, button): await toggle_role(interaction, "18-")

class RegionView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🇮🇳 India", style=discord.ButtonStyle.blurple, custom_id="region_india")
    async def india(self, interaction, button): await toggle_role(interaction, "India")
    @discord.ui.button(label="🌏 Asia", style=discord.ButtonStyle.blurple, custom_id="region_asia")
    async def asia(self, interaction, button): await toggle_role(interaction, "Asia")
    @discord.ui.button(label="🇺🇸 USA", style=discord.ButtonStyle.blurple, custom_id="region_usa")
    async def usa(self, interaction, button): await toggle_role(interaction, "USA")
    @discord.ui.button(label="🌍 Europe", style=discord.ButtonStyle.blurple, custom_id="region_europe")
    async def europe(self, interaction, button): await toggle_role(interaction, "Europe")
    @discord.ui.button(label="🌎 Other", style=discord.ButtonStyle.gray, custom_id="region_other")
    async def other(self, interaction, button): await toggle_role(interaction, "Other")

class GenderView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="He/Him", style=discord.ButtonStyle.blurple, custom_id="gender_he")
    async def he(self, interaction, button): await toggle_role(interaction, "He/Him")
    @discord.ui.button(label="She/Her", style=discord.ButtonStyle.blurple, custom_id="gender_she")
    async def she(self, interaction, button): await toggle_role(interaction, "She/Her")
    @discord.ui.button(label="They/Them", style=discord.ButtonStyle.gray, custom_id="gender_they")
    async def they(self, interaction, button): await toggle_role(interaction, "They/Them")

class HackerView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🔓 Pentester", style=discord.ButtonStyle.green, custom_id="rank_pentester")
    async def pentester(self, interaction, button): await toggle_role(interaction, "Pentester")
    @discord.ui.button(label="🐛 Bug Bounty Hunter", style=discord.ButtonStyle.green, custom_id="rank_bbh")
    async def bbh(self, interaction, button): await toggle_role(interaction, "Bug Bounty Hunter")
    @discord.ui.button(label="💻 Developer", style=discord.ButtonStyle.green, custom_id="rank_dev")
    async def dev(self, interaction, button): await toggle_role(interaction, "Developer")
    @discord.ui.button(label="🎯 CTF Player", style=discord.ButtonStyle.green, custom_id="rank_ctf")
    async def ctf(self, interaction, button): await toggle_role(interaction, "CTF Player")
    @discord.ui.button(label="🔧 OSINT Analyst", style=discord.ButtonStyle.green, custom_id="rank_osint")
    async def osint(self, interaction, button): await toggle_role(interaction, "OSINT Analyst")

class HackerView2(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="💉 Exploit Dev", style=discord.ButtonStyle.red, custom_id="rank_exploit")
    async def exploit(self, interaction, button): await toggle_role(interaction, "Exploit Dev")
    @discord.ui.button(label="🌐 Web App Tester", style=discord.ButtonStyle.blurple, custom_id="rank_wat")
    async def wat(self, interaction, button): await toggle_role(interaction, "Web App Tester")
    @discord.ui.button(label="👶 Script Kiddie", style=discord.ButtonStyle.gray, custom_id="rank_sk")
    async def sk(self, interaction, button): await toggle_role(interaction, "Script Kiddie")

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
        embed = discord.Embed(title="🔐 SYSTEM VERIFICATION", description="> `Scanning identity...`\n> `Checking credentials...`\n> `Press button to authenticate.`\n\nClick below to gain access to **Root Rebellion**.", color=0x00FF41)
        embed.set_footer(text="root@rebellion:~# ./verify.sh")
        await verify_ch.send(embed=embed, view=VerifyView())

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

    # ══════════════════════════════════════════
    # CTF PRACTICE
    # ══════════════════════════════════════════

    if cmd == "!ctf":
        pool = CHALLENGES["easy"] + CHALLENGES["medium"] + CHALLENGES["hard"]
        challenge = random.choice(pool)
        active_challenges[invoker.id] = challenge
        embed = discord.Embed(title=f"{challenge['category']} | {challenge['title']}", description=challenge['desc'], color=0x00FF41)
        embed.add_field(name="🏆 Points", value=f"`{challenge['points']} pts`", inline=True)
        embed.add_field(name="📌 Submit", value="`!submit flag{answer}`", inline=True)
        embed.add_field(name="💡 Hint", value="`!hint`", inline=True)
        embed.set_footer(text="root@rebellion:~# CTF MODE")
        await message.channel.send(embed=embed)

    # ══════════════════════════════════════════
    # CHALLENGE BY DIFFICULTY
    # ══════════════════════════════════════════

    elif cmd == "!challenge":
        diff = parts[1].lower() if len(parts) > 1 else "easy"
        if diff not in CHALLENGES:
            await message.channel.send(embed=discord.Embed(description="Usage: `!challenge easy / medium / hard / speedrun`", color=0xFF0000))
            return
        challenge = random.choice(CHALLENGES[diff])
        active_challenges[invoker.id] = challenge
        color = 0x00FF41 if diff == "easy" else 0xFFA500 if diff == "medium" else 0xFF0000 if diff == "hard" else 0x00FFFF
        embed = discord.Embed(title=f"{challenge['category']} | {challenge['title']} [{diff.upper()}]", description=challenge['desc'], color=color)
        embed.add_field(name="🏆 Points", value=f"`{challenge['points']} pts`", inline=True)
        embed.add_field(name="📌 Submit", value="`!submit flag{answer}`", inline=True)
        if diff == "speedrun":
            embed.add_field(name="⏱️ Time Limit", value=f"`{challenge.get('time_limit', 30)} seconds`", inline=True)
        embed.set_footer(text=f"root@rebellion:~# DIFFICULTY: {diff.upper()}")
        await message.channel.send(embed=embed)

    # ══════════════════════════════════════════
    # SPEEDRUN
    # ══════════════════════════════════════════

    elif cmd == "!speedrun":
        challenge = random.choice(CHALLENGES["speedrun"])
        active_speedruns[invoker.id] = {"challenge": challenge, "start_time": time.time()}
        active_challenges[invoker.id] = challenge
        embed = discord.Embed(
            title=f"⚡ SPEEDRUN | {challenge['title']}",
            description=f"> `root@rebellion:~# ./speedrun.sh --start`\n\n{challenge['desc']}\n\n**⏱️ Timer started! You have {challenge.get('time_limit', 30)} seconds!**",
            color=0x00FFFF
        )
        embed.add_field(name="Submit", value="`!submit flag{answer}`", inline=True)
        embed.add_field(name="Points", value=f"`{challenge['points']} pts`", inline=True)
        embed.set_footer(text="root@rebellion:~# CLOCK IS TICKING")
        msg = await message.channel.send(embed=embed)

        await asyncio.sleep(challenge.get('time_limit', 30))
        if invoker.id in active_speedruns:
            del active_speedruns[invoker.id]
            if invoker.id in active_challenges:
                del active_challenges[invoker.id]
            timeout_embed = discord.Embed(title="⏰ TIME'S UP", description=f"{invoker.mention} ran out of time! Use `!speedrun` to try again.", color=0xFF0000)
            await message.channel.send(embed=timeout_embed)

    # ══════════════════════════════════════════
    # 1v1 DUEL
    # ══════════════════════════════════════════

    elif cmd == "!duel":
        if not message.mentions:
            await message.channel.send(embed=discord.Embed(description="Usage: `!duel @user`", color=0xFF0000))
            return
        target = message.mentions[0]
        if target == invoker:
            await message.channel.send(embed=discord.Embed(description="You can't duel yourself!", color=0xFF0000))
            return
        if target.bot:
            await message.channel.send(embed=discord.Embed(description="Can't duel a bot!", color=0xFF0000))
            return

        diff = parts[2].lower() if len(parts) > 2 and parts[2].lower() in CHALLENGES else "medium"
        challenge = random.choice(CHALLENGES[diff])
        duel_id = f"{invoker.id}_{target.id}"
        active_duels[duel_id] = {
            "challenger": invoker.id,
            "challenged": target.id,
            "challenge": challenge,
            "start_time": time.time(),
            "channel": message.channel.id
        }
        active_challenges[invoker.id] = challenge
        active_challenges[target.id] = challenge

        embed = discord.Embed(
            title="⚔️ 1v1 DUEL INITIATED",
            description=f"> `root@rebellion:~# ./duel.sh --pvp`\n\n{invoker.mention} has challenged {target.mention} to a **1v1 hack duel!**\n\n**First to submit the correct flag wins!**",
            color=0xFF6600
        )
        embed.add_field(name="⚔️ Challenger", value=invoker.mention, inline=True)
        embed.add_field(name="🎯 Target", value=target.mention, inline=True)
        embed.add_field(name="Difficulty", value=f"`{diff.upper()}`", inline=True)
        embed.add_field(name="Category", value=challenge['category'], inline=True)
        embed.add_field(name="Points", value=f"`{challenge['points']} pts to winner`", inline=True)
        embed.set_footer(text="root@rebellion:~# MAY THE BEST HACKER WIN")
        await message.channel.send(embed=embed)

        challenge_embed = discord.Embed(
            title=f"🚩 DUEL CHALLENGE | {challenge['title']}",
            description=challenge['desc'],
            color=0xFF6600
        )
        challenge_embed.add_field(name="Submit", value="`!submit flag{answer}`", inline=True)
        challenge_embed.add_field(name="Hint", value="`!hint`", inline=True)
        await message.channel.send(embed=challenge_embed)

    # ══════════════════════════════════════════
    # TOURNAMENT
    # ══════════════════════════════════════════

    elif cmd == "!tournament":
        sub = parts[1].lower() if len(parts) > 1 else ""

        if sub == "start":
            if not has_mod_role(invoker):
                await message.channel.send(embed=discord.Embed(description="Only mods can start tournaments!", color=0xFF0000))
                return
            diff = parts[2].lower() if len(parts) > 2 and parts[2].lower() in CHALLENGES else "medium"
            active_tournaments[message.guild.id] = {
                "players": [],
                "diff": diff,
                "status": "signup",
                "scores": {}
            }
            embed = discord.Embed(
                title="🏆 TOURNAMENT STARTING",
                description=f"> `root@rebellion:~# ./tournament.sh --{diff}`\n\n**A {diff.upper()} difficulty tournament is open!**\n\nType `!tournament join` to enter.\nMod types `!tournament begin` to start when ready.",
                color=0xFFD700
            )
            embed.set_footer(text="root@rebellion:~# ENTER THE ARENA")
            await message.channel.send(embed=embed)

        elif sub == "join":
            t = active_tournaments.get(message.guild.id)
            if not t or t["status"] != "signup":
                await message.channel.send(embed=discord.Embed(description="No tournament open to join! Wait for a mod to start one.", color=0xFF0000))
                return
            if invoker.id in t["players"]:
                await message.channel.send(embed=discord.Embed(description="You're already in!", ephemeral=True, color=0xFFA500))
                return
            t["players"].append(invoker.id)
            t["scores"][invoker.id] = 0
            await message.channel.send(embed=discord.Embed(description=f"⚔️ {invoker.mention} joined the tournament! **{len(t['players'])} players** registered.", color=0x00FF41))

        elif sub == "begin":
            if not has_mod_role(invoker):
                await message.channel.send(embed=discord.Embed(description="Only mods can begin the tournament!", color=0xFF0000))
                return
            t = active_tournaments.get(message.guild.id)
            if not t or len(t["players"]) < 2:
                await message.channel.send(embed=discord.Embed(description="Need at least 2 players!", color=0xFF0000))
                return
            t["status"] = "active"
            t["round"] = 1
            t["round_scores"] = {pid: 0 for pid in t["players"]}
            challenge = random.choice(CHALLENGES[t["diff"]])
            t["current_challenge"] = challenge
            for pid in t["players"]:
                active_challenges[pid] = challenge

            mentions = " ".join([f"<@{pid}>" for pid in t["players"]])
            embed = discord.Embed(
                title="🏆 TOURNAMENT ROUND 1",
                description=f"> `root@rebellion:~# ./round.sh --1`\n\n**Players:** {mentions}\n\nFirst correct flag gets **+{challenge['points']} pts**. Keep going until the tournament ends!",
                color=0xFFD700
            )
            embed.add_field(name="Challenge", value=f"{challenge['category']} | **{challenge['title']}**", inline=False)
            embed.add_field(name="Description", value=challenge['desc'], inline=False)
            embed.add_field(name="Submit", value="`!submit flag{answer}`", inline=True)
            embed.set_footer(text="root@rebellion:~# ROUND 1 — FIGHT")
            await message.channel.send(embed=embed)

        elif sub == "standings":
            t = active_tournaments.get(message.guild.id)
            if not t:
                await message.channel.send(embed=discord.Embed(description="No active tournament.", color=0xFF0000))
                return
            sorted_players = sorted(t["scores"].items(), key=lambda x: x[1], reverse=True)
            desc = ""
            medals = ["🥇","🥈","🥉"]
            for i, (pid, pts) in enumerate(sorted_players):
                medal = medals[i] if i < 3 else f"`{i+1}.`"
                user = message.guild.get_member(pid)
                name = user.mention if user else f"`{pid}`"
                desc += f"{medal} {name} — **{pts} pts**\n"
            embed = discord.Embed(title="🏆 TOURNAMENT STANDINGS", description=desc, color=0xFFD700)
            await message.channel.send(embed=embed)

        elif sub == "end":
            if not has_mod_role(invoker):
                await message.channel.send(embed=discord.Embed(description="Only mods can end the tournament!", color=0xFF0000))
                return
            t = active_tournaments.pop(message.guild.id, None)
            if not t:
                await message.channel.send(embed=discord.Embed(description="No active tournament.", color=0xFF0000))
                return
            sorted_players = sorted(t["scores"].items(), key=lambda x: x[1], reverse=True)
            desc = ""
            medals = ["🥇","🥈","🥉"]
            for i, (pid, pts) in enumerate(sorted_players[:5]):
                medal = medals[i] if i < 3 else f"`{i+1}.`"
                user = message.guild.get_member(pid)
                name = user.mention if user else f"`{pid}`"
                desc += f"{medal} {name} — **{pts} pts**\n"
                scores[pid] = scores.get(pid, 0) + pts
            embed = discord.Embed(title="🏆 TOURNAMENT OVER", description=f"**Final Standings:**\n{desc}", color=0xFFD700)
            embed.set_footer(text="root@rebellion:~# GG — POINTS ADDED TO LEADERBOARD")
            await message.channel.send(embed=embed)

    # ══════════════════════════════════════════
    # SUBMIT FLAG
    # ══════════════════════════════════════════

    elif cmd == "!submit":
        challenge = active_challenges.get(invoker.id)
        if not challenge:
            await message.channel.send(embed=discord.Embed(description="No active challenge! Use `!ctf`, `!challenge`, `!speedrun`, or `!duel`.", color=0xFF0000))
            return
        if len(parts) < 2:
            await message.channel.send(embed=discord.Embed(description="Usage: `!submit flag{answer}`", color=0xFF0000))
            return
        submitted = parts[1].strip().lower()
        correct = challenge['flag'].lower()

        if submitted == correct:
            pts = challenge['points']

            # Check speedrun bonus
            speedrun_data = active_speedruns.pop(invoker.id, None)
            bonus = 0
            if speedrun_data:
                elapsed = time.time() - speedrun_data['start_time']
                time_limit = challenge.get('time_limit', 30)
                if elapsed < time_limit / 2:
                    bonus = 50
                    pts += bonus

            # Check duel win
            duel_won = None
            for duel_id, duel in list(active_duels.items()):
                if invoker.id in [duel['challenger'], duel['challenged']]:
                    opponent_id = duel['challenged'] if invoker.id == duel['challenger'] else duel['challenger']
                    duel_won = opponent_id
                    del active_duels[duel_id]
                    if opponent_id in active_challenges:
                        del active_challenges[opponent_id]
                    break

            # Check tournament
            t = active_tournaments.get(message.guild.id)
            if t and t.get("status") == "active" and invoker.id in t["players"]:
                t["scores"][invoker.id] = t["scores"].get(invoker.id, 0) + pts
                next_challenge = random.choice(CHALLENGES[t["diff"]])
                t["current_challenge"] = next_challenge
                for pid in t["players"]:
                    active_challenges[pid] = next_challenge

            scores[invoker.id] = scores.get(invoker.id, 0) + pts
            del active_challenges[invoker.id]

            if duel_won:
                opponent = message.guild.get_member(duel_won)
                embed = discord.Embed(
                    title="⚔️ DUEL WINNER!",
                    description=f"🏆 {invoker.mention} wins the duel!\n{'💀 ' + opponent.mention + ' has been defeated!' if opponent else ''}\n+**{pts} points** added.",
                    color=0x00FF41
                )
            elif speedrun_data:
                elapsed = round(time.time() - speedrun_data['start_time'] + (50 if bonus else 0), 2)
                embed = discord.Embed(
                    title="⚡ SPEEDRUN COMPLETE!",
                    description=f"{invoker.mention} completed the speedrun!\n{'🔥 **SPEED BONUS +50 pts!**' if bonus else ''}\n+**{pts} points** | Total: **{scores[invoker.id]} pts**",
                    color=0x00FFFF
                )
            else:
                embed = discord.Embed(
                    title="✅ CORRECT FLAG!",
                    description=f"{invoker.mention} captured the flag!\n+**{pts} points** | Total: **{scores[invoker.id]} pts**",
                    color=0x00FF41
                )
            embed.set_footer(text="root@rebellion:~# FLAG CAPTURED")
            await message.channel.send(embed=embed)

            if t and t.get("status") == "active":
                nc = t["current_challenge"]
                next_embed = discord.Embed(title=f"🏆 NEXT CHALLENGE | {nc['title']}", description=nc['desc'], color=0xFFD700)
                next_embed.add_field(name="Category", value=nc['category'], inline=True)
                next_embed.add_field(name="Points", value=f"`{nc['points']} pts`", inline=True)
                await message.channel.send(embed=next_embed)
        else:
            await message.channel.send(embed=discord.Embed(title="❌ WRONG FLAG", description="Incorrect. Keep trying or use `!hint`.", color=0xFF0000))

    # ══════════════════════════════════════════
    # HINT
    # ══════════════════════════════════════════

    elif cmd == "!hint":
        challenge = active_challenges.get(invoker.id)
        if not challenge:
            await message.channel.send(embed=discord.Embed(description="No active challenge!", color=0xFF0000))
            return
        await message.channel.send(embed=discord.Embed(title="💡 HINT", description=challenge['hint'], color=0xFFA500))

    elif cmd == "!skip":
        if invoker.id in active_challenges: del active_challenges[invoker.id]
        if invoker.id in active_speedruns: del active_speedruns[invoker.id]
        await message.channel.send(embed=discord.Embed(description="Challenge skipped. Use `!ctf` or `!challenge` for a new one.", color=0xFFA500))

    # ══════════════════════════════════════════
    # SCORES & LEADERBOARD
    # ══════════════════════════════════════════

    elif cmd == "!score":
        target = message.mentions[0] if message.mentions else invoker
        pts = scores.get(target.id, 0)
        await message.channel.send(embed=discord.Embed(title="📊 SCORE", description=f"{target.mention} has **{pts} points**.", color=0x00FF41))

    elif cmd == "!leaderboard":
        if not scores:
            await message.channel.send(embed=discord.Embed(description="No scores yet!", color=0xFF0000))
            return
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        desc = ""
        medals = ["🥇","🥈","🥉"]
        for i, (uid, pts) in enumerate(sorted_scores):
            medal = medals[i] if i < 3 else f"`{i+1}.`"
            user = message.guild.get_member(uid)
            name = user.mention if user else f"`{uid}`"
            desc += f"{medal} {name} — **{pts} pts**\n"
        embed = discord.Embed(title="🏆 LEADERBOARD", description=desc, color=0x00FF41)
        embed.set_footer(text="root@rebellion:~# TOP HACKERS")
        await message.channel.send(embed=embed)

    # ══════════════════════════════════════════
    # MODERATION
    # ══════════════════════════════════════════

    elif cmd == "!kick":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!kick @user reason`", 0xFFA500)); return
        target = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason"
        await target.kick(reason=reason)
        await message.channel.send(embed=mod_embed("👢 KICKED", f"`{target}` kicked.\n**Reason:** {reason}", 0xFFA500))

    elif cmd == "!ban":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!ban @user reason`", 0xFFA500)); return
        target = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason"
        await target.ban(reason=reason)
        await message.channel.send(embed=mod_embed("🔨 BANNED", f"`{target}` banned.\n**Reason:** {reason}", 0xFF0000))

    elif cmd == "!unban":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        if len(parts) < 2:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!unban username#0000`", 0xFFA500)); return
        bans = [entry async for entry in message.guild.bans()]
        for entry in bans:
            if str(entry.user) == parts[1]:
                await message.guild.unban(entry.user)
                await message.channel.send(embed=mod_embed("✅ UNBANNED", f"`{entry.user}` unbanned.", 0x00FF41)); return
        await message.channel.send(embed=mod_embed("❌ NOT FOUND", f"`{parts[1]}` not in ban list.", 0xFF0000))

    elif cmd == "!mute":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!mute @user minutes reason`", 0xFFA500)); return
        target = message.mentions[0]
        minutes = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 10
        reason = " ".join(parts[3:]) if len(parts) > 3 else "No reason"
        await target.timeout(discord.utils.utcnow() + __import__('datetime').timedelta(minutes=minutes), reason=reason)
        await message.channel.send(embed=mod_embed("🔇 MUTED", f"`{target}` muted for **{minutes} min**.", 0xFFA500))

    elif cmd == "!unmute":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!unmute @user`", 0xFFA500)); return
        await message.mentions[0].timeout(None)
        await message.channel.send(embed=mod_embed("🔊 UNMUTED", f"`{message.mentions[0]}` unmuted.", 0x00FF41))

    elif cmd == "!purge":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        amount = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        deleted = await message.channel.purge(limit=amount + 1)
        msg = await message.channel.send(embed=mod_embed("🗑️ PURGED", f"Deleted **{len(deleted)-1}** messages.", 0x00FF41))
        await asyncio.sleep(3)
        await msg.delete()

    elif cmd == "!warn":
        if not has_mod_role(invoker):
            await message.channel.send(embed=mod_embed("❌ ACCESS DENIED", "No permission.", 0xFF0000)); return
        if not message.mentions:
            await message.channel.send(embed=mod_embed("⚠️ USAGE", "`!warn @user reason`", 0xFFA500)); return
        reason = " ".join(parts[2:]) if len(parts) > 2 else "No reason"
        await message.channel.send(embed=mod_embed("⚠️ WARNED", f"{message.mentions[0].mention} warned.\n**Reason:** {reason}", 0xFFA500))

    elif cmd == "!userinfo":
        target = message.mentions[0] if message.mentions else invoker
        embed = discord.Embed(title=f"👤 {target.name}", color=0x00FF41)
        embed.add_field(name="ID", value=f"`{target.id}`", inline=True)
        embed.add_field(name="Joined", value=f"<t:{int(target.joined_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="Roles", value=" ".join([r.mention for r in target.roles[1:]]) or "None", inline=False)
        embed.set_thumbnail(url=target.display_avatar.url)
        await message.channel.send(embed=embed)

    elif cmd == "!serverinfo":
        guild = message.guild
        embed = discord.Embed(title=f"🖥️ {guild.name}", color=0x00FF41)
        embed.add_field(name="Members", value=f"`{guild.member_count}`", inline=True)
        embed.add_field(name="Channels", value=f"`{len(guild.text_channels)}`", inline=True)
        embed.add_field(name="Roles", value=f"`{len(guild.roles)}`", inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        await message.channel.send(embed=embed)

    elif cmd == "!commands":
        embed = discord.Embed(title="🤖 BOT COMMANDS", color=0x00FF41)
        embed.add_field(name="🚩 CTF Practice", value="`!ctf` `!hint` `!submit` `!skip` `!score` `!leaderboard`", inline=False)
        embed.add_field(name="🎯 Challenges", value="`!challenge easy/medium/hard/speedrun`", inline=False)
        embed.add_field(name="⚡ Speedrun", value="`!speedrun` — timed solo challenge", inline=False)
        embed.add_field(name="⚔️ 1v1 Duel", value="`!duel @user` — race to capture the flag", inline=False)
        embed.add_field(name="🏆 Tournament", value="`!tournament start/join/begin/standings/end`", inline=False)
        embed.add_field(name="🔨 Moderation", value="`!kick` `!ban` `!unban` `!mute` `!unmute` `!purge` `!warn`", inline=False)
        embed.add_field(name="ℹ️ Info", value="`!userinfo` `!serverinfo` `!commands`", inline=False)
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
    if not channel: return
    embed = discord.Embed(description=f"> `Initializing new connection...`\n> `Scanning user profile...`\n> `Access point detected.`\n> `root@rebellion:~# ./welcome.sh`\n\n# 👾 {member.mention} has entered the grid.\n\n**Read the rules. Verify yourself. Own the system.**", color=0x00FF41)
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
    if not channel: return
    embed = discord.Embed(description=f"> `Closing session...`\n> `Clearing traces...`\n> `Connection terminated.`\n> `root@rebellion:~# ./goodbye.sh`\n\n# 💀 **{member.name}** has left the grid.\n\n**You left. The impact stays. Good luck.**", color=0xFF0000)
    embed.set_image(url=LEAVE_GIF)
    embed.add_field(name="👤 User", value=f"`{member.name}`", inline=True)
    embed.add_field(name="🪪 ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="👥 Members Left", value=f"`{guild.member_count}`", inline=True)
    embed.set_footer(text="root@rebellion:~# SESSION CLOSED.")
    await channel.send(embed=embed)

client.run(TOKEN)
