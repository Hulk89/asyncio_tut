import asyncio
import sys
from functools import partial
import logging
import time

fomatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")
logger = logging.getLogger('mylogger')
streamHandler = logging.StreamHandler() # default로 sys.stdout
streamHandler.setFormatter(fomatter)
logger.addHandler(streamHandler)
logger.setLevel(logging.INFO)


def handle_stdin(queue):
    '''
    stdin을 받아서 queue에 put하는 함수.
    '''
    logger.debug('handle_stdin start')
    data = sys.stdin.readline().strip()
    if data == 'q':
        loop = asyncio.get_event_loop()
        loop.remove_reader(sys.stdin)
    logger.debug('queue.put({}) start'.format(data))
    '''
    asyncio.ensure_future: 
        future로 만들고, execution scheduling을 함
        물론, event loop이 시작한 이후에 실행된다. 
    '''
    asyncio.ensure_future(queue.put(data)) 
    logger.debug('queue.put({}) end'.format(data))

async def tick(queue):
    stop = False
    while not stop:
        logger.info('wait data')
        data = await queue.get()
        logger.info('Data received: {}'.format(data))
        if data == 'q':
            stop = True
    logger.info("tick finished.")

def main(): 
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
     # fd를 읽어서 callback을 달아줌
    loop.add_reader(sys.stdin, partial(handle_stdin, queue))
    logger.info('start run_until_complete')
    loop.run_until_complete(tick(queue))
    logger.info('loop close')
    loop.close()

if __name__ == '__main__':
    main()
