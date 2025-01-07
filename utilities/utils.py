from __future__ import annotations
from typing import Any, List, Optional, Tuple, Union
from discord import Colour, Embed, EmbedField
from datetime import datetime
import requests as req
import os


__all__ = (
    "getSpell",
    "getSpellResponse",
    "SPELL_NAMES_LS",
    "SPELL_INDEXES_LS",
    "make_embed"
)

def make_embed(
    *,
    title: str = None,
    description: str = None,
    url: str = None,
    colour: Optional[Union[Colour, int]] = None,
    thumbnail_url: str = None,
    image_url: str = None,
    author_name: str = None,
    author_url: str = None,
    author_icon: str = None,
    footer_text: str = None,
    footer_icon: str = None,
    timestamp: Union[datetime, bool] = False,
    fields: Optional[List[Union[Tuple[str, Any, bool], EmbedField]]] = None
) -> Embed:
    """Creates and returns a Discord embed with the provided parameters.
    
    All parameters are optional.
    
    Parameters:
    -----------
    title: :class:`str`
        The embed`s title
        
    description: :class:`str`
        The main text body of the embed.
        
    url: :class:`str`
        The URL for the embed title to link to.
        
    colour: Optional[Union[:class:`Colour`, :class:`int`]]
        The desired accent color. Defaults to :func:`colors.random_all()`
        
    thumbnail_url: :class:`str`
        The URL for the embed`s desired thumbnail image.
        
    image_url :class:`str`
        The URL for the embed`s desired main image
        
    author_name: :class:`str`
        The text to display at the top of the embed.
        
    author_url: :class:`str`
        The URL for the author text to link to.
        
    author_icon: :class:`str`
        The icon that appears to the left of the the author text.
        
    footer_text: :class:`str`
        The text to display at the bottom of the embed.
        
    footer_icon: :class:`str`
        The icon to display to the left of the footer text.
        
    timestamp: Union[:class:`datetime`, `bool`]
        Whether to add the current time to the bottom of the embed.
        Defaults to ``False``.
        
    fields: Optional[List[Union[Tuple[:class:`str`, Any, :class:`bool`], :class:`EmbedField`]]]
        List of tuples or EmbedFields, each denoting a field to be added
        to the embed. If entry is a tuple, values are as follows:
            0 -> Name | 1 -> Value | 2 -> Inline (bool)
        Note that in the event of a tuple, the value at index one is automatically cast to a string for you.
        
    Returns:
    --------
    :class:`Embed`
        The finished embed object
    """
    
    embed = Embed(
        colour=colour,
        title=title,
        description=description,
        url=url
    )
    
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_image(url=image_url)
    
    if author_name is not None:
        embed.set_author(
            name=author_name,
            url=author_url,
            icon_url=author_icon
        )
        
    if footer_text is not None:
        embed.set_footer(
            text=footer_text,
            icon_url=footer_icon
        )
    
    if isinstance(timestamp, datetime):
        embed.timestamp = timestamp
    elif timestamp is True:
        embed.timestamp = datetime.now()
        
        
    if fields is not None:
        if all(isinstance(f, EmbedField) for f in fields):
            embed.fields = fields
        else:
            for f in fields:
                if isinstance(f, EmbedField):
                    embed.fields.append(f)
                    
                elif isinstance(f, tuple):
                    embed.add_field(name=f[0], value=f[1], inline=f[2])
                else:
                    continue
    
    return embed


SPELL_NAMES_PATH = os.path.dirname(__file__) + "\\spell_names.txt"
SPELL_INDEXES_PATH = os.path.dirname(__file__) +  "\\spell_names_indexes.txt"

with open(SPELL_NAMES_PATH, "r") as spell_names_file:
    SPELL_NAMES_LS = spell_names_file.read().split("\n")
    
with open(SPELL_INDEXES_PATH, "r") as spell_indexes_file:
    SPELL_INDEXES_LS = spell_indexes_file.read().split("\n")


def getSpellResponse(spell_name: str=""):
    url = f"https://www.dnd5eapi.co/api/spells/{spell_name}"
    
    response = req.get(url)
    response.raise_for_status()
        
    return response
    

# Spell Checking
def isSpellName(spell_name):
        if spell_name in SPELL_NAMES_LS:
            return True
        return False

def isSpellIndex(spell_name):        
        if spell_name in SPELL_INDEXES_LS:
            return True
        return False
    
def switchSpellNameToIndex(spell_name):
    if spell_name in SPELL_NAMES_LS:
        spell_name = SPELL_INDEXES_LS[SPELL_NAMES_LS.index(spell_name)]
            
    return spell_name


# Retrieve
def getSpell(spell_name: str) -> bool | Any:
    # you should try and except the apropriate errors
    spell_name = switchSpellNameToIndex(spell_name)
    
    try:
        spell_response = getSpellResponse(spell_name)
    except req.exceptions.HTTPError as errH:
        raise ValueError("Spell couldn't be retrieved.")


    return spell_response.json()


# Testing Funcs
def getSpellName():
    while True:
        name = input("Inspect Spell: ").strip()
        
        if isSpellName(name):
            name = switchSpellNameToIndex(name)
        
        elif isSpellIndex(name):
            break
        
        else:
            continue
    
    return name

        
def print_keys(response_dict):
    return response_dict.keys()


def count_spell(response_dict):
    number_of_spells = response_dict['count']
    return f"Spell Count: {number_of_spells}"
    

def getVerboseSpell(response_dict):
    return getSpellResponse("chain-lightning")


def selectFunction(selections):
    while True:
        print("="*50)
        for index, process, in list(enumerate(selections)):
            print(f'[{index}]\t{process.__name__}')
        print("="*50)

        selection_index = input("[Pick a function index]: ")
        try:
            selection_index = int(selection_index.strip())
            selection = selections[selection_index]
        except IndexError as ex:
            print(f'{ex.__class__.__name__}: {ex} (Pick a number inside the valid range)')
        except ValueError as ex2:
            print(f'{ex2.__class__.__name__}: {ex2} (Enter a number)')
        else:
            return selection
   

def main():
    # ['index', 'name', 'desc', 'higher_level', 'range', 'components', 'material', 'ritual', 'duration', 'concentration', 'casting_time', 'level', 'damage', 'dc', 'school', 'classes', 'subclasses', 'url']
    # time = TimeStampStr("12:15")
    response_dict = getSpellResponse().json()
    while True:
        funcs = [print_keys, count_spell, getVerboseSpell, getSpellName, getSpell, switchSpellNameToIndex]
        selection = selectFunction(funcs)

        match selection.__name__:

            case count_spell.__name__ | print_keys.__name__:
                print(selection(response_dict))
                
            case getSpellName.__name__:
                response = getSpellResponse(selection())
                valid = bool(response)
                print(f"Is a valid response?: {valid}")
                print(f"Response:\n{response}" if bool(response) else "No response")
                
            case getSpell.__name__:
                spell_response = selection("misty-step")
                print(f"type: {type(spell_response)} | {spell_response}")
                
            case switchSpellNameToIndex.__name__:
                while True:
                    inp_spell_name = input(f"Enter a spell name to test [switchSpellNameToIndex()]: ")
                    if inp_spell_name in SPELL_NAMES_LS:
                        break
                    else:
                        print("not a spell name")
                print(f'[switchSpellNameToIndex] -> {switchSpellNameToIndex(inp_spell_name)}')




if __name__ == "__main__":
    main()