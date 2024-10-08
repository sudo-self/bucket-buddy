/*  src/index.js  

 wrangler secret put: MY_BUCKET
 secret: Your-Api-key
 cross-origin

 "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE",
      "Access-Control-Allow-Headers": "*", <-- set domain name
      "Access-Control-Expose-Headers": "Content-Length, Content-Type",
      "Access-Control-Max-Age": "3600"
    });

 Update these two lines in index.html
 
  const apiUrl = 'https://your-worker.workers.dev';
  const apiKey = 'your R2 api key'; 

 */


var src_default = {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);
    const headers = new Headers({
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE",
      "Access-Control-Allow-Headers": "*",
      "Access-Control-Expose-Headers": "Content-Length, Content-Type",
      "Access-Control-Max-Age": "3600"
    });

    if (request.method === "OPTIONS") {
      return new Response(null, { headers });
    }

    switch (request.method) {
      case "PUT":
        if (key) {
          await env.MY_BUCKET.put(key, request.body);
          return new Response(`Put ${key} successfully!`, { headers });
        } else {
          return new Response("Key is required for PUT request", { status: 400, headers });
        }
      case "GET":
        if (key === "list") {
          return await listObjects(env.MY_BUCKET, headers);
        } else {
          const object = await env.MY_BUCKET.get(key);
          if (object === null) {
            return new Response("Object Not Found", { status: 404, headers });
          }
          object.writeHttpMetadata(headers);
          headers.set("etag", object.httpEtag);
          return new Response(object.body, { headers });
        }
      case "DELETE":
        if (key) {
          await env.MY_BUCKET.delete(key);
          return new Response("Deleted!", { headers });
        } else {
          return new Response("Key is required for DELETE request", { status: 400, headers });
        }
      default:
        return new Response("Method Not Allowed", {
          status: 405,
          headers: {
            Allow: "PUT, GET, DELETE"
          }
        });
    }
  }
};

async function listObjects(bucket, headers) {
  try {
    const list = await bucket.list();
    const files = list.objects.map((obj) => ({ key: obj.key }));
    return new Response(JSON.stringify({ files }), {
      headers: { ...headers, "Content-Type": "application/json" }
    });
  } catch (error) {
    return new Response(`Error listing objects: ${error.message}`, { status: 500, headers });
  }
}

export {
  src_default as default
};

