// ============================================================
// SMOOTH SCROLL TO PREDICTOR
// ============================================================

function scrollToPredictor() {

    const predictor =
        document.getElementById("predictor");

    if (predictor) {

        predictor.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }

}


// ============================================================
// GET HTML ELEMENTS
// ============================================================

const form =
    document.getElementById("predictionForm");

const result =
    document.getElementById("result");

const predictedPrice =
    document.getElementById("predictedPrice");

const predictButton =
    document.getElementById("predictButton");

const buttonText =
    document.getElementById("buttonText");

const loader =
    document.getElementById("loader");


// ============================================================
// FORM SUBMISSION
// ============================================================

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // ----------------------------------------------------
        // Get values
        // ----------------------------------------------------

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


        // ----------------------------------------------------
        // Validate fields
        // ----------------------------------------------------

        if (
            !brand ||
            !year ||
            !kmDriven ||
            !fuel ||
            !transmission ||
            !sellerType ||
            !owner
        ) {

            alert(
                "Please fill in all the fields."
            );

            return;
        }


        // ----------------------------------------------------
        // Validate numbers
        // ----------------------------------------------------

        if (
            Number(year) < 1990 ||
            Number(year) > 2026
        ) {

            alert(
                "Please enter a valid manufacturing year."
            );

            return;
        }


        if (Number(kmDriven) < 0) {

            alert(
                "Kilometers driven cannot be negative."
            );

            return;
        }


        // ----------------------------------------------------
        // Show loading state
        // ----------------------------------------------------

        buttonText.classList.add("hidden");

        loader.classList.remove("hidden");

        predictButton.disabled = true;


        try {

            // ------------------------------------------------
            // Send request to Flask
            // ------------------------------------------------

            const response = await fetch(
                "/predict",
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


            // ------------------------------------------------
            // Read response
            // ------------------------------------------------

            const data =
                await response.json();


            // ------------------------------------------------
            // Check response
            // ------------------------------------------------

            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.error ||
                    "Prediction failed."
                );

            }


            // ------------------------------------------------
            // Format Indian currency
            // ------------------------------------------------

            const formattedPrice =
                new Intl.NumberFormat(
                    "en-IN",
                    {
                        style: "currency",

                        currency: "INR",

                        maximumFractionDigits: 0
                    }
                ).format(
                    data.predicted_price
                );


            // ------------------------------------------------
            // Display result
            // ------------------------------------------------

            predictedPrice.textContent =
                formattedPrice;

            result.classList.remove("hidden");


            // ------------------------------------------------
            // Scroll to result
            // ------------------------------------------------

            setTimeout(function () {

                result.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });

            }, 100);


        }

        catch (error) {

            console.error(
                "Prediction Error:",
                error
            );


            alert(
                "Unable to predict the car price.\n\n" +
                error.message
            );

        }

        finally {

            // ------------------------------------------------
            // Restore button
            // ------------------------------------------------

            buttonText.classList.remove("hidden");

            loader.classList.add("hidden");

            predictButton.disabled = false;

        }

    }
);