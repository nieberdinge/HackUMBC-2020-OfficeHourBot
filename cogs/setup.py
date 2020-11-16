# Author(s): Oliver Dininno, Eddie Nieberding, Gabby Khan
  
import discord
from discord.ext import commands 
from discord.utils import get

serverRoles = ["Professor", "TA", "Student"]

class serverSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("setup cog online.")

    # !setup
    #is_owner() at end
    @commands.command(pass_context=True)
    #@commands.is_owner()
    async def setup(self,ctx):
        await ctx.send("Setting Up!")

        myText = ctx.guild.text_channels
        myVoice = ctx.guild.voice_channels
        for text in myText:
            if text.name.lower() == "general":
                await text.delete()
        for voice in myVoice:
            if voice.name.lower() == "general":
                await text.delete()
        myCategories = ctx.guild.categories
        for cat in myCategories:
            if cat.name.lower() == "text channels" or text.name.lower() == "voice channels":
                await text.delete()

        studentTxtChannels = [ ("hangout", "general discussion"),
                            ("request", "Request help from an instructor, use !request_help for more info"), 
                            ("questions", "Ask general questions for peers or instructors to answer."),
                            ("assignments", "Instructors will update this when new assignments are posted.")]
        
        studentVcChannels = ["hangout", "waitroom"]
        
        instructorTxtChannels = [("instructor-hangout", "No students, no problems"),
                                ("instructor-commands", "Please be patient with them")]
        
        instructorVcChannels = ["student-free-hangout"]
        
       
        #Creates roles from the roles list
        for role in serverRoles:
            await ctx.guild.create_role(name = role)
        myRoles = ctx.guild.roles #[Everyone, Limbo, Student, TA, Professor, HACKER!!, BOT]
        member = ctx.message.author

        #creates objects of each role for easy access
        profRole = get(member.guild.roles, name="Professor")
        taRole = get(member.guild.roles, name="TA")
        stuRole = get(member.guild.roles, name="Student")
        everyRole = get(member.guild.roles, name="@everyone")
        
        profPerms = discord.Permissions()
        profPerms.update(create_instant_invite = True,kick_members=True, ban_members=True, administrator=True, manage_channels=True, 
                        manage_guild=True, add_reactions=True,view_audit_log=True, stream=True, read_messages=True, send_messages=True,
                        send_tts_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True,
                        mention_everyone=True,connect=True, speak=True,mute_members=True,deafen_members=True, move_members=True, 
                        change_nickname=True, manage_nicknames=True, manage_roles=True,manage_permisson=True, use_external_emojis=True,
                        manage_emojis=True)
        
        await profRole.edit(permissions = profPerms, hoist=True, color = 0xf74639)

        taPerms = discord.Permissions()
        taPerms.update(create_instant_invite = True,kick_members=True, ban_members=True, add_reactions=True, view_audit_log=True, 
                        stream=True, read_messages=True, send_messages=True, send_tts_messages=True, manage_messages=True, 
                        embed_links=True, attach_files=True, read_message_history=True,mention_everyone=True,connect=True, speak=True,
                        mute_members=True,deafen_members=True, move_members=True, change_nickname=True, manage_nicknames=True, manage_roles=True,
                        use_external_emojis=True,manage_emojis=True)

        await taRole.edit(permissions=taPerms, hoist=True, color = 0x0ce81a)

        stuPerms = discord.Permissions()
        stuPerms.update(add_reactions=True, stream=True, read_messages=True, send_messages=True, send_tts_messages=True,
                        embed_links=True, attach_files=True, mention_everyone=True,connect=True, speak=True, 
                        change_nickname=True,use_external_emojis=True)
        await stuRole.edit(permissions=stuPerms,hoist=True, color = 0x3583f0)

        #Creates instructor Category and sets permissions
        newCat = await ctx.guild.create_category("Instructors")
        await newCat.set_permissions(stuRole,read_messages=False)
        await newCat.set_permissions(everyRole,read_messages=False)
        await newCat.set_permissions(taRole,read_messages=True)

        #Creates Students Category and sets permissions
        newCat = await ctx.guild.create_category("Students")
        await newCat.set_permissions(everyRole,read_messages=False)
        await newCat.set_permissions(stuRole,read_messages=True)
        await newCat.set_permissions(taRole,read_messages=True)


        #Creates Authentication Category and sets permissions
        newCat = await ctx.guild.create_category("Authentication")
        for role in myRoles:
            if role != everyRole:
                await newCat.set_permissions(role,read_messages=False)
        channel = await newCat.create_text_channel("authenticate-here")
        await channel.edit(topic = "!authMe [code from instructor]")
        await channel.send("```!authMe [code from instructor]```Use code provided by your professsor")
        
        
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
                await channel.set_permissions(stuRole,read_messages=True,send_messages=False)

        for studChannel in studentVcChannels:
            channel = await myCategories[1].create_voice_channel(studChannel)

 


    
    @commands.command(pass_context=True)
    #@commands.is_owner()
    async def delete(self,ctx):
        myText = ctx.guild.text_channels
        myVoice = ctx.guild.voice_channels
        for text in myText:
            await text.delete()
        for voice in myVoice:
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