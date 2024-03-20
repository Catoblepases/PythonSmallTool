const year = dv.date("today").year;
const values = dv.pages('"Sources"').where((d) => d.file.cday.year == year);
const emptyColor = "rgba(178, 78, 0, 0.1)";

// == Fill data ==
let date = dv.luxon.DateTime.utc(year);
const calendar = [];
for (let i = 1; i <= 12; i++) {
  calendar[i] = [];
}

let dict_color = initiateColor();

while (date.year == year) {
  calendar[date.month].push(getDayEl(date, determineColor(dict_color, date)));
  date = addOneDay(date);
}

// == Render calendar ==
calendar.forEach((month, i) => {
  const monthEl = `<span style='display:inline-block;min-width:30px;font-size:small'>${dv.luxon.DateTime.utc(
    year,
    i
  ).toFormat("MMM")}</span>`;

  dv.el("div", monthEl + month.reduce((acc, curr) => `${acc} ${curr}`, ""));
});

function addOneDay(date) {
  return dv.luxon.DateTime.fromMillis(date + dv.duration("1d"));
}

function getDayEl(date, color) {
  const sizeOfDays = "12px";
  return `<span style="width:${sizeOfDays};height:${sizeOfDays};border-radius:2px;background-color:${color};display:inline-block;font-size:4pt;" title="${date.toFormat(
    "yyyy-MM-dd"
  )}"></span>`;
}

function determineColor(date) {
  const page = values.where((p) =>
    p.file.cday.startOf("day").equals(date.startOf("day"))
  );
  if (page.length == 0) return emptyColor;

  let opacity = page.length / 3;
  return `rgba(178, 78, 0, ${opacity})`;
}

function initiateColor() {
  var dict = {};

  values.forEach((p) => {
    var date = p.file.cday.startOf("day");
    if (dict[date] == undefined) {
      dict[date] = 1;
    } else {
      dict[date] += 1;
    }
  });

  var dict_color = {};

  for (const [key, value] of Object.entries(dict)) {
    let opacity = value / 3;
    dict_color[key] = `rgba(178, 78, 0, ${opacity})`;
  }
  return dict_color;
}

function determineColor(dict_color, date) {
  if (dict_color[date.startOf('day')] == undefined) {
    return emptyColor;
  }

  return dict_color[date.startOf('day')];
}
