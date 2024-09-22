## Bucket Buddy

1. index.js [worker]<br>
   
2. index.html [R2 bucket]<br>



<img width="396" alt="Screenshot 2024-09-11 at 2 48 49 PM" src="https://github.com/user-attachments/assets/1906c175-31ba-4d25-b1da-ce2f5f43a47e">

```
npm create cloudflare@latest -- your-worker-name
```

### CRUD (Create, Read, Update, Delete) 

1. PUT: Uploads an object to the bucket.
2. GET: Retrieves an object from the bucket.
3. DELETE: Removes an object from the bucket.
4. LIST: Retrieves a list of objects in the bucket.
   


replace the worker at src / `index.js` with the worker in this repo. 

## R2 binding

 Wrangler.toml
```
[[r2_buckets]]
binding = 'MY_BUCKET'
bucket_name = 'your-bucket-name-here'
```

## R2 CORS policy

**Need it from worker --> bucket on the same origin**

```
[
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
place an R2 storage API token from cloudflare

```
wrangler secret put MY_BUCKET
```
Then the API KEY as the secret ***************<br>

Deploy your worker

```
npx wrangler deploy
```

Visit the your worker URL and it should say "object not found" 404

```
<YOUR_WORKER>.<YOUR_SUBDOMAIN>.workers.dev
```

R2&nbsp;<a href="https://developers.cloudflare.com/r2/api/workers/workers-api-usage/">workers api docs</a><br>

configure your bucket for public acess then upload the `index.html` from this repo<br>

<YOUR_WORKER>.<YOUR_SUBDOMAIN>.workers.dev/<strong>index.html</strong><br>

Now have a mini GUI to interact with your R2<br>


<img width="1440" alt="Screenshot 2024-09-21 at 5 23 35 PM" src="https://github.com/user-attachments/assets/463d7083-5ad9-418b-92f8-5d0540371d5d">

## python GUI

<img width="818" alt="Screenshot 2024-09-21 at 10 14 05 PM" src="https://github.com/user-attachments/assets/1b7107b3-cebb-4477-8a83-b9c2f7b8fd2d">













