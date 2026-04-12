### Get Example Path Parameters

Source: https://docs.retool.com/assets/edu/ai/agent-wf.json

Retrieves example path parameters for a Retool component. Includes error handling.

```javascript
const getExamplePathParams = () => {
  try {
    return {};
  } catch {
    return { error: true, message: "Error parsing example path params" };
  }
};
```

---

### Get Example Headers

Source: https://docs.retool.com/assets/edu/ai/agent-wf.json

Retrieves example headers for a Retool component. Includes error handling.

```javascript
const getExampleHeaders = () => {
  try {
    return {};
  } catch {
    return { error: true, message: "Error parsing example headers" };
  }
};
```

---

### Example HTTP Method GET

Source: https://docs.retool.com/queries/reference/objects/query

Demonstrates the GET HTTP method. This is a read-only string.

```javascript
falseGET;
```

---

### Start Retool Instance with Docker Compose

Source: https://docs.retool.com/self-hosted/tutorials/docker

Run this command to start the Self-hosted Retool instance. The initial setup may take several minutes.

```bash
sudo docker compose up -d
```

---

### Get environments response example

Source: https://docs.retool.com/api/get-environments

A sample JSON response structure for the get environments request.

```json
{
  "success": true,
  "data": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "string",
      "description": "string",
      "color": "#FFFFFF",
      "default": true,
      "created_at": "string",
      "updated_at": "string"
    }
  ],
  "total_count": 0,
  "next_token": "string",
  "has_more": true
}
```

---

### Install dependencies

Source: https://docs.retool.com/apps/guides/custom/custom-component-libraries

Install the necessary project dependencies after cloning the repository.

```bash
npm install
```

---

### Set Width Example

Source: https://docs.retool.com/mobile/reference/components/layout/collapsible-container

Example demonstrating how to set the width property for a component.

```javascript
1280;
```

---

### Width Property Example

Source: https://docs.retool.com/mobile/reference/components/layout/card

Example demonstrating the 'width' property, which accepts a number.

```plaintext
false
1280
```

---

### Enable Just-In-Time (JIT) Provisioning

Source: https://docs.retool.com/reference/environment-variables

Set to `true` to enable JIT user provisioning.

```bash
JIT_ENABLED=true
```

---

### Start development mode

Source: https://docs.retool.com/apps/guides/custom/custom-component-libraries

Run the development server to sync local changes to Retool in real-time.

```bash
npx retool-ccl dev
```

---

### Global Setup Script Initialization

Source: https://docs.retool.com/assets/edu/examples/Mailing-List.json

A consolidated script used to initialize all required custom libraries for the project.

```javascript
// lodash
/* Edit library variable below */

const _ = require("lodash");

/* Add destructured imports from library below
eg. const { pow, log } = require("mathjs") */

// numbro
/* Edit library variable below */

const numbro = require("numbro");

/* Add destructured imports from library below
eg. const { pow, log } = require("mathjs") */

// papaparse
/* Edit library variable below */

const Papa = require("papaparse");

/* Add destructured imports from library below
eg. const { pow, log } = require("mathjs") */

// moment-timezone
/* Edit library variable below */

const moment = require("moment-timezone");

/* Add destructured imports from library below
eg. const { pow, log } = require("mathjs") */

// uuid
/* Edit library variable below */

const uuid = require("uuid");

/* Add destructured imports from library below
eg. const { pow, log } = require("mathjs") */
```

---

### Create Source Control configuration

Source: https://docs.retool.com/org-users/guides/retool-api/automate-spaces

Set up Source Control for a child Space. Ensure apps are migrated to Toolscript first.

```bash
curl -X POST https://{CHILD_SPACE_DOMAIN}/api/v2/source_control/config -H 'Authorization: Bearer $BEARER_TOKEN' -H 'Content-Type: application/json' --data {"config": {"config": {"type": "App", "app_id": "app_id", "installation_id": "installation_id", "private_key": PRIVATE_KEY, "url": "string", "enterprise_api_url": "string"}, "provider": "GitHub", "org": "github_organization", "repo": "github_repo", "default_branch": "main"}}
```

---

### Resource Response Schema Example

Source: https://docs.retool.com/api/get-resources

Example JSON response structure returned by the GET /resources endpoint.

```json
{
  "success": true,
  "data": [
    {
      "id": "string",
      "type": "airflow",
      "display_name": "string",
      "folder_id": "string",
      "protected": true,
      "created_at": "2019-02-08T11:45:48.899Z",
      "updated_at": "2019-02-24T18:28:18.790Z"
    }
  ],
  "total_count": 0,
  "next_token": "string",
  "has_more": true
}
```

---

### Initialize a component library

Source: https://docs.retool.com/apps/guides/custom/custom-component-libraries

Create a new component library by running the initialization command.

```bash
npx retool-ccl init
```

---

### Get Example Input JSON

Source: https://docs.retool.com/assets/edu/ai/agent-wf.json

Retrieves example input JSON for a Retool component. Includes error handling for parsing.

```javascript
const getExampleInputJSON = () => {
      try {
        return { /* example input JSON */ } \n      } catch {
        return { error: true, message: 'Error parsing example input JSON' }\n      }\n    }
```

---

### Example agent instructions

Source: https://docs.retool.com/agents/guides/prompting-guidance

Comprehensive examples demonstrating task-specific, context-rich, and role-based instructions.

```text
You are a data analysis assistant. When analyzing the provided dataset:
1. First identify the key metrics present
2. Calculate relevant statistical measures
3. Present insights in bullet points
4. If you spot any anomalies, highlight them separately

```

```text
You are helping with Retool app debugging. Given the error message:
- First identify the component type involved
- Check for common configuration issues
- Suggest specific fixes
- Provide example code if relevant
Only use features available in the current Retool version.

```

```text
Act as a SQL query optimizer. For any query provided:
1. Analyze the query structure
2. Identify potential performance bottlenecks
3. Suggest specific optimizations
4. Explain the reasoning behind each suggestion

```

---

### Prompting the Configuration Assistant for a Vacation Planner

Source: https://docs.retool.com/agents/guides/configure/config-assistant

Use this prompt example to instruct the assistant to build a vacation planning agent with internet search, email, and calendar capabilities.

```text
Create a vacation planner. When given dates, find the best place to go based on the weather that time of year. Search the internet for suggested things to do and places to stay. Email me an itinerary, and put the PTO on my calendar.
```

---

### Get Deployment Status using Node.js

Source: https://docs.retool.com/api/get-a-deployment

Example of how to call the Get Deployment Status API endpoint using Node.js. This snippet demonstrates making an authenticated GET request.

```javascript
const axios = require("axios");

const deploymentId = "YOUR_DEPLOYMENT_ID"; // Replace with the actual deployment ID
const apiToken = "YOUR_API_TOKEN"; // Replace with your Retool API token

axios
  .get(
    `https://your-retool-instance.retool.com/api/source_control/deployment/${deploymentId}`,
    {
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${apiToken}`,
      },
    },
  )
  .then((response) => {
    console.log("Deployment Status:", response.data);
  })
  .catch((error) => {
    console.error(
      "Error fetching deployment status:",
      error.response ? error.response.data : error.message,
    );
  });
```

---

### Accessing startTrigger.urlParams

Source: https://docs.retool.com/workflows/reference/objects/starttrigger

Example JSON structure for the urlParams property of the start trigger.

```json
{
  "id": "238j23abse9"
}
```

---

### Accessing startTrigger.pathParams

Source: https://docs.retool.com/workflows/reference/objects/starttrigger

Example JSON structure for the pathParams property of the start trigger.

```json
{
  "itemID": "12345"
}
```

---

### Select Login Method

Source: https://docs.retool.com/education/labs/development/cli

Displays the available authentication options within the CLI.

```text
? How would you like to login? (Use arrow keys)
❯ Log in using Google SSO in a web browser
  Log in with email and password
  Log in by pasting in cookies
  Log in to localhost:3000
```

---

### Accessing startTrigger.headers

Source: https://docs.retool.com/workflows/reference/objects/starttrigger

Example JSON structure for the headers property of the start trigger.

```json
{
  "employeeId": "92345324527"
}
```

---

### Create Kerberos configuration file

Source: https://docs.retool.com/data-sources/guides/authentication/mssql-kerberos

Create a krb5.conf file with the required realm, KDC, and domain information for your environment.

```text
[libdefaults]
    default_realm = <YOUR-REALM>                 # e.g., http://EXAMPLE.COM
    dns_lookup_realm = false                      # optional
    dns_lookup_kdc = false                        # optional
    ticket_lifetime = 24h                         # optional
    renew_lifetime = 7d                           # optional
    forwardable = true                            # optional

[realms]
    <YOUR-REALM> = {                            # e.g., http://EXAMPLE.COM
        kdc = <KDC-HOSTNAME-OR-IP>              # e.g., kdc.example.com
        admin_server = <KDC-HOSTNAME-OR-IP>     # e.g., kdc.example.com
    }

[domain_realm]
    <YOUR-DOMAIN> = <YOUR-REALM>                # e.g., corp.local = http://EXAMPLE.COM
    .<YOUR-DOMAIN> = <YOUR-REALM>               # e.g., .corp.local = http://EXAMPLE.COM

[logging]
    default = FILE:/var/log/krb5.log            # Log file for Kerberos
    kdc = FILE:/var/log/kdc.log                 # Log file for KDC operations
    admin_server = FILE:/var/log/kadmind.log    # Log file for admin server
```

---

### Create a new Retool application

Source: https://docs.retool.com/education/labs/development/cli

Initialize a new application using the -c flag and follow the interactive prompts.

```bash
retool apps -c
? App name? cli-test
Successfully created an App. 🎉
View in browser: https://(YOUR DOMAIN HERE)/editor/(SOME UNIQUE VALUE)
```

---

### Accessing startTrigger.data

Source: https://docs.retool.com/workflows/reference/objects/starttrigger

Example JSON structure for the data property of the start trigger.

```json
{
  "number": "2398252"
}
```

---

### Calendar Selected Interval Example

Source: https://docs.retool.com/apps/guides/presentation-styling/calendar

This object shows an example of the `selectedInterval` property when a user selects a time interval on the Calendar interface. It includes allDay, start, and end times.

```json
{
  "allDay": false,
  "end": "2025-03-27T10:00:00.000Z",
  "start": "2025-03-27T09:00:00.000Z"
}
```

---

### Get Deployment Status using cURL

Source: https://docs.retool.com/api/get-a-deployment

Example of how to call the Get Deployment Status API endpoint using cURL. Ensure you replace '<token>' with your actual API token.

```curl
curl -L './source_control/deployment/:id' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>'
```

---

### Create a RetoolDB table

Source: https://docs.retool.com/education/labs/development/cli

Initialize a new database table and define columns through interactive prompts.

```bash
 retool db -c
```

```bash
? Table name? patients
? Column name? Leave blank to finish. id
? Column name? Leave blank to finish. firstname
? Column name? Leave blank to finish. lastname
? Column name? Leave blank to finish. medical_record_number
? Column name? Leave blank to finish.
Successfully created a table named patients in RetoolDB. 🎉

View in browser: https://(YOUR DOMAIN HERE)/resources/data/(UNIQUE ID HERE)/patients?env=production
```

---

### Generate SQL from Natural Language Configuration

Source: https://docs.retool.com/data-sources/guides/connect/azure-openai/resource

Configuration examples for converting natural language questions into SQL queries.

```text
You are a SQL expert. Convert natural language questions into SQL Server queries. Return only the SQL query without explanations. Use the following schema: Tables: customers (id, name, email, created_at), orders (id, customer_id, total, status, order_date), products (id, name, price, category)

```

```text
{{ questionInput.value }}

```

---

### Calendar Changeset Example

Source: https://docs.retool.com/apps/guides/presentation-styling/calendar

This object shows an example of the `changeset` Calendar property when a user selects and moves an existing event. It includes the event ID and updated start and end times.

```json
{
  "6nt7smomc81s2jfsdsfvkkph88": {
    "allDay": false,
    "end": "2025-03-27T11:00:00.000Z",
    "id": "6nt7smomc81s2jfsdsfvkkph88",
    "start": "2025-03-27T10:00:00.000Z"
  }
}
```

---

### Agent Execution Response

Source: https://docs.retool.com/agents/tutorials/a2a-tutorial

Example output displayed in the terminal when the agent starts its execution process.

```text
((venv) )  yourname@Retool  ~/repo/folder  python my_script.py "What are the top AI models of 2025"

============================================================
Web Research Assistant
============================================================
Topic: What are the top AI models of 2025

╭──────────────────────────────────────────────────────────────────────────────────── Crew Execution Started ─────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                                                                 │
│  Crew Execution Started                                                                                                                                                                         │
│  Name: crew                                                                                                                                                                                     │
│  ID: id_number                                                                                                                                                       │
│  Tool Args:                                                                                                                                                                                     │
│                                                                                                                                                                                                 │
│                                                                                                                                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

🚀 Crew: crew
└── 📋 Task: task_id_number
    Status: Executing Task...
╭─────────────────────────────────────────────────────────────────────────────────────── 🤖 Agent Started ────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                                                                 │
│  Agent: Research Coordinator                                                                                                                                                                    │
│                                                                                                                                                                                                 │
│  Task: Research the following topic thoroughly: What are the top AI models of 2025                                                                                                              │
│                                                                                                                                                                                                 │
│          Use your web browsing capabilities to:                                                                                                                                                 │
│          1. Find recent and relevant information about this topic                                                                                                                               │
│          2. Identify key facts, trends, and insights                                                                                                                                            │
│          3. Note any important sources or references                                                                                                                                            │
│                                                                                                                                                                                                 │
│          Provide a comprehensive summary of your findings.                                                                                                                                      │
│                                                                                                                                                                                                 │
```

---

### API Key Authentication Example

Source: https://docs.retool.com/data-sources/concepts/authentication

Use this method when an integration requires an API key or token for authentication. Ensure you have obtained the necessary credentials.

```text
API Key: 1234567890abcdef1234567890abcdef
```

---

### Get environments via cURL

Source: https://docs.retool.com/api/get-environments

Example command to fetch environments using cURL with a Bearer token.

```bash
curl -L './environments' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>'
```

---

### Retool Workflows Overview

Source: https://docs.retool.com/llms.txt

This section provides an overview of Retool Workflows, including links to the main documentation, quickstart guide, and tutorials.

```APIDOC
## Retool Workflows

### Description
Retool Workflows allows you to build, schedule, and monitor your jobs, alerts, and ETL tasks.

### Documentation Links
- **Main Documentation**: [https://docs.retool.com/workflows](https://docs.retool.com/workflows)
- **Quickstart Guide**: [https://docs.retool.com/workflows/quickstart](https://docs.retool.com/workflows/quickstart)
- **Tutorial**: [https://docs.retool.com/workflows/tutorial](https://docs.retool.com/workflows/tutorial)
```

---

### Node Capacity Example

Source: https://docs.retool.com/self-hosted/tutorials/kubernetes

Example output from `kubectl describe nodes` showing the Capacity section. Verify that 'cpu' and 'memory' meet the specified requirements.

```yaml
Capacity:
  attachable-volumes-aws-ebs: 25
  cpu: 8
  ephemeral-storage: 83873772Ki
  hugepages-1Gi: 0
  hugepages-2Mi: 0
  memory: 7931556Ki
  pods: 29
```

---

### Item Mode Configuration

Source: https://docs.retool.com/apps/reference/components/navigation

Example of setting the item mode to dynamic.

```text
"dynamic"
```

---

### Building a Custom Docker Image

Source: https://docs.retool.com/self-hosted/concepts/hardened-images

Example of extending a Retool backend image to install additional packages. This approach is not recommended for hardened images.

```docker
FROM tryretool/backend
RUN apt-get install ...
```

---

### Status Component Properties Examples

Source: https://docs.retool.com/mobile/reference/components/forms/status

Examples demonstrating how to set various properties for the Status component.

```javascript
false;
```

```javascript
false[
  ("/icon:bold/shopping-gift",
  "/icon:bold/interface-user-single",
  "/icon:bold/interface-align-layers-1")
];
```

```javascript
falseleft;
```

```javascript
false"dynamic"
```

```javascript
false[("Label 1", "Label 2", "Label 3")];
```

```javascript
falseHello world!
```

---

### Start Trigger Webhook Configuration

Source: https://docs.retool.com/assets/edu/ai/ai-action-wf.json

Configuration for the 'startTrigger' webhook, including headers, input schema, and example JSON input for ticket-related data.

```json
{
  "ticket1": "I have lost my baggage and need someone to help me locate it! This is the third time this has happened in the past month and I am an exclusive frequent flyer on Air New England! This shouldn't be happening. Maybe I should switch to Nantucket Air!",
  "ticket2": "I am a frequent flyer and I need help because I missed my flight.",
  "ticket3": "I have missed my flight and need help."
}
```

---

### List SCIM Users with Node.js

Source: https://docs.retool.com/scim/list-users

Example of how to list SCIM users using Node.js. This snippet demonstrates making an authenticated GET request.

```javascript
const fetch = require("node-fetch");

async function listUsers() {
  const token = "<token>"; // Replace with your actual token
  const response = await fetch("https://retool.example.com/api/scim/v2/Users", {
    method: "GET",
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  console.log(data);
}

listUsers().catch(console.error);
```

---

### Prompt for Configuration Assistant

Source: https://docs.retool.com/education/labs/fundamentals/agentside

Use this prompt to guide the Configuration Assistant in setting up an inventory management agent. It specifies the agent's capabilities and data sources.

```text
Create a inventory management agent that is able to examine @Retool Database , flash_inventory table and
answer questions about the suppliers in this table including costs, lead time, manufacturing time and delivery time.
```

---

### Curl Request to Get Organization

Source: https://docs.retool.com/api/get-organization

Example using curl to fetch organization details. Ensure you replace '<token>' with your actual API token.

```curl
curl -L './organization/' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>'
```

---

### List Objects Request Examples

Source: https://docs.retool.com/api/list-objects-a-group-can-access

Examples of how to structure the request body and execute the API call.

```curl
curl -L './permissions/listObjects' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>' \
-d '{
  "subject": {
    "type": "group",
    "id": 0
  },
  "object_type": "folder",
  "include_inherited_access": true
}'
```

```json
{
  "subject": {
    "type": "group",
    "id": 0
  },
  "object_type": "folder",
  "include_inherited_access": true
}
```

---

### Node.js Request to Get Workflows

Source: https://docs.retool.com/api/get-all-workflows

Example of how to make a request to the workflows endpoint using Node.js, demonstrating the use of fetch with appropriate headers.

```javascript
fetch("./workflows", {
  headers: {
    Accept: "application/json",
    Authorization: "Bearer <token>",
  },
});
```

---

### Retool Apps Quickstart

Source: https://docs.retool.com/llms.txt

Learn the fundamental concepts of Retool apps.

```APIDOC
## Retool Apps Quickstart

### Description
Learn about the fundamental concepts of Retool apps.

### Endpoint
/apps/quickstart
```

---

### Curl Request to Get Workflows

Source: https://docs.retool.com/api/get-all-workflows

Example of how to make a curl request to the workflows endpoint, including necessary headers for authentication and content type.

```curl
curl -L './workflows' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>'
```

---

### List Users using Node.js

Source: https://docs.retool.com/api/list-users

Example of how to list users using Node.js. This snippet demonstrates making an authenticated GET request to the users endpoint.

```javascript
const options = {
  method: "GET",
  headers: {
    Accept: "application/json",
    Authorization: "Bearer <token>",
  },
};

fetch("./users", options)
  .then((response) => response.json())
  .then((response) => console.log(response))
  .catch((err) => console.error(err));
```

---

### View RetoolDB help

Source: https://docs.retool.com/education/labs/development/cli

Display available commands and options for managing RetoolDB.

```bash
retool db --help
Interface with Retool DB.

Options:
      --help          Show help                                        [boolean]
      --version       Show version number                              [boolean]
  -l, --list          List all tables in Retool DB.
  -c, --create        Create a new table.
  -u, --upload        Upload a new table from a CSV file. Usage:
                      retool db -u <path-to-csv>                         [array]
  -d, --delete        Delete a table. Usage:
                      retool db -d <table-name>                          [array]
  -f, --fromPostgres  Create tables from a PostgreSQL database. Usage:
                      retool db -f <postgres-connection-string>         [string]
  -g, --gendata       Generate data for a table interactively. Usage:
                      retool db -g <table-name>                         [string]
      --gpt           A modifier for gendata that uses GPT. Usage:
                      retool db --gendata <table-name> --gpt
```

---

### Configure General Instance Settings

Source: https://docs.retool.com/self-hosted/reference/environment-variables

Settings for domain restrictions, request body limits, and environment identification.

```bash
RESTRICTED_DOMAIN=example.com,example.org
```

```bash
RETOOL_CLIENT_MAX_BODY_SIZE=20mb
```

```bash
RETOOL_ENVIRONMENT=production
```

```bash
RETOOL_EXPOSED_{NAME}=RETOOL_EXPOSED_DB_USERNAME=db_user
```

---

### List Roles using Node.js

Source: https://docs.retool.com/api/list-roles

Example of how to list roles using Node.js. This snippet demonstrates making an authenticated GET request to the roles endpoint.

```javascript
const axios = require("axios");

const listRoles = async () => {
  const token = "YOUR_API_TOKEN"; // Replace with your actual token
  try {
    const response = await axios.get(
      "YOUR_RETOOL_INSTANCE_URL/api/role_permissions/roles",
      {
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${token}`,
        },
      },
    );
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error(
      "Error listing roles:",
      error.response ? error.response.data : error.message,
    );
    throw error;
  }
};

listRoles();
```

---

### Node.js Request to Get User Invite

Source: https://docs.retool.com/api/get-user-invite

Example of how to make a request to the user invites endpoint using Node.js. This snippet is a placeholder and requires implementation.

```javascript
// Node.js example not provided in source.
```

---

### Example URL with Both Query and Hash Parameters

Source: https://docs.retool.com/apps/guides/app-management/url-parameters

When including both query and hash parameters, hash parameters must appear after query strings.

```url
https://example.retool.com/app/customer-dashboard?q=chic&role=viewer&team=workplace#enabled=true
```

---

### Example Prompt for Assist

Source: https://docs.retool.com/data-sources/guides/connect/graphql

Use this prompt format to guide Assist in generating GraphQL queries from natural language. Reference your GraphQL resource using '@'.

```text
query the first 10 repositories using @GraphQL

```

---

### Basic HTTP Authentication Example

Source: https://docs.retool.com/data-sources/concepts/authentication

Use Basic HTTP authentication with a username and password. Ensure you have these credentials to establish the connection.

```text
Username: sampleUser
Password: samplePass123
```

---

### Cleanup Retool Docker Compose Installation

Source: https://docs.retool.com/education/labs/self-hosted/docker-compose

Use this command to stop and remove containers and networks associated with the Retool platform Docker Compose setup.

```bash
docker compose down
[+] Running 13/13
 ✔ Container retool-onpremise-master-https-portal-1          Removed                                                                                              3.7s
 ✔ Container retool-onpremise-master-api-1                   Removed                                                                                             10.9s
 ✔ Container retool-onpremise-master-db-ssh-connector-1      Removed                                                                                             10.9s
 ✔ Container retool-on premise-master-jobs-runner-1          Removed                                                                                             10.8s
 ✔ Container retool-onpremise-master-retooldb-postgres-1     Removed                                                                                              0.3s
 ✔ Container retool-onpremise-master-db-connector-1          Removed                                                                                             10.9s
 ✔ Container retool-onpremise-master-workflows-worker-1      Removed                                                                                             10.9s
 ✔ Container retool-onpremise-master-postgres-1              Removed                                                                                              0.3s
 ✔ Network retool-onpremise-master_backend-network           Removed                                                                                              0.2s
 ✔ Network retool-onpremise-master_db-ssh-connector-network  Removed                                                                                              0.2s
 ✔ Network retool-onpremise-master_workflows-network         Removed                                                                                              0.3s
 ✔ Network retool-onpremise-master_db-connector-network      Removed                                                                                              0.3s
 ✔ Network retool-onpremise-master_frontend-network          Removed                                                                                              0.1s
```

---

### Access App Management Help

Source: https://docs.retool.com/education/labs/development/cli

Displays help documentation and available flags for the 'retool apps' command.

```bash
retool apps --help
Interface with Retool Apps.

Options:
      --help               Show help                                   [boolean]
      --version            Show version number                         [boolean]
  -c, --create             Create a new app.
  -t, --create-from-table  Create a new app to visualize a Retool DB table.
  -l, --list               List folders and apps at root level. Optionally
                           provide a folder name to list all apps in that
                           folder. Usage:
                           retool apps -l [folder-name]
  -r, --list-recursive     List all apps and folders.
  -d, --delete             Delete an app. Usage:
                           retool apps -d <app-name>                     [array]
  -e, --export             Export an app JSON. Usage:
                           retool apps -e <app-name>                     [array]
```

---

### Node.js Request to Retrieve Configuration Variable

Source: https://docs.retool.com/api/retreive-a-single-configuration-variable-and-its-values

Example of how to make a GET request to retrieve a configuration variable using Node.js. Ensure you handle token management securely.

```javascript
const axios = require("axios");

const configurationVariableId = ":id"; // Replace with the actual ID
const token = "<token>"; // Replace with your actual token

axios
  .get(`./configuration_variables/${configurationVariableId}`, {
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${token}`,
    },
  })
  .then((response) => {
    console.log(response.data);
  })
  .catch((error) => {
    console.error("Error fetching configuration variable:", error);
  });
```

---

### Initialize Terraform

Source: https://docs.retool.com/education/labs/resources/appsync

Run this command in the directory containing your main.tf file to initialize Terraform and download necessary providers.

```bash
terraform init

```

---

### cURL Request to Retrieve Configuration Variable

Source: https://docs.retool.com/api/retreive-a-single-configuration-variable-and-its-values

Example of how to make a GET request to retrieve a configuration variable using cURL. Replace '<token>' with your actual API token.

```curl
curl -L './configuration_variables/:id' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>'
```

---

### Enable Custom Platform-Level Auth Steps

Source: https://docs.retool.com/reference/environment-variables

Set to `true` to allow custom authentication steps for user logins.

```bash
ENABLE_CUSTOM_PLATFORM_LEVEL_AUTH_STEPS=true
```

---

### Curl Request for User Invites

Source: https://docs.retool.com/api/get-organization-user-invites

Example of how to make a GET request to the user invites endpoint using curl. Ensure you replace `<token>` with your actual Bearer token.

```curl
curl -L './user_invites' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <token>'
```

---

### Configure License Key

Source: https://docs.retool.com/self-hosted/quickstarts/kubernetes/manifests

Examples for setting the license key in values.yaml using plain text or Kubernetes secrets.

```yaml
config:
  licenseKey: "XXX-XXX-XXX"
```

```yaml
config:
  licenseKeySecretName: license-key-secret
  licenseKeySecretKey: license-key
```

---

### Retrieve Observability Configurations using Node.js

Source: https://docs.retool.com/api/get-observability-provider-configurations

Example of how to retrieve observability configurations using Node.js. This snippet demonstrates making an HTTP GET request with the necessary headers.

```javascript
const options = {
  method: "GET",
  headers: {
    Accept: "application/json",
    Authorization: "Bearer <token>",
  },
};

fetch("./observability/config", options)
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    console.log(data);
  })
  .catch((error) => {
    console.error("Error fetching observability config:", error);
  });
```

---

### Configure CREATE_FIRST_ORG

Source: https://docs.retool.com/reference/environment-variables/general

Enables automatic creation of the first organization on the instance.

```bash
CREATE_FIRST_ORG=true
```
