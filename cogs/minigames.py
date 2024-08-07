from discord.ext import commands
import discord
import random

from utils.bot import Xeno
from utils.context import XenoContext

class TicTacToe(discord.ui.View):
    def __init__(self, two_player: bool = False):
        super().__init__()
        self.board = [
            [None, None, None], 
            [None, None, None], 
            [None, None, None]
        ]
        self.current_player = "X"
        self.two_player = two_player

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))
                
    def check_winner(self):
        # across
        for across in self.board:
            if across == ["X", "X", "X"]:
                return "X"
            elif across == ["O", "O", "O"]:
                return "O"
        
        # vertical
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
            
        # diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        
        if all(self.board[y][x] is not None for x in range(3) for y in range(3)):
            return "Tie"
        
        return None
    
    def update_button(self, x: int, y: int, state: str):
        for item in self.children:
            if item.x == x and item.y == y: # type: ignore
                item.style = discord.ButtonStyle.danger if state == "X" else discord.ButtonStyle.success # type: ignore
                item.label = state # type: ignore
                item.disabled = True # type: ignore
 # WHILE LOOP <------
                # advay  🤪🍆🍆🍆🍑🍑🍑🍑🍑🥴🥴🍆🍆🍆🤪🤪💅💅💅💅💅
                
        

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.gray, label="_", row=y)
        self.x: int = x
        self.y: int = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.x][self.y]
        
        if state is not None:
            return
        
        if view.current_player == "X":
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.update_button(self.y, self.x, "X")
            view.current_player = "O"
            
            if not view.two_player:
                position = [random.randint(0, 2), random.randint(0, 2)]
                while view.board[position[0]][position[1]] is not None:
                    position = [random.randint(0, 2), random.randint(0, 2)]
                
                view.update_button(position[0], position[1], "O")
                view.current_player = "X"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.update_button(self.y, self.x, "O")
            view.current_player = "X"
            
        winner = view.check_winner()
        if winner != None:
            view.stop()

            if winner == "Tie":
                embed = discord.Embed(
                    title = "Tic Tac Toe", 
                    description = "It was a tie!", 
                    color = discord.Colour.red()
                )
            else:
                embed = discord.Embed(
                    title = "Tic Tac Toe", 
                    description = "{winner} won!", 
                    color = discord.Colour.red()
                )

            return await interaction.response.edit_message(embed=embed, view=None)
            
            



class Minigames(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot      
        
    @commands.command()
    async def tic_tac_toe(self, ctx: XenoContext, two_player: bool = False):
        embed = discord.Embed(
            title = "Tic Tac Toe", 
            description = "Get 3 in a row to win!", 
            color = discord.Colour.dark_blue()
        )
        view = TicTacToe(two_player)
        await ctx.send(embed = embed, view=view)
        
        

async def setup(bot: Xeno):
    cog = Minigames(bot)
    await bot.add_cog(cog)