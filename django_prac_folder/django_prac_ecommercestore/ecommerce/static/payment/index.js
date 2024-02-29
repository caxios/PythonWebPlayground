var stripe = Stripe('pk_test_51KVDbjHKmi92LSUpXjyot87frrwM5FLOCyXr8fVgaKUR0gb3P6r5xGeXRRij71yoMd6HYoH7gBrKv7Nh58ZBWvRg00NgDe4A5a');

var elem = document.getElementById('submit')

// In 'templates/payment/home.html' we put our 'client_secret' data to the button element, whose 
// id is 'submit', to have our client key on user's page(it doesn't necessarily collected on button)
// And we are getting that value here to process payment of ther user with client key, which is 
// made by 'stripe'
var clientsecret = elem.getAttribute('data-secret')

var card = elements.create("card", { style: style });

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};

// Mount(insert) 'card' stripe-element into our 'payment/home.html' where tag id is 'card-element'
card.mount("#card-element");

// Flag errors that could happen when user typing payment detail(like csv, postocde etc).
card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    // We are using our own elements for country, and postcode etc and only utilizing from stripe of
    // typing and processing card payment. That's why we are getting values from html.
    var custName = document.getElementById("custName").value;
    var custAdd = document.getElementById("custAdd").value;
    var custAdd2 = document.getElementById("custAdd2").value;
    var postCode = document.getElementById("postCode").value;


    $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
        order_key: clientsecret,
        csrfmiddlewaretoken: CSRF_TOKEN,
        action: "post",
    },
    success: function (json) {
        console.log(json.success)

        // After successfully process ajax request, we then sent that processed data to 'stripe'
        stripe.confirmCardPayment(clientsecret, {
        payment_method: {
            card: card,
            billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2
            },
            name: custName
            },
        }
        }).then(function(result) {
        if (result.error) {
            console.log('payment error')
            console.log(result.error.message);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
            }
        }
        });

    },
    error: function (xhr, errmsg, err) {},
    });



});