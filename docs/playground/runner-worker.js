"use strict";
const PYODIDE_VERSION="0.27.7";
const BASE="https://cdn.jsdelivr.net/pyodide/v"+PYODIDE_VERSION+"/full/";
let pyodide;
const python=String.raw`
import io,sys,json
from usagilang import Interpreter,Parser,tokenize,UsagiError,diagnostic

def execute_usagi(source, input_text, mode):
    output=io.StringIO()
    if mode == "check":
        try:
            Parser(tokenize(source)).parse()
            return json.dumps({"ok":True,"output":"🐰 문법 검사 통과!"},ensure_ascii=False)
        except UsagiError as exc:
            return json.dumps({"ok":False,"output":diagnostic(exc,source,"main.usagi")},ensure_ascii=False)
    try:
        runner=Interpreter(stdin=io.StringIO(input_text + ("\\n" if input_text and not input_text.endswith("\\n") else "")),stdout=output,max_steps=20000)
        runner.run(source,source_path="/home/pyodide/main.usagi")
        return json.dumps({"ok":True,"output":output.getvalue()[:150000]},ensure_ascii=False)
    except UsagiError as exc:
        return json.dumps({"ok":False,"output":(output.getvalue()+diagnostic(exc,source,"main.usagi"))[:150000]},ensure_ascii=False)
    except RecursionError:
        return json.dumps({"ok":False,"output":(output.getvalue()+"🐰 [E900] 재귀 호출이 너무 깊어요.")[:150000]},ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"ok":False,"output":(output.getvalue()+"실행 오류: "+str(exc))[:150000]},ensure_ascii=False)
`;
async function start(){
 try{
  importScripts(BASE+"pyodide.js");
  pyodide=await loadPyodide({indexURL:BASE});
  const response=await fetch("./usagilang.py",{cache:"no-cache"});
  if(!response.ok)throw Error("usagilang.py 로드 실패: HTTP "+response.status);
  pyodide.FS.writeFile("/home/pyodide/usagilang.py",await response.text(),{encoding:"utf8"});
  pyodide.runPython(python);
  postMessage({type:"ready"});
 }catch(error){postMessage({type:"fatal",error:String(error)})}
}
self.onmessage=async ({data:m})=>{
 if(m.type!=="execute"||!pyodide)return;
 try{
  pyodide.globals.set("_usagi_source",m.source);
  pyodide.globals.set("_usagi_input",m.input||"");
  pyodide.globals.set("_usagi_mode",m.mode);
  const json=pyodide.runPython("execute_usagi(_usagi_source, _usagi_input, _usagi_mode)");
  postMessage({type:"result",id:m.id,...JSON.parse(json)});
 }catch(error){postMessage({type:"result",id:m.id,ok:false,output:String(error)})}
};
start();