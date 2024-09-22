# Bucket Buddy 🪣

## Overview

Bucket Buddy is a tool that allows users to interact with Cloudflare R2 storage using a simple interface. It includes a server-side worker for handling file uploads, downloads, and management.

### Components

1. **index.js** - [Worker]
2. **index.html** - [R2 Bucket]

![GUI Screenshot](https://github.com/user-attachments/assets/1906c175-31ba-4d25-b1da-ce2f5f43a47e)

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
bucket_name = 'your-bucket-name-here'<br>
</code>


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
<code>wrangler secret put MY_BUCKET</code><br>

1. open the .py add your worker domain<br>
<code>self.api_url = 'https://your-worker.workers.dev'</code>

<code>python3 bucket_buddy.py</code>

## GUI

<img width="818" alt="Screenshot 2024-09-21 at 10 14 05 PM" src="https://github.com/user-attachments/assets/8e780f38-53cd-4e4d-9491-e5eb24fe4e87">

### macOS app included unzip the .tar then run  the executable 
<code>tar -xvf bucketbuddy.tar</code><br>
<code>./bucketbuddy</code><br>
ENJOY!









