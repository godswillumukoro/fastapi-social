# Fast API
Built for APIs

## Tools
- PostgreSQL
- SQLAlchemy

Pydantic for schema definitions. Schemas solve the following challenges with APIs:
- Easily get data from request body
- Validate data recieved from client. Ensures the user sends what you are expecting
- Define data that can be sent from the frontend. ie. Do not accept arbitriary data from your frontend

The schema is like a contract between the frontend and backend. The server says, if you dont give me data exactly the way I want it, I am going to give you an error.

## Diff Between Put / Patch
With PUT, you pass all of the information for updating it. ie. All the fields

With PATCH, you send the specific data you want updated. ie. 1 field
