from ..agents.kv_store_agent import KeyValueStoreAgent
# from .other_agent import OtherAgent

AGENT_REGISTRY = {
    "kv_store": KeyValueStoreAgent,
    # "form_filler": OtherAgent,
}
