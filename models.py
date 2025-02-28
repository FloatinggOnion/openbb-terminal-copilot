from typing import Any, Literal
from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from enum import Enum
import json


class RoleEnum(str, Enum):
    ai = "ai"
    human = "human"
    tool = "tool"


class LlmFunctionCallResult(BaseModel):
    role: RoleEnum = RoleEnum.tool
    function: str = Field(description="The name of the called function.")
    input_arguments: dict[str, Any] | None = Field(
        default=None, description="The input arguments passed to the function"
    )
    content: str = Field(description="The result of the function call.")


class LlmFunctionCall(BaseModel):
    function: str
    input_arguments: dict[str, Any]


class LlmMessage(BaseModel):
    role: RoleEnum = Field(
        description="The role of the entity that is creating the message"
    )
    content: LlmFunctionCall | str = Field(
        description="The content of the message or the result of a function call."
    )

    @field_validator("content", mode="before")
    def parse_content(cls, v):
        # We do this to make sure, if the client appends the function call to
        # the messages that we're able to parse it correctly since the client
        # will send the LlmFunctionCall encoded as a string, rather than JSON.
        if isinstance(v, str):
            try:
                parsed_content = json.loads(v)
                if isinstance(parsed_content, str):
                    # Sometimes we need a second decode if the content is
                    # escaped and string-encoded
                    parsed_content = json.loads(parsed_content)
                return LlmFunctionCall(**parsed_content)
            except (json.JSONDecodeError, TypeError, ValueError):
                return v


class DataContent(BaseModel):
    content: Any = Field(description="The data content of the widget")


class RawContext(BaseModel):
    uuid: UUID = Field(description="The UUID of the widget.")
    name: str = Field(description="The name of the widget.")
    description: str = Field(
        description="A description of the data contained in the widget"
    )
    data: DataContent = Field(description="The data content of the widget")
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Additional widget metadata (eg. the selected ticker, etc)",
    )


class Widget(BaseModel):
    uuid: str = Field(description="The UUID of the widget.")
    name: str = Field(description="The name of the widget.")
    description: str = Field(
        description="A description of the data contained in the widget"
    )
    metadata: dict[Any, Any] | None = Field(
        default=None,
        description="Additional widget metadata (eg. the selected ticker, etc)",
    )


class AgentQueryRequest(BaseModel):
    messages: list[LlmFunctionCallResult | LlmMessage] = Field(
        description="A list of messages to submit to the copilot."
    )
    context: str | list[RawContext] | None = Field(
        default=None, description="Additional context."
    )
    use_docs: bool = Field(
        default=None, description="Set True to use uploaded docs when answering query."
    )
    widgets: list[Widget] = Field(
        default=None, description="A list of widgets for the copilot to consider."
    )

    @field_validator("messages")
    @classmethod
    def check_messages_not_empty(cls, value):
        if not value:
            raise ValueError("messages list cannot be empty.")
        return value

    
class Message(BaseModel):
    role: str = Field(description="The role of the entity that is creating the message.")
    content: str = Field(description="The content of the message or the result of a function call.")