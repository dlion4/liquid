// sourcery skip: avoid-function-declarations-in-blocks
"use strict";
!(function (NioApp, $) {
  function accountBalance(selector, set_data) {
    var $selector = $(selector || ".chart-account-balance");
    $selector.each(function () {
      for (
        var $self = $(this),
          _self_id = $self.attr("id"),
          _get_data = void 0 === set_data ? eval(_self_id) : set_data,
          chart_data = [],
          i = 0;
        i < _get_data.datasets.length;
        i++
      )
        chart_data.push({
          label: _get_data.datasets[i].label,
          data: _get_data.datasets[i].data,
          backgroundColor: _get_data.datasets[i].color,
          borderWidth: 2,
          borderColor: "transparent",
          hoverBorderColor: "transparent",
          borderSkipped: "bottom",
          barPercentage: NioApp.State.asMobile ? 1 : 0.75,
          categoryPercentage: NioApp.State.asMobile ? 1 : 0.75,
        });
    });
  }
  NioApp.coms.docReady.push(function () {
    accountBalance();
  });
  function referStats(selector, set_data) {
    var $selector = $(selector || ".chart-refer-stats");
    $selector.each(function () {
      for (
        var $self = $(this),
          _self_id = $self.attr("id"),
          _get_data = void 0 === set_data ? eval(_self_id) : set_data,
          selectCanvas = document.getElementById(_self_id).getContext("2d"),
          chart_data = [],
          i = 0;
        i < _get_data.datasets.length;
        i++
      )
        chart_data.push({
          label: _get_data.datasets[i].label,
          data: _get_data.datasets[i].data,
          backgroundColor: _get_data.datasets[i].color,
          borderWidth: 2,
          borderColor: "transparent",
          hoverBorderColor: "transparent",
          borderSkipped: "bottom",
          barPercentage: 0.8,
          categoryPercentage: 0.8,
        });
    });
  }
  NioApp.coms.docReady.push(function () {
    referStats();
  });
  function accountSummary(selector, set_data) {
    var $selector = $(selector || ".chart-account-summary");
    $selector.each(function () {
      for (
        var $self = $(this),
          _self_id = $self.attr("id"),
          _get_data = void 0 === set_data ? eval(_self_id) : set_data,
          selectCanvas = document.getElementById(_self_id).getContext("2d"),
          chart_data = [],
          i = 0;
        i < _get_data.datasets.length;
        i++
      )
        chart_data.push({
          label: _get_data.datasets[i].label,
          tension: 0.4,
          backgroundColor: "transparent",
          fill: !0,
          borderWidth: 2,
          borderColor: _get_data.datasets[i].color,
          pointBorderColor: "transparent",
          pointBackgroundColor: "transparent",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: _get_data.datasets[i].color,
          pointBorderWidth: 2,
          pointHoverRadius: 4,
          pointHoverBorderWidth: 2,
          pointRadius: 4,
          pointHitRadius: 4,
          data: _get_data.datasets[i].data,
        });
    });
  }
  NioApp.coms.docReady.push(function () {
    accountSummary();
  });
})(NioApp, jQuery);
