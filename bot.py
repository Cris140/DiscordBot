import discord
from discord.ext import commands
import requests
from flask import jsonify
bot = commands.Bot(command_prefix='!')
endpoint:str = 'http://localhost:31337/tts'
client = discord.Client()

@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None: 
        return 

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()
        
@bot.command()
async def ping(ctx):
    await ctx.send('Maradona')

@bot.command()
async def voice(ctx, *, channel: discord.VoiceChannel=None):
    if not channel:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise InvalidVoiceChannel('Nenhum canal para entrar. Especifique um canal válido ou junte-se a um.')

    vc = ctx.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Mover para o : <{channel}> deu time out.')
    else:
        try:
            await channel.connect()
        except asyncio.TimeoutError:
            raise VoiceConnectionError(f'Conectando ao: <{channel}> timed out.')

    await ctx.send(f'Conectado ao : **{channel}**', delete_after=20)

    
@bot.command()
async def tts(ctx, input_text, input_model):
    vc = ctx.voice_client
    data = {"input_text":input_text,"input_model":input_model} 
    await ctx.send("Esperando o servidor criar o audio...")
    req = requests.post(endpoint,data=data)
    batata = req.json()['voice']
    batata = "F:/falatron-website/api/"+batata
    vc.play(discord.FFmpegPCMAudio(batata), after=lambda e: print(f"Finished playing: {e}"))
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 1

    
bot.run('ODk0MDY2MTczODE2MjMzOTg0.YVkmAg.t-k6LLpqVtZNMnmj25yg0mdlq2I')