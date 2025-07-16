from ..agents.kv_store_agent import KeyValueStorageAgent
from ..agents.file_read_agent import FileReadAgent
from ..agents.job_search_agent import JobSearchAgent
# from .other_agent import OtherAgent

AGENT_REGISTRY = {
    "file_read": FileReadAgent,
    "job_search": JobSearchAgent,
     #"kv_store": KeyValueStorageAgent,
    # "form_filler": OtherAgent,
}
