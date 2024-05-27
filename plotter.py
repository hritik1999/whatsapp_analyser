from uagents import Agent,Context
from application.models import Message
from application.utils import data_analysis

plotter = Agent(name="plotter", seed="plotter recovery phrase",port=8002, endpoint="http://localhost:8002/submit")


@plotter.on_event("startup")
async def introduce_plotter(ctx: Context):
    ctx.logger.info(f"Hello, I'm {ctx.name} and my address is {ctx.address}.")


@plotter.on_query(model=Message,replies={Message})
async def plotter_query_handler(ctx: Context, sender: str, _query: Message):
    ctx.logger.info(f"Received message")
    analysis = data_analysis(_query.message)
    await ctx.send(sender, Message(message=analysis))

if __name__ == "__main__":
    plotter.run()