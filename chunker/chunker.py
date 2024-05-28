from uagents import Agent,Context
from application.models import Message
from application.utils import text_chunking

analyser_address = 'agent1qtladakw5ly6ap6xk4azz7p4r995rwjr3x8xm2yer479qdf502hvur2wpa4'

chunker = Agent(name="chunker", seed="chunker recovery phrase",port=8000, endpoint="http://whatsappchatanalyzer-chunker-1:8000/submit")


@chunker.on_event("startup")
async def introduce_chunker(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.name} and my address is {ctx.address}.")


@chunker.on_query(model=Message,replies={Message})
async def chunker_query_handler(ctx: Context,sender: str,_query: Message):
    ctx.logger.info(f"Received message from {sender}")
    text_chunks = text_chunking(_query.message)
    await ctx.send(sender, Message(message=text_chunks))

if __name__ == "__main__":
    chunker.run()


