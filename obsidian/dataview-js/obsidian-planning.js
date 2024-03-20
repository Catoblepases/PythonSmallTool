const { suggestpromt, update, autoprop } =
	this.app.plugins.plugins['metaedit'].api;
const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;
const { createButton } = app.plugins.plugins['buttons'];
const header =
	'---\ntitle: \ndate created: \ndate modified:\nType:\nSubject: \nTicks:\nTime Period: \n\nStatus: In Progress\n---\n```dataviewjs\n';
const TEMPLATE =
	'const { suggestpromt, update, autoprop } = this.app.plugins.plugins["metaedit"].api;const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;const { createButton } = app.plugins.plugins["buttons"];const foldername = "';
const TEMPLATE2 =
	'";const TEMPLATE = "---\\ntitle: \\ndate created: \\ndate modified:\\naliases: []\\n---\\n";const addplan = async (file, key) => { const newtext = await inputPrompt("note name"); await this.app.vault.create(foldername + "/" + newtext + ".md", TEMPLATE); await update(key, newtext, file);};const views = ["ALL", "✖"];const changeView = (viewName) => { removeView(); if (viewName == "ALL") { dv.table( ["Name", "date"], dv .pages(`"Sources"`) .sort((t) => t.priority) .where((t) => t.file.folder.contains(foldername)) .map((t) => [t.file.link, t.file.cday]) ); }};const createButtons = () => { const buttonContainer = dv.el("div", "", { cls: "tabButtons" }); const button2 = dv.el("button", "﹢"); button2.addEventListener("click", (event) => { event.preventDefault(); addplan(); }); buttonContainer.append(button2); views.forEach((view) => { const button = dv.el("button", view); button.addEventListener("click", (event) => { event.preventDefault(); changeView(view); }); buttonContainer.append(button); });};const removeView = () => { Array.from(this.container.children).forEach((el) => { if (!el.classList.contains("tabButtons")) { el.remove(); } });};createButtons();';
const footer = '\n```';
const sizeOfDays = '8px';
const emptyColor = 'rgba(208, 78, 78, 0.5)';
let edit_menu = dv.page('Sources/Organization/Planning Databse.md');
const createplan = async (key, folder_name, file) => {
	const planName = await inputPrompt('addPlan');
	await this.app.vault.create(
		'Sources/Plannings/' + planName + '.md',
		header + TEMPLATE + 'Sources/Notes/' + folder_name + TEMPLATE2 + footer,
	);
	await update(key, folder_name, file);
};
const addplan = async (file, key) => {
	const folder_name = await inputPrompt('Create a folder');
	if (folder_name != undefined) {
		await this.app.vault.createFolder('Sources/Notes/' + folder_name + '/');
	} else {
		return false;
	}
	await createplan(key, folder_name, file);
};
const addPlanToExistingFolder = async (file, key) => {
	const folder_name = await inputPrompt('add in Which folder');
	if (folder_name == undefined) {
		return false;
	}
	await createplan(key, folder_name, file);
};
const addPlanToInbox = async (file, key) => {
	const folder_name = 'Archive';
	await createplan(key, folder_name, file);
};
const planningEditMenu = async (file, key) => {
	const folder_name = 'Archive';
	await createplan(key, folder_name, file);
};
const dropdown = async (file, key) => {
	const newtext = await autoprop('Project');
	await update(key, newtext, file);
};
const dropdown1 = async (file, key) => {
	const newtext = await autoprop('Subject');
	await update(key, newtext, file);
};
const dropdown2 = async (file, key) => {
	const newtext = await autoprop('Type');
	await update(key, newtext, file);
};
const views = ['★', 'Current', '✖'];
const changeView = (viewName) => {
	removeView();
	if (viewName == 'Current') {
		dv.table(
			['Name', 'Subject', 'Actions', 'Type'],
			dv
				.pages(`"Sources/Plannings"`)
				.where((t) => t.status == 'In Progress')
				.sort((t) => t.file.cday, 'desc')
				.map((t) => [
					t.file.link,
					createButton({
						app,
						el: this.container,
						args: { name: t.Subject, class: 'tiny' },
						clickOverride: {
							click: dropdown1,
							params: [t.file.path, 'Subject'],
						},
					}),
					createButton({
						app,
						el: this.container,
						args: { name: t.Status, class: 'tiny' },
						clickOverride: { click: dropdown, params: [t.file.path, 'Status'] },
					}),
					createButton({
						app,
						el: this.container,
						args: { name: t.Type, class: 'tiny' },
						clickOverride: { click: dropdown2, params: [t.file.path, 'Type'] },
					}),
				]),
		);
	}
	if (viewName == '★') {
		dv.table(
			['Name', 'Subject', 'Actions', 'Type'],
			dv
				.pages(`"Sources/Plannings"`)
				.sort((t) => t.file.cday, 'desc')
				.where(
					(t) =>
						(t.file.folder == 'Sources/Plannings') &
						t.star &
						(t.status == 'In Progress'),
				)
				.map((t) => [
					t.file.link,
					createButton({
						app,
						el: this.container,
						args: { name: t.Subject, class: 'tiny' },
						clickOverride: {
							click: dropdown1,
							params: [t.file.path, 'Subject'],
						},
					}),
					createButton({
						app,
						el: this.container,
						args: { name: t.Status, class: 'tiny' },
						clickOverride: { click: dropdown, params: [t.file.path, 'Status'] },
					}),
					createButton({
						app,
						el: this.container,
						args: { name: t.Type, class: 'tiny' },
						clickOverride: { click: dropdown2, params: [t.file.path, 'Type'] },
					}),
				]),
		);
	}
};
const createtooltip = (hoverInfo) => {
	return `<span style="width:${sizeOfDays};height:${sizeOfDays};border-radius:2px;background-color:${emptyColor};display:inline-block;font-size:4pt;" title="${hoverInfo}"></span>`;
};
const createButtons = () => {
	const buttonContainer = dv.el('div', '', { cls: 'tabButtons' });
	const button2 = dv.el('button', '﹢');
	button2.addEventListener('click', (event) => {
		event.preventDefault();
		addplan();
	});
	buttonContainer.append(button2);
	views.forEach((view) => {
		const button = dv.el('button', view);
		button.addEventListener('click', (event) => {
			event.preventDefault();
			changeView(view);
		});
		buttonContainer.append(button);
	});
	const button3 = dv.el('button', createtooltip('Quick add to Inbox'));
	button3.addEventListener('click', (event) => {
		event.preventDefault();
		addPlanToInbox();
	});
	buttonContainer.append(button3);
	const button4 = dv.el('button', createtooltip('In an existing folder'));
	button4.addEventListener('click', (event) => {
		event.preventDefault();
		addPlanToExistingFolder();
	});
	buttonContainer.append(button4);
	changeView('★');
};
const removeView = () => {
	Array.from(this.container.children).forEach((el) => {
		if (!el.classList.contains('tabButtons')) {
			el.remove();
		}
	});
};
createButtons();
