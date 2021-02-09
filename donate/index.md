---
layout: page
permalink: /donate
---

<style>
.trademc-buyform-form {
    width: 1050px;
    text-align: center;
    left: auto;
    right: auto;
    margin-left: auto;
    margin-right: auto;
}

.trademc-buyform-title {
    font-weight: bold;
    font-size: 140%;
    margin-bottom: 20px;
    text-align: center;
}
</style>

<script src="https://api.trademc.org/trademcapi.js"></script>
<div class="trademc-buyform" id="trademc-buyform"></div>
<script>TrademcAPI.GetBuyForm({"Shop":"143633","Title":"Покупка привилегий","Nickname":"Введите ваш никнейм","Item":"Выберите товар","Coupon":"Введите промокод, если имеется","Button":"Продолжить","Success_URL":"http://cubeside.online/donate/success","Pending_URL":"http://cubeside.online/donate/wait","Fail_URL":"http://cubeside.online/donate/error","PastPlaceID":"trademc-buyform"});</script>