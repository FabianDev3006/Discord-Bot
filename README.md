RegEx Discord Bot

A Discord moderation bot built with Python that automatically detects and handles inappropriate messages using regular expressions. This bot deletes messages containing banned words or patterns, warns users, and can temporarily mute repeat offenders.

Features

Automatic message moderation: Detects offensive or banned words using powerful regex patterns.

Spam tracking: Monitors repeated infractions in a short time window.

Warnings and timeouts: Issues warnings, and mutes users who exceed the spam threshold.

Handles edited messages: Monitors both new messages and message edits.

Customizable regex patterns: Easily add or remove patterns to refine moderation.

Getting Started
Prerequisites

Python 3.9+

Discord bot token

discord.py library

python-dotenv library

Install dependencies with:

pip install discord.py python-dotenv

Setup

Clone the repository:

git clone <repository_url>
cd <repository_directory>


Create a .env file in the project root:

DISCORD_BOT_TOKEN=your_bot_token_here


Run the bot:

python bot.py

Configuration

You can configure the bot in the script:

SPAM_THRESHOLD: Number of infractions before a user is muted.

SPAM_TIME_WINDOW: Time window (in seconds) for counting repeated infractions.

TIMEOUT_DURATION: Duration (in seconds) for temporary mute.

banned_patterns: List of regex patterns to detect inappropriate messages.

How It Works

When a user sends a message, the bot checks it against banned_patterns.

If a banned pattern is detected:

The message is deleted.

The bot tracks infractions per user.

Warnings or timeouts are issued based on the number of infractions within the SPAM_TIME_WINDOW.

Edited messages are also monitored to prevent bypassing moderation.

Tech Stack

Python 3: Core programming language

discord.py: Discord bot framework

regex (re module): Pattern matching for moderation

python-dotenv: Load environment variables

License

This project is licensed under the MIT License.
