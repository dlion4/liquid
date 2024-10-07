$("#id_amount").on("keyup", function(e) {
    e.preventDefault();
    const amount = $(this).val();
    const errorElement = $("#id_error_amount");
    if (amount <= 50) {
        $(errorElement).text("Please enter an amount greater than 50");
        return false;
    }
    else{
        $(errorElement).text("");
        return true;
    }
})

$("#depositMoneyForm").submit(function (event) {
    event.preventDefault();

    // Parse the amount to a floating-point number
    const amount = parseFloat($("#id_amount").val());

    if (amount <= 50) {
        $("#id_error_amount").text("Please enter an amount greater than 50");
        return false;
    }

    if(amount> 50){
        $("#submitBtnDeposit").text("Initiating deposit workflow ...");
        $("#submitBtnDeposit").prop("disabled", true)
    }

    $.ajax({
        url: $(this).attr("action"),
        type: "post",
        data: JSON.stringify({
            account: $("#id_account").val(),
            amount: amount,  // Pass the parsed amount
            reason: $("#id_reason").val(),
        }),
        headers: { "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val() },
        contentType: "application/json",
        success: function (response) {
            console.log("Form submitted successfully:", response);
            // const { poolId, accountId, planId, amount, profileUserId } = response;
            $("#submitBtnDeposit").text("Redirecting to payment ...")
            
            AutomateAccountDepositPayment(response);
        },
        error: function (xhr, status, error) {
            console.log("Error during submission:", error);
            $("#submitBtnDeposit").text("Error processing payment ", error)
        }
    });
});


function AutomateAccountDepositPayment(data){
    const { poolId, accountId, planId, amount, profileUserId, emailAddress } = data;
    let discount_price = parseFloat("0.00")
    let handler = PaystackPop.setup({
        key: 'pk_live_94d90234cd2007c23e450c8cb398ac2970cd61d9',
        email: emailAddress,
        amount: amount * 100,
        currency: "KES",
        ref: '', 
        callback: function (response) {
            var reference = response.reference;
            alert('Payment complete! Reference: ' + reference);
            const url = `/payments/paystack/payment-status/?reference=${reference}`
            fetch(url, { method: 'GET' })
                .then((response) => response.json())
                .then(data => {
                    if (data.success) {
                        handleAccountDepositCreateTransaction(
                            poolId,
                            accountId,
                            planId,
                            emailAddress,
                            amount,
                            discount_price,
                            profileUserId,
                            reference,
                            'KES',
                            'Kenya')
                            .then(response => response.json())
                            .then(data => {});
                    } else {
                        handleDeleteTransaction(
                            poolId,
                            accountId,
                            planId,
                            reference,
                            emailAddress
                        );
                        
                    }
                });
        },
        onClose: function (error) {
            $("#submitBtnDeposit").text(`Transaction initialization error !`, error)
        }
    });
    handler.openIframe();
}




async function handleAccountDepositCreateTransaction(
    pool_id, 
    account_id, 
    plan_id, 
    phoneN,
    cleanedCurrency,
    discount_price,
    profileId,
    mpesa_code,
    currency, 
    country) {

    const url = `/dashboard/invest/handle-payment-create-transaction/${pool_id}/${account_id}/${plan_id}/`

    $.ajax({
        url: url,
        type: "POST",
        headers: {"Content-Type": "application/json"},
        data: JSON.stringify({
            phone_number: phoneN,
            amount: cleanedCurrency,
            discount_price: discount_price,
            currency: currency,
            profile: profileId,
            mpesa_transaction_code: mpesa_code,
            plan_id: plan_id,
            country: country
        }),
        success: function(response){
            // window.location.href = response.url
            console.log(response)
            $.ajax({
                type: "POST",
                url: `${url}verify-transaction/${mpesa_code}`,
                success: function (response) { 
                    console.log(response);
                    $("#submitBtnDeposit").text("Payment completed. Redirecting ...")
                    
                    setTimeout(()=>{
                        window.location.href = response.url
                    }, 2000)
                 },
                error: function (error) { 
                    console.log(error);
                    handleDeleteTransaction(
                        pool_id,
                        account_id,
                        plan_id,
                        mpesa_code,
                        "{{request.user.email}}"
                    )
                 }
            });

        },
        error: function(jxh, jQ, error){alert(error)}
    })
}

function handleDeleteTransaction(
    pool_id,
    account_id,
    plan_id,
    transaction_code,
    email
){
console.log(transaction_code, email);
    var url = `/dashboard/invest/handle-payment-create-transaction/${pool_id}/${account_id}/${plan_id}/delete-transaction/${transaction_code}`;

    $.ajax({
        type: "POST",
        url: url,
        headers: {"Content-Type": "application/json"},
        success: function(response){
            $("#submitBtnDeposit").text("Payment Failed. Redirecting ...")
            $("#submitBtnDeposit").prop("disabled", true)
            setTimeout(() => {
                window.location.href = response.url
            }, 2000)
        },
        error: function(jxH, jQ, errorThrown){
            alert(errorThrown)
        }
    })
}