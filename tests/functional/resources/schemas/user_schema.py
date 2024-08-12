user_default_response_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "username": {
            "type": "string"
        },
    },
    "required": ["id", "username"],
}

user_default_message_schema = {
    "type": "object",
    "properties": {
        "message": {
            "type": "string"
        },
    },
    "required": ["message"],
}
