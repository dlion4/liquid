$(document).ready(function () {


    const savingsDurationObject = {
        "1D": "1-day",
        "1W": "1-week",
        "2W": "2-weeks",
        "1M": "1-month",
        "3M": "3-months",
        "C": "custom",
    }

    const savingsPricing = {
        "1D": {
            min: 100,
            max: 1000
        },
        "1W": {
            min: 500,
            max: 1500
        },
        "2W": {
            min: 1000,
            max: 3000
        },
        "1M": {
            min: 2000,
            max: 6000
        },
        "3M": {
            min: 6000,
            max: 12000
        },
    }


    const investmentRate = parseFloat("0.005");
    const totalInvestment = $("#total-investment")
    $("#daily-rate").html(`(${investmentRate}%)`);
    const investmentPriceSlider = $("#amount-step");
    const investmentAmount = $("#custom-amount");
    const investmentAmountPaymentHiddenInput = $("#custom-amount-value");

    const investAmountSum = $("#invest-cc-amount");
    const investAmountSummaryDisplay = $("#select-cc-price-summary");
    const investmentAmountSummaryCostFee = $("#select-cc-price-summary-cost-fee");

    const investmentPaymentChoiceSummary = $("#selected-cc-payment-option");

    $(investmentAmount).val("0.00");
    var investmentAmountFee = parseInt(investmentRate * parseFloat($(investmentAmount).val()))
    $(investmentAmountPaymentHiddenInput).val("0.00");
    $(investAmountSum).html("0.00");
    $(investAmountSummaryDisplay).html("0.00");
    $(investmentAmountSummaryCostFee).html(investmentAmountFee);




    const calculateTheRateInvestment = (amount) => {
        $(investmentAmountSummaryCostFee).html(parseInt(investmentRate * amount));
    }
    const updateSliderValue = () => {
        const sliderValue = $(".noUi-handle-lower")
        const value = $(sliderValue).attr("aria-valuenow");
        const priceValue = parseFloat(Number.parseInt(value) * 100).toFixed(2);
        $(investmentAmount).val(priceValue);
        investmentAmountPaymentHiddenInput.value = priceValue;
        $(investAmountSum).html(priceValue);
        $(investAmountSummaryDisplay).html(priceValue);
        calculateTheRateInvestment(priceValue);
        $(totalInvestment).text(priceValue);
    }
    $(investmentPriceSlider).on("mouseover", updateSliderValue)
    $(investmentPriceSlider).on("click", updateSliderValue)


    const paymentSelectionBox = $("#invest-payment-selection-box")
    const paymentOptions = $("li.invest-cc-item")
    let selectedPaymentOption = $("#selected-payment-option")


    const paymentOptionInput = $("#invest-choose-wallet")

    $(paymentOptions).each(function () {
        $(this).click(function (event) {
            const selection = $(this).html();
            selectedPaymentOption.html(selection)
            const coinNameSpan = $(this).find('.coin-name[data-bs-pay-text="coin-pay-select"]');
            if (coinNameSpan) {
                console.log(coinNameSpan);
                $(investmentPaymentChoiceSummary).html($(coinNameSpan).text());
            }
            const coinWalletOption = $(this).find('.invest-cc-opt').attr('data-payment-option')

            $(paymentOptionInput).val(coinWalletOption);
        })
    })

    const amountLabel = $("#amount-label")
    const amountSummaryLabel = $("#amount-summary-label")
    const formNoteHelpSliderId = $("#form-note-slider-help-slider");
    const floatingMaxAmountLabel = $("#slider-max-money")
    let investmentPlanOptionBox = $("#selected-plan-type")
    const investTypeOptions = $(".invest-type-cc-item")
    const savingsDuration = $("#savings-duration")
    const overalInvestType = $("#overal-invest-type")
    $(savingsDuration).css("display", "none")
    $(investTypeOptions).each(function () {
        $(this).click(function (event) {
            const investTypePlanOption = $(this).html();
            investmentPlanOptionBox.html(investTypePlanOption);
            const investTypePlan = $(this).find(".invest-type-cc-opt")
            const savingDurationSummary = $("savings-duration-sumary")
            const savingDurationSummaryValue = $("selected-cc-saving-duration")

            if (investTypePlan) {
                const investTypePlanOption = $(investTypePlan).attr("data-investment-option");
                if ($.trim(investTypePlanOption).toLowerCase() === "savings") {
                    $(overalInvestType).val("save");
                    const SavingLimitDiv = $("#savings-limit");
                    $(savingDurationSummary).css("display", "block");
                    $(investmentPriceSlider).css("display", "none");
                    $(investmentAmount).prop("disabled", false);
                    $(investmentAmount).attr("type", "number");
                    $(savingsDuration).css("display", "block");
                    $(amountLabel).html("Principal Savings");
                    $(amountSummaryLabel).html("to Saving");
                    const saveDurations = $(".invest-amount-control");

                    $(saveDurations).each(function () {
                        $(this).click(function () {
                            if ($(this).checked) {
                                if (Object.values(savingsDurationObject).includes($(this).val())) {
                                    if ($(this).val() === "custom") {
                                        const summaryForm = $("#custom-save-duration-form")
                                    }

                                    const updateMinMaxValue = (minValue, maxValue) => {
                                        const savingValue = $(".noUi-handle-lower");
                                        $(savingValue).attr("aria-valuemin", parseFloat(minValue))
                                        $(savingValue).attr("aria-valuemax", parseFloat(maxValue))
                                    }

                                    const updateTheMinMaxHelpTextValue = (minValue, maxValue) => {
                                        $(formNoteHelpSliderId).html(
                                            `invest ${parseFloat(minValue).toFixed(2)} ksh and upto ${parseFloat(maxValue).toFixed(2)} ksh`
                                        )
                                        $(floatingMaxAmountLabel).html(`Max Amount ${maxValue.toLocaleString()} KSH`);

                                    }

                                    const updateTheValueAndText = (index) => {
                                        updateMinMaxValue(savingsPricing[index].min, savingsPricing[index].max)
                                        updateTheMinMaxHelpTextValue(savingsPricing[index].min, savingsPricing[index].max)
                                        $(investmentAmount).setAttribute("min", savingsPricing[index].min)
                                        $(investmentAmount).setAttribute("max", savingsPricing[index].max)
                                        $(investmentAmount).value = savingsPricing[index].min;
                                        InputSavingListenerFunction(savingsPricing[index].min, savingsPricing[index].max)
                                    }

                                    function InputSavingListenerFunction(min, max) {


                                        $(investAmountSummaryDisplay).html(min)
                                        $(investmentAmountPaymentHiddenInput).val(min)
                                        $(totalInvestment).text(min)

                                        $(investmentAmountSummaryCostFee).html(
                                            parseInt((investmentRate) * parseFloat(investmentAmount.value))
                                        )



                                        $(investmentAmount).keyup(function (e) {

                                            $(this).val(e.target.value);
                                            calculateTheRateInvestment($(this).val());

                                            $(investAmountSummaryDisplay).html($(this).val())
                                            $(investmentAmountPaymentHiddenInput).val($(this).val())
                                            $(totalInvestment).text($(investmentAmountPaymentHiddenInput).val())

                                            $(investmentAmountSummaryCostFee).html(parseInt((investmentRate) * parseFloat($(this).val())))

                                            $(totalInvestment).text(parseInt((investmentRate) * parseFloat($(this).val())))

                                            if (
                                                parseInt($(this).val()) < min ||
                                                parseInt($(this).val()) > max ||
                                                $(this).val() == '' ||
                                                $(this).val() == undefined ||
                                                $(this).val() == null
                                            ) {
                                                $(SavingLimitDiv).addClass("text-danger", "form-note", "pt-1")
                                                $(SavingLimitDiv).html(
                                                    `Amount can only be between ${min} and ${max} for the ${saveDuration.value} saving duration`
                                                )
                                                return false;
                                            } else {
                                                $(SavingLimitDiv).removeClass("text-danger")
                                                $(SavingLimitDiv).html("")
                                            }
                                        })



                                    }


                                    function updateSaveDurationValue(value) {

                                        if (value.includes("-")) {
                                            const parts = value.split("-");
                                            const part1 = parts[0]
                                            const formattedValue = parts[1].charAt(0).toUpperCase() + parts[1].slice(1);
                                            $(savingDurationSummaryValue).html(`${part1} + " " + ${formattedValue}`)
                                        } else {
                                            $(savingDurationSummaryValue).html(value)
                                        }
                                    }

                                    switch ($(this).val()) {
                                        case "1-day":
                                            updateTheValueAndText('1D')
                                            updateSaveDurationValue($(this).val())
                                            break;
                                        case "1-week":
                                            updateTheValueAndText('1W')
                                            updateSaveDurationValue($(this).val())
                                            break;
                                        case "2-weeks":
                                            updateTheValueAndText('2W')
                                            updateSaveDurationValue($(this).val())
                                            break;
                                        case "1-month":
                                            updateTheValueAndText('1M')
                                            updateSaveDurationValue($(this).val())
                                            break;
                                        case "3-months":
                                            updateTheValueAndText('3M')
                                            updateSaveDurationValue($(this).val())
                                            break;

                                        default:
                                            break;
                                    }
                                }

                                else {
                                    console.log(Object.values(savingsDurationObject))
                                }
                            }
                        })
                    })
                    console.log(savingsDurationObject)
                }

                else if ($.trim(investTypePlanOption).toLowerCase() === 'investment') {
                    savingsDuration.css("display", "none")
                    $(amountLabel).html("Principal Investment")
                    $(amountSummaryLabel).html("to Investment")
                    $(formNoteHelpSliderId).html("invest 1000 ksh and upto 10,000 ksh")
                    $(floatingMaxAmountLabel).html("Max Amount 10,000 KSH")
                    investmentPriceSlider.css("display", "block")
                    $(investmentAmount).setAttribute("disabled", "disabled");
                    $(investmentAmount).attr("type", "number")
                    $(savingDurationSummary).css("display", "none")
                    $(overalInvestType).val("invest")
                }
                else {
                    $(savingsDuration).css("display", "none");
                }

            }

        })
    })



})