const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;
const { createButton } = this.app.plugins.plugins["buttons"];

const TEMPLATE =
  '---\ntitle: \ndate created: \ndate modified:\nType:\nSubject: \nTicks:\nTime Period: \n\nStatus: In Progress\n---\n```button\nname ➕ note\ntype command\naction QuickAdd: addMA210\nclass blank\n```\n> [!note]- All notes\n> ```dataview\n> table from "Sources/Notes/German A1"\n> ```';

const newtext="TESTEST"
const addplan = async (file, key) => {
  const name = await inputPrompt("addFile");
  await this.app.vault.create(
    "Sources/Notes/" + newtext + "/" + name + ".md",
    "test"
  );
  await update(key, newtext, file);
};


const createButtons = () => {
  const buttonContainer = dv.el("div", "", { cls: "tabButtons" });
  const button2 = dv.el("button", "add");

  button2.addEventListener("click", (event) => {
    event.preventDefault();
    addplan();
  });

  buttonContainer.append(button2);
};

createButtons();
