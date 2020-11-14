  
import discord
from discord.ext import commands 


class queue(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Queue cog online.")

    @commands.command(pass_context=True)
    async def join(self,ctx):
        " -Join the queue"
        instructorID = ""
        studMsg = "No message given"
        if " " in ctx.message.content:
            studMsg = " ".join(ctx.message.content.split()[1:])
        
        for channel in ctx.guild.channels:
            if channel.name == "instructor-commands":
                instructorID = channel.id
            if channel.name == "request":
                studnetID = channel.id

        if ctx.message.channel.name == "request":
            await ctx.send("You are in the right channel!")

            embedVar = discord.Embed(title=ctx.message.author.name, description=studMsg, color=0xff0000)
            #embedVar.add_field(name="Field1", value="hi", inline=False)
            #embedVar.add_field(name="Field2", value="hi2", inline=False)
            await ctx.guild.get_channel(instructorID).send(embed=embedVar)
        else:
            await ctx.send("You are in the wrong channel idiot.")
        #"Put a string under the function to add to !help"
            


def setup(client):
    client.add_cog(queue(client))



