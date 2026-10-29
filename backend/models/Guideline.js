import mongoose from 'mongoose';
const schema=new mongoose.Schema({key:{type:String,default:'primary',unique:true},brand:{type:String,required:true},tone:{type:String,default:''},bannedTerms:[{term:String,replacement:String}],facts:[{incorrect:String,approved:String,source:String}],claimsPolicy:{type:String,default:'Superlatives and guarantees require approved evidence.'}},{timestamps:true});
export default mongoose.model('Guideline',schema);
