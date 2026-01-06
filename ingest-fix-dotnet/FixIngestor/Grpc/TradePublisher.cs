using Grpc.Net.Client;
using Surveillance;
using System.Threading.Tasks;

namespace FixIngestor.Grpc
{
    public class TradePublisher
    {
        private readonly TradeStream.TradeStreamClient _client;
        private readonly GrpcChannel _channel;

        public TradePublisher(string address = "http://localhost:50051")
        {
            _channel = GrpcChannel.ForAddress(address);
            _client = new TradeStream.TradeStreamClient(_channel);
        }

        public async Task<Ack> PublishBatchAsync(TradeBatch batch)
        {
            try 
            {
                return await _client.PublishTradesAsync(batch);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error publishing trades: {ex.Message}");
                return new Ack { Success = false, Message = ex.Message };
            }
        }

        public void Dispose()
        {
            _channel.Dispose();
        }
    }
}
