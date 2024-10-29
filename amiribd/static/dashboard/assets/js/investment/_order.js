
const handleProcessTransactionForSaveInvestPayment = (url, dataToSubmit) => {
    const newUrl = `/payments/paystack/payment-status/?reference=${reference}&principal_amount=${encodeURIComponent(dataToSubmit.principal_amount)}&duration_of_saving_investment=${encodeURIComponent(dataToSubmit.duration_of_saving_investment)}&interest_amount=${encodeURIComponent(dataToSubmit.interest_amount)}&expected_daily_interest_plus_amount=${encodeURIComponent(dataToSubmit.expected_daily_interest_plus_amount)}&instruction=${encodeURIComponent(dataToSubmit.instruction)}&reason=${encodeURIComponent(dataToSubmit.reason)}`;

    $.ajax({
        url: url,
        method: 'POST',
        data: JSON.stringify(dataToSubmit),
        success: function (data) {
            if (data.success) {
                setTimeout(() => {
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
                                setTimeout(() => {
                                    window.location.reload()
                                }, 3000)
                            },
                            error: function (jxh, jQ, error) {
                                alert(error);
                            }
                        })

                    })
                }, 1000)
            }
        },
        error: function (xhr, status, error) {
            console.log(xhr)
            alert(error)
        }
    })
}
handleProcessTransactionForSaveInvestPayment()