#!/usr/bin/env python3
"""Organize Java screenshot folders into the simple practice website."""
import argparse, json, re, shutil
from pathlib import Path

IMAGE_EXTS={".png",".jpg",".jpeg",".webp",".bmp",".gif"}
ALIASES={
"basic programming":["basic programming","basic prgraming","basic programming"],
"exception":["exception","exception handling"],
"functions":["functions","function"],
"inheritance":["inheritance"],
"input output":["input output","input/output","input-output"],
"interface":["interface","interfaces"],
"multi array":["multi array","multi-array","multi dimention array","multi dimensional array"],
"multithreading":["multithreading","multi threading","multithread"],
"oops":["oops","oop","oops"],
"packages":["packages","package"],
"single array":["single array","single dimention array","single dimension array","single dimension array"],
"strings":["strings","string"]
}
def norm(s): return re.sub(r'[^a-z0-9]+','',s.lower())
def main():
 p=argparse.ArgumentParser()
 p.add_argument("screenshots",help="Main folder containing the category folders")
 p.add_argument("--output",default=".",help="Website folder to generate into (default: current folder)")
 a=p.parse_args()
 root=Path(a.screenshots).expanduser().resolve(); out=Path(a.output).resolve()
 if not root.is_dir(): raise SystemExit(f"Screenshot folder not found: {root}")
 data=json.loads((Path(__file__).resolve().parents[1]/"questions.json").read_text(encoding="utf-8"))
 dirs=[x for x in root.iterdir() if x.is_dir()]
 all_programs=[]; report=["category,question,title,code_file,output_file,status"]
 image_dir=out/"screenshots"
 if image_dir.exists(): shutil.rmtree(image_dir)
 image_dir.mkdir(parents=True,exist_ok=True)
 for category,titles in data.items():
  aliases=ALIASES.get(norm(category),[category.lower()])
  matches=[d for d in dirs if norm(d.name) in {norm(x) for x in aliases}]
  if not matches:
   print(f"Warning: no folder found for {category}")
   continue
  src=matches[0]
  files=[f for f in src.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTS]
  pairs={}
  for f in files:
   stem=f.stem
   m=re.match(r'^(.*?)(?:[_\-\s.]*(code|output|out))$',stem,re.I)
   if not m: continue
   key=m.group(1).strip(" _-.")
   role="output" if m.group(2).lower() in ("output","out") else "code"
   pairs.setdefault(key,{})[role]=f
  def sortkey(item):
   return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)',item[0])]
  for idx,(key,pair) in enumerate(sorted(pairs.items(),key=sortkey),1):
   code=pair.get("code"); output=pair.get("output")
   title=titles[idx-1] if idx<=len(titles) else f"Question {idx}"
   destcat=image_dir/norm(category); destcat.mkdir(parents=True,exist_ok=True)
   cpath=opath=""
   if code:
    target=destcat/f"{idx:03d}-code{code.suffix.lower()}"; shutil.copy2(code,target); cpath=target.relative_to(out).as_posix()
   if output:
    target=destcat/f"{idx:03d}-output{output.suffix.lower()}"; shutil.copy2(output,target); opath=target.relative_to(out).as_posix()
   status="OK" if code and output else ("missing code" if not code else "missing output")
   report.append(f'"{category}",{idx},"{title.replace(chr(34), chr(39))}","{code.name if code else ""}","{output.name if output else ""}",{status}')
   all_programs.append({"category":category,"number":idx,"title":title,"code":cpath,"output":opath})
 (out/"programs.js").write_text("window.JAVA_PROGRAMS = "+json.dumps(all_programs,ensure_ascii=False,indent=2)+";\n",encoding="utf-8")
 (out/"pairing-review.csv").write_text("\n".join(report),encoding="utf-8-sig")
 print(f"Created {len(all_programs)} program entries. Review pairing-review.csv for missing screenshot pairs.")
if __name__=="__main__": main()
