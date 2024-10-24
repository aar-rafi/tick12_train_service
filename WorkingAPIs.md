# API Endpoints Documentation

### Book Ticket

- **Endpoint**: `http://localhost:8000/api/trains/get`
- **Method**: `POST`

#### Request Body

```json
{
    "from_station_name": "Dhaka",
    "to_station_name": "Khulna",
    "date": "2024-10-25"
}
```

#### Response
```json
[
    {
        "train_id": "0c355a51-ebb3-4082-a262-703a09273801",
        "train_name": "A",
        "departure_time": "10:00:00"
    }
]
```
