use crate::{canonical, hash_event, CaseEvent};
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::{collections::{HashMap, HashSet}, fs::{self, OpenOptions}, io::Write, path::{Component, Path, PathBuf}};

#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all="camelCase")]
pub struct BundleFile { pub path:String, pub content:String, pub sha256:String }
#[derive(Clone, Serialize, Deserialize)]
#[serde(rename_all="camelCase")]
pub struct ProjectBundle { pub format:String, pub created_at:String, pub files:Vec<BundleFile>, pub sha256:String }
#[derive(Serialize)]
#[serde(rename_all="camelCase")]
pub struct BundlePreview { pub format:String, pub valid:bool, pub errors:Vec<String>, pub file_count:usize, pub case_count:usize, pub case_ids:Vec<String> }

fn sha(b:&[u8])->String{format!("{:x}",Sha256::digest(b))}
fn safe(s:&str)->Result<PathBuf,String>{let p=Path::new(s);if p.as_os_str().is_empty()||p.is_absolute()||p.components().any(|c|!matches!(c,Component::Normal(_))){Err(format!("Unsafe bundle path: {s}"))}else{Ok(p.to_path_buf())}}
fn add_file(path:&str,content:String)->BundleFile{BundleFile{path:path.into(),sha256:sha(content.as_bytes()),content}}
fn seal_bundle(mut b:ProjectBundle)->Result<String,String>{b.sha256.clear();let v=serde_json::to_value(&b).map_err(|e|e.to_string())?;b.sha256=sha(serde_json::to_string(&canonical(&v)).map_err(|e|e.to_string())?.as_bytes());serde_json::to_string_pretty(&b).map_err(|e|e.to_string())}
fn parse(s:&str)->Result<ProjectBundle,String>{serde_json::from_str(s).map_err(|e|e.to_string())}

pub fn export_project(root:&Path)->Result<String,String>{
 let m:Value=serde_json::from_slice(&fs::read(root.join("book.workbench.json")).map_err(|e|e.to_string())?).map_err(|e|e.to_string())?;
 let mut rels:Vec<String>=vec!["book.workbench.json".into(),"book.workbench.seal.json".into(),"REGISTER-PREVERJANJ.jsonl".into()];
 if let Some(entries)=m["incomingTexts"].as_array(){for e in entries{if let Some(p)=e["sourcePath"].as_str(){rels.push(p.into())}}}
 rels.sort();rels.dedup();let mut files=Vec::new();for p in rels{let p=safe(&p)?;let full=root.join(&p);if full.is_file(){let content=String::from_utf8(fs::read(full).map_err(|e|e.to_string())?).map_err(|e|e.to_string())?;files.push(add_file(&p.to_string_lossy(),content))}}
 seal_bundle(ProjectBundle{format:"atmavictu-project-bundle-v1".into(),created_at:chrono::Utc::now().to_rfc3339(),files,sha256:String::new()})
}
pub fn export_case(root:&Path,id:&str)->Result<String,String>{
 let text=fs::read_to_string(root.join("REGISTER-PREVERJANJ.jsonl")).map_err(|e|e.to_string())?;let mut rows=Vec::new();for line in text.lines().filter(|l|!l.trim().is_empty()){let row:Value=serde_json::from_str(line).map_err(|e|e.to_string())?;if row["case_event"]["caseId"].as_str()==Some(id){rows.push(row)}}if rows.is_empty(){return Err(format!("Case {id} not found"))}
 let m:Value=serde_json::from_slice(&fs::read(root.join("book.workbench.json")).map_err(|e|e.to_string())?).map_err(|e|e.to_string())?;let source_ids=rows.iter().filter_map(|r|r["case_event"]["payload"]["incomingTextId"].as_str()).collect::<HashSet<_>>();
 let mut r=rows.iter().map(Value::to_string).collect::<Vec<_>>().join("\n");r.push('\n');let mut files=vec![add_file("REGISTER-PREVERJANJ.jsonl",r)];let mut incoming=Vec::new();
 if let Some(entries)=m["incomingTexts"].as_array(){for e in entries.iter().filter(|e|e["id"].as_str().is_some_and(|x|source_ids.contains(x))){let p=e["sourcePath"].as_str().ok_or("sourcePath missing")?;let p=safe(p)?;let body=String::from_utf8(fs::read(root.join(&p)).map_err(|e|e.to_string())?).map_err(|e|e.to_string())?;files.push(add_file(&p.to_string_lossy(),body));incoming.push(e.clone())}}
 files.push(add_file("case-manifest-fragment.json",serde_json::to_string(&json!({"incomingTexts":incoming})).map_err(|e|e.to_string())?));seal_bundle(ProjectBundle{format:"atmavictu-case-bundle-v1".into(),created_at:chrono::Utc::now().to_rfc3339(),files,sha256:String::new()})
}
pub fn restore_project(root:&Path,text:&str,overwrite:bool)->Result<BundlePreview,String>{
 let b=parse(text)?;let preview=validate(&b)?;if !preview.valid{return Err(preview.errors.join("; "))}if b.format!="atmavictu-project-bundle-v1"{return Err("Expected project backup".into())}
 let paths=b.files.iter().map(|f|safe(&f.path)).collect::<Result<Vec<_>,_>>()?;let collision=paths.iter().filter(|p|root.join(p).exists()).map(|p|p.display().to_string()).collect::<Vec<_>>();if !overwrite&&!collision.is_empty(){return Err(format!("Target already contains: {}",collision.join(", ")))}
 let old=paths.iter().map(|p|(p.clone(),fs::read(root.join(p)).ok())).collect::<Vec<_>>();let mut changed=Vec::new();
 for(f,p)in b.files.iter().zip(paths){let dest=root.join(&p);let result=(||->Result<(),String>{if let Some(parent)=dest.parent(){fs::create_dir_all(parent).map_err(|e|e.to_string())?}fs::write(&dest,f.content.as_bytes()).map_err(|e|e.to_string())})();if let Err(error)=result{for p in changed{let _=fs::remove_file(root.join(&p));}for(p,bytes)in old{if let Some(bytes)=bytes{let _=fs::write(root.join(p),bytes);}}return Err(error)}changed.push(p)}Ok(preview)
}
pub fn import_case(root:&Path,text:&str)->Result<BundlePreview,String>{
 let b=parse(text)?;let preview=validate(&b)?;if !preview.valid{return Err(preview.errors.join("; "))}if b.format!="atmavictu-case-bundle-v1"{return Err("Expected case bundle".into())}
 let reg=b.files.iter().find(|f|f.path=="REGISTER-PREVERJANJ.jsonl").ok_or("Case event register missing")?;let frag=b.files.iter().find(|f|f.path=="case-manifest-fragment.json").ok_or("Source manifest fragment missing")?;let frag:Value=serde_json::from_str(&frag.content).map_err(|e|e.to_string())?;
 let rp=root.join("REGISTER-PREVERJANJ.jsonl");let mp=root.join("book.workbench.json");let sp=root.join("book.workbench.seal.json");let oldr=fs::read(&rp).ok();let oldm=fs::read(&mp).ok();let olds=fs::read(&sp).ok();let old_text=oldr.as_ref().map(|b|String::from_utf8_lossy(b).into_owned()).unwrap_or_default();let mut existing_cases=HashSet::new();for l in old_text.lines(){if let Ok(v)=serde_json::from_str::<Value>(l){if let Some(id)=v["case_event"]["caseId"].as_str(){existing_cases.insert(id.to_owned());}}}
 let rows=reg.content.lines().filter(|l|!l.trim().is_empty()).map(|l|serde_json::from_str::<Value>(l).map_err(|e|e.to_string())).collect::<Result<Vec<_>,_>>()?;for row in &rows{let id=row["case_event"]["caseId"].as_str().ok_or("Case ID missing")?;if existing_cases.contains(id){return Err(format!("Case {id} already exists"))}}
 let mut manifest:Value=match &oldm{Some(bytes)=>serde_json::from_slice(bytes).map_err(|e|e.to_string())?,None=>json!({"manifestVersion":"2","incomingTexts":[],"fragments":[],"insertions":[],"concepts":[]})};let entries=manifest["incomingTexts"].as_array_mut().ok_or("incomingTexts missing")?;let mut ids=entries.iter().filter_map(|e|e["id"].as_str().map(str::to_owned)).collect::<HashSet<_>>();let source_map=b.files.iter().map(|f|(f.path.as_str(),f)).collect::<HashMap<_,_>>();let mut sources=Vec::new();
 for mut e in frag["incomingTexts"].as_array().ok_or("Bundle sources missing")?.clone(){let id=e["id"].as_str().ok_or("source id missing")?.to_owned();let path=e["sourcePath"].as_str().ok_or("sourcePath missing")?.to_owned();if !ids.insert(id.clone()){return Err(format!("Source ID collision: {id}"))}let rel=safe(&path)?;let f=source_map.get(path.as_str()).ok_or("Source bytes missing")?;if root.join(&rel).exists(){return Err(format!("Source path collision: {path}"))}e["status"]=Value::String("new".into());sources.push((rel,f.content.clone()));entries.push(e)}
 let pretty=format!("{}\n",serde_json::to_string_pretty(&manifest).map_err(|e|e.to_string())?);let compact=serde_json::to_string(&manifest).map_err(|e|e.to_string())?;let seal=json!({"manifestPath":mp.to_string_lossy(),"manifestSha256":sha(compact.as_bytes()),"receipts":{"manifest":true,"seal":true,"cli":false,"ci":false},"clock":{"sealedAt":chrono::Utc::now().to_rfc3339_opts(chrono::SecondsFormat::Millis,true),"receivedAt":null,"ci":false,"cli":false}});let mut written=Vec::new();
 let transaction=(||->Result<(),String>{for(rel,body)in &sources{let dest=root.join(rel);if let Some(parent)=dest.parent(){fs::create_dir_all(parent).map_err(|e|e.to_string())?}fs::write(&dest,body).map_err(|e|e.to_string())?;written.push(rel.clone())}fs::write(&mp,pretty).map_err(|e|e.to_string())?;fs::write(&sp,format!("{}\n",serde_json::to_string_pretty(&seal).map_err(|e|e.to_string())?)).map_err(|e|e.to_string())?;let mut output=OpenOptions::new().create(true).append(true).open(&rp).map_err(|e|e.to_string())?;for row in &rows{writeln!(output,"{row}").map_err(|e|e.to_string())?}Ok(())})();
 if let Err(error)=transaction{for p in written{let _=fs::remove_file(root.join(p));}restore_bytes(&rp,oldr);restore_bytes(&mp,oldm);restore_bytes(&sp,olds);return Err(error)}Ok(preview)
}
fn restore_bytes(path:&Path,bytes:Option<Vec<u8>>){match bytes{Some(bytes)=>{let _=fs::write(path,bytes);},None=>{let _=fs::remove_file(path);}}}
pub fn preview_text(text:&str)->Result<BundlePreview,String>{let b:ProjectBundle=serde_json::from_str(text).map_err(|e|e.to_string())?;validate(&b)}
pub fn preview_file(path:&Path)->Result<BundlePreview,String>{preview_text(&fs::read_to_string(path).map_err(|e|e.to_string())?)}
fn validate(bundle:&ProjectBundle)->Result<BundlePreview,String>{
 let mut errors=Vec::new();if !bundle.format.ends_with("-bundle-v1"){errors.push("Unsupported bundle format".into())}let mut blank=bundle.clone();blank.sha256.clear();let value=serde_json::to_value(blank).map_err(|e|e.to_string())?;if bundle.sha256!=sha(serde_json::to_string(&canonical(&value)).map_err(|e|e.to_string())?.as_bytes()){errors.push("Bundle hash mismatch".into())}let mut paths=HashSet::new();for f in &bundle.files{if safe(&f.path).is_err(){errors.push(format!("Unsafe path {}",f.path))}if !paths.insert(f.path.clone()){errors.push(format!("Duplicate path {}",f.path))}if sha(f.content.as_bytes())!=f.sha256{errors.push(format!("File hash mismatch {}",f.path))}}
 let mut cases:HashMap<String,Vec<CaseEvent>>=HashMap::new();if let Some(reg)=bundle.files.iter().find(|f|f.path=="REGISTER-PREVERJANJ.jsonl"){for(i,line)in reg.content.lines().enumerate(){if line.trim().is_empty(){continue}let row:Value=match serde_json::from_str(line){Ok(v)=>v,Err(e)=>{errors.push(format!("Invalid register line {}: {e}",i+1));continue}};if let Some(v)=row.get("case_event"){match serde_json::from_value::<CaseEvent>(v.clone()){Ok(e)=>cases.entry(e.case_id.clone()).or_default().push(e),Err(e)=>errors.push(format!("Invalid event {}: {e}",i+1))}}}}
 for(id,events)in &cases{let mut previous=None;for(i,e)in events.iter().enumerate(){if e.sequence!=i as u64+1||e.previous_hash!=previous||e.hash!=hash_event(e){errors.push(format!("Broken case chain {id}"))}previous=Some(e.hash.clone())}}let mut ids=cases.keys().cloned().collect::<Vec<_>>();ids.sort();Ok(BundlePreview{format:bundle.format.clone(),valid:errors.is_empty(),errors,file_count:bundle.files.len(),case_count:cases.len(),case_ids:ids})
}

#[cfg(test)]
mod bundle_tests {
    use super::*;
    include!("local_bundles.test.rs");
}
