const { executeChoice, inputPrompt } = this.app.plugins.plugins.quickadd.api;
const { createButton } = app.plugins.plugins['buttons'];
const pages = dv.pages('"Sources/Informations"');
const views = ['Extracts', 'Websites', 'Simpread', 'Books', 'close'];
const changeView = (viewName) => {
	removeView();
	if (viewName == 'Websites') {
		dv.table(
			['name'],
			dv
				.pages('"Sources/Informations/Websites"')
				.sort((t) => t.file.ctime, 'desc')
				.map((t) => [t.file.link]),
		);
	}
	if (viewName == 'Simpread') {
		dv.table(
			['name'],
			dv
				.pages('"Sources/Informations/SimpRead"')
				.sort((t) => t.file.ctime, 'desc')
				.map((t) => [t.file.link]),
		);
	}
	if (viewName == 'Books') {
		dv.table(
			['name'],
			pages
				.where(
					(t) =>
						t.file.folder.contains('Kindle') || t.file.folder.contains('ibook'),
				)
				.sort((t) => t.file.date-saved, 'desc')
				.map((t) => [t.file.link]),
		);
	}
	if (viewName == 'Extracts') {
		dv.table(
			['name', 'author'],
			pages
				.where((t) => t.file.folder.contains('Extracts')|| t.file.folder.contains('Omnivore'))
				.sort((t) => t.file.ctime, 'desc')
				.map((t) => [t.file.link, t.author]),
		);
	}
};
const createButtons = () => {
	const buttonContainer = dv.el('div', '', { cls: 'tabButtons' });
	const button2 = dv.el('button', '﹢');
	const button3 = dv.el('button', 'x');
	const addWebsite = async (file, key) => {
		const planName = await executeChoice('addWebsite');
		await update(key, newtext, file);
	};
	const addExtracts = async (file, key) => {
		const planName = await executeChoice('addExtract');
		await update(key, newtext, file);
	};
	button2.addEventListener('click', (event) => {
		event.preventDefault();
		addExtracts();
	});
	button3.addEventListener('click', (event) => {
		event.preventDefault();
		addWebsite();
	});
	buttonContainer.append(button2);
	buttonContainer.append(button3);
	views.forEach((view) => {
		const button = dv.el('button', view);
		button.addEventListener('click', (event) => {
			event.preventDefault();
			changeView(view);
		});
		buttonContainer.append(button);
	});
	changeView('Extracts');
};
const removeView = () => {
	Array.from(this.container.children).forEach((el) => {
		if (!el.classList.contains('tabButtons')) {
			el.remove();
		}
	});
};
createButtons();
