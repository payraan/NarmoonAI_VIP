import asyncio
from forwarder import ChannelForwarder

async def main():
    print("🔥 Telegram Channel Forwarder")
    print("📥 Source: @klondikeai")
    print("📤 Target: @NarmoonAI_VIP")
    print("=" * 50)
    
    forwarder = ChannelForwarder()
    await forwarder.start_monitoring()

if __name__ == "__main__":
    asyncio.run(main())
