# Author: Eddie Nieberding
# Co-Authors: Gabby Khan
import discord
import queue
from discord.ext import commands 


class queues(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ohQueue = [] #Holds Student ID
        self.ohMsg   = [] #Holds the message that was sent
    
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
        
        #Looks at all the channels and gets the id of the specific one
        for channel in ctx.guild.channels:
            if channel.name == "instructor-commands":
                instructorID = channel.id
            if channel.name == "request":
                studnetID = channel.id

        if ctx.message.channel.name == "request":
            if ctx.author.id not in self.ohQueue:
                studId = ctx.message.author.id
                authID = "!reject "+str(studId)

                #Puts embedded message in the instructor channel
                embedVar = discord.Embed(title=ctx.message.author.name, description=studMsg, color=0xff0000)
                embedVar.add_field(name="To reject: ", value=authID, inline=False)
                discordMsg = await ctx.guild.get_channel(instructorID).send(embed=embedVar)

                #adds the user and msg id to the queue
                self.ohQueue.append(studId)
                self.ohMsg.append(discordMsg)
            else:
                msg = "{} You are already in the queue".format(ctx.message.author.mention)
                await ctx.send(msg,delete_after=3)
        else:
            await ctx.send("You are in the wrong channel idiot.")
        #deletes the command after being called 
        await ctx.message.delete()
      
    @commands.command(pass_context=True)
    async def reject(self,ctx):
        " -Leave the queue"

        #!reject [Student ID] [Reason]
        msg = ctx.message.content.split()
        if len(msg) < 3:
            await ctx.send("Invalid commands. !reject [Student ID] [Reason]")
        else:
            if ctx.message.channel.name == "instructor-commands":
                studentID = int(msg[1])
                
                #removes unused items
                msg.pop(0)
                msg.pop(0)
                msg = " ".join(msg)
                studMsg = "you are being removed from the queue for the reason: "+msg
                rejectionId = self.ohQueue.index(studentID)

                #message returns user not other thing
                print(self.ohQueue[rejectionId])
                memId = self.ohQueue[rejectionId]
                guildId = await ctx.guild.fetch_member(studentID)
                await guildId.send(studMsg)
                print(guildId)

                await self.ohMsg[rejectionId].delete()
                await ctx.message.delete()
                self.ohMsg.pop(rejectionId)
                self.ohQueue.pop(rejectionId)
            else:
                await ctx.send("You are in the wrong channel. Please use the instructor-commands channel.")



    @commands.command(pass_context=True)
    async def position(self,ctx):
        "-Returns the position that you are in"
        noPosition = " You are not in the queue."
        index = 0
        try:
            index = self.ohQueue.index(ctx.message.author.id)
        except ValueError: 
            await ctx.send(ctx.message.author.mention + noPosition)
            index = -1
        if index != -1:
            await ctx.send(ctx.message.author.mention + ", you are number {} in the queue.".format(index+1))


    @commands.command(pass_context=True)
    async def leave(self,ctx):
        "-Lets the student leave the queue if they would like to"
        noPosition = "You are not in the queue."
        index = 0
        # do all of this to make sure that the user is in the queue
        try:
            index = self.ohQueue.index(ctx.message.author.id)
        except ValueError: 
            await ctx.send(ctx.message.author.mention + noPosition)
            index = -1
        if index != -1:
            # finds the student ID, gives a message and finsd rejectionID
            studnetID = ctx.message.author.id
            studMsg = "You have decided to leave the queue!"
            rejectionId = self.ohQueue.index(studnetID)

            #message returns user not other thing
            print(self.ohQueue[rejectionId])
            memId = self.ohQueue[rejectionId]
            guildId = await ctx.guild.fetch_member(studnetID)
            await guildId.send(studMsg)
            print(guildId)

            await self.ohMsg[rejectionId].delete()
            await ctx.message.delete()
            self.ohMsg.pop(rejectionId)
            self.ohQueue.pop(rejectionId)


    @commands.command(pass_context=True)
    async def request_help(self,ctx):
        "-shows students all command at the beginning"
        if ctx.message.channel.name == "request":
            await ctx.send("Here are the commands for this channel: ")
            await ctx.send("!join lets you join the queue")
            await ctx.send("!leave lets you leave the queue")
            await ctx.send("!position lets you see where you are in the queue")
            await ctx.send("!request_help lets you see this menu again")

    #counter to how many times people have joined 
    #first somehow get a list of everyone on the server ina  text doc
    #then everytime !join is used add an increment of sort to the students
    #can calculate weekly and daily if needed

def setup(client):
    client.add_cog(queues(client))