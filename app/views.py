import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
def get_connection():
    return psycopg2.connect(
        dbname='template-pool',
        user='doadmin',
        password=os.getenv('POSTGRES_PASSWORD'),
        host='template-pg-do-user-18003520-0.g.db.ondigitalocean.com',
        port='25061',
        sslmode='require'
    )

@csrf_exempt  # To allow POST requests without CSRF token for testing purposes
def get_train_names(request):
    if request.method == 'POST':

        # Parse the JSON payload
        data = json.loads(request.body)
        from_station_name = data.get('from_station_name')
        to_station_name = data.get('to_station_name')
        date = data.get('date')

        # TODO DELETE THE BELOW LINE AFTER DB HAS BEEN ADDED
        return JsonResponse({'from_station_name': from_station_name, 'to_station_name': to_station_name})

        if not from_station_name or not to_station_name or not date:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    # Query to get from_station_id and to_station_id
                    cursor.execute("SELECT id FROM stations WHERE name = %s", (from_station_name,))
                    from_station_id = cursor.fetchone()
                    cursor.execute("SELECT id FROM stations WHERE name = %s", (to_station_name,))
                    to_station_id = cursor.fetchone()

                    if not from_station_id or not to_station_id:
                        return JsonResponse({'error': 'Station not found'}, status=404)

                    from_station_id = from_station_id[0]
                    to_station_id = to_station_id[0]

                    # Query to get train_ids from the schedule
                    cursor.execute("""
                        SELECT train_id 
                        FROM schedule 
                        WHERE from_station_id = %s AND to_station_id = %s AND date = %s
                    """, (from_station_id, to_station_id, date))
                    train_ids = cursor.fetchall()

                    if not train_ids:
                        return JsonResponse({'trains': []})

                    # Extract train_ids into a list
                    train_ids = [train_id[0] for train_id in train_ids]

                    # Query to get train names
                    cursor.execute("SELECT name FROM train WHERE id IN %s", (tuple(train_ids),))
                    train_names = cursor.fetchall()

                    # Extract train names into a list
                    train_names = [train_name[0] for train_name in train_names]

                    return JsonResponse({'trains': train_names})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

