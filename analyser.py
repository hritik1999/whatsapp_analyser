from uagents import Agent,Context
from application.models import Message
from application.utils import personality_analyser

chunker_address = 'agent1q05pvyy4c5sraah8tck40urrpmnwh3dt5p6fa9znr9cj960cnka7v9n00d2'

analyser = Agent(name="analyser", seed="analyser recovery phrase",port=8001, endpoint="http://localhost:8001/submit")

@analyser.on_event("startup")
async def introduce_analyser(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.name} and my address is {ctx.address}.")


@analyser.on_query(model=Message,replies={Message})
async def analyser_query_handler(ctx: Context, sender: str, _query: Message):
    ctx.logger.info(f"Received message")
    analysis = personality_analyser(_query.message)
    await ctx.send(sender, Message(message=analysis))

if __name__ == "__main__":
    analyser.run()