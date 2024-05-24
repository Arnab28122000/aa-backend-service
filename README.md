# cloud-analytics-service

# Step1: Setup environment variables
This is required to setup environmemnt variables listed in .env.sample file<br>
`echo $variable_name`<br>
`export variable_name=value`<br>
<h3>Variables to set: </h3>
<li>dashtics_username</li>
<li>dashtics_password</li>
<li>dashtics_endpoint</li>
<li>dashtics_db_name</li>

# Step 2: Start the application
`uvicorn main:app --reload`<br>
# Step 3: Create docker container
`docker build -t cloud-analytics-service .`
`go to Docker Desktop and run it`