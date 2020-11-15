# Author(s): Eddie Nieberding, Gabby Khan, Oliver Dininno
import discord
from discord.ext import commands 
from discord.utils import get

class help(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Help cog online.")

    @commands.command(pass_context=True)    
    async def help(self,ctx):
    #"Put a string under the function to add to !help"
        #Get the category that help was called in

        textChannel = ctx.message.channel
        categoryId = textChannel.category_id
        category = get(textChannel.guild.categories, id = categoryId)

        if category.name == "Instructors":
            embedVar = discord.Embed(title="Commands Available to Instructors: ", color=0xff0000)
            embedVar.add_field(name="!startOh 'priority' (optional)", value=" -adds the caller to the office hour session", inline=False)
            embedVar.add_field(name="!endOh", value=" -ends the office hour session of the caller", inline=False)
            embedVar.add_field(name="!accept", value=" -accepts the person in front of the queue", inline=False)
            embedVar.add_field(name="!reset", value=" -resets all students queue priority, keeps total", inline=False)
            embedVar.add_field(name="!reject [Student ID] [Reason]", value=" -removes student from queue and direct message them the reason", inline=False)
            embedVar.add_field(name="!close", value=" -closes a category including all voice chats and text chats", inline=False)
            embedVar.add_field(name="!private", value=" -creates a private one on one session", inline=False)
            embedVar.add_field(name="!addAssignment [Name] ; [Due Date] ; [Description]", value=" -Creates an assignment for students to view", inline=False)
            embedVar.add_field(name="!clearAssignment", value=" -Will clear all the listed assignments", inline=False)
            embedVar.add_field(name="!beginLecture [Number of Breakout Rooms (optional)]", 
                                value = " -Begins a lecture and creates rooms if applicable",inline=False)
            embedVar.add_field(name="!endLecture", value="Removes the lecture chat and breakout groups",inline=False)
            discordMsg = await ctx.send(embed=embedVar)


        if category.name == "Students" or category.name == "Instructors":
            embedVar = discord.Embed(title="Commands Available to Students: ", color=0x00ff00)
            embedVar.add_field(name="!join [Reason]", value=" -Lets student join queue for office hours", inline=False)
            embedVar.add_field(name="!leave", value=" -Lets student leave queue for office hours", inline=False)
            embedVar.add_field(name="!position", value=" -Shows student their postion in queue", inline=False)
            embedVar.add_field(name="!onDuty", value=" -shows who the current TA's on duty are", inline=False)
            embedVar.add_field(name="!inQueue", value=" -Shows the current queue of students", inline=False)
            discordMsg = await ctx.send(embed=embedVar)
            
        if category.name == "Authentication":
            await ctx.send("```!authMe [class code]``` to be authorized. (Code provided by professor)")
       
    @commands.command(pass_context=True)    
    async def octoCat(self,ctx):
        await ctx.send(file=discord.File('Octocatgif.gif'))

def setup(client):
    client.add_cog(help(client))
