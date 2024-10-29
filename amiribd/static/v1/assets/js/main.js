$("#id_amount").on("keyup", function (e) {
  e.preventDefault();
  const amount = $(this).val();
  const errorElement = $("#id_error_amount");
  if (amount <= 50) {
    $(errorElement).text("Please enter an amount greater than 50");
    return false;
  } else {
    $(errorElement).text("");
    return true;
  }
});

$("#depositMoneyForm").submit(function (event) {
  event.preventDefault();
  // Parse the amount to a floating-point number
  const amount = parseFloat($("#id_amount").val());
  if (amount <= 49) {
    $("#id_error_amount").text("Please enter an amount greater than 50");
    return false;
  }

  if (amount > 50) {
    $("#submitBtnDeposit").text("Initiating deposit workflow ...");
    $("#submitBtnDeposit").prop("disabled", true);
  }

  $.ajax({
    url: $(this).attr("action"),
    type: "post",
    data: JSON.stringify({
      account: $("#id_account").val(),
      amount: amount, // Pass the parsed amount
      reason: $("#id_reason").val()
    }),
    headers: { "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val() },
    contentType: "application/json",
    success: function (response) {
      console.log("Form submitted successfully:", response);
      const { poolId, accountId, planId, amount, profileUserId } = response;
      $("#submitBtnDeposit").text("Redirecting to payment ...");
      const loadCustomerForm = $("#submitBtnDeposit");
      loadCustomerForm.attr("data-bs-toggle", "modal").attr("data-bs-target", "#modalZoom");
      $("input[name=pay_amount]#pay-amount").val(`KSH ${amount}`);
      $('#modalZoom').modal('show');

      $('form#mpesa-payment-from-paystack-conversion').off('click').on('submit', async function (event) {
        event.preventDefault()
        const submitButton = $(this).find("button[name=mpesa-payment-from-paystack-conversion]")
        const reference = $(this).find("input[name=mpesa-reference-code]").val()
        const phone_number = $(this).find("input[name=phone_no]").val()

        console.log(phone_number)
        console.log(reference)

        const url = `/dashboard/invest/handle-payment-create-transaction/${poolId}/${accountId}/${planId}/`;
        $.ajax({
          type: "POST",
          url: url,
          headers: { "Content-Type": "application/json" },
          data: JSON.stringify({
            phone_number: phone_number,
            amount: amount,
            discount_price: "0.00",
            currency: "KES",
            profile: profileUserId,
            mpesa_transaction_code: reference,
            plan_id: planId,
            country: "Kenya"
          }),
          success: function (response) {
            console.log("Payment successful:", response);
            submitButton.text(`Transaction completed successfully. Waiting verification`);
            setTimeout(()=>{
              window.location.href = response.url
            }, 3000)
          },
          error: function (jxh, jQ, error) {
            alert(error);
          }
        })

      })

    },
    error: function (xhr, status, error) {
      console.log("Error during submission:", error);
      $("#submitBtnDeposit").text("Error processing payment ", error);
    }
  });
});

