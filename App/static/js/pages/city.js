const cityForm = document.getElementById("cityForm");
if (cityForm) {
    cityForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        const city = data.city;

        const pathParts = window.location.pathname.split('/');
        const surveyId = parseInt(pathParts[3]);

        console.log(surveyId, city)

        document.cookie = `city=${encodeURIComponent(city)}; path=/`;

        window.location.href = `/survey/fill/${surveyId}`;
    });
};