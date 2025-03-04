
document.addEventListener("DOMContentLoaded", function () {

    $("button.dropdown-item").on('click', currencyChangeProcessing);

});


function currencyChangeProcessing(event) {
    let currency = $(this).attr('data-iso-name');
    Cookies.set("currency", currency);
    location.reload();
}
