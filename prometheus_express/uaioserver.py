"""
Variant of classic server for use with micropython asyncio.
borrows heavily from microdot for the asyncio web server bare minimums
"""
import asyncio

http_break = b'\r\n'
http_encoding = 'utf-8'
http_default_status = '200 OK'
http_default_type = 'text/plain'



class AIOServer:
    def __init__(self, router):
        self.router = router
        self.server = None

    @staticmethod
    async def _safe_readline(stream):
        line = (await stream.readline())
        # TODO - massive line checks? yolo!
        return line

    async def start_server(self, port, address="0.0.0.0", depth=2):
        """
        This is a coroutine
        """

        async def serve(reader, writer):
            """merge microdot and existing old stuff here"""
            await self.handle_request(reader, writer)

        self.server = await asyncio.start_server(serve, address, port, depth)

        while True:
            try:
                await self.server.wait_closed()
                break
            except AttributeError:
                # per microdot, this just means the server hasn't finished starting?
                await asyncio.sleep_ms(200)

    async def handle_request(self, reader, writer):
        # rip of microdot here?
        line = (await AIOServer._safe_readline(reader)).strip().decode()
        if not line:
            return None
        method, url, http_version = line.split()
        http_version = http_version.split('/', 1)[1]
        headers = {}
        content_length = 0
        while True:
            line = (await AIOServer._safe_readline(reader)).strip().decode()
            if line == "":  # end of headers
                break
            # FIXME - this is _meant_ to be case insensitive! we're just going to force it all
            header, value = line.split(":", 1)
            header = header.lower()
            value = value.strip()
            headers[header.lower()] = value
            if header.lower() == "content-length":
                content_length = int(value)
            body = b""
            if content_length and content_length < 16 * 1024: # arbitrary limit
                #print("huh? content-length on a prom metrics req?")
                body = await reader.readexactly(content_length)
            else:
                pass

            handler = self.router.select(method, url)
            resp = handler(headers, body)

            if 'type' not in resp:
                resp['type'] = http_default_type

            status = resp["status"]
            body = resp["content"]
            content_data = body.encode(http_encoding)
            content_len = len(content_data)

            # straight outta microdot
            MUTED_SOCKET_ERRORS = [
                32,  # Broken pipe
                54,  # Connection reset by peer
                104,  # Connection reset by peer
                128,  # Operation on closed socket
            ]

            try:
                # write out headers...
                headers_out = [
                    'HTTP/1.1 {}'.format(status),
                    'Connection: close',
                    'Content-Type: {}'.format(resp["type"]),
                    'Content-Length: {}'.format(content_len),
                ]
                for h in headers_out:
                    writer.write(h.encode())
                    writer.write(b"\r\n")
                    await writer.drain()
                writer.write(b"\r\n")
                await writer.drain()
                writer.write(content_data)
                await writer.drain()
            except OSError as exc:
                # We might have gotten a connection close or whatever, just let it go...
                if exc.errno in MUTED_SOCKET_ERRORS or exc.args[0] == 'Connection lost':
                    pass
                else:
                    raise
