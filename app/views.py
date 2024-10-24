from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2
import os
from dotenv import load_dotenv
import json
from datetime import datetime  # Import datetime

# Load environment variables
load_dotenv()

# Path to the CA certificate
ca_certificate_path = './ca-certificate.crt'

# Database connection configuration
connection_string = f"dbname=template-pool user=doadmin password={os.getenv('POSTGRES_PASSWORD')} host=template-pg-do-user-18003520-0.g.db.ondigitalocean.com port=25061 sslmode=require"

# Create a connection pool
def get_connection():
    return psycopg2.connect(
        connection_string,
        sslmode='verify-full',
        sslrootcert=ca_certificate_path,
        host="template-pg-do-user-18003520-0.g.db.ondigitalocean.com"
    )

def get_train_names(from_station_name, to_station_name, date):
    query = """
        SELECT t.train_id, t.train_name, s.time
        FROM trains t
        JOIN schedules s ON t.train_id = s.train_id
        JOIN stations from_station ON s.from_station_id = from_station.station_id
        JOIN stations to_station ON s.to_station_id = to_station.station_id
        WHERE from_station.station_name = %s
        AND to_station.station_name = %s
        AND s.date = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (from_station_name, to_station_name, date))
            result = cursor.fetchall()

    train_list = [{"train_id": row[0], "train_name": row[1], "departure_time": row[2].strftime("%H:%M:%S")} for row in result]
    
    return train_list

# CSRF exempt view to handle POST request
@csrf_exempt
def get_train_names_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            from_station_name = data.get('from_station_name')
            to_station_name = data.get('to_station_name')
            date_str = data.get('date')

            # Convert date from "dd/mm/yy" to "YYYY-MM-DD"
            date_obj = datetime.strptime(date_str, '%d/%m/%y')  # Convert to date object
            date_formatted = date_obj.strftime('%Y-%m-%d')  # Convert to "YYYY-MM-DD"

            trains = get_train_names(from_station_name, to_station_name, date_formatted)
            return JsonResponse(trains, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

