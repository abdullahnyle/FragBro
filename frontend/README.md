# FragBro frontend

React catalog and wear statistics backed by the FastAPI application in `../src/fragbro`.

Start the backend using the root README, then run these commands here:

```bash
npm ci
npm run dev
```

The API defaults to `http://127.0.0.1:8000`. Set `VITE_API_URL` before building to use another host. This value is public in the browser bundle.

`npm run build` creates the static bundle in `dist/`. `npm run lint` checks the frontend source.
