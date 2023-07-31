const values = dv.pages('"10 Example Data/projects"').where(p => p.started);
const year = 2022;
const emptyColor = "rgba(255,255,255,0.1)";

// == Fill data ==
let date = dv.luxon.DateTime.utc(year)
const calendar = [];
for(let i = 1; i <= 12; i++) {
	calendar[i] = []
}

while (date.year == year) {
	calendar[date.month].push(getDayEl(date, determineColor(date), createTooltip()))

	date = addOneDay(date);
	
	function createTooltip() {
		let tooltip = "";
		const vals = values.filter(p => checkDateEq(p.started, date) || checkDateEq(p.finished, date))
		for (let val of vals) {
			tooltip += `${val.file.name} `
		}
		return tooltip;
	}
}

// == Render calendar ==
calendar.forEach((month, i) => {
	const monthEl = `<span style='display:inline-block;min-width:30px;font-size:small'>${dv.luxon.DateTime.utc(year, i).toFormat('MMM')}</span>`
	
	dv.el("div", monthEl + month.reduce((acc, curr) => `${acc} ${curr}`, ""))
})

function addOneDay(date) {
	return dv.luxon.DateTime.fromMillis(date + dv.duration("1d"))
}
function getDayEl(date, color, hoverInfo) {
	const sizeOfDays = "12px";
	return `<span style="width:${sizeOfDays};height:${sizeOfDays};border-radius:2px;background-color:${color};display:inline-block;font-size:4pt;" title="${hoverInfo}"></span>`
}

function checkDateEq(date1, date2) {
	if (!date1 || !date2) return false
	return date1.startOf('day').equals(date2.startOf('day'))
}

function determineColor(date) {
	const started = values.find(p => p.started?.startOf('day').equals(date.startOf('day')));
	const finished = values.find(p => p.finished?.startOf('day').equals(date.startOf('day')));
	let color = emptyColor;

	if (started && finished) {
		color = '#9959ff';	
	} else if (started) {
		color = '#ff5976'
	} else if (finished) {
		color = 'green'
	}
	
	return color;
}