  
import discord
from discord.ext import commands 
from discord.utils import get
import random
import string

CODE = "TrueBit"
TACODE = "PleaseChooseMeToWinThePrize"

class authenticator(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("authenticator cog online.")

    @commands.command()
    async def authMe(self,ctx,*,uniqueId : str):
    #"Put a string under the function to add to !help"
        if ctx.message.channel == "authenticate-here":
            if uniqueId == "":
                await ctx.send("{} you did not enter a valid code".format(ctx.message.author.mention),delete_after=5)
            else:
                if uniqueId == CODE:
                    member = ctx.message.author
                    role = get(member.guild.roles, name="Student")
                    await member.add_roles(role)
                elif uniqueId == TACODE:
                    member = ctx.message.author
                    role = get(member.guild.roles, name="TA")
                    await member.add_roles(role)
                else:
                    await ctx.send("{} you did not enter a valid code".format(ctx.message.author.mention),delete_after=5)
        else:
            await ctx.send("You need to be in the authenticate-here channel",delete_after=5)
        ctx.message.delete()
    
    @commands.command()
    @commands.has_role("Professor")
    async def makeCodes(self,ctx):
        file = open("studentList.txt",'w')
        
        for line in file.readlines():
            file.write(line[:-1]+"|"+self.generate())
        
        file.close()

    #generates a random code
    def generate(self):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(10))



def setup(client):
    client.add_cog(authenticator(client))
