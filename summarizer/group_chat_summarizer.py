import os
import regex as re
import datetime
import argparse
import logging
import configparser
import pytz
from openai import OpenAI


# Load configuration
config = configparser.ConfigParser()
config.read('config.cfg')


# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# Initialize OpenAI client
try:
    api_key = config['OpenAI']['api_key']
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error("Failed to initialize OpenAI client: %s", str(e))
    raise

# Constants
CHAT_LOG_DATE_PATTERN = r'(\(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\))' # Whatsapp chat log expected date format : "(YYYY-MM-DDTHH:MM:SS.sssZ)" 
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
SUMMARY_PROMPT = config['OpenAI']['prompt']
MAX_WORD_COUNT = int(config['Summarizer']['max_word_count'])
TIMEZONE = config['Summarizer']['timezone']


def read_file(file_path):
    """Read the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def parse_whatsapp(text):
    """Parse WhatsApp messages."""
    message_splits = re.split(CHAT_LOG_DATE_PATTERN, text)
    parsed_messages = []
    for i in range(1, len(message_splits), 2):
        message = message_splits[i] + " " + message_splits[i + 1]
        message = whatsapp_remove_sender(message)
        date_str = message_splits[i][1:-1]
        date = datetime.datetime.strptime(date_str, DATE_FORMAT).replace(tzinfo=datetime.timezone.utc).astimezone(pytz.timezone(TIMEZONE)).date()
        parsed_messages.append((date, message))
    return parsed_messages


def whatsapp_remove_sender(message):
    """Remove sender info from WhatsApp message."""
    message_prefix = message.find(': ')
    return 'MESSAGE: ' + message[(message_prefix + 2):]


def filter_messages_by_dates(messages, start_day, end_day):
    """Filter messages based on date range."""
    filtered = []
    for message in messages:
        if message[0] < start_day:
            continue
        elif message[0] > end_day:
            break
        filtered.append(message)
    return filtered


def whatsapp_chunk_text(messages):
    """Split WhatsApp messages into chunks. Theoretically it's easier for GPT to summarize in chunks instead of the whole chat log at once."""
    current_word_count = 0
    current_chunk = ''
    chunks = []
    for _, message in messages:
        message_word_count = len(message.split())
        if current_word_count + message_word_count > MAX_WORD_COUNT:
            chunks.append(current_chunk.strip())
            current_chunk = ''
            current_word_count = 0
        current_chunk += message
        current_word_count += message_word_count
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def summarize_messages(chunks, model):
    """Summarize chunks of text."""
    summary = ''
    calls_counter = 0
    for chunk in chunks:
        calls_counter += 1
        logger.debug(f"Sending prompt {calls_counter} out of {len(chunks)} to GPT! Chunk size: {len(chunk)}")
        chunk_summary = summarize_text(chunk, model)
        summary += chunk_summary + '\n\n'
    return summary


def summarize_text(text, model):
    """Generate summary using GPT model."""
    prompt = f""""{SUMMARY_PROMPT}\n\n {text}"""
    return call_gpt(prompt, model)


def call_gpt(prompt, model):
    """Call the GPT model."""
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(model=model, messages=messages)
    response = completion.choices[0].message.content
    logger.debug('Response:\n' + response + '\n')
    return response


def main(chat_export_file, summary_file, start_day_s, end_day_s, model):
    logger.debug(f"Will run using GPT model: {model}")

    start_day = datetime.datetime.strptime(start_day_s, '%d/%m/%Y').date()
    end_day = datetime.datetime.strptime(end_day_s, '%d/%m/%Y').date()

    content = read_file(chat_export_file)
    parsed_messages = parse_whatsapp(content)
    filtered_messages = filter_messages_by_dates(
        parsed_messages, start_day, end_day)
    chunks = whatsapp_chunk_text(filtered_messages)

    summary = summarize_messages(chunks, model)

    logger.info('\n' + ('*' * 10) + '\nSummary:\n' + ('*' * 10))
    logger.info(summary)

    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Chat Summarizer")

    parser.add_argument("chat_export_file", help="Input file, export of the chat")
    parser.add_argument("summary_file", help="Summary output file")
    parser.add_argument("start_date", help="When to start summarizing from (DD/MM/YYYY)")
    parser.add_argument("end_date", help="Until when to summarize (DD/MM/YYYY)")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model to use for summarization")

    args = parser.parse_args()

    main(
        args.chat_export_file,
        args.summary_file,
        args.start_date,
        args.end_date,
        args.model
    )
