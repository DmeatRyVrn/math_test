import time
import datetime
from sys import stdout
import asyncio
import signal


delta_time = 10

async def timer(seconds):
    #loop = asyncio.get_event_loop()
    start_time = datetime.datetime.now()
    finish_time = start_time + datetime.timedelta(seconds=seconds)
    i = 0
    
    while datetime.datetime.now() < finish_time:
        timer = (str(datetime.datetime.now()-start_time).split('.')[0])
        #await loop.run_in_executor(None, stdout.flush)
        #await loop.run_in_executor(None, stdout.write, '\r')
        #await loop.run_in_executor(None, stdout.write, timer)
        #stdout.flush()

        if i == 1:
            stdout.write('\033[F')
        stdout.write(timer)
        stdout.write('Для выхода введите C:\n')


        if i == 0:
            i = 1
    
        
        
        #print('wait')
        await asyncio.sleep(1)

async def result():
    loop = asyncio.get_event_loop()
    #print('')
    # Ждём действия от пользователя
    while True:
        # Запускаем input() в отдельном потоке и ждём его завершения
        command = await loop.run_in_executor(None, input,)
        if command.lower() == 'c':
            #shutdown()
            print('end')
            break 

async def main():
    task1 = asyncio.create_task(timer(10))
    task2 = asyncio.create_task(result())

    await task1
    await task2

if __name__ == '__main__':
    asyncio.run(main())
    
