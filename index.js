export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const objectName = url.pathname.slice(1);

    console.log(`${request.method} object ${objectName}: ${request.url}`);

    try {
      switch (request.method) {
        case 'GET':
          if (objectName === '') {
            return new Response('Object name is required', { status: 400 });
          }

          const object = await env.MY_BUCKET.get(objectName);

          if (!object) {
            return new Response(`Object "${objectName}" not found`, { status: 404 });
          }

          const headers = new Headers();
          object.writeHttpMetadata(headers);
          headers.set('etag', object.httpEtag);
          return new Response(object.body, { headers });

        case 'PUT':
          if (objectName === '') {
            return new Response('Object name is required', { status: 400 });
          }

          await env.MY_BUCKET.put(objectName, request.body);
          return new Response(`Object "${objectName}" stored successfully`, { status: 200 });

        case 'DELETE':
          if (objectName === '') {
            return new Response('Object name is required', { status: 400 });
          }

          await env.MY_BUCKET.delete(objectName);
          return new Response(`Object "${objectName}" deleted successfully`, { status: 200 });

        default:
          return new Response('Unsupported method', { status: 405 });
      }
    } catch (error) {
      console.error(error);
      return new Response('Internal Server Error', { status: 500 });
    }
  }
};

