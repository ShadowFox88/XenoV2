from discord.ext import commands
import discord
import random

from utils.bot import Xeno
from utils.context import XenoContext


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
        
        # Check if it's the player's turn
        if view.two_player:
            if interaction.user.id != view.author.id and view.current_player == "X" and interaction.user.id in (view.author.id, view.second_player.id):
                return await interaction.response.send_message(f"It's not your turn {interaction.user.mention}!", ephemeral=True)
            elif interaction.user.id != view.second_player.id and view.current_player == "O" and interaction.user.id in (view.author.id, view.second_player.id):
                return await interaction.response.send_message(f"It's not your turn {interaction.user.mention}!", ephemeral=True)
            elif interaction.user.id not in (view.author.id, view.second_player.id):
                return await interaction.response.send_message(f"You aren't a player {interaction.user.mention}!", ephemeral=True)
        else:
            if interaction.user.id != view.author.id:
                return await interaction.response.send_message(f"You aren't a player {interaction.user.mention}!", ephemeral=True)
        
        if view.current_player == "X":
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.x][self.y] = "X" # type: ignore
            view.current_player = "O"

        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.x][self.y] = "O" # type: ignore
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
                if winner == "X":
                    winner = view.author.mention
                elif view.two_player:
                    winner = view.second_player.mention
                else:
                    winner = "The Computer"
                embed = discord.Embed(
                    title = "Tic Tac Toe", 
                    description = f"{winner} won!", 
                    color = discord.Colour.red()
                )

            return await interaction.response.edit_message(embed=embed, view=view)
        
        if not view.two_player:
                position = [random.randint(0, 2), random.randint(0, 2)]
                while view.board[position[0]][position[1]] is not None:
                    position = [random.randint(0, 2), random.randint(0, 2)]
                
                view.update_button(position[0], position[1], "O")
                view.board[position[0]][position[1]] = "O" # type: ignore
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
                if winner == "X":
                    winner = view.author.mention
                elif view.two_player:
                    winner = view.second_player.mention
                else:
                    winner = "The Computer"
                embed = discord.Embed(
                    title = "Tic Tac Toe", 
                    description = f"{winner} won!", 
                    color = discord.Colour.red()
                )

            return await interaction.response.edit_message(embed=embed, view=view)
        
        await interaction.response.edit_message(view=view)
        
        
class TicTacToe(discord.ui.View):
    def __init__(self, author: discord.User | discord.Member, second_player: discord.User | discord.Member):
        super().__init__()
        self.board = [
            [None, None, None], 
            [None, None, None], 
            [None, None, None]
        ]
        self.current_player = "X"
        self.author = author
        self.second_player = second_player
        self.two_player = True if second_player else False 

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))
                
    def cancel_all_buttons(self):
        for item in self.children:
            assert isinstance(item, TicTacToeButton)
            item.disabled = True
                
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
            assert isinstance(item, TicTacToeButton)
            if item.x == x and item.y == y:
                item.style = discord.ButtonStyle.danger if state == "X" else discord.ButtonStyle.success
                item.label = state
                item.disabled = True
            
            



class Minigames(commands.Cog):
    def __init__(self, bot: Xeno):
        self.bot = bot      
        
    @commands.command(aliases=["ttt", "tic-tac-toe", "tictactoe"])
    async def tic_tac_toe(self, ctx: XenoContext, player: discord.User = None): # type: ignore
        embed = discord.Embed(
            title = "Tic Tac Toe", 
            description = "Get 3 in a row to win!", 
            color = discord.Colour.dark_blue()
        )
        view = TicTacToe(ctx.author, player)
        await ctx.send(embed = embed, view=view)
        
        

async def setup(bot: Xeno):
    cog = Minigames(bot)
    await bot.add_cog(cog)