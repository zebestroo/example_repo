fetch("/conf/")
    .then((result) => { return result.json(); })
        .then((data) => {
            const stripe = Stripe(data.public_key);
            document.querySelector("#btn").addEventListener("click", () => {
            var strka = document.getElementById('inp').value;
            fetch("/buy/" + strka)
            .then((result) => { return result.json(); })
            .then((data) => {
              return stripe.redirectToCheckout({sessionId: data.sessionId})
            });
          });
        });