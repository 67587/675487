# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 20:35:00 2020

@author: ACER
"""



token = "NjE5MDgzNjg1MDAxNDI4OTky.XXDEnA.CwvZaB1o20w8z9cAKhYyVSPtt6I"





import discord
from discord.ext import commands
import nest_asyncio
import datetime
import json
import os
from urllib import parse, request
import re
import random

nest_asyncio.apply()


client = commands.Bot(command_prefix = '!')
@client.command()
async def ping(ctx):
    await ctx.send('pong')
    
@client.command()
async def test(ctx):
    await ctx.send('str(user.id)')

@client.command(aliases = ["point"])
async def points(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}的錢╭[◕ ͜🔴◕]👍🏼")
    em.add_field(name = "你的錢包" ,value = wallet_amt)
    #em.add_field(name = "你的保險箱" ,value = bank_amt)
    await ctx.send(embed = em)
    
@client.command()
@commands.cooldown(1,59, commands.BucketType.user)
async def 乞討(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(1,10)

    await ctx.send(f" {ctx.author.name}乞討到{earnings}元💰!一分鐘後可再乞討一次")
    
    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json","w") as f:
        json.dump(users,f)

@client.command()
async def 賭(ctx , amount):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    amount = int(amount)
    roll = random.randrange(100)
    earnings = amount 
    
    if amount>users[str(user.id)]["wallet"]:
        await ctx.send(f"@{ctx.author}你錢不夠༼ ◕ ͟🔴◕ ༽! ")
        return
    elif roll <50:
        await ctx.send(f"{ctx.author} 骰到 {roll} 並輸掉 {earnings} 元")
        users[str(user.id)]["wallet"] -= earnings 
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    if 99 > roll >50:
        await ctx.send(f"{ctx.author}骰到 {roll} 並贏得 {earnings} 元!!╭[◕ ͜🔴◕]👍")
        users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json","w") as f:
        json.dump(users,f)
    if roll > 99:
        await ctx.send(f" {ctx.author} 骰到{roll} 並贏得大獎 {earnings} 元!!╭[◕ ͜🔴◕]👍🏼╭[◕ ͜🔴◕]👍🏼╭[◕ ͜🔴◕]👍")
        users[str(user.id)]["wallet"] += (1.5)*earnings   
    with open("mainbank.json" , "w") as f:
        json.dump(users,f)


@client.command()
async def 偷(ctx,member:discord.Member):
   users = await get_bank_data()
   user = ctx.author
   await open_account(ctx.author)
   await open_account(member)
   roll = random.randrange(100)
   earnings = random.randrange(1,10)    
   variable =  ["💎","🍌","👙","🍔","🧀","👟"]
   if 10>users[str(member.id)]["wallet"]:
    await ctx.send(f"@{ctx.author}，{member}身上太窮偷不到錢!༼ ◕ ͟🔴◕ ༽ ")
    return
   elif roll >49:
     await ctx.send(f"{ctx.author}想偷 {member}🤚...，偷錢成功! 從{member}身上偷到{random.choice(variable)}價值{earnings}元!")
     users[str(user.id)]["wallet"] += earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)    
     users[str(member.id)]["wallet"] -= earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)   
   elif 20< roll <49:      
     await ctx.send(f"{ctx.author}想偷 {member}🤚...，可是被{member}告而被反拿{earnings}元!")
     users[str(user.id)]["wallet"] -= earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)    
     users[str(member.id)]["wallet"] += earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f) 
   elif 20> roll :      
     await ctx.send(f"{ctx.author}想偷 {member}🤚...，可是被{member}打而自己被搶走{earnings}元!")
     users[str(user.id)]["wallet"] -= earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)    
     users[str(member.id)]["wallet"] += earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)   
          
          
@client.command(aliases = ["avatar"])
async def 頭貼評分(ctx, member: discord.Member):
    amount = random.randrange(0,100)
    embed = discord.Embed(title=f"這張頭貼的評分為......{amount}分!!╭[◕ ͜🔴◕]👍🏼 ", description=f"{member}的頭貼")
    embed.set_image(url=member.avatar_url)

    await ctx.send(embed=embed)
    
@client.command()
@commands.cooldown(1,59, commands.BucketType.user)
async def 抽獎(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    roll = random.randrange(100)
    rand1 = [" ʕ◕ ͜⚫◕ʔ","💥🔫༼ ◕ ͟👃🏿◕ ༽🖕🏿","༼ ◔╭ܫ╮◔ ༽","༼ᗜ◕ ͜🐽◕ᗜ༽","㊗️🏴󠁧󠁢󠁥󠁮󠁧󠁿🀄️💯祝你期中100","₁₂₃₄₅₆₇₈₉¹²³⁴⁵⁶⁷⁸⁹小型字體"]
    rand2 =  ["╙╨༼ ◕ ͟🔴◕༽╨╜","༼ ( ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞⊙ ͟🔴 ͟͟͞ ͟༽ ͟͟͞ ͟͟͞ ͟͟͞⊙"," [̲̅$̲̅(̲̅◕ ͟🔴◕)̲̅$̲̅]","o͡͡͡╮༼ ◔╭ܫ╮◔ ༽╭o͡͡͡","╭◕ ͟🔴◕╮ﻝﮞ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜⦿💦包莖675","ጿ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ጿ ኈ ቼ跳街舞","﷽特殊符號","┖\\\◔ ͟◔\\\┓┏/◔ ͟◔/┛67舞"]
    rand3 = ["🉑🈶🉑🈚️","╭[◕ ͟🔴◕]👎","🆆🆃🅵","╭ ͝◕ ͟🔴 ͝◕╮生氣五"]
    rand4 = ["🎰╭[◕ ͜🔴◕]👍🏼🎰大鼻子賭場","╭[◕ ͜🔴◕]👍🏼╭[◕ ͜🔶◕]👍🏼╭[◕ ͜🔔◕]👍🏼╭[◕ ͜❎◕]👍🏼╭[◕ ͜🔵◕]👍🏼╭[◕ ͜🌀◕]👍🏼╭[◕ ͜💜◕]👍🏼彩虹675","⎝⧹╲⎝⧹༼ ﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞo.◕ ͜🔴◕ ༽oﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞ.⧸⎠╱⧸⎠ l 激光675"]
    if roll < 50:
        await ctx.send(f"{ctx.author} 抽到{random.choice(rand1)} 並贏得 5 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 5
        with open("mainbank.json","w") as f:
          json.dump(users,f)
        return
    elif 50 <= roll < 75:
        await ctx.send(f"{ctx.author} 抽到{random.choice(rand2)} 並贏得 10 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 10
        with open("mainbank.json","w") as f:
            json.dump(users,f)
        return
    elif 96 > roll >= 75:
        await ctx.send(f"{ctx.author} 抽到{random.choice(rand3)} 並贏得 0 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 0
        with open("mainbank.json" , "w") as f:
            json.dump(users,f)
        return
    elif 96>= roll :
        await ctx.send(f"{ctx.author} 抽到{random.choice(rand4)} 並贏得 大獎 30 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 30
        with open("mainbank.json" , "w") as f:
            json.dump(users,f)
            
@client.command(aliases = ["lb"])
async def 排行(ctx,x = 10):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f" 金錢排行榜{x} " , description = "╭[◕ ͜🔴◕]👍🏼",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)
    
@client.command()
async def give(ctx,member:discord.Member,amount):
   users = await get_bank_data()
   user = ctx.author
   amount = int(amount)
   await open_account(ctx.author)
   await open_account(member)   
   earnings = amount
   if amount > users[str(user.id)]["wallet"]:
    await ctx.send(f"@{ctx.author}你錢不夠༼ ◕ ͟🔴◕ ༽! ")
    return
   else:    
     await ctx.send(f"{ctx.author}  給了 {member} {earnings}元!╭[◕ ͜🔴◕]👍🏼")
     users[str(user.id)]["wallet"] -= earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)    
     users[str(member.id)]["wallet"] += earnings
     with open("mainbank.json","w") as f:
          json.dump(users,f)   
          


          
@client.command(aliases = ["快算快答"])
@commands.cooldown(1,59, commands.BucketType.channel)
async def cal(ctx):
    a = random.randrange(1,99)
    b=random.randrange(1,99)        
    aa = int(a+b)
    
    ans = aa
    
    with open("cal.json","w") as f:
      data = ans
      json.dump(data, f)     
    await ctx.send( f"聊天室快算快答!{a}+{b}，輸入!a 數字搶答!(EX:!a 30)╭[◕ ͜🔴◕]👍🏼")
@client.command()
async def a(ctx,amount):
    user = ctx.author
    users = await get_bank_data()
    amount = int(amount)
    with open("cal.json","r") as f:
     data = json.load(f)
     data=int(data)
    if amount == data:
     with open("cal.json","w") as f:
      new = 1438797864
      json.dump(new, f)  
     await ctx.send(f"答案為{amount}，{ctx.author}第一個算出答案並贏得10元!╭[◕ ͜🔴◕]👍，一分鐘後可算下一題")
     users[str(user.id)]["wallet"] += 10
     with open("mainbank.json","w") as f:
          json.dump(users,f)  
    else:
     with open("cal.json","w") as f:
      new1 = data
      json.dump(new1, f)       
     
     
@client.command(aliases = ["code"])
async def 終極密碼(ctx,amount):
    user = ctx.author
    users = await get_bank_data()
    amount = int(amount)
    with open("pass.json","r") as f:
     ans = json.load(f)
     ans=int(ans)
    if amount == ans:
     with open("pass.json","w") as f:
      new = random.randrange(1,99)
      json.dump(new, f)
     await ctx.send(f"答案為{amount}，{ctx.author}第一個猜中答案並贏得15元!╭[◕ ͜🔴◕]👍")
     users[str(user.id)]["wallet"] += 10
     with open("mainbank.json","w") as f:
         json.dump(users,f)         
    elif amount < ans:
      await ctx.send(f"答{ctx.author}花費2元猜了{amount}...再高一點!")
      users[str(user.id)]["wallet"] -= 2
      with open("mainbank.json","w") as f:
         json.dump(users,f)  
    elif amount > ans:
      await ctx.send(f"答{ctx.author}花費2元猜了{amount}...再低一點!")
      users[str(user.id)]["wallet"] -= 2
      with open("mainbank.json","w") as f:
         json.dump(users,f)  
         
async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f) 
    return users






        
 
client.run(token)