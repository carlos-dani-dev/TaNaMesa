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
        const payload = {
            city: city
        }

        try{
            const response = await fetch("/survey/create_city_cookies", {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            if (response.ok){
            }else{
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        }catch(error){
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        };

        window.location.href = `/survey/fill/${surveyId}`;
        return
    });
};