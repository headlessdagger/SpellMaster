from discord import ButtonStyle, Embed, Interaction, PartialEmoji
from ui.common import PageTurnButton, PageTurnerView
from utilities import make_embed

__all__ = (
    "SpellPagesUI",
)

class SpellPagesUI:
    def __init__(self, long_list):
        self.long_list = long_list
    
    async def display_components(self, interaction: Interaction) -> None:
        self.btn_left = PageTurnButton(update=self.update_embed, direction_is_right=False, style=ButtonStyle.secondary, label="<-", disabled=True) # emoji=PartialEmoji(name="left_arrow", animated=False, id=1326108115867013140)
        self.btn_right = PageTurnButton(update=self.update_embed, direction_is_right=True, style=ButtonStyle.secondary, label="->") # emoji=PartialEmoji(name="right_arrow", animated=False, id=1326109624218292296)
        
        self.view = PageTurnerView(long_list=self.long_list)
        self.view.add_item(self.btn_left)
        self.view.add_item(self.btn_right)
                
        embed = self.make_custom_embed()
        
        await interaction.response.send_message(embed=embed, view=self.view)
    
    def make_custom_embed(self) -> Embed:
        """Returns an embed preset used for this UI"""
        embed = make_embed(
            title=f"Spells, Page: {self.view.page_num}",
            fields=[(spell, "", False) for spell in self.long_list[self.view.page_num * self.view.page_size : (self.view.page_num+1) * self.view.page_size:]]
            )
        
        return embed
    
    async def update_embed(self, interaction: Interaction) -> None:
        for child in self.view.children:
            if not isinstance(child, PageTurnButton):
                continue
            
            if (not child.direction_is_right) and self.view.page_num == 0:
                child.disabled = True
            
            elif child.direction_is_right and self.view.page_num == self.view.max_pages:
                child.disabled = True
                
            else:
                child.disabled = False
                
        await interaction.response.edit_message(embed=self.make_custom_embed(), view=self.view)