# Steam Deck Stock Notifier

Get instant Discord notifications when Steam Deck OLED models become available for purchase. This tool monitors the official Steam store and alerts you as soon as stock appears.

## Features

- **Automated Monitoring**: Runs on a scheduled GitHub Actions workflow, checking every 25 minutes
- **Real-Time Alerts**: Sends instant Discord DM notifications when inventory changes
- **Selective Tracking**: Monitors only OLED models (512GB and 1TB) by default
- **Headless Operation**: Uses headless Chrome browser for efficient, background monitoring
- **Easy Configuration**: All settings managed via environment variables (.env file)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A Discord bot token
- Chrome/Chromium browser installed on your system
- A Discord account and server

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jgorf/Steam-Deck-Stock-Notifier.git
   cd Steam-Deck-Stock-Notifier
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root with your Discord credentials:
   ```
   BOT_TOKEN=your_discord_bot_token_here
   USER_ID=your_discord_user_id_here
   CHANNEL_ID=your_discord_channel_id_here
   ```
   
   - **BOT_TOKEN**: Your Discord bot's authentication token (get from [Discord Developer Portal](https://discord.com/developers/applications))
   - **USER_ID**: Your Discord user ID (enable Developer Mode in Discord settings to copy IDs)
   - **CHANNEL_ID**: The Discord channel ID where notifications will be posted (currently sends DMs by default)

### Usage

#### Run Locally

Execute the script directly:
```bash
python notifier.py
```

The script will:
1. Launch a headless Chrome browser
2. Navigate to the [Steam Deck store page](https://store.steampowered.com/steamdeck/)
3. Check inventory status for configured models
4. Send a Discord DM if any model is in stock
5. Exit cleanly

#### Run on Schedule (GitHub Actions)

The repository includes a workflow configuration that automatically runs the stock checker every 25 minutes. To enable it:

1. Configure the required secrets in your repository settings:
   - `DISCORD_BOT_TOKEN`
   - `DISCORD_USER_ID`
   - `DISCORD_CHANNEL_ID`

2. The workflow will execute automatically on the configured schedule

### Customization

To monitor different Steam Deck models, edit the `DECK_MODELS` list in `notifier.py`:

```python
DECK_MODELS = ["512GB OLED", "1TB OLED"]  # Edit this list
```

To send notifications to a Discord channel instead of DMs, uncomment the relevant section in the `send_discord_notification()` function and update your `CHANNEL_ID`.

## How It Works

1. **Web Scraping**: Uses Selenium with Chromium to load the Steam Deck store page
2. **DOM Parsing**: Searches for product cards and extracts model names and availability
3. **Stock Detection**: Checks for the presence of the `ReservationUnavailable` class to determine stock status
4. **Notifications**: Sends Discord messages asynchronously when stock is detected

## Dependencies

Key libraries used:
- **discord.py** - Discord bot communication
- **selenium** - Web browser automation
- **webdriver-manager** - Automatic Chrome driver management
- **python-dotenv** - Environment variable management

See `requirements.txt` for the complete dependency list.

## Support & Documentation

- **Issues**: Report bugs or suggest features via [GitHub Issues](https://github.com/Jgorf/Steam-Deck-Stock-Notifier/issues)
- **Discord.py Docs**: https://discordpy.readthedocs.io/
- **Selenium Docs**: https://www.selenium.dev/documentation/

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and suggest improvements
- Submit pull requests with enhancements
- Improve documentation and examples

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is designed for personal use. Please respect Steam's terms of service and rate limits when running automated checks. The author is not responsible for any consequences of using this tool.