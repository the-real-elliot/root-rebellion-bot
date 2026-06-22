import discord
import os
import threading
from discord.ext import commands
from discord.ui import Button, View
from http.server import BaseHTTPRequestHandler, HTTPServer

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"root@rebellion network is online.")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args): pass

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_dummy_server)
server_thread.daemon = True
server_thread.start()

TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD_ID = 1515008902821838948
WELCOME_GIF = "https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/welcome_banner.gif"
LEAVE_GIF = "https://raw.githubusercontent.com/the-real-elliot/root-rebellion-assets/main/leave_banner.gif"
LEARN_URL = "https://kali-learner--alimhussain1266.replit.app/"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class RebellionBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    async def setup_hook(self):
        self.add_view(VerifyView())
        self.add_view(AgeView())
        self.add_view(RegionView())
        self.add_view(GenderView())
        self.add_view(HackerView())
        self.add_view(HackerView2())
        self.add_view(LearnHackingView())

bot = RebellionBot()

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

class VerifyView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verify Me", style=discord.ButtonStyle.green, custom_id="verify_btn")
    async def verify(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        verified = discord.utils.get(guild.roles, name="Verified")
        unverified = discord.utils.get(guild.roles, name="Unverified")
        if verified and verified in member.roles:
            await interaction.response.send_message("Already verified!", ephemeral=True)
            return
        if verified: await member.add_roles(verified)
        if unverified and unverified in member.roles: await member.remove_roles(unverified)
        await interaction.response.send_message("✅ Access granted! Go to **#self-roles** and pick your roles!", ephemeral=True)

class AgeView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="18+", style=discord.ButtonStyle.blurple, custom_id="age_18plus")
    async def age_18plus(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "18+")
    @discord.ui.button(label="18-", style=discord.ButtonStyle.gray, custom_id="age_18minus")
    async def age_18minus(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "18-")

class RegionView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🇮🇳 India", style=discord.ButtonStyle.blurple, custom_id="region_india")
    async def india(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "India")
    @discord.ui.button(label="🌏 Asia", style=discord.ButtonStyle.blurple, custom_id="region_asia")
    async def asia(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Asia")
    @discord.ui.button(label="🇺🇸 USA", style=discord.ButtonStyle.blurple, custom_id="region_usa")
    async def usa(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "USA")
    @discord.ui.button(label="🌍 Europe", style=discord.ButtonStyle.blurple, custom_id="region_europe")
    async def europe(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Europe")
    @discord.ui.button(label="🌎 Other", style=discord.ButtonStyle.gray, custom_id="region_other")
    async def other(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Other")

class GenderView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="He/Him", style=discord.ButtonStyle.blurple, custom_id="gender_he")
    async def he(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "He/Him")
    @discord.ui.button(label="She/Her", style=discord.ButtonStyle.blurple, custom_id="gender_she")
    async def she(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "She/Her")
    @discord.ui.button(label="They/Them", style=discord.ButtonStyle.gray, custom_id="gender_they")
    async def they(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "They/Them")

class HackerView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🔓 Pentester", style=discord.ButtonStyle.green, custom_id="rank_pentester")
    async def pentester(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Pentester")
    @discord.ui.button(label="🐛 Bug Bounty Hunter", style=discord.ButtonStyle.green, custom_id="rank_bbh")
    async def bbh(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Bug Bounty Hunter")
    @discord.ui.button(label="💻 Developer", style=discord.ButtonStyle.green, custom_id="rank_dev")
    async def dev(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Developer")
    @discord.ui.button(label="🎯 CTF Player", style=discord.ButtonStyle.green, custom_id="rank_ctf")
    async def ctf(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "CTF Player")
    @discord.ui.button(label="🔧 OSINT Analyst", style=discord.ButtonStyle.green, custom_id="rank_osint")
    async def osint(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "OSINT Analyst")

class HackerView2(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="💉 Exploit Dev", style=discord.ButtonStyle.red, custom_id="rank_exploit")
    async def exploit(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Exploit Dev")
    @discord.ui.button(label="🌐 Web App Tester", style=discord.ButtonStyle.blurple, custom_id="rank_wat")
    async def wat(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Web App Tester")
    @discord.ui.button(label="👶 Script Kiddie", style=discord.ButtonStyle.gray, custom_id="rank_sk")
    async def sk(self, interaction: discord.Interaction, button: Button): await toggle_role(interaction, "Script Kiddie")

class LearnHackingView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🧠 Start Learning", style=discord.ButtonStyle.green, custom_id="learn_btn")
    async def learn(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            f"🔓 **Access Granted!**\nYour hacking journey starts here:\n{LEARN_URL}",
            ephemeral=True
        )

CTF_CHALLENGES = {
    "crypto1": ("🔑 Crypto 1 — Base64", "Decode this:\n```ZmxhZ3toZWxsb19mcm9tX2Jhc2U2NH0=```"),
    "crypto2": ("🔑 Crypto 2 — Binary", "Convert binary to ASCII:\n```01100110 01101100 01100001 01100111 01111011 01100010 01101001 01101110 01100001 01110010 01111001 01011111 01101001 01110011 01011111 01100110 01110101 01101110 01111101```"),
    "crypto3": ("🔑 Crypto 3 — Caesar ROT13", "Decode ROT13:\n```synt{ebg_guregrra_vf_rnfl}```"),
    "crypto4": ("🔑 Crypto 4 — Hex", "Convert hex to ASCII:\n```666c61677b6865785f6d61737465727d```"),
    "web1": ("🌐 Web 1 — Robots.txt", "robots.txt found:\n```\nDisallow: /admin-secret-panel/\nDisallow: /flag.txt\n```\nWhat is the flag path?"),
    "web2": ("🌐 Web 2 — SQLi", "Login query:\n```sql\nSELECT * FROM users WHERE user='INPUT' AND pass='INPUT'\n```\nWhat payload bypasses auth? Flag format: `flag{payload}`"),
    "web3": ("🌐 Web 3 — XSS", "Find XSS payload:\n```html\n<input value='USER_INPUT'>\n```\nFlag: `flag{xss_payload}`"),
    "web4": ("🌐 Web 4 — IDOR", "API: `/api/user?id=1` returns admin.\nWhat id gives flag?\nFlag: `flag{idor_found}`"),
    "brute1": ("💥 Brute 1 — PIN Crack", "4-digit PIN. Hint: year between 1990-2000.\nFlag: `flag{year}`"),
    "brute2": ("💥 Brute 2 — MD5 Hash", "Crack this MD5:\n```5f4dcc3b5aa765d61d8327deb882cf99```\nFlag: `flag{plaintext}`"),
    "brute3": ("💥 Brute 3 — Wordlist", "SSH cracked with rockyou.txt top password.\nFlag: `flag{password}`"),
    "brute4": ("💥 Brute 4 — JWT", "JWT with weak secret 'secret'.\nForge admin token.\nFlag: `flag{forged}`"),
    "osint1": ("🕵️ OSINT 1 — Username", "Find GitHub of `th3r34l3ll10t`.\nWhat's the repo name?\nFlag: `flag{repo_name}`"),
    "osint2": ("🕵️ OSINT 2 — IP Recon", "IP: `93.184.216.34`\nWhat domain? Flag: `flag{domain}`"),
    "osint3": ("🕵️ OSINT 3 — GPS", "Lat: 40.7128, Long: -74.0060\nWhat city? Flag: `flag{city}`"),
    "linux1": ("🐧 Linux 1 — Find Flag", "Find hidden flag:\n```bash\nfind /etc -name '*.flag' 2>/dev/null\n```\nFlag: `flag{found_it}`"),
    "linux2": ("🐧 Linux 2 — SUID", "Find SUID binary for privesc:\n```bash\nfind / -perm -4000 2>/dev/null\n```\nFlag: `flag{binary_name}`"),
    "linux3": ("🐧 Linux 3 — Cron", "Crontab:\n```\n* * * * * root /tmp/backup.sh\n```\nHow to exploit? Flag: `flag{exploit_method}`"),
    "net1": ("📡 Network 1 — Nmap", "Open ports: 22, 80, 443, 3306.\nWhat runs on 3306? Flag: `flag{service}`"),
    "net2": ("📡 Network 2 — Wireshark", "Plaintext Telnet capture.\nUsername: admin visible.\nFlag: `flag{admin_password}`"),
    "net3": ("📡 Network 3 — DNS", "TXT record for `rebellion.hack`:\n```\nflag{dns_recon_master}\n```\nFlag?"),
}

CTF_ANSWERS = {
    "crypto1": "flag{hello_from_base64}",
    "crypto2": "flag{binary_is_fun}",
    "crypto3": "flag{rot_thirteen_is_easy}",
    "crypto4": "flag{hex_master}",
    "web1": "flag{flag.txt}",
    "web2": "flag{' OR '1'='1}",
    "web3": "flag{xss_payload}",
    "web4": "flag{idor_found}",
    "brute1": "flag{1999}",
    "brute2": "flag{password}",
    "brute3": "flag{123456}",
    "brute4": "flag{forged}",
    "osint1": "flag{root-rebellion-bot}",
    "osint2": "flag{example.com}",
    "osint3": "flag{new_york}",
    "linux1": "flag{found_it}",
    "linux2": "flag{/usr/bin/passwd}",
    "linux3": "flag{write_to_script}",
    "net1": "flag{mysql}",
    "net2": "flag{admin_password}",
    "net3": "flag{dns_recon_master}",
}

@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
    print(f"✅ root@rebellion:~# bot online as {bot.user}")
    if not guild: return

    verify_ch = next((c for c in guild.text_channels if "verify" in c.name), None)
    if verify_ch:
        async for msg in verify_ch.history(limit=10):
            if msg.author == bot.user: await msg.delete()
        embed = discord.Embed(title="🔐 SYSTEM VERIFICATION", description="> `Scanning identity...`\n> `Checking credentials...`\n> `Press button to authenticate.`\n\nClick below to gain access to **Root Rebellion**.", color=0x00FF41)
        embed.set_footer(text="root@rebellion:~# ./verify.sh")
        await verify_ch.send(embed=embed, view=VerifyView())

    roles_ch = next((c for c in guild.text_channels if "self-roles" in c.name), None)
    if roles_ch:
        async for msg in roles_ch.history(limit=20):
            if msg.author == bot.user: await msg.delete()
        await roles_ch.send(embed=discord.Embed(title="🔞 Age", description="Pick your age group.", color=0x9B59B6), view=AgeView())
        await roles_ch.send(embed=discord.Embed(title="🌍 Region", description="Pick your region.", color=0x3498DB), view=RegionView())
        await roles_ch.send(embed=discord.Embed(title="⚧ Gender", description="Pick your pronouns.", color=0xE91E63), view=GenderView())
        await roles_ch.send(embed=discord.Embed(title="💀 Hacker Rank", description="Pick your specialization — multiple allowed.", color=0x00FF41), view=HackerView())
        await roles_ch.send(view=HackerView2())

@bot.event
async def on_member_join(member):
    guild = member.guild
    unverified = discord.utils.get(guild.roles, name="Unverified")
    if unverified:
        try: await member.add_roles(unverified)
        except: pass
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

@bot.event
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

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"[SYSTEM] Wiped {amount} messages.", delete_after=5)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"[SYSTEM] {member.mention} disconnected. (Kick)")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"[SYSTEM] {member.mention} blacklisted. (Ban)")

@bot.command()
async def challenges(ctx):
    embed = discord.Embed(title="🎯 CTF TRAINING GROUNDS", description="> `root@rebellion:~# ./list_challenges.sh`\n\nUse `!ctf <id>` to load. Submit with `!submit <flag>`", color=0x00FF41)
    embed.add_field(name="🔑 Crypto", value="`crypto1` `crypto2` `crypto3` `crypto4`", inline=False)
    embed.add_field(name="🌐 Web", value="`web1` `web2` `web3` `web4`", inline=False)
    embed.add_field(name="💥 Brute Force", value="`brute1` `brute2` `brute3` `brute4`", inline=False)
    embed.add_field(name="🕵️ OSINT", value="`osint1` `osint2` `osint3`", inline=False)
    embed.add_field(name="🐧 Linux", value="`linux1` `linux2` `linux3`", inline=False)
    embed.add_field(name="📡 Network", value="`net1` `net2` `net3`", inline=False)
    embed.set_footer(text="root@rebellion:~# hack the planet 🌐")
    await ctx.send(embed=embed)

@bot.command()
async def ctf(ctx, challenge: str = None):
    if not challenge:
        await ctx.send("❌ Specify a challenge! Use `!challenges` for list.")
        return
    challenge = challenge.lower()
    if challenge not in CTF_CHALLENGES:
        await ctx.send("❌ Challenge not found! Use `!challenges` for list.")
        return
    title, desc = CTF_CHALLENGES[challenge]
    embed = discord.Embed(title=f"🚩 {title}", description=desc, color=0xFF0000)
    embed.set_footer(text="root@rebellion:~# Submit with !submit flag{...}")
    await ctx.send(embed=embed)

@bot.command()
async def submit(ctx, *, flag: str = None):
    if not flag:
        await ctx.send("❌ Usage: `!submit flag{...}`")
        return
    for challenge, answer in CTF_ANSWERS.items():
        if flag.strip() == answer:
            embed = discord.Embed(title="🎉 CORRECT FLAG!", description=f"> `✅ FLAG ACCEPTED`\n\n**{ctx.author.mention} solved `{challenge}`!**\n\n🏆 Keep grinding hacker!", color=0x00FF41)
            await ctx.send(embed=embed)
            return
    embed = discord.Embed(title="❌ WRONG FLAG", description="> `❌ ACCESS DENIED`\n\nTry harder.", color=0xFF0000)
    await ctx.send(embed=embed)

@bot.command()
async def postlearn(ctx):
    embed = discord.Embed(
        title="🧠 LEARN HACKING",
        description=f"> `root@rebellion:~# ./learn.sh`\n\nWant to learn ethical hacking, Kali Linux, cybersecurity?\n\n**Click below to access our learning platform!**\n\n✅ Kali Linux basics\n✅ Nmap & recon\n✅ Burp Suite & web hacking\n✅ CTF techniques\n✅ Bug bounty hunting",
        color=0x00FF41
    )
    embed.set_footer(text="root@rebellion:~# knowledge is power 🧠")
    await ctx.send(embed=embed, view=LearnHackingView())

bot.run(TOKEN)
