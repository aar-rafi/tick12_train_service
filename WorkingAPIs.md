# API Endpoints Documentation

### Book Ticket

- **Endpoint**: `http://localhost:8000/api/train/get`
- **Method**: `POST`

#### Request Body

```json
{
  "from_station_name": "Dhaka",
  "to_station_name": "Khulna",
  "date": "01827216261",
}
```

#### Response
```json
{
    "train": {
        "ticket_id": "f66bd837-0981-43cc-9fc2-ffcebb452384",
        "user_id": "6037e588-7da9-4422-8bfc-d780eb7d39e0",
        "train_id": "0c355a51-ebb3-4082-a262-703a09273801",
        "seat_number": "12",
        "price": "200.00",
        "status": 1
    }
}
```