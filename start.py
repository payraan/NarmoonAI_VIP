#!/usr/bin/env python3
import asyncio
from forwarder import ChannelForwarder

def main():
    print("🔥 Telegram Channel Forwarder Starting...")
    print("📥 Source: @klondikeai")
    print("📤 Target: @NarmoonAI_VIP")
    print("=" * 50)
    
    async def run():
        forwarder = ChannelForwarder()
        await forwarder.start_monitoring()
    
    asyncio.run(run())

if __name__ == "__main__":
    main()
