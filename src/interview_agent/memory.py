import json
import time
from enum import Enum
from pathlib import Path
from typing import Type, Iterator

from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage


MEMORY_DIR = Path("memory")
MEMORY_DIR.mkdir(exist_ok=True)

MEMORY_DELL_DIR = Path("memory_dell")
MEMORY_DELL_DIR.mkdir(exist_ok=True)

RATINGS_DIR = Path("ratings.jsonl")


def read_ratings() -> dict[str, int]:
    if not RATINGS_DIR.exists():
        return {}
    data = {}
    with RATINGS_DIR.open("r") as f:
        for rating_dict in (json.loads(line) for line in f):
            data[rating_dict["chat_id"]] = rating_dict["rating"]
    return data


def write_rating(rating: dict):
    with RATINGS_DIR.open("a") as f:
        print(json.dumps(rating), file=f)


class Role(str, Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    FUNCTION = "FUNCTION"

    @classmethod
    def from_str(cls, role: str) -> "Role":
        return cls[role.upper()]


WRAP_FUNCTION_MAPPING: dict[Role, Type[BaseMessage]] = {
    Role.SYSTEM: SystemMessage,
    Role.USER: HumanMessage,
    Role.ASSISTANT: AIMessage,
    Role.FUNCTION: AIMessage,
}


class MemoryItem(BaseModel):
    role: Role
    content: str
    unix_timestamp: int = int(time.time())


def load_memory_general(chat_id: str, memory_dir: Path) -> list[MemoryItem]:
    memory_file = memory_dir / f"{chat_id}.json"
    if not memory_file.exists():
        return []
    with memory_file.open("r") as f:
        return [MemoryItem(**item) for item in json.load(f)]


def save_memory_general(chat_id: str, memory: list[MemoryItem], memory_dir: Path):
    memory_file = memory_dir / f"{chat_id}.json"
    with memory_file.open("w") as f:
        json.dump([item.model_dump() for item in memory], f, indent=4)


def load_all_memory_items_general(memory_dir: Path) -> Iterator[MemoryItem]:
    for memory_file in memory_dir.glob("*.json"):
        yield from load_memory(memory_file.stem)


def load_memory(chat_id: str) -> list[MemoryItem]:
    return load_memory_general(chat_id, MEMORY_DIR)


def save_memory(chat_id: str, memory: list[MemoryItem]):
    return save_memory_general(chat_id, memory, MEMORY_DIR)


def load_all_memory_items() -> Iterator[MemoryItem]:
    return load_all_memory_items_general(MEMORY_DIR)