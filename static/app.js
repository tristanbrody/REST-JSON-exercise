//get all cupcakes from API and add to DOM
getCupcakes();

//declare constants
const NOCUPCAKESFOUND_H2 = document.createElement('h1');
NOCUPCAKESFOUND_H2.innerText = 'No cupcakes to be found. Make one?';

const submitCupcakeForm = document.querySelector('.add-cupcake-form');

//add event listener to send post request to our API upon form submission
submitCupcakeForm.addEventListener('submit', async function (e) {
	e.preventDefault();
	const data = new FormData(e.target);
	const formData = Object.fromEntries(data.entries());
	const res = fetch('/api/cupcakes', {
		method: 'POST',
		body: JSON.stringify(formData),
		headers: { 'Content-Type': 'application/json' }
	});
	window.location.href = '';
});

async function getCupcakes() {
	const res = await axios.get('/api/cupcakes');
	for (let cupcake of res.data.cupcakes) {
		const li = document.createElement('li');
		li.innerText = `flavor: ${cupcake.flavor} | rating: ${cupcake.rating}`;
		document.querySelector('.cupcakes-ul').append(li);
	}
	if (res.data.cupcakes.length === 0) document.body.prepend(NOCUPCAKESFOUND_H2);
}
