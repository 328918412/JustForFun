import asyncio

async def wget(host):
    print('Wget {} ...'.format(host))
    header = 'GET / HTTP/1.0\r\nHost: {}\r\n\r\n'.format(host)
    connect = asyncio.open_connection(host,80)
    reader,writer = await connect
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':break
        print('{} header > {}'.format(host,line.decode('utf-8').rstrip()))
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.qq.com','www.sina.com','www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
