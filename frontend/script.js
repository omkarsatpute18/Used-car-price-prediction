const form = document.getElementById("predictionForm");

const result = document.getElementById("result");

const predictedPrice =
    document.getElementById("predictedPrice");

const predictButton =
    document.getElementById("predictButton");

const buttonText =
    document.getElementById("buttonText");

const loader =
    document.getElementById("loader");


form.addEventListener("submit", async function(event) {

    event.preventDefault();


    // Get form values

    const brand =
        document.getElementById("brand").value;

    const year =
        document.getElementById("year").value;

    const km_driven =
        document.getElementById("km_driven").value;

    const fuel =
        document.getElementById("fuel").value;

    const transmission =
        document.getElementById("transmission").value;

    const seller_type =
        document.getElementById("seller_type").value;

    const owner =
        document.getElementById("owner").value;


    // Show loading state

    buttonText.classList.add("hidden");

    loader.classList.remove("hidden");

    predictButton.disabled = true;


    try {

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    brand: brand,

                    year: year,

                    km_driven: km_driven,

                    fuel: fuel,

                    transmission: transmission,

                    seller_type: seller_type,

                    owner: owner

                })
            }
        );


        const data = await response.json();


        if (!data.success) {

            throw new Error(data.error);

        }


        // Format price

        const formattedPrice =
            new Intl.NumberFormat(
                "en-IN",
                {
                    style: "currency",
                    currency: "INR",
                    maximumFractionDigits: 0
                }
            ).format(data.predicted_price);


        predictedPrice.textContent =
            formattedPrice;


        result.classList.remove("hidden");


        // Scroll to result

        result.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        alert(
            "Unable to predict price. " +
            "Please make sure the backend server is running."
        );

        console.error(error);

    }


    // Restore button

    buttonText.classList.remove("hidden");

    loader.classList.add("hidden");

    predictButton.disabled = false;

});