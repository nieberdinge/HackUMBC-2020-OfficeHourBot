  
# import discord
# from discord.ext import commands 


# class TEMPLATE(commands.Cog):

#     def __init__(self, client):
#         self.client = client
    
#     @commands.Cog.listener()
#     async def on_ready(self):
#         print("TEMPLATE cog online.")

#     @commands.command()
#     async def Anything(self,ctx):
#     #"Put a string under the function to add to !help"
#         await ctx.send("")


# def setup(client):
#     client.add_cog(TEMPLATE(client))



# #here is how to get user input
# import asyncio

# try:
#     choice = await self.client.wait_for('message', check=is_correct, timeout=5.0)
# except asyncio.TimeoutError:
#     return ctx.send('Sorry, you took too long.')