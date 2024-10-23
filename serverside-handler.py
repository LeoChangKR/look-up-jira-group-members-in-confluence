import json
import os
import requests
 
def handle(event, context):
    # Set default CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',  # Adjust as per security requirements
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '3600',  # Adjust according to your needs
    }
 
    # Check if the path matches the expected endpoint for Jira API requests
    if event.path == '/function/jira-wiki-function':
        try:
            body = json.loads(event.body)  # Directly load without decoding
            group_name = body.get('groupName')
 
            # Retrieve admin credentials from environment variables
            admin_username = os.environ.get('ADMIN_USERNAME')
            admin_password = os.environ.get('ADMIN_PASSWORD')
 
            # Construct the Jira API request URL
            jira_url = f"https://$YOUR JIRA URL$/rest/api/2/group/member?groupname={group_name}&includeInactiveUsers=true&maxResults=10000"
 
            # Make the request to Jira API using Basic Authentication
            response = requests.get(jira_url, auth=(admin_username, admin_password))
 
            if response.ok:
                # Return the successful JSON response from Jira
                return {"statusCode": 200, "headers": cors_headers, "body": response.json()}
            else:
                # Return an error response if the Jira API call failed
                return {"statusCode": response.status_code, "headers": cors_headers, "body": {"error": "Failed to fetch group members"}}
        except json.JSONDecodeError:
            return {"statusCode": 400, "headers": cors_headers, "body": {"error": "Invalid JSON format"}}
        except KeyError:
            return {"statusCode": 400, "headers": cors_headers, "body": {"error": "Missing groupName in request"}}
 
    # Handle other paths or return a default response for unmatched routes
    return {"statusCode": 404, "headers": cors_headers, "body": {"error": "Not Found"}}
