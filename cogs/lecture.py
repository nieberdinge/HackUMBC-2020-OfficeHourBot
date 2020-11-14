import discord
from discord.ext import commands 


class lecture(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lecture cog online.")

    @commands.command()
    async def beginLecture(self,ctx,num=0:int):
    #"Put a string under the function to add to !help"
        studentRole = get(ctx.message.guild.roles, name="Student")
        newCategory = await ctx.guild.create_category("lecture")
        TC = await newCategory.create_text_channel("Lecture Chat")
        VC = await newCategory.create_voice_channel("Lecture Voice Chat")
        await TC.send("Welcome to lecture!")

        for x in range(num):
            await newCategory.create_text_channel("Breakout Chat #{}".format(x+1))
            await newCategory.create_voice_channel("Breakout Voice Chat #{}".format(x+1))


def setup(client):
    client.add_cog(lecture(client))