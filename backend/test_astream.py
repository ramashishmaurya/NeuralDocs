import asyncio
from app.rag.pipeline import build_rag_chain

async def test():
    chain = build_rag_chain('c2d24fbc-0bf9-442d-8a89-9ccd9137838e')
    print("Testing astream...")
    async for c in chain.astream({'input': 'hello', 'chat_history': []}):
        print("Chunk:", c.keys())
        if 'answer' in c:
            print("Answer content:", repr(c['answer']))

asyncio.run(test())
