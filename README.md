# cloud-analytics-service

# Step1: Setup environment variables
This is required to setup environmemnt variables listed in .env.sample file<br>
`echo $variable_name`<br>
`export variable_name=value`<br>
<h3>Variables to set: </h3>
<li>DATABASE_URL</li>

# Step 2: Start the application
`uvicorn main:app --reload`<br>
# Step 3: Create docker container
`docker build -t aa-backend-service .`
`go to Docker Desktop and run it`