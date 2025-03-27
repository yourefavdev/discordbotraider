import discord
import asyncio

BLUE = "\033[94m"
RESET = "\033[0m"

MENU = f"""{BLUE}
$$$$$$$$\                            $$\                 $$\   $$\ $$$$$$$$\ $$$$$$$$\ 
\__$$  __|                           $$ |                $$$\  $$ |$$  _____|\__$$  __|
   $$ |$$\   $$\  $$$$$$\   $$$$$$\  $$ | $$$$$$\        $$$$\ $$ |$$ |         $$ |   
   $$ |\$$\ $$  |$$  __$$\ $$  __$$\ $$ |$$  __$$\       $$ $$\$$ |$$$$$\       $$ |   
   $$ | \$$$$  / $$ /  $$ |$$ /  $$ |$$ |$$$$$$$$ |      $$ \$$$$ |$$  __|      $$ |   
   $$ | $$  $$<  $$ |  $$ |$$ |  $$ |$$ |$$   ____|      $$ |\$$$ |$$ |         $$ |   
   $$ |$$  /\$$\ \$$$$$$$ |\$$$$$$$ |$$ |\$$$$$$$\       $$ | \$$ |$$$$$$$$\    $$ |   
   \__|\__/  \__| \____$$ | \____$$ |\__| \_______|      \__|  \__|\________|   \__|   
                 $$\   $$ |$$\   $$ |                                                  
                 \$$$$$$  |\$$$$$$  |                                                  
                  \______/  \______/                                                   
{RESET}
"""

# Load tokens from file
def load_tokens(filename="tokens.txt"):
    try:
        with open(filename, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
            print(f"✅ Loaded {len(tokens)} tokens.")
            return tokens
    except FileNotFoundError:
        print("❌ Error: 'tokens.txt' not found!")
        return []

# Function to run each bot
async def run_bot(token, recipient_id, is_channel, message, count):
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'✅ {client.user} is logged in!')

        try:
            if is_channel:
                channel = client.get_channel(recipient_id)
                if not channel:
                    print(f"⚠️ Error: Channel {recipient_id} not found!")
                    await client.close()
                    return
                
                for _ in range(count):
                    await channel.send(message)
                    print(f"📨 Message sent to channel {channel.name}!")
            
            else:
                user = await client.fetch_user(recipient_id)
                if not user:
                    print(f"⚠️ Error: User {recipient_id} not found!")
                    await client.close()
                    return
                
                for _ in range(count):
                    await user.send(message)
                    print(f"📨 Message sent to {user.name}!")
            
        except Exception as e:
            print(f'⚠️ Error sending message: {e}')
        
        await client.close()

    try:
        await client.start(token)
    except Exception as e:
        print(f'❌ Failed to start bot: {e}')


async def main():
    print(MENU)  
    
    tokens = load_tokens()
    if not tokens:
        print("❌ No valid tokens found. Exiting...")
        return
    
    try:
        print("📌 Choose the target type:")
        print("1️⃣  Send message to a Discord User")
        print("2️⃣  Send message to a Discord Channel")
        choice = input("👉 Enter your choice (1/2): ").strip()

        if choice == "1":
            recipient_id = int(input("🔹 Enter the Discord User ID: "))
            is_channel = False
        elif choice == "2":
            recipient_id = int(input("🔹 Enter the Discord Channel ID: "))
            is_channel = True
        else:
            print("❌ Invalid choice! Please enter 1 or 2.")
            return

        message = input("💬 Enter the message to send: ")
        count = int(input("🔢 How many messages should be sent? "))
    except ValueError:
        print("❌ Invalid input. Please enter numeric values for IDs and message count.")
        return

    tasks = [run_bot(token, recipient_id, is_channel, message, count) for token in tokens]
    await asyncio.gather(*tasks)

# Run the program
asyncio.run(main())
