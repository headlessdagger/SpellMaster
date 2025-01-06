from __future__ import annotations
print("Loading Imports.", end="")
from discord import Bot, Intents, ApplicationContext, Option, SlashCommandOptionType
print(".", end="")
print(".", end="")
from utilities import make_embed, getSpell, SPELL_NAMES_LS
print(".", end="")
from dotenv import load_dotenv
print(".", end="")
import typing
print(".", end="")
from os import listdir, getenv
print(".")


print("Building Bot...")
bot = Bot(
    description="I'm the spell book bot!",
    intents=Intents.default(),
    debug_guilds=[1079621474270322788],
)

@bot.event
async def on_ready() -> None:
    print("SpellMaster Online!")
    
@bot.slash_command(name="display-spell-names")
async def displaySpellsCommand(ctx: ApplicationContext, j=Option(input_type=str, required=True) ):
    await ctx.respond(f"Hello! {j}")
    

@bot.slash_command(name="find-spell", description="Display Info for a specific spell")
async def find_spell_command(ctx: ApplicationContext, spellname=Option(SlashCommandOptionType.string)):
    spell_info = getSpell(spellname)
    if not spell_info:
        await ctx.respond(f"No spell response from [{ctx.command.name}]")
        return None
    
    embed = make_embed(
        title="Spell Description",
        description=f"{spell_info.json()}",
    )
    await ctx.respond(f"Command: [{ctx.command.name}] Invoked!")
    await ctx.respond(embed=embed)
        

load_dotenv()

bot.run(getenv("BOT_TOKEN"))
