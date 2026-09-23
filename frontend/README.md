# FragBro frontend

React catalog and wear statistics backed by the FastAPI application in `../src/fragbro`.

Start the backend using the root README, then run these commands here:

Use Node.js 24 (the version selected in CI).

```bash
npm ci
npm run dev
```

Local development reads the API at `http://127.0.0.1:8000` by default; `VITE_API_URL` can point it to another host. Production builds bundle `src/demo.json` instead of requesting the sleeping backend. Regenerate that file from the repository root with `python scripts/build_demo_snapshot.py` after changing the seed records. The API docs link still opens the backend directly.

`npm run build` creates the static bundle in `dist/`. `npm run lint` checks the frontend source.
