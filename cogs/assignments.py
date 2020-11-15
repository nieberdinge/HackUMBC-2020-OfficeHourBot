# Author: Oliver Dininno
# Co-Authors: Eddie Nieberdinge, Gabby Khan
import discord
from discord.ext import commands 

class assignments(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("assignment cog online.")


    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def add(self,ctx):
        #"!addAssignment 'name'; 'date'; 'description'
        #!addAssignment name: Proj1  - 11/14/20  desc: Create a bot

        #parse out command
        if " " in ctx.message.content:
            assign = " ".join(ctx.message.content.split()[1:])
        #split up command into sections
        assignArgs = assign.split(';')

        #make sure only 3 commands given
        if(len(assignArgs) == 3):
            if ctx.message.channel.name == "instructor-commands":
                assignID= ""
                for channel in ctx.guild.channels:
                    if channel.name == "assignments":
                        assignID = channel.id
                #Puts embedded message in the instructor channel
                embedVar = discord.Embed(title=assignArgs[0], description=assignArgs[2], color=0x0026ff)
                embedVar.add_field(name="Due Date: ", value=assignArgs[1], inline=False)
                await ctx.guild.get_channel(assignID).send(embed=embedVar)
            else:
                await ctx.send("You are in the wrong channel idiot.", delete_after=5)
                await ctx.message.delete()
        else:
            await ctx.send("Incorrect format, please try again", delete_after=15)
            await ctx.message.delete()
        
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def purgeAssign(self,ctx):
        for channel in ctx.guild.channels:
            if channel.name == "assignments":
                await channel.purge(limit = 100)

def setup(client):
    client.add_cog(assignments(client))