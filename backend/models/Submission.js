import mongoose from 'mongoose';
const findingSchema=new mongoose.Schema({id:String,type:String,risk:String,snippet:String,explanation:String,guideline:String,evidence:String,suggestion:String,sourceId:String,decision:{type:String,enum:['open','accepted','rejected'],default:'open'}},{_id:false});
const historySchema=new mongoose.Schema({action:String,text:String,actor:{type:mongoose.Schema.Types.ObjectId,ref:'User'},actorName:String,at:{type:Date,default:Date.now},note:String},{_id:false});
const schema=new mongoose.Schema({text:{type:String,required:true},currentText:{type:String,required:true},status:{type:String,enum:['draft','submitted','changes_requested','approved'],default:'draft'},findings:[findingSchema],history:[historySchema],createdBy:{type:mongoose.Schema.Types.ObjectId,ref:'User',required:true},reviewedBy:{type:mongoose.Schema.Types.ObjectId,ref:'User',default:null}},{timestamps:true});
export default mongoose.model('Submission',schema);
