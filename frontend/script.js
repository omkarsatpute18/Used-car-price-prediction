javascript
const form = document.getElementById("predictionForm");

const result = document.getElementById("result");
const predictedPrice = document.getElementById("predictedPrice");

const predictButton = document.getElementById("predictButton");
const buttonText = document.getElementById("buttonText");
const loader = document.getElementById("loader");


form.addEventListener("submit", async function (event) {

    event.preventDefault();


    // Get values from the form
    const brand =
        document.getElementById("brand").value;

    const year =
        document.getElementById("year").value;

    const kmDriven =
        document.getElementById("km_driven").value;

    const fuel =
        document.getElementById("fuel").value;

    const transmission =
        document.getElementById("transmission").value;

    const sellerType =
        document.getElementById("seller_type").value;

    const owner =
        document.getElementById("owner").value;


    // Basic validation
    if (
        !brand ||
        !year ||
        !kmDriven ||
        !fuel ||
        !transmission ||
        !sellerType ||
        !owner
    ) {

        alert("Please fill in all the fields.");

        return;
    }


    // Show loading state
    buttonText.classList.add("hidden");

    loader.classList.remove("hidden");

    predictButton.disabled = true;


    try {

        // Send data to Flask
        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    brand: brand,

                    year: Number(year),

                    km_driven: Number(kmDriven),

                    fuel: fuel,

                    seller_type: sellerType,

                    transmission: transmission,

                    owner: owner

                })
            }
        );


        // Convert response to JSON
        const data = await response.json();


        // Check API response
        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Prediction failed."
            );

        }


        // Format price in Indian currency
        const formattedPrice =
            new Intl.NumberFormat(
                "en-IN",
                {
                    style: "currency",
                    currency: "INR",
                    maximumFractionDigits: 0
                }
            ).format(data.predicted_price);


        // Display result
        predictedPrice.textContent =
            formattedPrice;

        result.classList.remove("hidden");


        // Scroll to result
        result.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        console.error(
            "Prediction Error:",
            error
        );

        alert(
            "Unable to predict the car price.\n\n" +
            "Please make sure the Flask backend is running."
        );

    } finally {

        // Restore button
        buttonText.classList.remove("hidden");

        loader.classList.add("hidden");

        predictButton.disabled = false;

    }

});
