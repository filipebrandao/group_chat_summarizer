# Group Chat Summarizer

This is a Python-based script that takes in the exports of your chat from either WhatsApp and provides a portuguese 🇵🇹summarization of the conversations that occurred during a specified time period. The script uses OpenAI's GPT to generate a summarized text, making it a handy tool for understanding the main points of long conversations.

This project can be used to generate summaries of your conversations covering the topics discussed during the specified time range.

## Requirements

- Python 3.7 or higher
- `openai` Python package
- `regex` Python package
- `dateutil` Python package
- `argparse` Python package
- An exported group chat from either WhatsApp

## Installation

Before installation, it's recommended to create a Python virtual environment to isolate the project dependencies. You can do this using the following commands:

```bash
python3 -m venv env
source env/bin/activate
```

Then, install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

## Exporting Chat History

To use this script, you need to have an exported group chat from either WhatsApp as a text file. Here are the instructions on how to export your chat history from WhatsApp:

### WhatsApp

To export your group chat from WhatsApp, follow these steps:

1. Open WhatsApp and go to the group chat you want to export.
2. Tap on the group name at the top of the screen to open the group info.
3. Scroll down and tap on "Export chat".
4. Choose whether to include media files or not.
5. Select how you want to share the chat export file. You can send it to yourself via email, save it to your device, or use any other method.
6. Save the chat export file as a text file with a .txt extension.

## Usage

First you must update the `config.ini` file to set your own OpenAI api key.
Then, to use this script, navigate to the directory containing the script, and run it in the terminal. The basic usage is:

```bash
python group_chat_summarize.py <chat_export_file> <summary_file> <start_date> <end_date> --model=<model>
```

Here's a description of the command-line arguments:

- `chat_export_file`: This is the path to the text file that contains your chat history export.
- `summary_file`: This is the path to the output text file where the summary will be written.
- `start_date`: This is the date from which the summary should start. The format should be "dd/mm/yyyy".
- `end_date`: This is the date till which the summary should go. The format should be "dd/mm/yyyy".
- `--model`: This optional argument specifies the OpenAI model. Default is 'gpt-4'. If 'gpt-4' is not supported in your environment, you can switch to 'gpt-3.5-turbo'

For example:

```bash
python group_chat_summarize.py chat_export.txt summary.txt 01/01/2023 31/01/2023 --model='gpt-3.5-turbo'
```

The script will print the summary to the console and write it to the output file.

## Contribution

Contributions to the project are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code follows the style of the existing project code, and add tests for any new features.

## License

See [LICENSE](./LICENSE) for more details.
