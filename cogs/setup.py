# This cog will populate a fresh server with different channels 
# along with setting up roles / permissions
  
import discord
from discord.ext import commands 

serverRoles = ["Professor", "TA", "Student"]

class serverSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("TEMPLATE cog online.")

    # !setup
    #is_owner() at end
    @commands.command(pass_context=True)
    async def setup(self,ctx):
        "- Builds the server from the ground up"
        await ctx.send("Setting Up!")
        studentTxtChannels = [ ("hangout", "general discussion"),
                            ("request", "Request help from an instructor, use !help for more info"), 
                            ("faq", "Ask general questions for peers or instructors to answer."),
                            ("assignments", "Instructors will update this when new assignments are posted.")]
        
        studentVcChannels = ["hangout", "waitroom"]
        
        instructorTxtChannels = [("instructor-hangout", "No students, no problems"),
                                ("instructor-commands", "Please be patient with them")]
        
        instructorVcChannels = ["studen-free-hangout"]
        
        OHTxtChannels = ["Office-Hours", "If you don't have a mic, type questions here"]
        OHVcChannels = ["Office-Hours"]
        
        
        #Creates a clean slate for the server
        # myText = ctx.guild.text_channels
        # for text in myText:
        #     await text.delete()
        # myCategories = ctx.guild.categories
        # for cat in myCategories:
        #     await cat.delete()
        


        #Creates roles
        for role in serverRoles:
            newRole = await ctx.guild.create_role(name = role)
            if role == "Professor":
                await newRole.edit(all = True)
            if role == "TA":
                await newRole.edit(mute_members = True, deafen_members = True, move_member = True, manage_nicknames = True)


        
        myRoles = ctx.guild.roles
        #myRoles[1] = Students
        #myRoles[2] = TA
        #myRoles[3] = Professor
        #instructor cate
        newCat = await ctx.guild.create_category("Instructors")
        await newCat.set_permissions(myRoles[1],read_messages=False)
        #student cate
        await ctx.guild.create_category("Students")
        #creates office hours category
        newCat = await ctx.guild.create_category("Office-Hours")
        await newCat.set_permissions(myRoles[1],read_messages=False)
        myCategories = ctx.guild.categories
        
        #creates instructor text and voice channels
        for i in instructorTxtChannels:
            channel = await myCategories[0].create_text_channel(i[0])
            await channel.edit(topic = i[1])
            
        for i in instructorVcChannels:
            channel = await myCategories[0].create_voice_channel(i)
        
        #creates student text and voice channels
        for studChannel in studentTxtChannels:
            channel = await myCategories[1].create_text_channel(studChannel[0])
            await channel.edit(topic = studChannel[1])
            if channel.name == "assignments":
                await channel.set_permissions(myRoles[1],read_messages=True,send_messages=False)

        for studChannel in studentVcChannels:
            channel = await myCategories[1].create_voice_channel(studChannel)

       # channel = await myCategories[2].create_text_channel(OHTxtChannels[0])
        #await channel.edit(topic = OHTxtChannels[1])
        
        #channel = await myCategories[2].create_voice_channel(OHVcChannels[0])
        



    @commands.command(pass_context=True)
    async def delete(self,ctx):
        "- Will purge the entire server"
        myText = ctx.guild.text_channels
        myVoice = ctx.guild.voice_channels
        for text in myText:
            if text.name != "general":
                await text.delete()
        for voice in myVoice:
            if voice.name != "General":
                await voice.delete()

        myCategories = ctx.guild.categories
        for cat in myCategories:
            await cat.delete()

        myRoles = ctx.guild.roles
        for role in myRoles:
            if role.name in str(serverRoles):
                await role.delete()






















































def setup(client):
    client.add_cog(serverSetup(client))