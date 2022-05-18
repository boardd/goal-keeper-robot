from concurrent.futures import ThreadPoolExecutor
from asyncio import events
import serial_asyncio
import asyncio


async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)


async def read(reader):
    while True:
        line = await reader.readline()
        print("Recevied:", line)


async def write(writer):
    while True:
        command_str = await ainput(":")
        writer.write(bytes(command_str, "utf-8"))


async def main():
    loop = events.get_running_loop()

    reader, writer = await serial_asyncio.open_serial_connection(
        url="COM3", loop=loop, baudrate=1000000
    )

    read_task = loop.create_task(read(reader))
    write_task = loop.create_task(write(writer))

    await read_task
    await write_task


if __name__ == "__main__":
    asyncio.run(main())
