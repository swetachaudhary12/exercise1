const http = require("http");
const https = require("https");
const url = "https://time.com";

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/getTimeStories") {
    https
      .get(url, (response) => {
        let data = "";

        response.on("data", (chunk) => {
          data += chunk;
        });

        response.on("end", () => {
          const pattern =
            /<li class="latest-stories__item">\s*<a href="([^"]+)">\s*<h3 class="latest-stories__item-headline">([^<]+)<\/h3>/g;
          const matches = [];
          let match;

          while ((match = pattern.exec(data)) !== null) {
            matches.push({
              title: match[2],
              link: `https://time.com${match[1]}`,
            });
          }

          const responseData = matches.slice(0, 6);
          res.writeHead(200, { "Content-Type": "application/json" });
          res.end(JSON.stringify(responseData));
        });
      })
      .on("error", (error) => {
        console.error(error);
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ error: "Internal Server Error" }));
      });
  } else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

const PORT = 80;
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
