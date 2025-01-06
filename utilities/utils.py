from __future__ import annotations
from typing import Any, List, Optional, Tuple, Union
from discord import Colour, Embed, EmbedField
from datetime import datetime
import requests as req


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


SPELL_NAMES_PATH = r"C:\Users\Big Poppin D\Documents\ProgrammingStuff\python\discord_bot\SpellMaster\utilities\spell_names.txt"
SPELL_INDEXES_PATH = r"C:\Users\Big Poppin D\Documents\ProgrammingStuff\python\discord_bot\SpellMaster\utilities\spell_names_indexes.txt"

with open(SPELL_NAMES_PATH, "r") as spell_names_file:
    SPELL_NAMES_LS = spell_names_file.read().split("\n")
    
with open(SPELL_INDEXES_PATH, "r") as spell_indexes_file:
    SPELL_INDEXES_LS = spell_indexes_file.read().split("\n")


def getSpellResponse(spell_name: str=""):
    url = f"https://www.dnd5eapi.co/api/spells/{spell_name}"
    
    try:
        response = req.get(url)

    except Exception as e:
        print(e.__class__.__name__)
        return False
        
    else:
        return response
    

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


def getSpell(spell_name: str) -> bool | Any:
    if isSpellName(spell_name):
        spell_name = switchSpellNameToIndex(spell_name)
    
    elif isSpellIndex(spell_name):
        spell_response = getSpellResponse(spell_name)
        if spell_response.status_code == 200:
            return spell_response.json()
        return False
    
    else:
        return False


# Functions for testing
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


class TimeStampStr(str):
    # Change __set__ to be whatever for when you actually get the variable like there are three different things?
    # make init be able to take a value unless that is not somehting you are supposed to do for descriptor classes
    def __init__(self, time_stamp_str: str = None):
        if time_stamp_str:
            self.__set__()
    
    def __set_name__(self, owner, name):
        self._name = name
        
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    
    def __set__(self, instance, value):
        # substrings are less than or equal to 60
        # substrings are positive
        # value is string
        # (1, seconds), (2, minutes), (3, hours), (4, days), (5, years)
        
        if not isinstance(value, str):
            raise ValueError("invalid literal \"{value}\" for TimeStampStr: must be set to string type literal")
        
        if value.replace(" ", "") == value:
            raise ValueError(f"invalid literal \"{value}\" for TimeStampStr: no spaces allowed in string")
        
        try:
            segments = value.split(":")
        except:
            raise ValueError("invalid literal \"{value}\" for TimeStampStr: time segments must be seperated by \":\" characters in format \"years:days:hours:minutes\"")
        

        for idx, segment in enumerate(segments[::-1]):
            if idx == 0:
                segment_type = "seconds"
                segment_max_count = 59
                
                if self._isPositiveNumberGreaterThanValueStr(segment, max=segment_max_count):
                    self.seconds = segment
                else:
                    raise ValueError(f"invalid literal \"{value}\" for TimeStampStr: {segment_type} must be positive numbers lower than or equal to {segment_max_count}")
                    
            elif idx == 1:
                segment_type = "minutes"
                segment_max_count = 59
                
                if self._isPositiveNumberGreaterThanValueStr(segment, max=segment_max_count):
                    self.minutes = segment
                else:
                    raise ValueError(f"invalid literal \"{value}\" for TimeStampStr: {segment_type} must be positive numbers lower than or equal to {segment_max_count}")
            
            elif idx == 2:
                segment_type = "hours"
                segment_max_count = 59
                
                if self._isPositiveNumberGreaterThanValueStr(segment, max=segment_max_count):
                    self.hours = segment
                else:
                    raise ValueError(f"invalid literal \"{value}\" for TimeStampStr: {segment_type} must be positive numbers lower than or equal to {segment_max_count}")
                
            elif idx == 3:
                segment_type = "days"
                segment_max_count = 365
                
                if self._isPositiveNumberGreaterThanValueStr(segment, max=segment_max_count):
                    self.days = segment
                else:
                    raise ValueError(f"invalid literal \"{value}\" for TimeStampStr: {segment_type} must be positive numbers lower than or equal to {segment_max_count}")

            elif idx == 4:
                segment_type = "years"
                segment_max_count = 9999
                
                if self._isPositiveNumberGreaterThanValueStr(segment, max=segment_max_count):
                    self.years = segment
                else:
                    raise ValueError(f"invalid literal \"{value}\" for TimeStampStr: {segment_type} must be positive numbers lower than or equal to {segment_max_count}")
            
            else:
                raise ValueError("invalid literal \"{value}\" for TimeStampStr: 5 segments permitted more than 5 in literal")
            

    
    
    def _isPositiveNumberGreaterThanValueStr(self, number_str: str, max: int):
        try:
            int_number_str = int(number_str)
        except:
            return False
        else:
            if 0 <= int_number_str < max:
                return True


    def __add__(self, time_stamps) -> "TimeStampStr":
        ...


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
                print(f"Response:\n{response}" if bool(respo))
                
            case getSpell.__name__:
                print(selection("misty-step"))
                
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