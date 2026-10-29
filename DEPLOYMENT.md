# TRUST MARK deployment

1. Push this repository to GitHub. Do not commit `.env` files.
2. Create MongoDB Atlas cluster and application database user. Copy the SRV URI.
3. Deploy `ai-service` as a Render Python web service. Build: `pip install -r requirements.txt`. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`. Set `GEMINI_API_KEY` and `GEMINI_MODEL` if using Gemini. Record service URL.
4. Deploy `backend` as a Render Node web service. Build: `npm install`. Start: `npm start`. Set `MONGO_URI`, `JWT_SECRET` (32+ characters), `DEMO_PASSWORD`, `AI_URL` (step 3 URL), `FRONTEND_URL` (step 5 URL). Check `/api/health` returns mongodb storage.
5. Seed users **once** against the Atlas database: run `cd backend && npm run seed` in an environment with the same Mongo URI and demo password. Do not run seed on each production restart.
6. Deploy `frontend` on Vercel with root directory `frontend`, build `npm run build`, output `dist`. Set `VITE_API_URL=https://YOUR-BACKEND.onrender.com/api` and deploy.
7. Update backend `FRONTEND_URL` to the actual Vercel origin, then redeploy backend. Test login and full workflow.
8. If using client-side routes in future, add a Vercel rewrite to index.html. This MVP currently uses in-page navigation.

Production considerations: configure HTTPS, restrict Atlas network access where possible, enable service logs, rotate credentials if exposed, and disable/change shared demo accounts before using real organization data. Free services may sleep.
