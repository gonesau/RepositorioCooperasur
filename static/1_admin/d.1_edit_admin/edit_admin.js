function changeStatusInputsAndBtn(statusInputs) {
	let btnSendData = document.getElementById("btnModData");
	let lstIdInputs = ["name", "lastName", "country"];
	let editDataChk = document.getElementById("editDataChk");
	lstIdInputs.forEach((ele, index) => {
		let input = document.getElementById(ele);
		input.value = dataAdmin[index];
		input.disabled = statusInputs;
	});

	btnSendData.disabled = statusInputs;
}

changeStatusInputsAndBtn(true);

(() => {
	editDataChk.addEventListener("click", () => {
		let status = editDataChk.checked;
		if (status) {
			changeStatusInputsAndBtn(false);
		} else {
			changeStatusInputsAndBtn(true);
		}
	});
})();