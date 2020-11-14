# Author: Oliver Dininno
# Co-Authors: Eddie Nieberding, Gabby Khan
  
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
    async def setup(self,ctx):
        "- Builds the server from the ground up"
        await ctx.send("Setting Up!")
        studentTxtChannels = [ ("hangout", "general discussion"),
                            ("request", "Request help from an instructor, use !request_help for more info"), 
                            ("faq", "Ask general questions for peers or instructors to answer."),
                            ("assignments", "Instructors will update this when new assignments are posted.")]
        
        studentVcChannels = ["hangout", "waitroom"]
        
        instructorTxtChannels = [("instructor-hangout", "No students, no problems"),
                                ("instructor-commands", "Please be patient with them")]
        
        instructorVcChannels = ["student-free-hangout"]
        
        OHTxtChannels = ["office-hours", "If you don't have a mic, type questions here"]
        OHVcChannels = ["office-hours"]

        #TAPerms = discord.Permissions(mute_members = True, deafen_members = True, move_member = True, manage_nicknames = True)
        #Creates roles
        for role in serverRoles:
            await ctx.guild.create_role(name = role)
        myRoles = ctx.guild.roles #[Everyone, Limbo, Student, TA, Professor, HACKER!!, BOT]
        member = ctx.message.author
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



        newCat = await ctx.guild.create_category("Instructors")
        await newCat.set_permissions(stuRole,read_messages=False)
        await newCat.set_permissions(everyRole,read_messages=False)
        await newCat.set_permissions(taRole,read_messages=True)

        #student cate
        newCat = await ctx.guild.create_category("Students")
        await newCat.set_permissions(everyRole,read_messages=False)
        await newCat.set_permissions(stuRole,read_messages=True)
        await newCat.set_permissions(taRole,read_messages=True)

        #creates office hours category
        newCat = await ctx.guild.create_category("Office-Hours")
        await newCat.set_permissions(stuRole,read_messages=False)
        await newCat.set_permissions(everyRole,read_messages=False)
        await newCat.set_permissions(taRole,read_messages=True)


        #creates authenticator 
        newCat = await ctx.guild.create_category("Authentication")
        for role in myRoles:
            if role != everyRole:
                await newCat.set_permissions(role,read_messages=False)
        await newCat.create_text_channel("authenticate-here")
        
        
        
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

        channel = await myCategories[2].create_text_channel(OHTxtChannels[0])
        await channel.edit(topic = OHTxtChannels[1])
        
        channel = await myCategories[2].create_voice_channel(OHVcChannels[0])
        



    @commands.command(pass_context=True)
    async def delete(self,ctx):
        "- Will purge the entire server"
        myText = ctx.guild.text_channels
        myVoice = ctx.guild.voice_channels
        for text in myText:
            if text.name != "general":
                await text.delete()
        for voice in myVoice:
            if voice.name != "general":
                await voice.delete()

        myCategories = ctx.guild.categories
        for cat in myCategories:
            await cat.delete()

        myRoles = ctx.guild.roles
        for role in myRoles:
            if role.name in str(serverRoles):
                await role.delete()


    @commands.command(pass_context=True)
    async def perms(self,ctx):
        "test"
        await ctx.send("Setting up permissions!")
        myRoles = ctx.guild.roles #[Everyone, Student, TA, Professor, HACKER!!, BOT]

        profPerms = discord.Permissions()
        profPerms.update(create_instant_invite = True,kick_members=True, ban_members=True, administrator=True, manage_channels=True, 
                        manage_guild=True, add_reactions=True,view_audit_log=True, stream=True, read_messages=True, send_messages=True,
                        send_tts_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True,
                        mention_everyone=True,connect=True, speak=True,mute_members=True,deafen_members=True, move_members=True, 
                        change_nickname=True, manage_nicknames=True, manage_roles=True,manage_permisson=True, use_external_emojis=True,
                        manage_emojis=True)
        
        await myRoles[3].edit(permissions = profPerms, hoist=True, color = 0xf74639)

        taPerms = discord.Permissions()
        taPerms.update(create_instant_invite = True,kick_members=True, ban_members=True, add_reactions=True, view_audit_log=True, 
                        stream=True, read_messages=True, send_messages=True, send_tts_messages=True, manage_messages=True, 
                        embed_links=True, attach_files=True, read_message_history=True,mention_everyone=True,connect=True, speak=True,
                        mute_members=True,deafen_members=True, move_members=True, change_nickname=True, manage_nicknames=True, manage_roles=True,
                        use_external_emojis=True,manage_emojis=True)

        await myRoles[2].edit(permissions=taPerms, hoist=True, color = 0x0ce81a)

        stuPerms = discord.Permissions()
        stuPerms.update(add_reactions=True, stream=True, read_messages=True, send_messages=True, send_tts_messages=True,
                        embed_links=True, attach_files=True, mention_everyone=True,connect=True, speak=True, 
                        change_nickname=True,use_external_emojis=True)
        await myRoles[1].edit(permissions=stuPerms,hoist=True, color = 0x3583f0)

    @commands.command(pass_context=True)
    async def shutdown(ctx, extension):
        await ctx.bot.logout()


def setup(client):
    client.add_cog(serverSetup(client))