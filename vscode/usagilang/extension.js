"use strict";
const vscode = require("vscode");

async function runCurrentFile(action) {
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.languageId !== "usagilang") {
    vscode.window.showWarningMessage("Open a .usagi file first.");
    return;
  }
  await editor.document.save();
  const cliPath = vscode.workspace.getConfiguration("usagilang").get("cliPath", "usagi");
  const folder = vscode.workspace.getWorkspaceFolder(editor.document.uri);
  const task = new vscode.Task(
    {type:"usagilang",task:action,file:editor.document.uri.fsPath},
    folder || vscode.TaskScope.Workspace,
    "UsagiLang: " + action,
    "UsagiLang",
    new vscode.ShellExecution(cliPath, [action, editor.document.uri.fsPath])
  );
  task.presentationOptions = {reveal:vscode.TaskRevealKind.Always, panel:vscode.TaskPanelKind.Shared};
  await vscode.tasks.executeTask(task);
}

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand("usagilang.runFile", () => runCurrentFile("run")));
  context.subscriptions.push(vscode.commands.registerCommand("usagilang.checkFile", () => runCurrentFile("check")));
  const keywords = [
    "プルャ","ウラ","ハァ","フゥン","プルルルル","ツツウラウラ",
    "ウララヤハ","ウラララ","インポート","クラス","ためす","つかまえる",
    "가져와","푸루야","우라","클래스","시도","잡기",
    "import","as","class","try","catch","throw","func","return",
    "math","text","random","clock","append","pop"
  ];
  context.subscriptions.push(vscode.languages.registerCompletionItemProvider("usagilang", {
    provideCompletionItems() {
      return keywords.map(word => new vscode.CompletionItem(word, vscode.CompletionItemKind.Keyword));
    }
  }));
}

function deactivate() {}
module.exports = {activate, deactivate};
