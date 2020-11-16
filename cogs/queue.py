# Author(s): Eddie Nieberding, Gabby Khan, Oliver Dininno
import discord
import queue
from discord.utils import get
from discord.ext import commands 


FILENAME = "membersId.txt"
RESET_DAY = "Sunday"
DELIMITER = '|' 


# today = date.today()
# dateFormat = today.strftime("%m/%d/%Y")
# ex. 12/28/99
class Student():
    def __init__(self,id,weekly,allTime):
        self.id = id
        self.weekly = weekly
        self.allTime = allTime
        #self.weeklyDate #reset based on the day of RESET_DAY

class queues(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ohQueue  = [] #Holds Student member
        self.ohMsg    = [] #Holds the message that was the bot sent
        self.taOnDuty = []
        self.data = []
        self.priority = False #says if it is a priority queue
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Queue cog online.")     

    #Reads file
    def updateStats(self):
        myFile = open(FILENAME)
        self.data = []
        for line in myFile.readlines():
            data = line.split(DELIMITER) 
            #id| week count | all time count
            self.data.append(Student(int(data[0]),int(data[1]),int(data[2])))
        myFile.close()

    def writeStats(self):
        myFile = open(FILENAME,'w')
        for data in self.data:
            msg = str(data.id)+DELIMITER+str(data.weekly)+DELIMITER+str(data.allTime)
            print(msg)
            myFile.write(msg)
            myFile.write(DELIMITER+"\n")
        myFile.close()

    #memberId|0|0
    def tick(self, memberId):
        self.updateStats()

        for student in self.data:
            if str(memberId) == str(student.id):
                student.weekly += 1
                student.allTime += 1
                break
        else:
            self.data.append(Student(memberId,1,1))
            
        self.writeStats()
            
    def findUser(self,memberId):
        self.updateStats()
        for user in self.data:
            if memberId == user.id:
                return user
        return -1

    ## Resets weekly variable
    @commands.command()
    @commands.has_any_role('Professor','TA')
    async def reset(self,ctx):
        await ctx.send("Reset all current priority")
        for student in self.data:
            student.weekly = 0
        self.writeStats()
    # insertion sort   
    #append unsorted ohQueue
    def sortQueueP(self):
        #first iterate to end of list (insertion)
        #first check if empty, if not keep running

        if self.ohQueue != [] and len(self.ohQueue) > 1:  
            poppedItem = self.ohQueue.pop()
            msgInsert = self.ohMsg.pop()

            studentArr = []
            #converts discord members to student class
            inserter = self.findUser(poppedItem.id)
            print("insterter: " + str(inserter))
            if inserter == -1:
                self.ohQueue.insert(0,poppedItem)
                self.ohMsg.insert(0,msgInsert)

            else:
                for member in self.ohQueue:
                    student = self.findUser(member.id)
                    studentArr.append(student)

                counter = 0
                hasSwapped = False
                while counter < len(self.ohQueue) and hasSwapped != True:
                    #Finds something with a bigger size
                    print(studentArr[counter])
                    if studentArr[counter].weekly > inserter.weekly:
                        self.ohQueue.insert(counter,poppedItem)
                        hasSwapped = True
                    counter += 1 
                
                #if it is the largest in the queue
                if hasSwapped == False:
                    self.ohQueue.append(poppedItem)
                    self.ohMsg.append(msgInsert)



    ## Starts Office Hours
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def startOh(self,ctx,priority=""):
        if ctx.message.channel.name == "instructor-commands":
            ta = ctx.message.author
            color = 0x00ff00
            if priority == "priority":
                self.priority = True
                color = 0xff00ff
            #no one is in office hours
            if len(self.taOnDuty) == 0:
                channel = get(ta.guild.channels,name="request")
                embedVar = discord.Embed(title="Office hours are open!", description="Use !join [reason] to join", color=color)

                if self.priority == True:
                    embedVar.add_field(name="Using Priority Queue System.", value = "Please be patient.", inline=False)
                
                await channel.send(embed=embedVar)
                self.taOnDuty.append(ta)
                await ctx.send("You have checked into office hours!",delete_after=5)
                if self.priority == True:
                    await ctx.send("*Priority Queue is active.*", delete_after=5)
            #someone else is in office hours
            elif ta not in self.taOnDuty:
                self.taOnDuty.append(ta)
                await ctx.send("You have checked into office hours!",delete_after=5) 
            # you are already in office hours  
            else:
                await ctx.send("You are already in the office hours")
        else:
            await ctx.send("Please move to the 'instructor-commands' channel",delete_after=5)
            await ctx.message.delete()

    ## Ends Office Hours for specific TA
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def endOh(self,ctx):
        if ctx.message.channel.name == "instructor-commands":
            ta = ctx.message.author
            
            if ta in self.taOnDuty:
                self.taOnDuty.remove(ta)
                await ctx.send("You have checked out of office hours!", delete_after=5)
                
                #There are no more TAs on duty
                if len(self.taOnDuty) == 0:
                    if self.priority == True:
                        self.priority = False
                    channel = get(ta.guild.channels, name="request")
                    embedVar = discord.Embed(title="Office hours are now over!", description="Please wait for a TA to open Office hours to join", color=0xff0000)
                    await channel.send(embed=embedVar)

                    #tells all students in the queue they have been removed
                    print(self.ohQueue)
                    for x in range(len(self.ohMsg)):
                        await self.ohMsg[x].delete()
                        await self.ohQueue[x].send("Office Hours are now closed. You have been removed from the queue.")
                    self.ohMsg.clear()
                    self.ohQueue.clear()
            else:
                await ctx.send("You are not in office hours")
        else:
            await ctx.send("Please move to the 'instructor-commands' channel",delete_after=5)
            await ctx.message.delete()

    ## Accept a Students Plea for Help and sets permissions
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def accept(self,ctx):
        if ctx.message.channel.name == "instructor-commands":
            ta = ctx.message.author
            if ta in self.taOnDuty:
                studentMember = self.ohQueue.pop(0)
                self.ohMsg.pop(0)
                
                
                self.tick(studentMember.id)

                member = ctx.message.author
                ctx.guild.roles #[Everyone, Limbo, Student, TA, Professor, HACKER!!, BOT]

                #creates objects of each role for easy access
                profRole = get(member.guild.roles, name="Professor")
                taRole = get(member.guild.roles, name="TA")
                stuRole = get(member.guild.roles, name="Student")
                everyRole = get(member.guild.roles, name="@everyone")
                #create a temp role to assign to student
                name = studentMember.display_name
                await ctx.guild.create_role(name=name)
                tempRole = get(member.guild.roles, name=studentMember.display_name)
                await studentMember.add_roles(tempRole)
                
                newCategory = await ctx.guild.create_category("{} Office Hour Session".format(studentMember.display_name))
                await newCategory.set_permissions(everyRole,read_messages=False)
                await newCategory.set_permissions(stuRole,read_messages=False)
                await newCategory.set_permissions(tempRole, read_messages=True)
                await newCategory.set_permissions(taRole, read_messages=True)
                await newCategory.set_permissions(profRole, read_messages=True)

                TC = await newCategory.create_text_channel("{} Text Chat".format(studentMember.display_name))
                await newCategory.create_voice_channel("Session Voice Chat")
                await TC.send("{} and {}, time to figure out those bugs! Use !close to end the session.".format(studentMember.mention,ta.mention ))
            else:
                await ctx.send("You are not in office hours")
        else:
            await ctx.send("Please move to the 'instructor-commands' channel",delete_after=5)
            await ctx.message.delete()

    ## Deny a Student's Plea for Help
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def reject(self,ctx):
        if ctx.message.channel.name == "instructor-commands":
            #!reject [Student ID] [Reason]
            msg = ctx.message.content.split()
            if len(msg) < 3:
                await ctx.send("Invalid commands. !reject [Student ID] [Reason]")
            else:
                if ctx.message.channel.name == "instructor-commands":
                    studentID = int(msg[1])
                    index = -1
                    #looks through queue to find student
                    for x in range(len(self.ohQueue)):
                        if self.ohQueue[x].id == studentID:
                            index = x

                    if index == -1:
                        await ctx.send("You typed in the id wrong. Try again.")
                    else:
                        #removes unused items and sends DM to student why
                        msg.pop(0)
                        msg.pop(0)
                        msg = " ".join(msg)
                        studMsg = "you are being removed from the queue for the reason:\n"+msg

                        #message returns user not other thing
                        guildId = await ctx.guild.fetch_member(studentID)
                        await guildId.send(studMsg)

                        await self.ohMsg[index].delete()
                        await ctx.message.delete()
                        self.ohMsg.pop(index)
                        self.ohQueue.pop(index)
                else:
                    await ctx.send("You are in the wrong channel. Please use the instructor-commands channel.")
        else:
            await ctx.send("Please move to the 'instructor-commands' channel",delete_after=5)
            await ctx.message.delete()
    
    ## Allows a Student to Make a Plea for Help
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA',"Student")
    async def join(self,ctx):
        if ctx.message.channel.name == "request":
            if len(self.taOnDuty) > 0:
                instructorID = ""
                studMsg = "No message given"
                if " " in ctx.message.content:
                    studMsg = " ".join(ctx.message.content.split()[1:])
                
                #Looks at all the channels and gets the id of the specific one
                for channel in ctx.guild.channels:
                    if channel.name == "instructor-commands":
                        instructorID = channel.id

                if ctx.message.channel.name == "request":
                    if ctx.author not in self.ohQueue:
                        studentMember = ctx.message.author
                        authID = "!reject "+str(studentMember.id)
                        studentData = self.findUser(studentMember.id)
                        #Puts embedded message in the instructor channel
                        embedVar = discord.Embed(title=ctx.message.author.display_name, description=studMsg, color=0xff0000)
                        embedVar.add_field(name="To reject: ", value=authID, inline=False)
                        if studentData != -1:
                            embedVar.add_field(name="Current Priority: ", value=studentData.weekly, inline=True)
                            embedVar.add_field(name="All Time OH accepts: ", value=studentData.allTime, inline=True)
                        else:
                            embedVar.add_field(name="Current Priority: ", value=0, inline=True)
                            embedVar.add_field(name="All Time OH accepts: ", value=0, inline=True)


                        discordMsg = await ctx.guild.get_channel(instructorID).send(embed=embedVar)

                        #adds the user and msg id to the queue
                        self.ohQueue.append(studentMember) 
                        self.ohMsg.append(discordMsg)

                        # sorts on join 
                        if self.priority == True:
                            self.sortQueueP()
                        
                    else:
                        msg = "{} You are already in the queue".format(ctx.message.author.mention)
                        await ctx.send(msg,delete_after=3)
                else:
                    await ctx.send("You are in the wrong channel idiot.")
                #deletes the command after being called 
                await ctx.message.delete()
            else:
                await ctx.send("The instructors are taking a break, please wait for them to return" )
        else:
            await ctx.send("Please move to the 'request' channel",delete_after=5)
            await ctx.message.delete()
      
    ## Allows a Student to Give Up on Getting Help
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA',"Student")
    async def leave(self,ctx):
        if ctx.message.channel.name == "request":
            userId = ctx.message.author.id
            index = -1
            for x in range(len(self.ohQueue)):
                if self.ohQueue[x].id == userId:
                    index = x
            if index != -1:
                # finds the student ID, gives a message and finsd rejectionID
                studentID = ctx.message.author.id
                studMsg = "You have decided to leave the queue!"

                #message returns user not other thing
                guildId = await ctx.guild.fetch_member(studentID)
                await guildId.send(studMsg)

                await self.ohMsg[index].delete()
                self.ohMsg.pop(index)
                self.ohQueue.pop(index)
            else:
                await ctx.send("{} you are not in the queue".format(ctx.message.author.mention))
        else:
            await ctx.send("Please move to the 'request' channel",delete_after=5)
        await ctx.message.delete()

    ## Shows a Student Their Position in the Queue
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA',"Student")
    async def position(self,ctx):
        if ctx.message.channel.name == "request":
            userId = ctx.message.author.id 
            index = -1
            for x in range(len(self.ohQueue)):
                if self.ohQueue[x].id == userId:
                    index = x
            if index != -1:
                await ctx.send(ctx.message.author.mention + ", you are number {} in the queue.".format(index+1), delete_after=5)
            else:
                await ctx.send("{} you are not in the queue".format(ctx.message.author.mention), delete_after=5)
        else:
            await ctx.send("Please move to the 'request' channel",delete_after=5)
        await ctx.message.delete()

    ## Closes a Temporary Category and it's Channels
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA')
    async def close(self,ctx):
        untouchable = ["Instructors","Students","Authentication","Lecture"]
        message = ctx.message
        textChannel = message.channel
        categoryId = textChannel.category_id
        category = get(textChannel.guild.categories, id = categoryId)
        #deletes a role if called from inside of office hours
        if "Office Hour Session" in category.name:
            catName = category.name
            userName = catName.split(" Office",1)
            tempRole = get(message.guild.roles, name = userName[0])
            await tempRole.delete()
        #deletes all items under a category
        if category.name not in untouchable:
            for vc in category.voice_channels:
                await vc.delete()
            for tc in category.text_channels:
                await tc.delete()
            await category.delete()
        else:
            await ctx.send("You are not in the correct chat to call this command.")
            await ctx.message.delete()


    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA','Student')
    async def onDuty(self,ctx):
        if len(self.taOnDuty) == 0:
            await ctx.send("There are no current TAs on duty")
        else:
            tas = "TAs on duty:\n"
            for ta in self.taOnDuty:
                tas += ta.display_name + "\n"

            await ctx.send(tas)
            
        
    
    @commands.command(pass_context=True)
    @commands.has_any_role('Professor','TA','Student')
    async def inQueue(self,ctx):
        size = len(self.ohQueue)
        await ctx.send("There are currently {} students in the queue.".format(size))
        if size != 0:
            index = 1
            students = "Current Queue:\n"
            for stu in self.ohQueue:
                students += str(index) + ". "+ stu.display_name + "\n"
                index += 1
            await ctx.send(students)
        
        
    #counter to how many times people have joined 
    #first somehow get a list of everyone on the server ina  text doc
    #then everytime !join is used add an increment of sort to the students
    #can calculate weekly and daily if needed

def setup(client):
    client.add_cog(queues(client))