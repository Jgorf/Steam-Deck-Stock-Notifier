# For notifying user via discord message in server
import discord

# Needed for reading variables from .env file
import os
from dotenv import load_dotenv

# For scraping stock data from Steam's webpage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

URL = "https://store.steampowered.com/steamdeck/"

CARD_CLASS = "_1GzH4ChDWcNv3vCKTlSIfb"
OUT_OF_STOCK_CLASS = "ReservationUnavailable"

DECK_MODELS = ["512GB OLED", "1TB OLED"] # Steam Deck models to check for stock

# Discord credentials loaded from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID   = int(os.getenv("USER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


async def send_discord_notification(title: str):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Uncomment below to also post an @mention in the server channel
        # channel_message = f"<@{USER_ID}>**RESTOCK ALERT:** {title} is **IN STOCK** on Steam!\nBuy now: {URL}"
        # Send to channel
        # channel = client.get_channel(CHANNEL_ID)
        # if channel:
        #     await channel.send(message)
        
        # Send a DM directly to the user
        message = f"**RESTOCK ALERT:** {title} is **IN STOCK** on Steam!\nBuy now: {URL}"
        user = await client.fetch_user(USER_ID)
        if user:
            await user.send(message)
        print(f"Discord notification sent for {title}")
        await client.close()

    await client.start(BOT_TOKEN)

"""
    Builds and returns a headless (no browser window) Chrome driver.
"""
def build_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new") # Run without a visible browser window
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

"""
    Loads the Steam Deck page, finds all product cards,
    and checks each wanted model for stock availability.
    Sends a Discord DM if any wanted model is in stock.
"""
def check_stock(driver: webdriver.Chrome):
    import asyncio

    driver.get(URL)

    # Wait up to 20 seconds for product cards to appear in the DOM
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f".{CARD_CLASS}"))
    )

    # Grab all Steam Deck product cards on the page
    cards = driver.find_elements(By.CSS_SELECTOR, f".{CARD_CLASS}")
    print(f"Found {len(cards)} Steam Deck card(s)\n")

    for card in cards:
        # Extract the full model name from the .skutype div and its subelements
        try:
            sku_div = card.find_element(By.CSS_SELECTOR, ".skutype")
            span_text = sku_div.find_element(By.TAG_NAME, "span").text.strip()
            full_text = sku_div.text.strip()
            direct_text = full_text.replace(span_text, "").strip()
            title = f"{direct_text} {span_text}".strip()
        except:
            title = "(title not found)"

         # Skip models that are no longer purchasable (LCD models)
        if not any(model in title for model in DECK_MODELS):
            print(f"Skipping {title}")
            continue

        # If the out-of-stock div exists inside this card, the model is unavailable
        unavailable = card.find_elements(By.CSS_SELECTOR, f".{OUT_OF_STOCK_CLASS}")

        if unavailable:
            print(f"{title}: OUT OF STOCK")
        else:
            # Out-of-stock div is absent —> model is available
            print(f"{title}: IN STOCK — sending Discord notification!")
            asyncio.run(send_discord_notification(title))

    input("\nPress Enter to close the browser...")


if __name__ == "__main__":
    driver = build_driver()
    try:
        check_stock(driver) # Check stock of Steam Deck models
    finally:
        driver.quit() # Closes browser whether the check succeeds or fails
