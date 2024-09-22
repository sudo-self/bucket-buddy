# Bucket Buddy 🪣

<img width="675" alt="Screenshot 2024-09-21 at 11 40 03 PM" src="https://github.com/user-attachments/assets/11a8b566-b8e4-48a2-acd0-ef97ac962857">

## Overview

Bucket Buddy is a tool that allows users to interact with Cloudflare R2 storage using a simple interface. It includes a server-side worker for handling file uploads, downloads, and management.

### Components

1. **index.js** - [Worker]
2. **index.html** - [R2 Bucket]

## Getting Started

To create your Cloudflare Worker, run the following command:

```bash
npm create cloudflare@latest -- your-worker-name
```

CRUD Operations

PUT: Uploads an object to the bucket.<br>
GET: Retrieves an object from the bucket.<br>
DELETE: Removes an object from the bucket.<br>
LIST: Retrieves a list of objects in the bucket.<br>

<code>[[r2_buckets]]<br>
binding = 'MY_BUCKET'<br>
bucket_name = 'your-bucket-name-here'<br></code><br>
Then place a secret in your worker<br>
<code>wrangler secret put MY_BUCKET</code><br>
<code>YOUR-R2-STORAGE-API-KEY</code><br>



1. binding in wrangler.toml
2. secret
3. Replace src/index.js with the one from this repo ```index.js```
4. deploy your worker
<code>npm wrangler deploy</code><br>

open ```bucket_buddy.py``` and append this line with your worker URL<br>

<code>self.api_url = 'https://your-worker.workers.dev'</code><br>

***make sure your bucket is configured for public access***

### run<code>python bucket_buddy.py</code><br>
<img width="818" alt="Screenshot 2024-09-21 at 10 14 05 PM" src="https://github.com/user-attachments/assets/8e780f38-53cd-4e4d-9491-e5eb24fe4e87">


alternatively upload the index.html to you bucket then access the buddy at https://your-worker.workers.dev/index.html


## coors cross-origin

```[
  {
    "AllowedOrigins": [
      "http://YOUR-BUCKET-NAME",
      "https://YOUR-WORKER-NAME"
    ],
    "AllowedMethods": [
      "GET",
      "PUT",
      "POST",
      "DELETE"
    ],
    "AllowedHeaders": [
      "*"
    ],
    "ExposeHeaders": [
      "Content-Length",
      "Content-Type"
    ],
    "MaxAgeSeconds": 3600
  }
]

```















