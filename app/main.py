from .agents.kv_store_agent import KeyValueStorageAgent

task = {
    "key": "user:123",
    "value": {"name": "Alice"},
    "store_type": "mongo",
    "store_config": {
        "host": "localhost",
        "port": 27017,
        "db": "mcp_test",
        "collection": "users"
    },
    # Optional agent chaining
    "next_agent": "logger",
    "next_task": {"message": "Data stored successfully."}
}

agent = KeyValueStorageAgent()
result = agent.run(task)
print(result)
