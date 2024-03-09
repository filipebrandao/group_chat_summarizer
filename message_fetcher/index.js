"use strict";
const crypto = require("crypto");
const fs = require("fs");
const qrcode = require("qrcode-terminal");

const { Client, LocalAuth } = require("whatsapp-web.js");

// Import the configuration file
const config = require("./config.json");

function sha1Hash(str) {
  let hash = crypto.createHash("sha1");
  hash.update(str);
  return hash.digest("hex");
}

function anonymizeMessageBody(message) {
  let body = message.body
  message.mentionedIds.forEach((mention) => body = body.split(mention.user).join(sha1Hash(`${mention.user}@${mention.server}`)))
  return body
}

const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: "authFolder",
  }),
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("ready", () => {
  console.log("Client is ready!");
  client.getChats().then((chats) => {
    console.log("Got chats!");
    let chatId = null;
    for (let chat of chats) {
      if (chat.name === config.groupChatTitle) {
        chatId = chat.id._serialized;
        console.log("Got chat id: " + chatId);
        break;
      }
    }
    console.log("Getting chat: " + chatId);
    client.getChatById(chatId).then((chat) => {
      console.log("Got chat!");
      chat.fetchMessages({ limit: config.messagesToFetch }).then((messages) => {
        console.log("Got messages!");
        let chatExport = "";
        for (let message of messages) {
          chatExport += `(${new Date(message.timestamp * 1000).toISOString()}) ${sha1Hash(message.author)}: ${anonymizeMessageBody(message)}\n`;
        }
        fs.writeFile("chat_export.txt", chatExport, (err) => {
          // In case of an error throw err.
          if (err) {
            throw err;
          }
        });
        console.log("File written!");
      });
    });
  });
});

void client.initialize();

process.on("SIGINT", async () => {
  console.log("(SIGINT) Shutting down...");
  await client.destroy();
  process.exit(0);
});
