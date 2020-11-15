import discord
from discord.ext import commands 
from discord.utils import get

class lecture(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Lecture cog online.")

    @commands.command()
    @commands.has_any_role('Professor','TA')
    async def beginLecture(self,ctx,num=0):
    #"Put a string under the function to add to !help"
        studentRole = get(ctx.message.guild.roles, name="Student")
        newCategory = await ctx.guild.create_category("Lecture")
        TC = await newCategory.create_text_channel("Lecture Chat")
        VC = await newCategory.create_voice_channel("Lecture Voice Chat")
        await TC.send("Welcome to lecture!")

        for x in range(num):
            await newCategory.create_voice_channel("Breakout Voice Chat #{}".format(x+1))
    
    @commands.command()
    @commands.has_any_role('Professor','TA')
    async def endLecture(self,ctx):
        category = get(ctx.message.guild.categories, name = "Lecture")
        for vc in category.voice_channels:
            await vc.delete()
        for tc in category.text_channels:
            await tc.delete()
        await category.delete()


def setup(client):
    client.add_cog(lecture(client))