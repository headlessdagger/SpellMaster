from __future__ import annotations
print("Loading Imports.", end="")
from discord import Bot, Intents, ApplicationContext, Interaction, Option, SlashCommandOptionType, Button, ButtonStyle
print(".", end="")
from utilities import make_embed, getSpell, SPELL_NAMES_LS
print(".", end="")
from dotenv import load_dotenv
print(".", end="")
from classes import SpellPagesUI
# print(".", end="")
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
async def displaySpellsCommand(ctx: ApplicationContext):
    ui = SpellPagesUI(SPELL_NAMES_LS)
    await ui.display_components(ctx.interaction)
    

@bot.slash_command(name="find-spell", description="Display Info for a specific spell")
async def find_spell_command(ctx: ApplicationContext, spellname=Option(SlashCommandOptionType.string)):
    spellname = spellname.title()
    try:
        spell_info_dict = getSpell(spellname)
    
    except ValueError as errV:
        await ctx.respond(str(errV))
        return None
 
    
    embed = make_embed(
        title=spellname,
        description=f"This info was pulled from https://www.dnd5eapi.co",
        colour=0x008cff, # Cornflower blue ish
        fields=[(key_str, spell_info_dict[key_str], False)  for key_str in spell_info_dict.keys()]
    )

    await ctx.respond(embed=embed)
        

load_dotenv()

bot.run(getenv("BOT_TOKEN"))
