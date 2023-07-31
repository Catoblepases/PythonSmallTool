const { suggestpromt, update, autoprop } =
  this.app.plugins.plugins["metaedit"].api;

const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;

const { createButton } = app.plugins.plugins["buttons"];

const header =
  "---\ntitle: \ndate created: \ndate modified:\nType:\nSubject: \nTicks:\nTime Period: \n\nStatus: In Progress\n---\n```dataviewjs\n";

const TEMPLATE =
  'const { suggestpromt, update, autoprop } = this.app.plugins.plugins["metaedit"].api;const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;const { createButton } = app.plugins.plugins["buttons"];const foldername = "';

const TEMPLATE2 =
  '";const TEMPLATE = "---\\ntitle: \\ndate created: \\ndate modified:\\naliases: []\\n---\\n";const addplan = async (file, key) => { const newtext = await inputPrompt("note name"); await this.app.vault.create(foldername + "/" + newtext + ".md", TEMPLATE); await update(key, newtext, file);};const views = ["ALL", "close"];const changeView = (viewName) => { removeView(); if (viewName == "ALL") { dv.table( ["Name", "date"], dv .pages(`"Sources"`) .sort((t) => t.priority) .where((t) => t.file.folder.contains(foldername)) .map((t) => [t.file.link, t.file.cday]) ); }};const createButtons = () => { const buttonContainer = dv.el("div", "", { cls: "tabButtons" }); const button2 = dv.el("button", "+"); button2.addEventListener("click", (event) => { event.preventDefault(); addplan(); }); buttonContainer.append(button2); views.forEach((view) => { const button = dv.el("button", view); button.addEventListener("click", (event) => { event.preventDefault(); changeView(view); }); buttonContainer.append(button); }); changeView("ALL");};const removeView = () => { Array.from(this.container.children).forEach((el) => { if (!el.classList.contains("tabButtons")) { el.remove(); } });};createButtons();';

const footer = "\n```";
const sizeOfDays = "8px";

const emptyColor = "rgba(208, 78, 78, 0.5)";

// ---------------------------Button Setting---------------------------

const addplan = async (file, key) => {
  const newtext = await inputPrompt("in Which folder");

  if (newtext != undefined) {
    await this.app.vault.createFolder("Sources/Notes/" + newtext + "/");
  }

  const planName = await inputPrompt("addPlan");

  await this.app.vault.create(
    "Sources/Plannings/" + planName + ".md",

    header + TEMPLATE + "Sources/Notes/" + newtext + TEMPLATE2 + footer
  );

  await update(key, newtext, file);
};

const addplans = async (file, key) => {
  const newtext = await inputPrompt("in Which folder");

  const planName = await inputPrompt("addPlan");

  await this.app.vault.create(
    "Sources/Plannings/" + planName + ".md",

    header + TEMPLATE + "Sources/Notes/" + newtext + TEMPLATE2 + footer
  );

  await update(key, newtext, file);
};

const addplanquick = async (file, key) => {
  const newtext = "Archive";

  const planName = await inputPrompt("addPlan");

  await this.app.vault.create(
    "Sources/Plannings/" + planName + ".md",

    header + TEMPLATE + "Sources/Notes/" + newtext + TEMPLATE2 + footer
  );

  await update(key, newtext, file);
};

const dropdown = async (file, key) => {
  const newtext = await autoprop("Project");

  await update(key, newtext, file);
};

const dropdown1 = async (file, key) => {
  const newtext = await autoprop("Subject");

  await update(key, newtext, file);
};

// ---------------------------View---------------------------

const views = ["Current Plan", "ALL", "x"];

const changeView = (viewName) => {
  removeView();

  if (viewName == "Current Plan") {
    dv.table(
      ["Name", "Subject", "Actions"],

      dv

        .pages(`"Sources/Plannings"`)

        .sort((t) => t.priority)

        .where((t) => t.status == "In Progress")

        .map((t) => [
          t.file.link,

          createButton({
            app,

            el: this.container,

            args: { name: t.Subject, class: "tiny" },

            clickOverride: {
              click: dropdown1,

              params: [t.file.path, "Subject"],
            },
          }),

          createButton({
            app,

            el: this.container,

            args: { name: t.Status, class: "tiny" },

            clickOverride: { click: dropdown, params: [t.file.path, "Status"] },
          }),
        ])
    );
  }

  if (viewName == "ALL") {
    dv.table(
      ["Name", "Subject", "Actions"],

      dv

        .pages(`"Sources/Plannings"`)

        .sort((t) => t.file.cday, "desc")

        .where((p) => p.file.folder == "Sources/Plannings")

        .map((t) => [
          t.file.link,

          createButton({
            app,

            el: this.container,

            args: { name: t.Subject, class: "tiny" },

            clickOverride: {
              click: dropdown1,

              params: [t.file.path, "Subject"],
            },
          }),

          createButton({
            app,

            el: this.container,

            args: { name: t.Status, class: "tiny" },

            clickOverride: { click: dropdown, params: [t.file.path, "Status"] },
          }),
        ])
    );
  }
};



const createtooltip = (hoverInfo) => {
  return `<span style="width:${sizeOfDays};height:${sizeOfDays};border-radius:2px;background-color:${emptyColor};display:inline-block;font-size:4pt;" title="${hoverInfo}"></span>`;
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

  const button3 = dv.el("button", createtooltip("quick add to Inbox"));

  button3.addEventListener("click", (event) => {
    event.preventDefault();

    addplanquick();
  });

  buttonContainer.append(button3);

  const button4 = dv.el("button", createtooltip("without folder"));

  button4.addEventListener("click", (event) => {
    event.preventDefault();

    addplans();
  });

  buttonContainer.append(button4);

  changeView("Current Plan");
};

const removeView = () => {
  Array.from(this.container.children).forEach((el) => {
    if (!el.classList.contains("tabButtons")) {
      el.remove();
    }
  });
};

createButtons();
