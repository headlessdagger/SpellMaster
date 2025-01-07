from discord import Emoji, Interaction, ButtonStyle, EmbedField, Embed
from discord.ui import View, Button
from utilities import make_embed, SPELL_NAMES_LS
from typing import Callable

__all__ = (
    "PageTurnButton",
    "PageTurnerView"
)


class PageTurnButton(Button):
    def __init__(self, update: Callable[[Interaction], None], direction_is_right: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction_is_right = direction_is_right
        self.update = update
        
    async def callback(self, interaction: Interaction):
        if self.direction_is_right:
            self.view.page_num += 1
            
        else:
            self.view.page_num -= 1
            
        await self.update(interaction)

class PageTurnerView(View):
    def __init__(self, long_list: list, page_size: int = 20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_num = 0
        self.page_size = page_size
        self.max_pages = len(long_list) // page_size
        
        

        
        
        