payload_example = [
    {
        "jsonrpc": "2.0",
        "method": "tasks/send",
        "id": "1",
        "params": {
            "id": "task-123",
            "message": {
                "role": "user",
                "parts": [
                    {
                        "type": "text",
                        "text": "What is the exchange rate between USD and EUR?",
                        "content_type": "text/plain",
                    }
                ],
            },
        },
    },
    {
        "jsonrpc": "2.0",
        "method": "tasks/sendSubscribe",
        "id": "1",
        "params": {
            "id": "task-123",
            "message": {
                "role": "user",
                "parts": [
                    {
                        "type": "text",
                        "text": "What is the exchange rate between USD and EUR?",
                        "content_type": "text/plain",
                    }
                ],
            },
        },
    },
]
