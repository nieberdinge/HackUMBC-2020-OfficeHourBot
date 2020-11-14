import discord
import queue
from discord.ext import commands 


class queues(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ohQueue = [] #The people currently in the queue
        self.ohMsg   = [] #A list that mirros the Queue but holds the message ids 
    
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
            await ctx.send("You are in the right channel!")
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
            await ctx.send("You are in the wrong channel idiot.")
        #deletes the command after being called 
        await ctx.message.delete()

    @commands.command(pass_context=True)
    async def position(self,ctx):
        "-Returns the position that you are in"
        position = "You are not in the queue."
        index = 0
        try:
            index = self.ohMsg.index(ctx.message.author.id)
        except ValueError: 
            ctx.send("You are not in the queue.")
        ctx.send("You are {} in the queue.".format(index))
        
            

            
    @commands.command(pass_context=True)
    async def reject(self,ctx):
        " -Leave the queue"

        #!reject [Student ID] [Reason]
        msg = ctx.message.content.split()
        if len(msg) != 3:
            await ctx.send("Invalid commands. !reject [Student ID] [Reason]")
        else:
            if ctx.message.channel.name == "instructor-commands":
                instructorID = ""
                studMsg = "you are being removed from the queue for the reason: "+msg[2]
                rejectionId = self.ohQueue.index(int(msg[1]))
                print(self.ohMsg)
                print(self.ohQueue)
                #message returns user not other thing
                await ctx.send("You are in the right channel!")
                print(self.ohMsg[rejectionId])
                await self.ohMsg[rejectionId].send(studMsg)
                await self.ohMsg[rejectionId].delete()
                await ctx.message.delete()
                self.ohMsg.pop(rejectionId)
                self.ohQueue.pop(rejectionId)



            
            else:
                await ctx.send("You are in the wrong channel. Please use the instructor-commands channel.")



            # #Looks at all the channels and gets the id of the specific one
            # for channel in ctx.guild.channels:
            #     if channel.name == "instructor-commands":
            #         instructorID = channel.id
            #     if channel.name == "request":
            #         studnetID = channel.id
            
            
                
            # # This is jst an output message
            # await ctx.send("You are aboutta be out of queue!")
            # authID = "!reject "+str(ctx.message.author.id)

            # #Puts embedded message in the instructor channel
            # embedVar = discord.Embed(title=ctx.message.author.name, description=studMsg, color=0xff0000)
            # embedVar.add_field(name="To reject: ", value=authID, inline=False)
            # discordMsg = await ctx.guild.get_channel(instructorID).send(embed=embedVar)

            # #removes the user from the queue
            # # need to look through ID and auto remove and send DM why
            # index = 0
            # for i in self.ohQueue:
            #     if self.ohQueue[i] == instMsg[1]:
            #         self.ohQueue.remove(i)
            #         index = i
            # self.ohMsg.remove(index)

            # await ctx.guild.get_channel(instructorID).send(embed=embedVar)
            # #"Put a string under the function to add to !help"

def setup(client):
    client.add_cog(queues(client))