---
layout: page
title: Сервер CubeSide
---
# Инфо о сервере CubeSide

## Игроки на сервере

<script src="https://api.trademc.org/trademcapi.js"></script>
<div id="trademc-online"></div>
<script>TrademcAPI.GetOnline({"Shop":"1","TextMask":"Играют {players} игроков. Всего: {max_players}. Версия - {version}","UIColor":"#333333","PastPlaceID":"trademc-online"});</script>

## Донат на сервер

<script src="https://api.trademc.org/trademcapi.js"></script>
<div id="trademc-buyform"></div>
<script>TrademcAPI.GetBuyForm({"Shop":"143633","Title":"Донат на сервер","Nickname":"Никнейм","Item":"Привелегия","Coupon":"Промокод, если есть","Button":"Купить!","Success_URL":"http://cubeside.online/server/donate/success","Pending_URL":"http://cubeside.online/server/donate/wait","Fail_URL":"http://cubeside.online/server/donate/fail","PastPlaceID":"trademc-buyform"});</script>
