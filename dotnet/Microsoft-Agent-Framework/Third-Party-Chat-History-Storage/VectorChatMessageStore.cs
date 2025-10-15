using Microsoft.Agents.AI;
using Microsoft.Extensions.VectorData;
using System.Text.Json;
using Microsoft.Extensions.AI;

namespace Third_Party_Chat_History_Storage
{
    internal sealed class VectorChatMessageStore : ChatMessageStore
    {
        private readonly VectorStore _vectorStore;

        public VectorChatMessageStore(
            VectorStore vectorStore,
            JsonElement serializedStoreState,
            JsonSerializerOptions? jsonSerializerOptions = null)
        {
            this._vectorStore = vectorStore ?? throw new ArgumentNullException(nameof(vectorStore));
            if (serializedStoreState.ValueKind is JsonValueKind.String)
            {
                this.ThreadDbKey = serializedStoreState.Deserialize<string>();
            }
        }

        public string? ThreadDbKey { get; private set; }

        public override async Task AddMessagesAsync(
            IEnumerable<ChatMessage> messages,
            CancellationToken cancellationToken)
        {
            this.ThreadDbKey ??= Guid.NewGuid().ToString("N");
            var collection = this._vectorStore.GetCollection<string, ChatHistoryItem>("ChatHistory");
            await collection.EnsureCollectionExistsAsync(cancellationToken);
            await collection.UpsertAsync(messages.Select(x => new ChatHistoryItem()
            {
                Key = this.ThreadDbKey + x.MessageId,
                Timestamp = DateTimeOffset.UtcNow,
                ThreadId = this.ThreadDbKey,
                SerializedMessage = JsonSerializer.Serialize(x),
                MessageText = x.Text
            }), cancellationToken);
        }

        public override async Task<IEnumerable<ChatMessage>> GetMessagesAsync(
            CancellationToken cancellationToken)
        {
            var collection = this._vectorStore.GetCollection<string, ChatHistoryItem>("ChatHistory");
            await collection.EnsureCollectionExistsAsync(cancellationToken);
            var records = new List<ChatHistoryItem>();
            await foreach (var item in collection
                .GetAsync(
                    x => x.ThreadId == this.ThreadDbKey, 10,
                    new() { OrderBy = x => x.Descending(y => y.Timestamp) },
                    cancellationToken))
            {
                records.Add(item);
            }
            var messages = records.ConvertAll(x => JsonSerializer.Deserialize<ChatMessage>(x.SerializedMessage!)!);
            messages.Reverse();
            return messages;
        }

        public override JsonElement Serialize(JsonSerializerOptions? jsonSerializerOptions = null) =>
            // We have to serialize the thread id, so that on deserialization we can retrieve the messages using the same thread id.
            JsonSerializer.SerializeToElement(this.ThreadDbKey);

        private sealed class ChatHistoryItem
        {
            [VectorStoreKey]
            public string? Key { get; set; }
            [VectorStoreData]
            public string? ThreadId { get; set; }
            [VectorStoreData]
            public DateTimeOffset? Timestamp { get; set; }
            [VectorStoreData]
            public string? SerializedMessage { get; set; }
            [VectorStoreData]
            public string? MessageText { get; set; }
        }
    }
}

