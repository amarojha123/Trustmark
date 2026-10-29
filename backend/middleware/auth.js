import jwt from 'jsonwebtoken';
export function authenticate(req,res,next){const h=req.headers.authorization||'';const token=h.startsWith('Bearer ')?h.slice(7):null;if(!token)return res.status(401).json({error:'Login required'});try{req.user=jwt.verify(token,process.env.JWT_SECRET,{algorithms:['HS256']});next()}catch{return res.status(401).json({error:'Invalid or expired token'})}}
export const authorize=(...roles)=>(req,res,next)=>roles.includes(req.user?.role)?next():res.status(403).json({error:'Permission denied'});
