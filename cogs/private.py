#Author: Gabby Khan
import discord
from discord.ext import commands 
from discord.utils import get

#need to first validate a command only from a TA or Instructor
#once that command is validated, we make the channel limit of 2 people on it
#the instructor can then drag a student into it
#after the instructor does the session or needs to close it can call closeP101

class Private(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Private cog online.")

    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def private (self,ctx):
        "sets up a Private One on One Session"
        if ctx.message.channel.name == "instructor-commands":
            member = ctx.message.author
            myRoles = ctx.guild.roles #[Everyone, Limbo, Student, TA, Professor, HACKER!!, BOT]

            if ctx.message.channel.name == "instructor-commands":
                #creates objects of each role for easy access
                profRole = get(member.guild.roles, name="Professor")
                taRole = get(member.guild.roles, name="TA")
                stuRole = get(member.guild.roles, name="Student")
                everyRole = get(member.guild.roles, name="@everyone")

                PVcChannel = "Private One on One"
                newCategory = await ctx.guild.create_category("Private")
                TC = await newCategory.create_text_channel("private-chat")
                await TC.send("Welcome to your own private session. You can drag students from a voice chat into the private-chat")
                await TC.send("To close this session, use !close")
                channel = await newCategory.create_voice_channel("private-chat")
                await newCategory.set_permissions(stuRole,read_messages=False)
                await newCategory.set_permissions(everyRole,read_messages=False)
                await newCategory.set_permissions(taRole,read_messages=True)
                await newCategory.set_permissions(profRole,read_messages=True)
            else:
                studentID = ctx.message.author.id
                studMsg = "Please only do this command in instructor-commands"
                guildId = await ctx.guild.fetch_member(studentID)
                await guildId.send(studMsg)
        else:
            await ctx.send("Please move to the 'instructor-commands' channel",delete_after=5)
            await ctx.message.delete()
            
def setup(client):
    client.add_cog(Private(client))



