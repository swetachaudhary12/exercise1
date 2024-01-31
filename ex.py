import http.server
import http.client
import re
import json

class TimeStoriesHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/getTimeStories":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            url = "https://time.com"
            connection = http.client.HTTPSConnection(url)
            connection.request("GET", "/")

            response = connection.getresponse()
            data = response.read().decode("utf-8")

            pattern = re.compile(r'<li class="latest-stories__item">\s*<a href="([^"]+)">\s*<h3 class="latest-stories__item-headline">([^<]+)<\/h3>', re.MULTILINE)
            matches = pattern.findall(data)

            responseData = [{"title": match[1], "link": f"https://time.com{match[0]}"} for match in matches[:6]]

            self.wfile.write(json.dumps(responseData).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Not Found".encode("utf-8"))

if __name__ == "__main__":
    PORT = 80
    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, TimeStoriesHandler)
    print(f"Server is running on http://localhost:{PORT}")
    httpd.serve_forever()
