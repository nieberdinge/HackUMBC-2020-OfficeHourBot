  
import discord
from discord.ext import commands 
import random
import string

CODE = "CMSC202FA20"


class authenticator(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("authenticator cog online.")

    @commands.command()
    async def authMe(self,ctx,*,uniqueId : str):
    #"Put a string under the function to add to !help"
        if uniqueId == "":
            await ctx.send("{} you did not enter a valid code".format(ctx.message.author.mention))
        else:
            await ctx.send(uniqueId)
            if uniqueId == CODE:
                await ctx.send("Wow! I guess you are a studnet")
    
    @commands.command()
    @commands.has_role("Professor")
    async def makeCodes(self,ctx):
        file = open("studentList.txt",'w')
        
        for line in file.readlines():
            print("messed up")
            print(line[:-1]+"|"+self.generate())
            file.write(line[:-1]+"|"+self.generate())
        
        file.close()

    #generates a random code
    def generate(self):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(10))



def setup(client):
    client.add_cog(authenticator(client))
