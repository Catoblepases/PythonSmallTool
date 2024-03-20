// define pages

const pages = dv
  .pages('""')
  .filter(
    (p) =>
      p.file.folder == "Extras/Calendar/DailyNotes" ||
      p.file.folder == "Sources/DeadLine"
  );

// OPEN TASKS

const tasks = pages.file.tasks.where((t) => !t.completed && !t.quit);

const priorityColorMap = {
  low: "rgb(55 166 155)",
  medium: "orange",
  high: "red",
};

// regex to remove the field priority in text

const regex = /\[priority[^\]]+\]/g;

// assign colors according to priority

for (let task of tasks) {
  task.visual = getColorCode(task.priority) + task.text.replace(regex, "");
}

// render open tasks

const order = Object.keys(priorityColorMap);

// COMPLETED TASKS

const done = pages.file.tasks.where((t) => t.completed);

function getColorCode(priority) {
  const color = priorityColorMap[priority] ?? "grey";

  return `<span style='border-left: 3px solid ${color};'>&nbsp;</span>`;
}

//----------------------

const views = [
  "clean",
  "All",
  "By date",
  "By file",
  "Today",
  "Progress",
  "quit",
  "close",
];

const changeView = (viewName) => {
  removeView();

  if (viewName == "clean") {
    dv.taskList(
      tasks.sort(
        (a, b) => order.indexOf(b.priority) - order.indexOf(a.priority)
      ),
      false
    );
  }

  if (viewName == "All") {
    dv.taskList(
      tasks.sort(
        (a, b) => order.indexOf(b.priority) - order.indexOf(a.priority)
      ),
      false
    );

    // render completed tasks and add a limit to the number of the listed tasks (sorted by the completion date - need to activate auto-completion in dataview settings)

    if (done.length >= 1) {
      dv.taskList(done.sort((t) => t.completion, "desc").limit(5), false);
    }

    // change opacity of completed tasks

    this.container
      .querySelectorAll("li.task-list-item.is-checked")
      .forEach((s) => (s.style.opacity = "30%"));
  }

  if (viewName == "By date") {
    dv.taskList(tasks);
  }

  if (viewName == "By file") {
    dv.taskList(dv.pages().file.tasks.where((t) => !t.completed));
  }

  if (viewName == "Today") {
    dv.taskList(
      tasks.where((t) => t.due && t.due.ts == dv.date("today").ts),
      false
    );
  }

  if (viewName == "quit") {
    dv.taskList(dv.pages().file.tasks.where((t) => !t.completed && t.quit));
  }
};

const createButtons = () => {
  const buttonContainer = dv.el("div", "", { cls: "tabButtons" });

  views.forEach((view) => {
    const button = dv.el("button", view);

    button.addEventListener("click", (event) => {
      event.preventDefault();

      changeView(view);
    });

    buttonContainer.append(button);
  });

  changeView("clean");
};

const removeView = () => {
  Array.from(this.container.children).forEach((el) => {
    if (!el.classList.contains("tabButtons")) {
      el.remove();
    }
  });
};

createButtons();
