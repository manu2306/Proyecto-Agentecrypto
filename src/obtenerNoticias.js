const Parser = require("rss-parser");
const parser = new Parser();

async function obtenerNoticias() {
  const feed = await parser.parseURL("https://www.coindesk.com/arc/outboundfeeds/rss/");

  console.log(`Se encontraron ${feed.items.length} noticias.\n`);

  feed.items.slice(0, 5).forEach((noticia, index) => {
    console.log(`${index + 1}. ${noticia.title}`);
    console.log(`   Fecha: ${noticia.pubDate}`);
    console.log(`   Enlace: ${noticia.link}`);
    console.log("");
  });
}

obtenerNoticias();