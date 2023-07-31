const { suggestpromt, update, autoprop } =
  this.app.plugins.plugins["metaedit"].api;
const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;
const { createButton } = app.plugins.plugins["buttons"];

const foldername = "Sources/Notes/Archive";

const TEMPLATE =
  "---\ntitle: \ndate created: \ndate modified:\naliases: []\n---\n";

const addplan = async (file, key) => {
  const newtext = await inputPrompt("note name");
  await this.app.vault.create(foldername + "/" + newtext + ".md", TEMPLATE);
  await update(key, newtext, file);
};

const views = ["ALL", "close"];

const changeView = (viewName) => {
  removeView();
  if (viewName == "ALL") {
    dv.table(
      ["Name", "date"],
      dv
        .pages(`"Sources"`)
        .sort((t) => t.priority)
        .where((t) => t.file.folder.contains(foldername))
        .map((t) => [t.file.link, t.file.cday])
    );
  }
};

const createButtons = () => {
  const buttonContainer = dv.el("div", "", { cls: "tabButtons" });

  const button2 = dv.el("button", "+");

  button2.addEventListener("click", (event) => {
    event.preventDefault();

    addplan();
  });

  buttonContainer.append(button2);

  views.forEach((view) => {
    const button = dv.el("button", view);
    button.addEventListener("click", (event) => {
      event.preventDefault();
      changeView(view);
    });

    buttonContainer.append(button);
  });

  changeView("ALL");
};

const removeView = () => {
  Array.from(this.container.children).forEach((el) => {
    if (!el.classList.contains("tabButtons")) {
      el.remove();
    }
  });
};

createButtons();