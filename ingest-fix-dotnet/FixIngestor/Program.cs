using FixIngestor.Grpc;
using Surveillance;
using Google.Protobuf.WellKnownTypes;

Console.WriteLine("Starting FIX Ingestor (.NET)...");

// 1. connection to Python Engine
var publisher = new TradePublisher("http://localhost:50051");

Console.WriteLine("Connected to Surveillance Engine at http://localhost:50051");
Console.WriteLine("Press any key to start publishing synthetic CEX trades...");
Console.ReadKey();

var random = new Random();
var instruments = new[] { "BTC-USDT", "ETH-USDC", "SOL-USDT" };
var participants = new[] { "CEX-ALICE", "CEX-BOB", "INSTITUTIONAL-X" };

try
{
    while (true)
    {
        // 2. Generate Synthetic Trade
        var trade = new CanonicalTrade
        {
            EventTimeNs = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() * 1000000,
            Venue = "Injestor.NET",
            Instrument = instruments[random.Next(instruments.Length)],
            Side = random.Next(2) == 0 ? "BUY" : "SELL",
            Price = 40000 + (random.NextDouble() * 1000),
            Quantity = 0.5 + (random.NextDouble() * 2.0),
            ParticipantId = participants[random.Next(participants.Length)],
            OrderId = Guid.NewGuid().ToString(),
            ExecutionId = Guid.NewGuid().ToString(),
            Origin = "CEX"
        };

        var batch = new TradeBatch();
        batch.Trades.Add(trade);

        // 3. Publish
        var ack = await publisher.PublishBatchAsync(batch);
        
        if (ack.Success)
        {
            Console.WriteLine($"[NET] Published: {trade.ParticipantId} {trade.Side} {trade.Quantity:F4} @ {trade.Venue}");
        }
        else
        {
            Console.WriteLine($"[NET] Failed: {ack.Message}");
        }

        await Task.Delay(1000); // 1 sec delay
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Critical Error: {ex.Message}");
}
