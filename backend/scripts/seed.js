import 'dotenv/config';
import mongoose from 'mongoose';import bcrypt from 'bcryptjs';import User from '../models/User.js';import Guideline from '../models/Guideline.js';
if(!process.env.MONGO_URI)throw Error('Set MONGO_URI in backend/.env');
await mongoose.connect(process.env.MONGO_URI);
const accounts=[['Admin','admin@trustmark.local','Admin'],['Creator','creator@trustmark.local','Creator'],['Manager','manager@trustmark.local','Manager']];
for(const [name,email,role] of accounts){const password=process.env.DEMO_PASSWORD;if(!password||password.length<10)throw Error('Set DEMO_PASSWORD (at least 10 characters) in backend/.env before seeding');const passwordHash=await bcrypt.hash(password,12);await User.updateOne({email},{$set:{name,role,passwordHash}},{upsert:true})}
await Guideline.updateOne({key:'primary'},{$setOnInsert:{key:'primary',brand:'Acme Cloud',tone:'Clear, helpful and evidence-based',bannedTerms:[{term:'app',replacement:'platform'},{term:'cheap',replacement:'affordable'}],facts:[{incorrect:'5 million',approved:'3.2 million',source:'Approved customer report, sample Q3'}],claimsPolicy:'Superlatives and guarantees require approved evidence.'}},{upsert:true});
console.log('Demo accounts seeded. Password is the DEMO_PASSWORD value from .env');await mongoose.disconnect();
