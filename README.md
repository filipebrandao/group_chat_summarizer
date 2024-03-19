# Whatsapp Group Chat Summarizer

This software allows you to automate generating the summary of a WhatsApp chat group.  

# Modules Description

## Message Fetcher

Fetches the messages from a WhatsApp group in an anonymised fashion.

## Summarizer

Relies on GPT to summarize a given chat log produced by the Message Fetcher. It works in chunks in order to keep the AI model focused on smaller tasks thus improving the output reliability.

# How to use this

1. Ensure the configurations for the Message Fetcher at `message_fetcher/config.json`.
2. Ensure the configurations for the Summarizer at `summarizer/config.ini`, specially make sure that the OpenAI API KEY is defined. 
3. Run the Message Fetcher (you might want to run it once first just to setup your Whatsapp authentication that will be used from thereafter). If you don't know how to run it, read its README file. A file with the chat log will be generated.
4. You can now run the Summarizer, according to its README file, using as input the file generated in the previous point. A new file will be outputted with the resulting summary and that's it!


## Contribution

Contributions to the project are welcome! Please fork the repository and create a pull request with your changes. 

## License

See [LICENSE](./../LICENSE) for more details.
